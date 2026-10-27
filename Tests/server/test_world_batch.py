"""Validate every exported map plus paginated discovery and edge spawn pages against real Skynet."""
import importlib.util
import json
from pathlib import Path
import queue
import signal
import socket
import subprocess
import sys
import threading
import time
import unittest

ROOT=Path(__file__).resolve().parents[2]
WORLD=ROOT/'Build/unity-world'

class BatchTests(unittest.TestCase):
    def test_complete_accounting_and_payloads(self):
        catalog=json.loads((WORLD/'catalog.json').read_text())['scenes']
        report=json.loads((WORLD/'port-report.json').read_text())
        exported={s['sceneId'] for s in catalog};failed={s['sceneId'] for s in report['failures']};inactive=set(report['inactiveSceneIds'])
        self.assertFalse(exported & failed);self.assertFalse(exported & inactive);self.assertFalse(failed & inactive)
        spec=importlib.util.spec_from_file_location('export_world',ROOT/'Tools/unity/export_world.py')
        exporter=importlib.util.module_from_spec(spec);spec.loader.exec_module(exporter)
        config=exporter.ini(ROOT/'Server/configs/SceneInfo.ini')
        declared={int(s[5:]) for s in config.sections() if s.startswith('scene') and s[5:].isdigit()}
        self.assertEqual(exported | failed | inactive,declared)
        self.assertEqual(report['exported'],len(catalog));self.assertEqual(report['blocked'],len(failed))
        total=0
        for row in catalog:
            sid=row['sceneId'];bundle=json.loads((WORLD/f'{sid}.json').read_text())
            self.assertEqual(bundle['sceneId'],sid);self.assertEqual(bundle['sceneType'],row['sceneType'])
            self.assertEqual(len(bundle['entities']),row['entityCount']);self.assertEqual(len(bundle['staticObjects']),row['staticObjectCount'])
            self.assertEqual(len({e['id'] for e in bundle['entities']}),row['entityCount'])
            self.assertFalse(bundle['simulationReady'])
            self.assertEqual((WORLD/f'{sid}.heights.bytes').stat().st_size,(bundle['width']+1)*(bundle['depth']+1)*4)
            self.assertEqual((WORLD/f'{sid}.cells.bytes').stat().st_size,bundle['width']*bundle['depth'])
            self.assertEqual(sum(e['kind']=='npc' for e in bundle['entities']),row['npcCount'])
            self.assertEqual(len(bundle['warnings']),row['warningCount'])
            self.assertEqual(len(bundle['skippedEntities']),row['skippedEntityCount'])
            total+=row['entityCount']
        self.assertEqual(total,report['entityCount'])
        print(f'Validated {len(catalog)} map bundles, {total} source spawn placements, and all {len(declared)} scene dispositions')

    def test_gateway_all_maps_and_bounded_pages(self):
        expected=json.loads((WORLD/'catalog.json').read_text())['scenes']
        process=subprocess.Popen([sys.executable,str(ROOT/'Tools/server/run_unity_gateway.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        lines=queue.Queue()
        def collect():
            for line in process.stdout:lines.put(line)
        threading.Thread(target=collect,daemon=True).start()
        try:
            deadline=time.monotonic()+20;port=None
            while time.monotonic()<deadline:
                try:line=lines.get(timeout=.25)
                except queue.Empty:continue
                if line.startswith('UNITY_GATEWAY_READY '):port=int(line.split()[1]);break
            self.assertIsNotNone(port)
            with socket.create_connection(('127.0.0.1',port),timeout=15) as connection:
                stream=connection.makefile('rb')
                def call(method,params=None):
                    connection.sendall((json.dumps(dict(v=1,id='batch',method=method,params=params))+'\n').encode())
                    line=stream.readline(65537);self.assertLess(len(line),65536);self.assertTrue(line)
                    return json.loads(line)
                listed=[];offset=0
                while offset<len(expected):
                    page=call('world.list',dict(offset=offset,limit=37))['result']
                    self.assertGreater(page['nextOffset'],offset);listed+=page['scenes'];offset=page['nextOffset']
                self.assertEqual([s['sceneId'] for s in listed],[s['sceneId'] for s in expected])
                self.assertEqual(call('world.list',dict(offset=offset))['error']['code'],'PAGE_OUT_OF_RANGE')
                self.assertEqual(call('world.list',dict(limit=101))['error']['code'],'INVALID_PAGINATION')
                for row in expected:
                    sid=row['sceneId'];data=json.loads((WORLD/f'{sid}.json').read_text())
                    entered=call('world.enter',dict(sceneId=sid))['result']
                    self.assertEqual(entered['entityCount'],len(data['entities']));self.assertEqual(entered['sceneType'],data['sceneType'])
                    for i in {0,max(0,len(data['entities'])-1)}:
                        reply=call('world.entities',dict(sceneId=sid,offset=i,limit=1))
                        if not data['entities']:
                            self.assertEqual(reply['error']['code'],'PAGE_OUT_OF_RANGE')
                        else:
                            actual=reply['result']['items'][0];original=data['entities'][i]
                            self.assertEqual(actual['id'],original['id']);self.assertEqual(actual['templateId'],original['templateId'])
                # Revisit an evicted map to verify lazy reload after more than four worlds.
                first=expected[0]
                self.assertEqual(call('world.enter',dict(sceneId=first['sceneId']))['result']['entityCount'],first['entityCount'])
                print(f'Gateway validated discovery and enter/edge spawn pages for {len(expected)} maps; every response below 64KiB')
        finally:
            process.send_signal(signal.SIGINT)
            try:process.wait(timeout=8)
            except subprocess.TimeoutExpired:process.kill();process.wait()
            process.stdout.close()

if __name__=='__main__':unittest.main()
