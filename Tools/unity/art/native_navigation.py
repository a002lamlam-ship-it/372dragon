"""Validate exported navigation using the built source native reader, never infer from file existence."""
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[3]

def inspect(root):
    files=sorted((root/'nav').glob('*.path'))
    lua='package.cpath='+json.dumps(str(ROOT/'Server/GameServer/luaclib/?.so'))+';local nav=require("unitynav");'
    for p in files:
        lua+='do local n=nav.new();print('+json.dumps(p.name)+',n:load('+json.dumps(str(p.resolve()))+'))end;'
    result=subprocess.run([str(ROOT/'Server/GameServer/framework/3rd/lua/lua'),'-e',lua],capture_output=True,text=True,timeout=120,check=True)
    status={}
    for line in result.stdout.splitlines():
        name,ok=line.split('\t');status[name]=ok=='true'
    if set(status)!={p.name for p in files}:raise ValueError('Incomplete native nav validation')
    return status

def validate(root):
    status=inspect(root);blocked=[]
    for summary in json.loads((root/'catalog.json').read_text())['scenes']:
        p=root/(str(summary['sceneId'])+'.json');w=json.loads(p.read_text())
        ok=status.get(Path(w.get('navFile','')).name,False)
        w['combatNavigationAvailable']=ok
        if not ok:
            w['combatNavigationError']='Source nav image rejected by native triangle reader (empty or unsupported geometry)'
            blocked.append(dict(sceneId=w['sceneId'],name=w['name'],navFile=w.get('navFile'),reason=w['combatNavigationError']))
        else:w.pop('combatNavigationError',None)
        p.write_text(json.dumps(w,ensure_ascii=False,separators=(',',':'),allow_nan=False))
    report=dict(schema=1,images=len(status),loaded=sum(status.values()),blockedScenes=blocked)
    (root/'combat-navigation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return report
