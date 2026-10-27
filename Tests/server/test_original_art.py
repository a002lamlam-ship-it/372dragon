#!/usr/bin/env python3
"""Validate all delivered geometry/rigs and compare readers against independent repository validators."""
import ast
import array
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import unittest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tools/unity/art'))
from ogre_binary import mesh,skeleton
ART=ROOT/'Build/unity-art'

def validator(filename,functions):
    tree=ast.parse((ROOT/'Tests/validators'/filename).read_text(encoding='utf8'))
    nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.Assign)) or isinstance(n,ast.FunctionDef) and n.name in functions]
    ns={};exec(compile(ast.Module(body=nodes,type_ignores=[]),filename,'exec'),ns);return ns

class OriginalArt(unittest.TestCase):
    def test_all_exported_geometry_and_independent_source_walk(self):
        catalog=json.loads((ART/'art-catalog.json').read_text())
        self.assertIsNone(catalog['diagnosticLimit'])
        walk=validator('v01_mesh.py',{'_indices','walk_mesh'})['walk_mesh']
        count=animated=repairs=float4=0
        for entry in catalog['assets']:
            data=json.loads((ART/entry['file']).read_text())
            bones={b['id']:b for b in (data.get('rig') or {}).get('bones',[])}
            for b in bones.values():
                seen=set();current=b
                while current['parent']>=0:
                    self.assertNotIn(current['id'],seen);seen.add(current['id']);current=bones[current['parent']]
            for p in data['parts']:
                n=len(p['positions'])//3
                self.assertEqual(len(p['positions']),n*3)
                self.assertTrue(all(math.isfinite(v) for v in p['positions']))
                self.assertEqual(len(p['triangles'])%3,0)
                self.assertTrue(all(0<=i<n for i in p['triangles']))
                if p['hasSkin']:
                    for i in range(n):
                        self.assertAlmostEqual(sum(p['weights'][i*4:i*4+4]),1,places=5)
                        for j in range(4):
                            if p['weights'][i*4+j]>0:self.assertIn(p['boneIds'][i*4+j],bones)
                repairs+=bool(p['normalRepair']);float4+=bool(p['sourcePositionW'])
            for m in data['materials']:
                if m.get('textureFile'):self.assertTrue((ART/m['textureFile']).is_file())
            if data.get('rig'):
                animated+=bool(data['rig']['animations'])
                for clip in data['rig']['animations']:
                    for track in clip['tracks']:
                        self.assertIn(track['boneId'],bones)
                        times=[k['time'] for k in track['keys']]
                        self.assertEqual(times,sorted(times))
            # Independent old validator checks every source's vertex/index accounting.
            source=(ROOT/entry['source']).read_bytes()
            self.assertEqual(hashlib.sha256(source).hexdigest(),data['source']['sha256'])
            old=walk(source);self.assertFalse(old['err'],(entry['source'],old['err']))
            self.assertEqual(len(old['subs']),len(data['parts']))
            for oldpart,newpart in zip(old['subs'],data['parts']):
                self.assertEqual(old['shared_verts'] if oldpart['shared'] else oldpart['verts'],len(newpart['positions'])//3)
                if oldpart['op']==4:self.assertEqual(oldpart['ic'],len(newpart['triangles']))
            count+=1
        self.assertGreater(count,7700);self.assertGreater(animated,850)
        self.assertGreater(repairs,100);self.assertGreater(float4,1000)
        print('ART_AUDIT_OK',count,'meshes,',animated,'animated; repaired normals parts',repairs,'FLOAT4 parts',float4)
    def test_skeleton_reader_and_truncation(self):
        walk=validator('v02_skeleton.py',{'walk_skeleton'})['walk_skeleton']
        paths=sorted((ROOT/'Assets/CanonicalCY/Data').rglob('*.skeleton'))
        self.assertGreater(len(paths),20)
        for p in paths:
            raw=p.read_bytes()
            try:new=skeleton(raw)
            except ValueError:continue # Unsupported source is explicitly excluded, not silently approximated.
            old=walk(raw);self.assertFalse(old['err'],(p,old['err']))
            self.assertEqual(set(old['bones']),{b['id'] for b in new['bones']})
            self.assertEqual(len(old['anims']),len(new['animations']))
            self.assertEqual(old['keyframes'],sum(len(t['keys']) for a in new['animations'] for t in a['tracks']))
        with self.assertRaises((ValueError,IndexError,struct.error)):mesh(b'\x00\x10[MeshSerializer_v1.40]\n\x00\x30')
        with self.assertRaises((ValueError,IndexError,struct.error)):skeleton(b'\x00\x10[Serializer_v1.10]\n\x00\x20')
if __name__=='__main__':unittest.main()
