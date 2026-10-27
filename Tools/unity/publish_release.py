#!/usr/bin/env python3
"""Resume and publish the user's authorized Unity port Release after GitHub API access is enabled."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[2]
BUILD=ROOT/'Build'
REPO='a002lamlam-ship-it/372dragon'
TAG='unity-native-port-20261027'

def gh(*args):
    return subprocess.check_output(['gh',*args],cwd=ROOT,text=True)

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    manifest=json.loads((BUILD/'release-assets.json').read_text())
    for item in manifest['assets']:
        p=BUILD/item['name']
        if not p.is_file() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
            raise RuntimeError('Asset changed; rebuild release manifest: '+item['name'])
    # API preflight before any remote mutation. Never replace platform authentication.
    info=json.loads(gh('api','repos/'+REPO))
    if not info.get('permissions',{}).get('push'):raise RuntimeError('GitHub contents/write permission is required')
    releases=json.loads(gh('api','repos/'+REPO+'/releases?per_page=100'))
    release=next((r for r in releases if r['tag_name']==TAG),None)
    if release is None:
        gh('release','create',TAG,'--repo',REPO,'--target',manifest['baseCommit'],'--draft','--prerelease','--latest=false','--title','Unity native port: maps, original art and development PvE','--notes-file',str(BUILD/'RELEASE-NOTES.md'))
        release=json.loads(gh('api',f'repos/{REPO}/releases/tags/{TAG}'))
    if not release['draft']:
        raise RuntimeError('Release already published; refusing to alter existing published assets')
    for item in manifest['assets']:
        remote=json.loads(gh('api',f'repos/{REPO}/releases/{release["id"]}/assets?per_page=100'))
        existing=next((a for a in remote if a['name']==item['name']),None)
        if existing:
            if existing['size']!=item['bytes']:raise RuntimeError('Existing remote asset differs: '+item['name'])
            digest=existing.get('digest')
            if digest and digest!='sha256:'+item['sha256']:raise RuntimeError('Existing remote asset checksum differs: '+item['name'])
            if not digest:
                with tempfile.TemporaryDirectory(prefix='dragon-verify-') as tmp:
                    gh('release','download',TAG,'--repo',REPO,'--pattern',item['name'],'--dir',tmp)
                    if sha(Path(tmp)/item['name'])!=item['sha256']:raise RuntimeError('Remote asset hash differs: '+item['name'])
            print('Verified existing:',item['name'],flush=True)
        else:
            gh('release','upload',TAG,str(BUILD/item['name']),'--repo',REPO)
            print('Uploaded:',item['name'],flush=True)
    remote=json.loads(gh('api',f'repos/{REPO}/releases/{release["id"]}/assets?per_page=100'))
    for item in manifest['assets']:
        a=next(a for a in remote if a['name']==item['name'])
        assert a['size']==item['bytes']
        if a.get('digest'):assert a['digest']=='sha256:'+item['sha256']
    gh('release','edit',TAG,'--repo',REPO,'--draft=false','--prerelease','--latest=false')
    # Verify an actual downloadable ZIP after publication, not only the release page.
    with tempfile.TemporaryDirectory(prefix='dragon-download-') as tmp:
        name='UnityOriginalActors-Starter.zip'
        gh('release','download',TAG,'--repo',REPO,'--pattern',name,'--dir',tmp)
        expected=next(i['sha256'] for i in manifest['assets'] if i['name']==name)
        assert sha(Path(tmp)/name)==expected
    print('RELEASE_PUBLISHED_AND_DOWNLOAD_VERIFIED',release['html_url'])
if __name__=='__main__':main()
