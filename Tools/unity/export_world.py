#!/usr/bin/env python3
"""Export real TLBB scene/spawn/terrain data to a Unity-neutral bundle; source files stay unchanged."""
import argparse
import configparser
import hashlib
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
from functools import lru_cache


def ini(path):
    parser = configparser.ConfigParser(interpolation=None, inline_comment_prefixes=(';',), strict=False)
    text=Path(path).read_bytes().decode('gb18030')
    # Match legacy inireader: semicolon starts a comment even directly after '='.
    parser.read_string('\n'.join(line.split(';',1)[0] for line in text.splitlines()))
    return parser


def contained(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Reference escapes data root: '+relative)
    return path


def number(value, label):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('Nonfinite '+label)
    return result


@lru_cache(maxsize=4)
def templates(path):
    lines = [s for s in Path(path).read_bytes().decode('gb18030').splitlines() if s and not s.startswith('#')]
    keys = lines[1].split('\t')
    result = {}
    for line in lines[2:]:
        cells = line.split('\t')
        if not cells[0].lstrip('-').isdigit():
            continue
        row = dict(zip(keys, cells))
        result[int(cells[0])] = row
    return result


def heightmap(path, width, depth):
    raw = Path(path).read_bytes()
    if len(raw) < 16 or struct.unpack('<4I', raw[:16]) != (0x4645484D, 0x100000, width+1, depth+1):
        raise ValueError('Heightmap header/dimensions mismatch: '+str(path))
    if len(raw) != 16+4*(width+1)*(depth+1):
        raise ValueError('Heightmap payload size mismatch')
    values = struct.unpack('<'+'f'*((width+1)*(depth+1)), raw[16:])
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Nonfinite height sample')
    return values, raw[16:]


def gridinfo(path, width, depth):
    raw = Path(path).read_bytes()
    magic, version, w, d = struct.unpack('<4I', raw[:16])
    if magic != 0x46454749 or not 0x100000 <= version <= 0x100002 or (w,d)!=(width,depth):
        raise ValueError('Invalid GridInfo header')
    offset = 16
    wide = False
    if version >= 0x100002:
        wide = bool(raw[offset]); offset += 1
    layer_size = 3 if wide else 2
    stride = 2*layer_size + (1 if version >= 0x100001 else 0)
    if len(raw) != offset+stride*w*d:
        raise ValueError('Invalid GridInfo size')
    result = bytearray()
    for i in range(w*d):
        row = raw[offset+i*stride:offset+(i+1)*stride]
        first = int.from_bytes(row[:2], 'little') if wide else row[0]
        second = int.from_bytes(row[layer_size:layer_size+2], 'little') if wide else row[layer_size]
        flip = row[-1]&1 if version >= 0x100001 else 0
        result.append(flip | (2 if first == 0 else 0))
    return bytes(result)


def sample(values, flags, width, depth, x, z):
    x = min(max(x,0),width); z = min(max(z,0),depth)
    ix = min(int(x),width-1); iz = min(int(z),depth-1)
    u,v = x-ix,z-iz
    a,b = values[iz*(width+1)+ix:iz*(width+1)+ix+2]
    c,d = values[(iz+1)*(width+1)+ix:(iz+1)*(width+1)+ix+2]
    if flags[iz*width+ix]&1:
        return a+(b-a)*u+(d-b)*v if v<=u else a+(d-c)*u+(c-a)*v
    return a+(b-a)*u+(c-a)*v if u+v<=1 else d+(c-d)*(1-u)+(b-d)*(1-v)


@lru_cache(maxsize=4)
def resource_index(data):
    lookup = {}
    for path in data.rglob('*'):
        if path.is_file() and path.suffix.lower() in ('.scene', '.terrain', '.heightmap', '.gridinfo'):
            lookup.setdefault(path.name.casefold(), []).append(path)
    return lookup


def resource(data, reference, preferred=None):
    relative = reference.replace('\\','/')
    contained(data, relative)  # Reject absolute or escaping references before lookup.
    if preferred:
        direct = contained(preferred, relative)
        if direct.is_file(): return direct
    matches = resource_index(data).get(Path(relative).name.casefold(), [])
    if len(matches)==1: return matches[0]
    if not matches: raise FileNotFoundError('Client resource missing: '+reference)
    raise ValueError('Ambiguous client resource: '+reference)


def export_scene(server, data, scene_id, output, aliases=None):
    source_paths = []
    def source(path):
        path=Path(path); source_paths.append(path); return path
    info_path=source(server/'configs/SceneInfo.ini')
    info=ini(info_path)['scene'+str(scene_id)]
    scene_root=server/'Game_2/Scene'
    config=ini(source(contained(scene_root, info['file'])))['System']
    visual_name=Path(info['file']).stem
    folder=data/'SceneFolder'
    resolution={'kind':'scene-file-stem'}
    try:
        visual=source(resource(data,visual_name+'.Scene',folder))
    except FileNotFoundError:
        nav_name=Path(config.get('navmapname','')).stem
        try:
            if not nav_name or nav_name.casefold()==visual_name.casefold(): raise FileNotFoundError('Client resource missing: '+visual_name+'.Scene')
            visual=source(resource(data,nav_name+'.Scene',folder))
            resolution={'kind':'navigation-file-stem'}
        except FileNotFoundError:
            alias=(aliases or {}).get(scene_id)
            if not alias: raise
            visual=source(resource(data,alias['resource'],data))
            resolution=alias
            source(data/'ConfigFolder/SceneDefineEx.txt')
    scene_xml=ET.parse(visual).getroot()
    terrain_ref=scene_xml.find('Terrain')
    if terrain_ref is None: raise ValueError('Scene has no terrain')
    terrain_path=source(resource(data,terrain_ref.attrib['filename'],visual.parent))
    terrain_xml=ET.parse(terrain_path).getroot()
    width,depth=int(terrain_xml.attrib['xsize']),int(terrain_xml.attrib['zsize'])
    if not 0<width<=4096 or not 0<depth<=4096: raise ValueError('Terrain dimensions outside supported bounds')
    scale=None; origin=None
    for child in terrain_xml:
        if child.tag in ('scale','size'):
            v=[number(child.attrib[k],k) for k in ('x','y','z')]
            scale=v if child.tag=='scale' else [v[0]/width,v[1],v[2]/depth]
            if min(scale)<=0: raise ValueError('Scale must be positive')
            origin=[-scale[0]*width/2,0,-scale[2]*depth/2]
        elif child.tag in ('position','centre','center'):
            if scale is None: raise ValueError('Position before scale')
            origin=[number(child.attrib[k],k) for k in ('x','y','z')]
            if child.tag!='position': origin=[origin[0]-scale[0]*width/2,origin[1],origin[2]-scale[2]*depth/2]
    if scale is None: raise ValueError('Terrain scale is required')
    ref=terrain_xml.find('heightmap')
    if ref is None or ref.get('type','standard')!='standard':raise ValueError('Only standard FEHM heightmaps supported')
    values,height_bytes=heightmap(source(resource(data,ref.attrib['filename'],terrain_path.parent)),width,depth)
    grid=terrain_xml.find('gridInfo')
    flags=gridinfo(source(resource(data,grid.attrib['filename'],terrain_path.parent)),width,depth) if grid is not None else bytes(width*depth)
    attr=templates(source(server/'configs/MonsterAttrExTable.txt'))
    spawns=ini(source(contained(scene_root,config['monsterfile']))) if config.get('monsterfile') else None
    entities=[]; skipped=[]; warnings=[]; skipped_entities=[]
    angles={0:0,5:135,9:270,14:315,18:180,23:45,27:90,32:225}
    for i in range(int(spawns['info']['monstercount']) if spawns else 0):
        key='monster'+str(i)
        if key not in spawns:
            skipped.append(key); continue
        row=spawns[key]
        if not row.get('pos_x') or not row.get('pos_z'):
            skipped.append(key); continue
        type_id=int(row['type'])
        if type_id not in attr:
            skipped_entities.append(dict(section=key,reason=f'template {type_id} missing; legacy server also skips this entity'))
            continue
        template=attr[type_id]
        x,z=number(row['pos_x'],key),number(row['pos_z'],key)
        if not 0<=x<=width or not 0<=z<=depth:
            warnings.append(f'{key}: spawn outside terrain bounds ({x},{z})')
        direction=number(row.get('dir','27'),key)
        radians=direction if direction>=100 else math.pi/2-math.radians(angles.get(direction,90))
        entities.append(dict(id=f'{scene_id}:{key}',templateId=type_id,
            modelId=int(template.get('外型ID') or 0),kind='npc' if template.get('是否可以交互')=='1' else 'monster',
            name=row.get('name') or template.get('名称$1$',''),title=row.get('title',''),
            x=x,y=sample(values,flags,width,depth,x,z),z=z,yaw=math.degrees(radians),
            level=int(template.get('等级') or 0),hp=int(template.get('HP上限') or 0),
            scriptId=int(row.get('script_id','-1')),aiType=int(row.get('base_ai',template.get('基础AI') or '0')),
            respawnMilliseconds=int(row.get('respawn_time','-1')),sourceSection=key))
    objects=[]
    for obj in scene_xml.iter('Object'):
        if obj.get('type')!='StaticEntity':continue
        props={p.get('name'):p.get('value') for p in obj.findall('Property')}
        if 'mesh name' not in props:continue
        position=[float(v) for v in props.get('position','0 0 0').split()]
        q=[float(v) for v in props.get('orientation','1 0 0 0').split()]
        objects.append(dict(resource=props['mesh name'],x=(position[0]-origin[0])/scale[0],
            y=(position[1]-origin[1])/scale[1],z=(position[2]-origin[2])/scale[2],
            rotation=dict(x=q[1],y=q[2],z=q[3],w=q[0]),
            sourceScale=[float(v) for v in props.get('scale','1 1 1').split()]))
    world=dict(schema=1,sceneId=scene_id,sceneType=int(info.get('type',0)),clientResourceId=int(info.get('clientres',scene_id)),name=info.get('name',''),
        coordinates='server-grid-XZ-height-samples-Y',width=width,depth=depth,
        sourceScale=scale,sourceOrigin=origin,resourceResolution=resolution,entities=entities,staticObjects=objects,
        skippedSections=skipped,skippedEntities=skipped_entities,warnings=warnings,simulationReady=False,
        sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in dict.fromkeys(source_paths)])
    output.mkdir(parents=True,exist_ok=True)
    (output/f'{scene_id}.heights.bytes').write_bytes(height_bytes)
    (output/f'{scene_id}.cells.bytes').write_bytes(flags)
    (output/f'{scene_id}.json').write_text(json.dumps(world,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf-8')
    return dict(sceneId=scene_id,name=world['name'],width=width,depth=depth,entityCount=len(entities),
                npcCount=sum(e['kind']=='npc' for e in entities),monsterCount=sum(e['kind']=='monster' for e in entities),staticObjectCount=len(objects),warningCount=len(warnings),skippedEntityCount=len(skipped_entities),sceneType=int(info.get('type',0)))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--server-root',type=Path,required=True)
    ap.add_argument('--client-data',type=Path,required=True)
    ap.add_argument('--scenes',default='2,6')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    catalog=[export_scene(args.server_root.resolve(),args.client_data.resolve(),int(s),args.out.resolve()) for s in args.scenes.split(',')]
    (args.out/'catalog.json').write_text(json.dumps(dict(schema=1,scenes=catalog),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(catalog,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
