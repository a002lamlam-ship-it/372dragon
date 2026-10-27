#!/usr/bin/env python3
"""Convert original referenced Ogre meshes and linked skeletal animations into Unity import data."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
from PIL import Image
from asset_source import AssetSource, ROOT, variants
from ogre_binary import mesh,skeleton,text


def dbc(path):
    raw=path.read_bytes();magic,nf,nr,poolsize=struct.unpack_from('<4I',raw)
    if magic!=0xDDBBCC00 or len(raw)!=16+nf*4+nf*nr*4+poolsize:raise ValueError('Invalid DBC: '+str(path))
    types=struct.unpack_from('<'+'I'*nf,raw,16);base=16+4*nf;pool=raw[base+nf*nr*4:];rows={}
    for r in range(nr):
        values=struct.unpack_from('<'+'I'*nf,raw,base+r*nf*4);out=[]
        for t,v in zip(types,values):
            if t==2:out.append(text(pool[v:pool.index(b'\0',v)]))
            elif t==1:out.append(struct.unpack('<f',struct.pack('<I',v))[0])
            else:out.append(struct.unpack('<i',struct.pack('<I',v))[0])
        rows[out[0]]=out
    return rows


def materials(raw):
    result={};header=None;body=[];depth=0;opened=False
    for line in raw.splitlines(keepends=True):
        clean=line.split(b'//',1)[0].strip()
        if header is None:
            if not clean.startswith(b'material '):continue
            header=clean[9:].split(b'{',1)[0].strip();body=[line];depth=clean.count(b'{')-clean.count(b'}');opened=b'{' in clean
        else:
            body.append(line);depth+=clean.count(b'{')-clean.count(b'}');opened=opened or b'{' in clean
        if opened and depth==0:
            try:
                parts=header.split(b':',1);name=text(parts[0].strip().strip(b'"'))
                base=text(parts[1].strip().strip(b'"')) if len(parts)>1 else ''
                result.setdefault(name,dict(body=b''.join(body),base=base))
            except UnicodeError:pass
            header=None;body=[];opened=False
    return result


def material_info(name,blocks):
    seen=set();parts=[];current=name
    while current and current not in seen:
        seen.add(current);block=blocks.get(current)
        if not block:break
        parts.append(block['body']);current=block['base']
    combined=b'\n'.join(parts)
    texture=''
    candidates=re.findall(rb'(?m)^\s*set_texture_alias\s+<baseTexture>\s+("[^"]+"|[^\r\n]+)',combined)
    if not candidates:candidates=re.findall(rb'(?m)^\s*texture\s+("[^"]+"|[^\r\n]+)',combined)
    if candidates:
        raw=candidates[0].strip();raw=raw[1:-1] if raw.startswith(b'"') else raw.split()[0]
        try:texture=text(raw)
        except UnicodeError:pass
    alpha=re.search(rb'alpha_rejection\s+greater(?:_equal)?\s+(\d+)',combined)
    transparent=bool(re.search(rb'scene_blend\s+(alpha_blend|src_alpha)',combined))
    return dict(name=name,textureReference=texture,textureFile='',alphaCutoff=int(alpha[1])/255 if alpha else 0,
                transparent=transparent,doubleSided=b'cull_hardware none' in combined,
                shaderApproximation=True,sourceMaterialFound=name in blocks)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--world-root',type=Path,default=ROOT/'Build/unity-world')
    ap.add_argument('--out',type=Path,default=ROOT/'Build/unity-art')
    ap.add_argument('--limit',type=int,help='Optional mesh limit for format diagnostics only')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    source=AssetSource();failures=[]
    try:
        source.fetch(['Assets/CanonicalCY/Data/ConfigFolder/CharModelEx.txt','Assets/CanonicalCY/Data/MaterialFolder/all.material'])
        models=dbc(ROOT/'Assets/CanonicalCY/Data/ConfigFolder/CharModelEx.txt')
        scenery=set();used_models=set()
        for summary in json.loads((args.world_root/'catalog.json').read_text())['scenes']:
            world=json.loads((args.world_root/f"{summary['sceneId']}.json").read_text())
            scenery.update(r['resource'] for r in world['staticObjects']);used_models.update(r['modelId'] for r in world['entities'])
        requests={};scenery_bindings=[];actor_bindings=[];unresolved_actors=[]
        for name in sorted(scenery):
            path=source.resolve(name)
            if path:requests[path]=name;scenery_bindings.append(dict(resource=name,path=path))
            else:failures.append(dict(kind='missing-scenery-mesh',resource=name))
        for model_id in sorted(used_models):
            row=models.get(model_id)
            if not row:
                unresolved_actors.append(dict(modelId=model_id,reason='CharModelEx row absent'));continue
            object_name=row[1];name=str(Path(object_name).with_suffix('.mesh'))
            path=source.resolve(name)
            if not path:
                unresolved_actors.append(dict(modelId=model_id,objectReference=object_name,reason='all.obj absent and no exact same-name single mesh; multipart composition not inferred'));continue
            requests[path]=name
            actor_bindings.append(dict(modelId=model_id,path=path,objectReference=object_name,importScale=1.0,actionSetFileId=row[20],bindingEvidence='CharModelEx object stem matches mesh name; original all.obj composition/transforms unavailable; unit import scale 1, CharModelEx column 3 is fuse time, not model scale'))
        # Always retain a concrete original animated monster for the combat/animation smoke workflow.
        ape=source.resolve('高山白猿.mesh')
        if ape:requests[ape]='高山白猿.mesh'
        paths=sorted(requests)
        if args.limit:
            paths=([ape] if ape else [])+[p for p in paths if p!=ape][:max(0,args.limit-1)]
        source.fetch(paths)
        converted={};parsed={};skeleton_paths=set()
        for i,path in enumerate(paths,1):
            try:
                result=mesh((ROOT/path).read_bytes());parsed[path]=result
                if result['skeleton']:
                    skel_path=source.resolve(result['skeleton'])
                    if not skel_path:raise ValueError('Linked skeleton missing: '+result['skeleton'])
                    skeleton_paths.add(skel_path)
            except (ValueError,KeyError,IndexError,UnicodeError,struct.error) as e:failures.append(dict(kind='mesh-conversion',path=path,reason=str(e)))
            if i%500==0:print(f'Meshes decoded {i}/{len(paths)}',flush=True)
        source.fetch(skeleton_paths)
        skeletons={};pending=set(skeleton_paths)
        while pending:
            next_paths=set()
            for path in sorted(pending):
                if path in skeletons:continue
                try:
                    result=skeleton((ROOT/path).read_bytes());skeletons[path]=result
                    for link in result['links']:
                        linked=source.resolve(link['name'])
                        if not linked:raise ValueError('Animation link absent: '+link['name'])
                        if linked not in skeletons:next_paths.add(linked)
                except (ValueError,KeyError,IndexError,UnicodeError,struct.error) as e:failures.append(dict(kind='skeleton-conversion',path=path,reason=str(e)))
            source.fetch(next_paths);pending=next_paths
        blocks=materials((ROOT/'Assets/CanonicalCY/Data/MaterialFolder/all.material').read_bytes())
        mats={};textures=set()
        for result in parsed.values():
            for part in result['parts']:
                name=part['material']
                if name not in mats:
                    info=material_info(name,blocks);mats[name]=info
                    if info['textureReference']:
                        path=source.resolve(info['textureReference'])
                        if path:textures.add(path);info['texturePath']=path
        source.fetch(textures)
        texture_errors=[]
        for i,path in enumerate(sorted(textures),1):
            name=source.index[path]['sha256'][:24]+'.png'
            try:
                target=args.out/name
                if target.exists():
                    with Image.open(target) as cached:cached.verify()
                else:
                    with Image.open(ROOT/path) as image:image.convert('RGBA').save(target)
                for info in mats.values():
                    if info.get('texturePath')==path:info['textureFile']=name
            except (ValueError,OSError) as e:texture_errors.append(dict(path=path,reason=str(e)))
            if i%500==0:print(f'Textures converted {i}/{len(textures)}',flush=True)
        def merge_animations(base,path,visited):
            if path in visited:raise ValueError('Cyclic skeleton animation link')
            visited=visited|{path}
            result=skeletons.get(path)
            if result is None:raise ValueError('Skeleton conversion failed')
            names={a['name'] for a in base['animations']}
            base_names={b['id']:b['name'] for b in base['bones']}
            for link in result['links']:
                linked=source.resolve(link['name']);child=skeletons.get(linked)
                if not child or {b['id']:b['name'] for b in child['bones']}!=base_names:raise ValueError('Linked skeleton bone layout mismatch')
                for animation in child['animations']:
                    if animation['name'] in names:continue
                    copied=json.loads(json.dumps(animation));factor=link['scale']
                    for track in copied['tracks']:
                        for key in track['keys']:key['position']=[v*factor for v in key['position']]
                    base['animations'].append(copied);names.add(copied['name'])
                merge_animations(base,linked,visited)
        for i,(path,result) in enumerate(parsed.items(),1):
            try:
                skel=None
                if result['skeleton']:
                    skel_path=source.resolve(result['skeleton']);skel=json.loads(json.dumps(skeletons.get(skel_path)))
                    if skel is None:raise ValueError('Referenced skeleton failed conversion')
                    merge_animations(skel,skel_path,set())
                    handles={b['id'] for b in skel['bones']}
                    for part in result['parts']:
                        if part['hasSkin']:
                            if any(b not in handles for b,w in zip(part['boneIds'],part['weights']) if w>0):raise ValueError('Skin references missing bone')
                            if any(sum(part['weights'][n:n+4])<.999 for n in range(0,len(part['weights']),4)):raise ValueError('Unweighted vertex in skinned part')
                result['rig']=skel
                result['materials']=[mats[part['material']] for part in result['parts']]
                result['source']=dict(path=path,sha256=source.index[path]['sha256'],unitScale=.01,winding='reversed-for-Unity',axes='XYZ-preserved')
                asset_id=source.index[path]['sha256'][:24];output=args.out/(asset_id+'.dragon.json')
                output.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf8')
                converted[path]=dict(assetId=asset_id,file=output.name,source=path,parts=len(result['parts']),vertices=sum(len(p['positions'])//3 for p in result['parts']),animationCount=len(skel['animations']) if skel else 0)
            except (ValueError,KeyError,IndexError,UnicodeError,TypeError) as e:failures.append(dict(kind='asset-assembly',path=path,reason=str(e)))
            if i%500==0:print(f'Unity art exported {i}/{len(parsed)}',flush=True)
        scenery_bindings=[dict(resource=b['resource'],assetId=converted[b['path']]['assetId']) for b in scenery_bindings if b['path'] in converted]
        actor_bindings=[dict(modelId=b['modelId'],assetId=converted[b['path']]['assetId'],importScale=b['importScale'],actionSetFileId=b['actionSetFileId'],objectReference=b['objectReference'],bindingEvidence=b['bindingEvidence']) for b in actor_bindings if b['path'] in converted]
        report=dict(schema=1,assets=list(converted.values()),sceneryBindings=scenery_bindings,actorBindings=actor_bindings,
            failures=failures,unresolvedActors=unresolved_actors,textureFailures=texture_errors,ambiguities=source.ambiguities,
            allObjPresent=any(p.casefold().endswith('/all.obj') for p in source.index),diagnosticLimit=args.limit,
            integrity='Source member CRC and SHA-256 verified; full archive hash not verified')
        (args.out/'art-catalog.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
        (args.out/'art-source-audit.json').write_text(json.dumps(list(source.verified.values()),ensure_ascii=False,indent=2))
        print(json.dumps(dict(meshes=len(converted),animatedMeshes=sum(v['animationCount']>0 for v in converted.values()),sceneryBindings=len(scenery_bindings),actorBindings=len(actor_bindings),unresolvedActors=len(unresolved_actors),failures=len(failures),textures=len(textures),textureFailures=len(texture_errors),allObjPresent=report['allObjPresent']),ensure_ascii=False),flush=True)
    finally:source.close()

if __name__=='__main__':main()
