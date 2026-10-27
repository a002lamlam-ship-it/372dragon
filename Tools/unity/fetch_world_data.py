#!/usr/bin/env python3
"""Fetch selected world inputs from the published ZIP using range reads, CRC and member SHA-256."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import zipfile
from remote_zip import RemoteZip

ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--maps',default='dali_new_320,wuliang')
    ap.add_argument('--root',type=Path,default=ROOT)
    args=ap.parse_args()
    root=args.root.resolve()
    manifest=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
    file_id=re.search(r'/d/([^/]+)',manifest['google_drive_url'])[1]
    endpoint='https://drive.usercontent.google.com/download'
    initial=endpoint+'?'+urllib.parse.urlencode({'id':file_id,'export':'download'})
    with urllib.request.urlopen(initial,timeout=30) as response:
        if 'text/html' not in response.headers.get('Content-Type',''):
            raise ValueError('Expected Drive download confirmation')
        page=response.read(100000).decode('utf-8')
    params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
    if params.get('id')!=file_id or params.get('confirm')!='t':
        raise ValueError('Unrecognized public download form')
    remote=RemoteZip(endpoint+'?'+urllib.parse.urlencode(params),manifest['bytes'])
    maps=args.maps.split(',')
    if any(not re.fullmatch(r'[A-Za-z0-9_]+',m) for m in maps):raise ValueError('Invalid map name')
    checked=[]
    with zipfile.ZipFile(remote) as archive:
        records=json.loads(archive.read('DATA-FILES.json'))
        index={r['path']:r for r in records}
        names=archive.namelist()
        license_names=[n for n in names if 'llicense' in n.lower()]
        selected=[]
        for name in names:
            base=name.rsplit('/',1)[-1].lower()
            if name in ['Server/configs/SceneInfo.ini','Server/configs/MonsterAttrExTable.txt']:
                selected.append(name)
            elif name.startswith('Server/Game_2/Scene/') and any(base.startswith(m+'.') or base.startswith(m+'_') for m in maps):
                selected.append(name)
            elif name.startswith('Assets/CanonicalCY/Data/SceneFolder/') and any(base==m+ext for m in maps for ext in ['.scene','.terrain','.heightmap','.gridinfo']):
                selected.append(name)
        for name in selected:
            destination=(root/name).resolve()
            if not destination.is_relative_to(root):raise ValueError('Unsafe archive path')
            expected=index[name]
            if destination.exists():
                if hashlib.sha256(destination.read_bytes()).hexdigest()!=expected['sha256']:
                    raise ValueError('Existing local file differs; refusing overwrite: '+name)
            else:
                data=archive.read(name) # zipfile checks CRC on complete member reads.
                if len(data)!=expected['bytes'] or hashlib.sha256(data).hexdigest()!=expected['sha256']:
                    raise ValueError('Member checksum mismatch: '+name)
                destination.parent.mkdir(parents=True,exist_ok=True)
                with destination.open('xb') as stream:stream.write(data)
            checked.append(dict(path=name,sha256=expected['sha256'],bytes=expected['bytes']))
    report=root/'Build/unity-world-source-audit.json'
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(dict(archive=manifest['name'],archiveMemberCount=len(names),
        llicenseNamedMembers=license_names,checkedMembers=checked,rangeBytesTransferred=remote.transferred,
        integrityScope='ZIP member CRC and SHA-256 from embedded index; full archive SHA-256 not verified'),ensure_ascii=False,indent=2))
    print(f'Checked {len(checked)} files; archive has {len(names)} entries; llicense-named entries: {len(license_names)}. Full archive hash not verified.')

if __name__=='__main__':main()
