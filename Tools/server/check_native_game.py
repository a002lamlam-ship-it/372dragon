#!/usr/bin/env python3
"""Report missing local full-game inputs. A pass is not a gameplay acceptance test."""
from pathlib import Path
import argparse

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server-root', type=Path, default=ROOT / 'Server')
    parser.add_argument('--skip-license-check', action='store_true',
                        help='Match explicit skip_license_check=true development configuration')
    args = parser.parse_args()
    server = args.server_root.resolve()
    missing = []
    for relative in ['configs', 'Game_2/Scene']:
        path = server / relative
        if not path.is_dir() or not any(p.is_file() for p in path.rglob('*')):
            missing.append(f'{relative}: external data missing')
    for template in sorted(server.glob('confs/publish_yu/*.template')):
        if '.example.' in template.name:
            continue
        if not template.with_suffix('').is_file():
            missing.append(f'{template.with_suffix("").relative_to(server)}: private configuration missing')
    game = server / 'GameServer'
    if not args.skip_license_check and not any((game / p).is_file() for p in ['luaclib/llicense.so', 'framework/luaclib/llicense.so',
                                              'lualib/llicense.lua', 'services/llicense.lua']):
        missing.append('llicense: required by services/license_check.lua; source/module absent')
    if not (game / 'framework/skynet').is_file():
        missing.append('framework/skynet: build required')
    if missing:
        print('\n'.join('MISSING: ' + item for item in missing))
        raise SystemExit(1)
    print('Local inputs present. Still verify module architecture, MongoDB 4.4.31/MQTT, credentials, service readiness and gameplay.')

if __name__ == '__main__':
    main()
