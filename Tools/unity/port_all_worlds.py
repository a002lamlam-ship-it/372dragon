#!/usr/bin/env python3
"""Fetch source-backed scene inputs, export active maps, and report every failure explicitly."""
import argparse
import configparser
import xml.etree.ElementTree as ET
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import zipfile
import struct
from cached_remote_zip import CachedRemoteZip
from export_world import ini,export_scene

ROOT=Path(__file__).resolve().parents[2]

def download(root):
    manifest=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
    file_id=re.search(r'/d/([^/]+)',manifest['google_drive_url'])[1]
    endpoint='https://drive.usercontent.google.com/download'
    with urllib.request.urlopen(endpoint+'?'+urllib.parse.urlencode(dict(id=file_id,export='download')),timeout=30) as response:
        page=response.read(100000).decode('utf-8')
    params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
    if params.get('id')!=file_id or params.get('confirm')!='t':raise ValueError('Unrecognized public download form')
    remote=CachedRemoteZip(endpoint+'?'+urllib.parse.urlencode(params),manifest['bytes'],root/'Build/world-range-cache.zip')
    records=[]
    with zipfile.ZipFile(remote) as archive:
        index_bytes=archive.read('DATA-FILES.json')
        (root/'Build/world-data-index.json').write_bytes(index_bytes)
        index={r['path']:r for r in json.loads(index_bytes)}
        selected=[]
        for info in archive.infolist():
            name=info.filename
            if name in ['Server/configs/SceneInfo.ini','Server/configs/MonsterAttrExTable.txt','Assets/CanonicalCY/Data/ConfigFolder/SceneDefineEx.txt'] or name.startswith('Server/Game_2/Scene/') or (name.startswith('Assets/CanonicalCY/Data/') and name.lower().endswith(('.scene','.terrain','.heightmap','.gridinfo'))):
                selected.append(info)
        pending=[]
        for info in selected:
            expected=index[info.filename];dest=(root/info.filename).resolve()
            if not dest.is_relative_to(root):raise ValueError('Unsafe archive path')
            if dest.exists():
                if hashlib.sha256(dest.read_bytes()).hexdigest()!=expected['sha256']:raise ValueError('Local data differs; refusing overwrite: '+info.filename)
            else:pending.append(info)
        spans=[]
        for info in sorted(pending,key=lambda i:i.header_offset):
            start=info.header_offset;end=min(remote.size,start+30+len(info.filename.encode('utf8'))+len(info.extra)+info.compress_size+512)
            if spans and start-spans[-1][1]<=65536 and end-spans[-1][0]<=8*1024*1024:
                spans[-1]=(spans[-1][0],max(spans[-1][1],end))
            else:spans.append((start,end))
        print(f'Selected {len(selected)} members; {len(pending)} missing locally; {len(spans)} ranges, {sum(b-a for a,b in spans)/1048576:.1f} MiB',flush=True)
        remote.prefetch(spans)
        for i,info in enumerate(selected,1):
            path=root/info.filename;expected=index[info.filename]
            if not path.exists():
                data=archive.read(info)
                if len(data)!=expected['bytes'] or hashlib.sha256(data).hexdigest()!=expected['sha256']:raise ValueError('Member checksum mismatch: '+info.filename)
                path.parent.mkdir(parents=True,exist_ok=True)
                with path.open('xb') as stream:stream.write(data)
            records.append(dict(path=info.filename,sha256=expected['sha256'],bytes=expected['bytes']))
            if i%500==0:print(f'Verified {i}/{len(selected)} members',flush=True)
    (root/'Build/unity-world-source-audit.json').write_text(json.dumps(dict(archive=manifest['name'],archiveMemberCount=len(archive.infolist()),llicenseNamedMembers=[n for n in archive.namelist() if 'llicense' in n.lower()],checkedMembers=records,rangeBytesTransferred=remote.transferred,integrityScope='Member CRC and SHA-256 from embedded index; full archive hash not verified'),ensure_ascii=False,indent=2))
    # The cache holds compressed source ranges only; all selected members have verified retained copies.
    remote.cache.unlink()

def verified_aliases(root, config):
    index_path=root/'Build/world-data-index.json'
    if not index_path.exists(): index_path=root/'Build/cloud/recheck/DATA-FILES.json'
    if not index_path.exists(): return {}
    index={row['path'].casefold():row for row in json.loads(index_path.read_text())}
    data=root/'Assets/CanonicalCY/Data'
    raw=(data/'ConfigFolder/SceneDefineEx.txt').read_bytes()
    magic,columns,rows,pool_size=struct.unpack_from('<4I',raw)
    if magic!=0xDDBBCC00 or columns<5 or len(raw)!=16+columns*4+columns*rows*4+pool_size:raise ValueError('Invalid SceneDefineEx DBC')
    types=struct.unpack_from('<'+'I'*columns,raw,16)
    if types[4]!=2: raise ValueError('SceneDefineEx resource column is not STRING')
    base=16+4*columns;pool=raw[base+4*columns*rows:];definitions={}
    for r in range(rows):
        cells=struct.unpack_from('<'+'I'*columns,raw,base+4*columns*r)
        offset=cells[4]
        if offset>=len(pool):raise ValueError('Invalid DBC string offset')
        text=pool[offset:pool.index(b'\0',offset)]
        try: name=text.decode('utf8')
        except UnicodeDecodeError:name=text.decode('gb18030')
        definitions[cells[0]]=name
    aliases={}
    for section in config.sections():
        if not section.startswith('scene') or not section[5:].isdigit():continue
        sid=int(section[5:]);row=config[section]
        if row.get('active')!='1' or row.get('type')!='0':continue
        definition=definitions.get(sid)
        if not definition:continue
        source=root/'Server/Game_2/Scene'/row.get('file','')
        if not source.is_file():continue
        nav=ini(source)['System'].get('navmapname')
        if not nav:continue
        server_nav=root/'Server/Game_2/Scene'/nav
        if not server_nav.is_file():continue
        server_hash=hashlib.sha256(server_nav.read_bytes()).hexdigest()
        stem=Path(definition).stem
        matches=[v for key,v in index.items() if key.startswith('assets/canonicalcy/data/') and key.endswith('/'+stem.casefold()+'.path') and v['sha256']==server_hash]
        if len(matches)!=1:continue
        aliases[sid]=dict(kind='client-dbc-with-matching-navigation-sha256',resource=definition,
            navigationSha256=server_hash,clientNavigation=matches[0]['path'],serverNavigation=str(server_nav.relative_to(root)))
    return aliases


def export_all(root,out):
    config=ini(root/'Server/configs/SceneInfo.ini')
    aliases=verified_aliases(root,config)
    catalog=[];failed=[];inactive=[]
    for section in config.sections():
        if not section.startswith('scene') or not section[5:].isdigit():continue
        sid=int(section[5:]);row=config[section]
        if row.get('active')!='1':inactive.append(sid);continue
        try:
            catalog.append(export_scene(root/'Server',root/'Assets/CanonicalCY/Data',sid,out,aliases))
        except (ValueError,KeyError,OSError,IndexError,TypeError,UnicodeError,ET.ParseError,configparser.Error,OverflowError) as error:
            failed.append(dict(sceneId=sid,name=row.get('name',''),sceneType=row.get('type'),file=row.get('file'),reason=str(error)))
        if (len(catalog)+len(failed))%25==0:print(f'Processed {len(catalog)+len(failed)} active scenes: {len(catalog)} exported, {len(failed)} blocked',flush=True)
    out.mkdir(parents=True,exist_ok=True)
    (out/'catalog.json').write_text(json.dumps(dict(schema=1,scenes=catalog),ensure_ascii=False,indent=2))
    report=dict(exported=len(catalog),blocked=len(failed),inactive=len(inactive),entityCount=sum(s['entityCount'] for s in catalog),scenes=catalog,failures=failed,inactiveSceneIds=inactive)
    (out/'port-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['scenes','failures','inactiveSceneIds']},ensure_ascii=False),flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--out',type=Path,default=ROOT/'Build/unity-world')
    ap.add_argument('--no-download',action='store_true')
    args=ap.parse_args()
    if not args.no_download:download(args.root.resolve())
    export_all(args.root.resolve(),args.out.resolve())

if __name__=='__main__':main()
