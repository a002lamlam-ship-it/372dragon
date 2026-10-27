#!/usr/bin/env bash
# Build the bundled runtime/modules, then run the real-runtime smoke test.
set -euo pipefail
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
game_root="$project_root/Server/GameServer"
case "$(uname -s)" in
  Darwin)
    if [ "$(uname -m)" != arm64 ]; then
      echo 'Run this script in a native arm64 terminal, outside Rosetta.' >&2
      exit 1
    fi
    xcrun --find clang >/dev/null
    command -v brew >/dev/null || { echo 'Install native Homebrew and openssl@3 first.' >&2; exit 1; }
    openssl_root="$(brew --prefix openssl@3)"
    test -f "$openssl_root/include/openssl/ssl.h"
    platform=macosx
    compiler=clang
    cxx_compiler=clang++
    ;;
  Linux)
    platform=linux_nojemalloc
    compiler="${CC:-cc}"
    cxx_compiler="${CXX:-c++}"
    openssl_root="${OPENSSL_PREFIX:-/usr}"
    ;;
  *) echo 'Supported build hosts: macOS ARM64 and Linux.' >&2; exit 1 ;;
esac
command -v python3 >/dev/null
jobs="${NATIVE_JOBS:-2}"
# Force recompilation: do not reuse objects from another OS, CPU or profiler mode.
make -C "$game_root/framework" -B "$platform" -j"$jobs" \
    CC="$compiler" CXX="$cxx_compiler" \
    TLS_INC="$openssl_root/include" TLS_LIB="$openssl_root/lib"
make -C "$game_root" -B -j"$jobs" CC="$compiler" CXX="$cxx_compiler" PROFILE_FLAGS=
if [ "$platform" = macosx ]; then
    lipo -verify_arch arm64 "$game_root/framework/skynet"
    for module in "$game_root"/luaclib/*.so "$game_root/framework"/luaclib/*.so; do
        lipo -verify_arch arm64 "$module"
    done
fi
python3 "$project_root/Tests/server/run_native_smoke.py"

(cd "$project_root" && "$game_root/framework/3rd/lua/lua" Tests/server/test_license_startup.lua)
python3 "$project_root/Tests/server/test_unity_gateway.py"
