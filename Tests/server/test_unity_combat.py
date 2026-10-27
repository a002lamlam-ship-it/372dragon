"""Actual Skynet/native-nav combat tests; clients cannot specify damage, HP or movement speed."""
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
class CombatTests(unittest.TestCase):
 def test_actual_authority_and_lifecycle(self):
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
   with socket.create_connection(('127.0.0.1',port),timeout=5) as connection:
    stream=connection.makefile('rb')
    def call(method,params):
     connection.sendall((json.dumps(dict(v=1,id='combat-test',method=method,params=params))+'\n').encode())
     line=stream.readline(65537);self.assertTrue(line);self.assertLess(len(line),65536);return json.loads(line)
    self.assertEqual(call('combat.attack',dict(targetId='6:monster0'))['error']['code'],'COMBAT_NOT_JOINED')
    self.assertEqual(call('combat.join',dict(sceneId=40))['error']['code'],'COMBAT_NAV_UNAVAILABLE')
    joined=call('combat.join',dict(sceneId=6));self.assertTrue(joined['ok'],joined);self.assertFalse(joined['result']['persistent']);print('JOIN',joined['result'])
    self.assertEqual(call('combat.join',dict(sceneId=6))['error']['code'],'COMBAT_ALREADY_JOINED')
    before=call('combat.snapshot',dict(limit=100))['result'];self.assertLessEqual(before['player']['hp'],100)
    self.assertEqual(call('combat.move',dict(x=-1,z=0))['error']['code'],'INVALID_POSITION')
    self.assertEqual(call('combat.move',dict(x=300,z=300,speed=9999))['error']['code'],'MOVE_TOO_FAR')
    source=json.loads((ROOT/'Build/unity-world/6.json').read_text())
    npc=next(e for e in source['entities'] if e['kind']=='npc')
    self.assertEqual(call('combat.attack',dict(targetId=npc['id']))['error']['code'],'TARGET_NOT_HOSTILE')
    far=next(e for e in source['entities'] if e['kind']=='monster' and abs(e['x']-before['player']['x'])+abs(e['z']-before['player']['z'])>50)
    self.assertEqual(call('combat.attack',dict(targetId=far['id']))['error']['code'],'OUT_OF_RANGE')
    attack=call('combat.attack',dict(targetId='6:monster0',damage=1000000000,hp=99999,critical=True))
    self.assertTrue(attack['ok'],attack);print('ATTACK',attack['result']);self.assertLess(attack['result']['damage'],100)
    repeat=call('combat.attack',dict(targetId='6:monster0'))
    self.assertIn(repeat['error']['code'],['ATTACK_COOLDOWN','TARGET_DEAD'])
    after=call('combat.snapshot',dict(limit=100))['result'];self.assertTrue(after['events']);self.assertLessEqual(after['player']['hp'],100)
    self.assertEqual(call('combat.respawn',{})['error']['code'],'PLAYER_ALIVE')
    self.assertTrue(call('combat.leave',{})['result']['left'])
    self.assertEqual(call('combat.snapshot',{})['error']['code'],'COMBAT_NOT_JOINED')
    self.assertTrue(call('combat.join',dict(sceneId=6))['ok'])
   with socket.create_connection(('127.0.0.1',port),timeout=5) as other:
    other.sendall(b'{"v":1,"id":"other","method":"combat.snapshot","params":{}}\n')
    self.assertEqual(json.loads(other.makefile('rb').readline())['error']['code'],'COMBAT_NOT_JOINED')
  finally:
   process.send_signal(signal.SIGINT)
   try:process.wait(timeout=8)
   except subprocess.TimeoutExpired:process.kill();process.wait()
   process.stdout.close()
if __name__=='__main__':unittest.main()
