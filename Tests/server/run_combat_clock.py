"""Run lifecycle and original-math checks in real Skynet with an injected monotonic test clock."""
from pathlib import Path
import importlib.util
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[2];GAME=ROOT/'Server/GameServer';FW=GAME/'framework'
spec=importlib.util.spec_from_file_location('native_smoke',ROOT/'Tests/server/run_native_smoke.py');smoke=importlib.util.module_from_spec(spec);spec.loader.exec_module(smoke)
values={'thread':2,'harbor':0,'bootstrap':'snlua bootstrap','start':'combat_clock','unity_world_root':str(ROOT/'Build/unity-world'),'lualoader':str(FW/'lualib/loader.lua'),'luaservice':f'{ROOT}/Tests/server/native/?.lua;{FW}/service/?.lua','lua_path':f'{FW}/lualib/?.lua;{FW}/lualib/?/init.lua;{GAME}/lualib/?.lua;{GAME}/services/?.lua','lua_cpath':f'{GAME}/luaclib/?.so;{FW}/luaclib/?.so','cpath':str(FW/'cservice/?.so')}
with tempfile.TemporaryDirectory() as directory:
 config=Path(directory)/'config';config.write_text('\n'.join(f'{k} = {v if isinstance(v,int) else smoke.lua_string(v)}' for k,v in values.items()))
 r=subprocess.run([str(FW/'skynet'),str(config)],cwd=GAME,capture_output=True,text=True,timeout=30)
 output=r.stdout+r.stderr;print(output)
 assert r.returncode==0 and 'COMBAT_CLOCK_OK' in output and 'COMBAT_CLOCK_FAILED' not in output,'Combat lifecycle checks failed'
