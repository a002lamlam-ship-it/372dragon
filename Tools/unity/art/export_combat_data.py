#!/usr/bin/env python3
"""Export source combat stats/nav and verbatim basic combat functions for the new server adapter."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
import urllib.request
import urllib.parse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_world import templates,ini,contained
from remote_zip import RemoteZip
ROOT=Path(__file__).resolve().parents[3]

def main():
    source=ROOT/'Server/GameServer/services/scene/skill/combat_core.lua'
    raw=source.read_text()
    methods=['calculate_hit_rate','calculate_critical_rate','is_hit','is_critical_hit','physical_damage']
    functions=[];hashes={}
    for name in methods:
        start=raw.index('function combat_core:'+name+'(')
        next_method=raw.find('\nfunction combat_core:',start+1)
        body=raw[start:next_method if next_method>=0 else len(raw)].rstrip()
        functions.append(body.replace('function combat_core:','function M:',1))
        hashes[name]=hashlib.sha256(body.encode()).hexdigest()
    output=ROOT/'Server/GameServer/lualib/unity_legacy_combat.lua'
    output.write_text('-- Generated from combat_core.lua: verbatim basic methods, not the complete skill/impact system.\nlocal define=require "define"\nlocal enum_damage_type={IDX_DAMAGE_PHY=0}\nlocal M={}\n\n'+'\n\n'.join(functions)+'\nreturn M\n')
    trait_path=ROOT/'Server/configs/AttackTraits.txt'
    if not trait_path.exists():
        manifest=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
        endpoint='https://drive.usercontent.google.com/download'
        fid=re.search('/d/([^/]+)',manifest['google_drive_url'])[1]
        with urllib.request.urlopen(endpoint+'?'+urllib.parse.urlencode(dict(id=fid,export='download')),timeout=30) as response:page=response.read(100000).decode()
        params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
        if params.get('id')!=fid or params.get('confirm')!='t':raise ValueError('Unrecognized Drive form')
        url=endpoint+'?'+urllib.parse.urlencode(params)
        with zipfile.ZipFile(RemoteZip(url,manifest['bytes'])) as archive:
            name='Server/configs/AttackTraits.txt';data=archive.read(name)
            index={r['path']:r for r in json.loads(archive.read('DATA-FILES.json'))}
            if hashlib.sha256(data).hexdigest()!=index[name]['sha256']:raise ValueError('Combat traits checksum mismatch')
            trait_path.write_bytes(data)
    source_traits=templates(trait_path)
    traits={str(k):float(v.get('C-phy') or 0) for k,v in source_traits.items()}
    monsters={}
    for key,row in templates(ROOT/'Server/configs/MonsterAttrExTable.txt').items():
        def n(field,default=0):return float(row.get(field) or default)
        monsters[str(key)]=dict(hp=n('HP上限'),attack=n('物理攻击'),defence=n('物理防御'),hit=n('命中率'),miss=n('闪避'),critical=n('会心率'),criticalDefence=n('会心防御'),speed=n('移动速度')/1000,cooldownMilliseconds=n('攻击冷却时间',2400),actionMilliseconds=n('攻击动作时间',1200),traitId=10,sourceTraitId=n('攻击特性ID'),camp=n('阵营'),isNpc=n('是否可以交互')==1)
    world_root=ROOT/'Build/unity-world';config=ini(ROOT/'Server/configs/SceneInfo.ini');nav_root=world_root/'nav';nav_root.mkdir(exist_ok=True)
    nav_checked={}
    for summary in json.loads((world_root/'catalog.json').read_text())['scenes']:
        sid=summary['sceneId'];path=world_root/f'{sid}.json';world=json.loads(path.read_text())
        scn=ini(contained(ROOT/'Server/Game_2/Scene',config['scene'+str(sid)]['file']))['System']
        name=scn.get('navmapname')
        world['combatNavigationAvailable']=False
        if name:
            original=contained(ROOT/'Server/Game_2/Scene',name)
            if original.is_file():
                digest=hashlib.sha256(original.read_bytes()).hexdigest();filename=digest[:24]+'.path'
                target=nav_root/filename
                if not target.exists():target.write_bytes(original.read_bytes())
                if hashlib.sha256(target.read_bytes()).hexdigest()!=digest:raise ValueError('Altered exported nav image: '+str(target))
                world['navFile']='nav/'+filename;world['combatNavigationAvailable']=True
                nav_checked[name]=digest
        path.write_text(json.dumps(world,ensure_ascii=False,separators=(',',':'),allow_nan=False))
    from native_navigation import validate
    navigation_report=validate(world_root)
    print('Native navigation:',json.dumps(navigation_report,ensure_ascii=False))
    data=dict(schema=1,templates=monsters,physicalTraits=traits,sourceFunctions=hashes,sourceCoreSha256=hashlib.sha256(source.read_bytes()).hexdigest(),sourceMonsterSha256=hashlib.sha256((ROOT/'Server/configs/MonsterAttrExTable.txt').read_bytes()).hexdigest(),sourceTraitsSha256=hashlib.sha256(trait_path.read_bytes()).hexdigest(),navigation=nav_checked,
        profile=dict(id='unity-development',hp=100,attack=10,defence=5,hit=1000,miss=0,critical=0,criticalDefence=1,speed=5,cooldownMilliseconds=600,range=3),
        scope='Development basic physical combat only; original formulas/stats/nav are reused, full skills/equipment/buffs/progression are not connected')
    (world_root/'combat-data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False))
    print(f'Exported {len(monsters)} source templates, {len(traits)} physical traits, {len(nav_checked)} source nav files and {len(methods)} verbatim combat methods')
if __name__=='__main__':main()
