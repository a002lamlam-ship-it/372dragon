"""Public archive access and GBK/mojibake resource resolution, preserving source bytes."""
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import zipfile
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cached_remote_zip import CachedRemoteZip

ROOT=Path(__file__).resolve().parents[3]

def variants(value):
    value=value.replace('\\','/').strip().strip('"')
    result={value.casefold()}
    for encoding in ['latin1','cp1252']:
        try:result.add(value.encode(encoding).decode('gb18030').casefold())
        except UnicodeError:pass
    return result

class AssetSource:
    def __init__(self,root=ROOT):
        self.root=root
        m=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
        endpoint='https://drive.usercontent.google.com/download'
        fid=re.search('/d/([^/]+)',m['google_drive_url'])[1]
        with urllib.request.urlopen(endpoint+'?'+urllib.parse.urlencode(dict(id=fid,export='download')),timeout=30) as r:page=r.read(100000).decode()
        params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
        if params.get('id')!=fid or params.get('confirm')!='t':raise ValueError('Unrecognized download form')
        self.remote=CachedRemoteZip(endpoint+'?'+urllib.parse.urlencode(params),m['bytes'],root/'Build/art-source-cache.zip')
        self.zip=zipfile.ZipFile(self.remote)
        self.index={r['path']:r for r in json.loads(self.zip.read('DATA-FILES.json'))}
        self.lookup={}
        for path in self.index:
            prefix='Assets/CanonicalCY/Data/'
            if not path.startswith(prefix):continue
            relative=path[len(prefix):];parts=relative.split('/',1)
            if len(parts)<2:continue
            for name in [parts[1],Path(relative).name]:
                for key in variants(name):self.lookup.setdefault(key,[]).append(path)
        self.ambiguities={};self.verified={}
    def resolve(self,name):
        matches=set()
        for key in variants(name):matches.update(self.lookup.get(key,[]))
        if not matches:return None
        def order(path):
            folder=path.split('/')[3]
            kind=re.match(r'(.*?)(\d*)(Folder)$',folder)
            rank=(int(kind[2]) if kind and kind[2] else 1)
            return rank,path.encode('utf8')
        chosen=sorted(matches,key=order)[-1]
        if len({self.index[p]['sha256'] for p in matches})>1:
            self.ambiguities[name]=dict(chosen=chosen,alternatives=sorted(matches),rule='last resource folder/location, as documented by existing validator')
        return chosen
    def fetch(self,names):
        paths=sorted(set(p for p in names if p))
        pending=[]
        for name in paths:
            if name not in self.index:raise ValueError('Unknown archive member: '+name)
            destination=(self.root/name).resolve()
            if not destination.is_relative_to(self.root.resolve()):raise ValueError('Unsafe archive path')
            if destination.exists():
                if hashlib.sha256(destination.read_bytes()).hexdigest()!=self.index[name]['sha256']:raise ValueError('Local file differs; refusing overwrite: '+name)
            else:pending.append(self.zip.getinfo(name))
        spans=[]
        for info in sorted(pending,key=lambda i:i.header_offset):
            a=info.header_offset;b=min(self.remote.size,a+30+len(info.filename.encode('utf8'))+len(info.extra)+info.compress_size+512)
            if spans and a-spans[-1][1]<=32768 and b-spans[-1][0]<=8*1024*1024:spans[-1]=(spans[-1][0],max(b,spans[-1][1]))
            else:spans.append((a,b))
        if spans:print(f'Fetching {len(pending)} art members in {len(spans)} ranges ({sum(b-a for a,b in spans)/1048576:.1f} MiB)',flush=True)
        self.remote.prefetch(spans)
        for i,name in enumerate(paths,1):
            destination=self.root/name
            if not destination.exists():
                data=self.zip.read(name)
                if len(data)!=self.index[name]['bytes'] or hashlib.sha256(data).hexdigest()!=self.index[name]['sha256']:raise ValueError('Art member checksum mismatch: '+name)
                destination.parent.mkdir(parents=True,exist_ok=True)
                with destination.open('xb') as stream:stream.write(data)
            self.verified[name]=self.index[name]
            if i%1000==0:print(f'Art members checked: {i}/{len(paths)}',flush=True)
    def close(self):
        self.zip.close()
        if self.remote.cache.exists():self.remote.cache.unlink()
