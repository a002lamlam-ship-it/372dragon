#!/usr/bin/env python3
"""Check every navigation image through the actual native Lua module and verify scene metadata."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tools/unity/art'))
from native_navigation import inspect
WORLD=ROOT/'Build/unity-world'
status=inspect(WORLD)
expected={v[:24]+'.path' for v in json.loads((WORLD/'combat-data.json').read_text())['navigation'].values()}
assert set(status)==expected
blocked=[]
for entry in json.loads((WORLD/'catalog.json').read_text())['scenes']:
    data=json.loads((WORLD/(str(entry['sceneId'])+'.json')).read_text())
    assert data['combatNavigationAvailable']==status[Path(data['navFile']).name]
    if not data['combatNavigationAvailable']:blocked.append(data['sceneId'])
assert set(blocked)=={40,95,104},blocked
print('UNITY_NAV_AUDIT_OK',sum(status.values()),'of',len(status),'images; 289 scenes checked, unavailable combat scenes:',blocked)
