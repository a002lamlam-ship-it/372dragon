#!/usr/bin/env python3
"""Download the port ZIPs over HTTPS, reassemble large ZIPs and verify SHA-256."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import urllib.request
BASE='https://raw.githubusercontent.com/a002lamlam-ship-it/372dragon/unity-port-downloads-20261027/Downloads/'
def sha(path):
 with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest() if hasattr(hashlib,'file_digest') else hashlib.sha256(f.read()).hexdigest()
def fetch(name,target):
 with urllib.request.urlopen(BASE+name,timeout=120) as r,target.open('wb') as out:shutil.copyfileobj(r,out,1024*1024)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--all',action='store_true');ap.add_argument('--starter',action='store_true');ap.add_argument('--out',type=Path,default=Path('DragonPort-Downloads'));args=ap.parse_args()
 with urllib.request.urlopen(BASE+'download-manifest.json',timeout=60) as r:manifest=json.load(r)
 args.out.mkdir(parents=True,exist_ok=True)
 names={'UnityOriginalActors-Starter.zip'} if args.starter else {'UnityOriginalActors-Starter.zip','UnityMapPort.zip','NativeServerChanges.zip'}
 for item in manifest['files']:
  if not args.all and item['name'] not in names:continue
  for name in [item['name']]+[p['name'] for p in item['pieces']]:
   if Path(name).name!=name or name in ('.','..'):raise ValueError('Invalid manifest filename')
  final=args.out/item['name']
  if final.exists():
   if final.stat().st_size==item['bytes'] and sha(final)==item['sha256']:print('Already verified:',final,flush=True);continue
   raise RuntimeError('Existing file differs; preserve/rename it before retry: '+str(final))
  print('Downloading:',item['name'],flush=True)
  with tempfile.TemporaryDirectory(prefix='.dragon-download-',dir=args.out) as tmp:
   folder=Path(tmp);combined=folder/'combined.zip'
   with combined.open('wb') as output:
    for piece in item['pieces']:
     path=folder/piece['name'];fetch(piece['name'],path)
     if path.stat().st_size!=piece['bytes'] or sha(path)!=piece['sha256']:raise ValueError('Checksum failed: '+piece['name'])
     with path.open('rb') as source:shutil.copyfileobj(source,output,1024*1024)
     path.unlink()
   if combined.stat().st_size!=item['bytes'] or sha(combined)!=item['sha256']:raise ValueError('Reassembled ZIP checksum failed: '+item['name'])
   combined.rename(final)
  print('Verified:',final,flush=True)
 print('Finished. ZIPs are in',args.out.resolve())
if __name__=='__main__':main()
