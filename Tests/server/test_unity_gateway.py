"""Integration checks against a fresh actual Skynet gateway, using fragmented TCP frames."""
import json
from pathlib import Path
import queue
import socket
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[2]

def main():
    process = subprocess.Popen([sys.executable, str(ROOT/'Tools/server/run_unity_gateway.py'), '--port', '0'],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    lines = queue.Queue()
    def collect():
        for line in process.stdout:
            lines.put(line)
    threading.Thread(target=collect, daemon=True).start()
    try:
        deadline = time.monotonic()+20
        port = None
        while time.monotonic() < deadline:
            try:
                line = lines.get(timeout=0.25)
            except queue.Empty:
                if process.poll() is not None: raise AssertionError('Gateway exited before readiness')
                continue
            if line.startswith('UNITY_GATEWAY_READY '):
                port = int(line.split()[1]); break
        assert port, 'Gateway readiness timeout'
        with socket.create_connection(('127.0.0.1', port), timeout=3) as connection:
            incoming = connection.makefile('rb')
            def receive():
                line = incoming.readline(65537)
                assert line, 'unexpected EOF'
                return json.loads(line)
            request = json.dumps({'v':1, 'id':'h1', 'method':'hello'}).encode()+b'\n'
            connection.sendall(request[:4]); connection.sendall(request[4:])
            hello = receive()
            assert hello['id']=='h1' and hello['ok'] and not hello['result']['gameplayReady']
            connection.sendall(b'{"v":1,"id":"p1","method":"ping"}\n{"v":1,"id":"x1","method":"login"}\n')
            ping = receive(); unknown = receive()
            assert ping['id']=='p1' and ping['result']['pong']
            assert unknown['id']=='x1' and unknown['error']['code']=='METHOD_NOT_IMPLEMENTED'
            for raw, expected in [(b'not-json\n', 'INVALID_JSON'), (b'null\n','INVALID_REQUEST'),
                                  (b'{"v":1}\n','INVALID_ID'),
                                  (b'{"v":2,"id":"v2","method":"ping"}\n','UNSUPPORTED_VERSION')]:
                connection.sendall(raw); assert receive()['error']['code']==expected
        with socket.create_connection(('127.0.0.1', port), timeout=3) as connection:
            connection.sendall(b'x'*70000)
            assert connection.recv(1)==b'', 'oversized frame must close'
        with socket.create_connection(('127.0.0.1', port), timeout=3) as connection:
            connection.sendall(b'{"v":1,"id":"p2","method":"ping"}\n')
            assert json.loads(connection.makefile('rb').readline())['id']=='p2'
        print('PASS: 9 gateway checks: hello, ping, unknown method, malformed JSON, null, missing ID, version, frame limit, reconnect; fragmented/coalesced framing exercised')
    finally:
        process.send_signal(__import__('signal').SIGINT)
        try: process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            process.kill(); process.wait()
        process.stdout.close()

if __name__ == '__main__':
    main()
