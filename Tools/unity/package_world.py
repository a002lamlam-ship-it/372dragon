#!/usr/bin/env python3
"""Create a self-contained Unity import ZIP from tested scripts and source-backed exported worlds."""
import argparse
import json
from pathlib import Path
import shutil
import zipfile
ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--world-root',type=Path,default=ROOT/'Build/unity-world')
    ap.add_argument('--out',type=Path,default=ROOT/'Build/UnityMapPort.zip')
    args=ap.parse_args()
    catalog=json.loads((args.world_root/'catalog.json').read_text())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.out,'w',zipfile.ZIP_DEFLATED) as archive:
        package=ROOT/'Tools/unity/Package'
        for path in sorted(package.rglob('*')):
            if path.is_file():archive.write(path,str(path.relative_to(package)))
        for scene in catalog['scenes']:
            sid=scene['sceneId']
            for suffix in ['.json','.heights.bytes','.cells.bytes']:
                path=args.world_root/(str(sid)+suffix)
                archive.write(path,f'Assets/DragonPort/Data/{sid}/{path.name}')
        report=args.world_root/'port-report.json'
        if report.exists(): archive.write(report,'PORT-REPORT.json')
        for preview in args.world_root.glob('*.preview.png'):
            archive.write(preview,'Previews/'+preview.name)
        archive.write(args.world_root/'catalog.json','Assets/DragonPort/Data/catalog.json')
        for name in ['export_world.py','fetch_world_data.py','remote_zip.py','cached_remote_zip.py','port_all_worlds.py']:
            archive.write(ROOT/'Tools/unity'/name,'Tools/unity/'+name)
        manifest=ROOT/'Publication/test-data-manifest.json'
        archive.write(manifest,'Publication/test-data-manifest.json')
        audit=ROOT/'Build/unity-world-source-audit.json'
        if audit.exists():archive.write(audit,'SOURCE-AUDIT.json')
        notice=ROOT/'Build/cloud/recheck/DATA-NOTICE.txt'
        if notice.exists():archive.write(notice,'DATA-NOTICE.txt')
    print(args.out, args.out.stat().st_size,'bytes')
    with zipfile.ZipFile(args.out) as archive:
        bad=archive.testzip()
        if bad:raise ValueError('Package CRC failed: '+bad)
        print('Package CRC verified:',len(archive.infolist()),'files')

if __name__=='__main__':main()
