"""Validate source-backed exports and actual paginated gateway responses for both exported maps."""
import importlib.util
import json
from pathlib import Path
import queue
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('export_world',ROOT/'Tools/unity/export_world.py')
exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)

class FormatTests(unittest.TestCase):
    def test_legacy_disabled_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'spawns.ini'
            path.write_bytes(b'[monster0]\npos_x=;108.1\npos_z=;140.3\n')
            parsed=exporter.ini(path)
            self.assertEqual(parsed['monster0']['pos_x'],'')
            self.assertEqual(parsed['monster0']['pos_z'],'')

    def test_triangle_interpolation_respects_flip(self):
        values=[0,2,4,10]
        self.assertAlmostEqual(exporter.sample(values,b'\0',1,1,.5,.5),3)
        self.assertAlmostEqual(exporter.sample(values,b'\1',1,1,.5,.5),5)
        self.assertAlmostEqual(exporter.sample(values,b'\1',1,1,1,1),10)
    def test_corrupt_and_truncated_heightmaps_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'map.Heightmap'
            for data in [b'',struct.pack('<4I',0,0x100000,2,2)+bytes(16),struct.pack('<4I',0x4645484D,0x100000,2,2)+bytes(12)]:
                path.write_bytes(data)
                with self.assertRaises(ValueError):exporter.heightmap(path,1,1)
    def test_grid_holes_and_flips(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'map.GridInfo'
            path.write_bytes(struct.pack('<4I',0x46454749,0x100002,2,1)+b'\1'+struct.pack('<HBHBB',1,0,0,0,1)+bytes(7))
            self.assertEqual(exporter.gridinfo(path,2,1),b'\1\2')
    def test_references_cannot_escape_data_root(self):
        with self.assertRaises(ValueError):exporter.contained(ROOT,'../escape')
    def test_source_backed_bundles(self):
        for sid,npc,mob in [(2,172,8),(6,22,317)]:
            world=json.loads((ROOT/f'Build/unity-world/{sid}.json').read_text())
            self.assertFalse(world['simulationReady'])
            self.assertEqual(sum(e['kind']=='npc' for e in world['entities']),npc)
            self.assertEqual(sum(e['kind']=='monster' for e in world['entities']),mob)
            self.assertEqual(len({e['id'] for e in world['entities']}),len(world['entities']))
            for row in world['entities']:
                self.assertGreaterEqual(row['x'],0);self.assertLessEqual(row['x'],world['width'])
                self.assertGreaterEqual(row['z'],0);self.assertLessEqual(row['z'],world['depth'])
            for suffix,count in [('heights.bytes',(world['width']+1)*(world['depth']+1)*4),('cells.bytes',world['width']*world['depth'])]:
                self.assertEqual((ROOT/f'Build/unity-world/{sid}.{suffix}').stat().st_size,count)

class GatewayTests(unittest.TestCase):
    def test_real_world_pagination_and_errors(self):
        process=subprocess.Popen([sys.executable,str(ROOT/'Tools/server/run_unity_gateway.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        lines=queue.Queue()
        def collect():
            for line in process.stdout:lines.put(line)
        threading.Thread(target=collect,daemon=True).start()
        try:
            port=None; deadline=time.monotonic()+20
            while time.monotonic()<deadline:
                try:line=lines.get(timeout=.25)
                except queue.Empty:continue
                if line.startswith('UNITY_GATEWAY_READY '):port=int(line.split()[1]);break
            self.assertIsNotNone(port)
            with socket.create_connection(('127.0.0.1',port),timeout=5) as connection:
                incoming=connection.makefile('rb')
                def call(method,params=None):
                    connection.sendall((json.dumps(dict(v=1,id='world-test',method=method,params=params))+'\n').encode())
                    raw=incoming.readline(65537);self.assertLess(len(raw),65536)
                    return json.loads(raw)
                listing=[]; list_offset=0
                while True:
                    page=call('world.list',dict(offset=list_offset,limit=50))['result']
                    listing+=page['scenes'];list_offset=page['nextOffset']
                    if list_offset==page['total']:break
                self.assertTrue({2,6}.issubset({x['sceneId'] for x in listing}))
                for sid in [2,6]:
                    expected=json.loads((ROOT/f'Build/unity-world/{sid}.json').read_text())['entities']
                    entered=call('world.enter',dict(sceneId=sid))['result']
                    self.assertEqual(entered['entityCount'],len(expected));self.assertFalse(entered['simulationReady'])
                    collected=[];offset=0
                    while offset<len(expected):
                        result=call('world.entities',dict(sceneId=sid,offset=offset,limit=50))['result']
                        self.assertGreater(result['nextOffset'],offset);offset=result['nextOffset'];collected+=result['items']
                    self.assertEqual([r['id'] for r in collected],[r['id'] for r in expected])
                    for actual,original in zip(collected,expected):
                        self.assertEqual(actual['templateId'],original['templateId']);self.assertAlmostEqual(actual['y'],original['y'],places=6)
                    self.assertEqual(call('world.entities',dict(sceneId=sid,offset=offset))['error']['code'],'PAGE_OUT_OF_RANGE')
                for params,error in [(dict(sceneId=999),'WORLD_NOT_FOUND'),(dict(sceneId=2,limit=101),'INVALID_PAGINATION'),(dict(sceneId=2,offset=-1),'INVALID_PAGINATION')]:
                    self.assertEqual(call('world.entities',params)['error']['code'],error)
        finally:
            process.send_signal(signal.SIGINT)
            try:process.wait(timeout=8)
            except subprocess.TimeoutExpired:process.kill();process.wait()
            process.stdout.close()

if __name__=='__main__':unittest.main()
