#!/usr/bin/env python3
"""Start the development JSON/TCP gateway; no DB, game data, MQTT or llicense needed."""
import argparse
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / 'Server/GameServer'
FRAMEWORK = GAME / 'framework'

def quote(value):
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"') + '"'

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=15800)
    parser.add_argument('--world-root', type=Path, default=ROOT/'Build/unity-world', help='Exported world bundle directory')
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port must be 0..65535')
    values = {
        'thread': 2, 'harbor': 0, 'bootstrap': 'snlua bootstrap',
        'start': 'unity_gateway', 'skip_license_check': 'true',
        'unity_world_root': str(args.world_root.resolve()), 'unity_host': args.host, 'unity_port': args.port,
        'lualoader': FRAMEWORK / 'lualib/loader.lua',
        'luaservice': f'{GAME}/services/?.lua;{FRAMEWORK}/service/?.lua',
        'lua_path': f'{GAME}/services/?.lua;{GAME}/lualib/?.lua;{FRAMEWORK}/lualib/?.lua;{FRAMEWORK}/lualib/?/init.lua',
        'lua_cpath': f'{GAME}/luaclib/?.so;{FRAMEWORK}/luaclib/?.so',
        'cpath': FRAMEWORK / 'cservice/?.so',
    }
    with tempfile.TemporaryDirectory(prefix='372dragon-unity-') as directory:
        config = Path(directory) / 'config.lua'
        config.write_text('\n'.join(f'{k} = {v if isinstance(v, int) else quote(v)}' for k,v in values.items())+'\n')
        process = subprocess.Popen([str(FRAMEWORK / 'skynet'), str(config)], cwd=GAME)
        try:
            raise SystemExit(process.wait())
        except KeyboardInterrupt:
            pass
        finally:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()

if __name__ == '__main__':
    main()
