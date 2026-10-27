#!/usr/bin/env python3
"""Boot the actual Skynet runtime, load game modules and exercise loopback TCP/timers."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
GAME = ROOT / 'Server/GameServer'
FRAMEWORK = GAME / 'framework'

def lua_string(value):
    return '"' + str(value).replace('\\', '\\\\').replace('"', '\\"') + '"'

def main():
    with tempfile.TemporaryDirectory(prefix='372dragon-native-') as tmp:
        config = Path(tmp) / 'config.lua'
        values = {
            'skip_license_check': 'true', 'enablecipher': 'true', 'enablessl': 'true', 'thread': 2, 'harbor': 0, 'bootstrap': 'snlua bootstrap', 'start': 'smoke',
            'lualoader': str(FRAMEWORK / 'lualib/loader.lua'),
            'luaservice': f'{ROOT}/Tests/server/native/?.lua;{FRAMEWORK}/service/?.lua',
            'lua_path': f'{FRAMEWORK}/lualib/?.lua;{FRAMEWORK}/lualib/?/init.lua;{GAME}/lualib/?.lua;{GAME}/services/?.lua',
            'lua_cpath': f'{GAME}/luaclib/?.so;{FRAMEWORK}/luaclib/?.so',
            'cpath': str(FRAMEWORK / 'cservice/?.so'),
        }
        config.write_text('\n'.join(f'{k} = {v if isinstance(v, int) else lua_string(v)}' for k,v in values.items())+'\n')
        result = subprocess.run([str(FRAMEWORK / 'skynet'), str(config)], cwd=GAME,
                                capture_output=True, text=True, errors="replace", timeout=45)
        output = result.stdout + result.stderr
        print(output, end='')
        if result.returncode or 'NATIVE_SMOKE_OK' not in output or 'NATIVE_SMOKE_FAILED' in output:
            raise SystemExit(f'Native smoke failed (exit {result.returncode})')
        print('PASS: runtime boot, native modules, GBK, navmesh, TCP ping/pong, monotonic profiler and timer')

if __name__ == '__main__':
    main()
