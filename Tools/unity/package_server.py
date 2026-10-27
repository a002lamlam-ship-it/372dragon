#!/usr/bin/env python3
"""Package this checkout's source delta and exported world/combat data, never native binaries."""
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile
ROOT=Path(__file__).resolve().parents[2]

def main():
    paths=set()
    for arguments in [['git','diff','--name-only','-z','HEAD'],['git','ls-files','--others','--exclude-standard','-z']]:
        paths.update(p for p in subprocess.check_output(arguments,cwd=ROOT).decode().split('\0') if p)
    target=ROOT/'Build/NativeServerChanges.zip'
    temporary=tempfile.NamedTemporaryFile(prefix='server-delta-',suffix='.zip',dir=target.parent,delete=False)
    pending=Path(temporary.name);temporary.close()
    with zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name in sorted(paths):
            p=ROOT/name
            if p.is_file() and not any(part in ['Build','__pycache__','.git'] for part in p.parts) and p.suffix not in ['.so','.o','.pyc']:
                z.write(p,name)
        for p in sorted((ROOT/'Build/unity-world').rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(ROOT)))
        z.writestr('SOURCE-DELTA.json',json.dumps(dict(baseCommit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),repository='a002lamlam-ship-it/372dragon',instructions='Apply onto the base checkout. Contains source changes and world/combat data, not compiled macOS binaries. See Tools/unity/Package/ART-COMBAT.md.'),indent=2))
    with zipfile.ZipFile(pending) as z:
        assert z.testzip() is None
        assert 'Build/unity-world/combat-data.json' in z.namelist()
        expected={v[:24]+'.path' for v in json.loads((ROOT/'Build/unity-world/combat-data.json').read_text())['navigation'].values()}
        assert {n.rsplit('/',1)[-1] for n in z.namelist() if n.startswith('Build/unity-world/nav/')}==expected
    pending.replace(target)
    print(target,target.stat().st_size)
if __name__=='__main__':main()
