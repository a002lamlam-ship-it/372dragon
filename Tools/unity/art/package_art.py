#!/usr/bin/env python3
"""Package converted original art into mergeable, bounded ZIP downloads and a complete starter."""
import hashlib
import json
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[3]
ART=ROOT/'Build/unity-art'
OUT=ROOT/'Build'
PREFIX='Assets/DragonPort/Art/'

def archive(path,files,catalog):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        z.writestr(PREFIX+'art-catalog.json',json.dumps(catalog,ensure_ascii=False,separators=(',',':')))
        for name in sorted(files):z.write(ART/name,PREFIX+name)
    with zipfile.ZipFile(path) as z:
        if z.testzip():raise ValueError('Bad ZIP '+str(path))
    return dict(file=path.name,bytes=path.stat().st_size,sha256=hashlib.file_digest(path.open('rb'),'sha256').hexdigest())

def main():
    c=json.loads((ART/'art-catalog.json').read_text())
    required=set();starter_ids=set()
    models=set()
    for sid in [2,6]:
        w=json.loads((OUT/f'unity-world/{sid}.json').read_text())
        models.update(e['modelId'] for e in w['entities'])
    starter_ids.update(a['assetId'] for a in c['actorBindings'] if a['modelId'] in models)
    starter_files=set()
    for a in c['assets']:
        required.add(a['file'])
        data=json.loads((ART/a['file']).read_text())
        deps={m['textureFile'] for m in data['materials'] if m.get('textureFile')}
        required.update(deps)
        if a['assetId'] in starter_ids:starter_files.update(deps|{a['file']})
    starter=dict(c)
    starter['assets']=[a for a in c['assets'] if a['assetId'] in starter_ids]
    starter['actorBindings']=[a for a in c['actorBindings'] if a['assetId'] in starter_ids]
    starter['sceneryBindings']=[]
    first=archive(OUT/'UnityOriginalActors-Starter.zip',starter_files,starter)
    print('Starter:',first,flush=True)
    # Bound by uncompressed size too, to keep imports/downloads manageable.
    packs=[];files=[];size=0
    for name in sorted(required):
        n=(ART/name).stat().st_size
        if files and size+n>250*1024*1024:
            packs.append(archive(OUT/f'UnityOriginalArt-{len(packs)+1:02d}.zip',files,c));print(packs[-1],flush=True);files=[];size=0
        files.append(name);size+=n
    if files:packs.append(archive(OUT/f'UnityOriginalArt-{len(packs)+1:02d}.zip',files,c));print(packs[-1],flush=True)
    manifest=dict(schema=1,starter=first,packs=packs,assetCount=len(c['assets']),files=len(required),instructions='Merge all full packs into the same Unity project Assets folder; starter is an optional self-contained actor subset for scenes 2 and 6. Full packs include the full catalog. Import skips missing assets until remaining packs are copied.')
    (OUT/'art-downloads.json').write_text(json.dumps(manifest,indent=2))
    lines=['# Original art downloads','','Start with [UnityMapPort.zip](UnityMapPort.zip), [starter actors](UnityOriginalActors-Starter.zip) and [server source/data](NativeServerChanges.zip).','',
        'Copy Assets folders into your Unity project. Starter contains only bindable actors used in maps 2 and 6, without scenery. For all converted scenery/actors, merge **every full pack below**; these are separate ZIPs, not multipart ZIP volumes. Run Tools → Dragon Port → Import Original Meshes and Animations after copying.','',
        'Missing all.obj composition data prevents reliable automatic binding for 755 of 914 referenced actor models. These retain capsule placeholders. Original shader effects and full legacy skill logic are not ported. See ART-COMBAT.md at the root of the core ZIP.','', '| Download | MiB |','|---|---:|']
    for p in packs:lines.append(f"| [{p['file']}]({p['file']}) | {p['bytes']/1024**2:.1f} |")
    lines+=['','Checksums and exact byte counts: [art-downloads.json](art-downloads.json).','', 'Preview rendered in Blender from converted original mesh and original attack keys: [rest](art-render/rest.png), [attack](art-render/attack.png). Unity Editor and macOS execution remain untested.']
    (OUT/'ART-DOWNLOADS.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()
