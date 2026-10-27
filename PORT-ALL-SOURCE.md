# Toàn bộ code/script của bản port Unity/native

92 file trích nguyên byte từ NativeServerChanges.zip. Không gồm dữ liệu Build/unity-world hoặc mesh/texture/animation nhị phân.

Áp dụng lên repository gốc tại commit `436a12317f0408f303692078790f48537a33fd20`. Nhánh này đã chứa code; file bên dưới là bản trình bày để chép tay.

Unity: copy thư mục `Tools/unity/Package/Assets/DragonPort` vào Assets của project. Server: cần repository gốc và dữ liệu export để chạy. Unity Editor và macOS ARM64 chưa được kiểm thực tế.

Mục lục:

- `.github/workflows/server-native.yml`
- `Docs/guide/llicense-audit.md`
- `Docs/guide/server-macos-arm64.md`
- `Docs/guide/server-setup.md`
- `Docs/guide/unity-gateway.md`
- `Docs/guide/world-unity-port.md`
- `SOURCE-DELTA.json`
- `Server/GameServer/Makefile`
- `Server/GameServer/framework/.gitignore`
- `Server/GameServer/framework/3rd/lua/Makefile`
- `Server/GameServer/framework/Makefile`
- `Server/GameServer/framework/RESTORED-SOURCES.json`
- `Server/GameServer/framework/platform.mk`
- `Server/GameServer/framework/skynet-src/skynet_daemon.c`
- `Server/GameServer/framework/skynet-src/skynet_daemon.h`
- `Server/GameServer/framework/skynet-src/skynet_env.c`
- `Server/GameServer/framework/skynet-src/skynet_env.h`
- `Server/GameServer/framework/skynet-src/skynet_error.c`
- `Server/GameServer/framework/skynet-src/skynet_handle.c`
- `Server/GameServer/framework/skynet-src/skynet_handle.h`
- `Server/GameServer/framework/skynet-src/skynet_harbor.c`
- `Server/GameServer/framework/skynet-src/skynet_harbor.h`
- `Server/GameServer/framework/skynet-src/skynet_imp.h`
- `Server/GameServer/framework/skynet-src/skynet_log.c`
- `Server/GameServer/framework/skynet-src/skynet_log.h`
- `Server/GameServer/framework/skynet-src/skynet_main.c`
- `Server/GameServer/framework/skynet-src/skynet_malloc.h`
- `Server/GameServer/framework/skynet-src/skynet_module.c`
- `Server/GameServer/framework/skynet-src/skynet_module.h`
- `Server/GameServer/framework/skynet-src/skynet_monitor.c`
- `Server/GameServer/framework/skynet-src/skynet_monitor.h`
- `Server/GameServer/framework/skynet-src/skynet_mq.c`
- `Server/GameServer/framework/skynet-src/skynet_mq.h`
- `Server/GameServer/framework/skynet-src/skynet_server.c`
- `Server/GameServer/framework/skynet-src/skynet_server.h`
- `Server/GameServer/framework/skynet-src/skynet_socket.c`
- `Server/GameServer/framework/skynet-src/skynet_socket.h`
- `Server/GameServer/framework/skynet-src/skynet_start.c`
- `Server/GameServer/framework/skynet-src/skynet_timer.c`
- `Server/GameServer/framework/skynet-src/skynet_timer.h`
- `Server/GameServer/lualib-src/lunitynav.cc`
- `Server/GameServer/lualib-src/profile/profile.c`
- `Server/GameServer/lualib/unity_combat.lua`
- `Server/GameServer/lualib/unity_legacy_combat.lua`
- `Server/GameServer/lualib/unity_world.lua`
- `Server/GameServer/services/license_check.lua`
- `Server/GameServer/services/unity_gateway.lua`
- `Tests/server/native/combat_clock.lua`
- `Tests/server/native/smoke.lua`
- `Tests/server/run_combat_clock.py`
- `Tests/server/run_native_smoke.py`
- `Tests/server/test_license_startup.lua`
- `Tests/server/test_original_art.py`
- `Tests/server/test_unity_combat.py`
- `Tests/server/test_unity_gateway.py`
- `Tests/server/test_unity_nav.py`
- `Tests/server/test_unity_world.py`
- `Tests/server/test_world_batch.py`
- `Tools/server/build_native.sh`
- `Tools/server/check_native_game.py`
- `Tools/server/run_unity_gateway.py`
- `Tools/unity/NativeServerConnection.cs`
- `Tools/unity/Package/ART-COMBAT.md`
- `Tools/unity/Package/Assets/DragonPort/Editor/DragonArtImport.cs`
- `Tools/unity/Package/Assets/DragonPort/Editor/DragonWorldBrowser.cs`
- `Tools/unity/Package/Assets/DragonPort/Editor/DragonWorldImport.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonArtData.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonCombatClient.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonOriginalAnimation.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonPrefabLibrary.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonSpawn.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonWorldData.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonWorldLoader.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/DragonWorldSession.cs`
- `Tools/unity/Package/Assets/DragonPort/Runtime/NativeServerConnection.cs`
- `Tools/unity/Package/MAPS.md`
- `Tools/unity/Package/README.md`
- `Tools/unity/art/asset_source.py`
- `Tools/unity/art/export_art.py`
- `Tools/unity/art/export_combat_data.py`
- `Tools/unity/art/native_navigation.py`
- `Tools/unity/art/ogre_binary.py`
- `Tools/unity/art/package_art.py`
- `Tools/unity/art/render_original_smoke.py`
- `Tools/unity/cached_remote_zip.py`
- `Tools/unity/export_world.py`
- `Tools/unity/fetch_world_data.py`
- `Tools/unity/package_server.py`
- `Tools/unity/package_world.py`
- `Tools/unity/port_all_worlds.py`
- `Tools/unity/publish_release.py`
- `Tools/unity/remote_zip.py`

## .github/workflows/server-native.yml

SHA-256: `130d7e7c6672e195ed2c903bce5177fd7917abf3759896efc05ec7ce2b3400ea`

````yaml
name: Native server runtime
on:
  workflow_dispatch:
  push:
    paths: ['Server/GameServer/**', 'Tests/server/**', 'Tools/server/**', 'Tools/unity/**', '.github/workflows/server-native.yml']
  pull_request:
    paths: ['Server/GameServer/**', 'Tests/server/**', 'Tools/server/**', 'Tools/unity/**', '.github/workflows/server-native.yml']
permissions:
  contents: read
jobs:
  runtime:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-24.04, macos-15]
    runs-on: ${{ matrix.os }}
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - if: runner.os == 'macOS'
        run: |
          test "$(uname -m)" = arm64
          brew install openssl@3
      - if: runner.os == 'Linux'
        run: sudo apt-get update && sudo apt-get install -y build-essential libssl-dev zlib1g-dev python3
      - run: bash Tools/server/build_native.sh

````

## Docs/guide/llicense-audit.md

SHA-256: `6b9d94bf1ce9799a98a440fc9c66e6cd093bbb98dd0dbfc2f858d9eb61ef0b7b`

````markdown
# Kiểm tra phụ thuộc llicense

## Kết quả source Git

- `Server/GameServer/main.lua:17-18` gọi wrapper trước khi khởi tạo Manager/cụm.
- `services/license_check.lua:6` nạp `llicense`; dòng 13 gọi duy nhất `mod.check()` không truyền tham số.
- Caller chỉ đọc `info.result`; không dùng giá trị trả về cho gameplay, database, packet hoặc scene.
- Không nạp được module: gọi `skynet.abort()` (code -3). `check()` ném lỗi: gọi abort (code -5).
- `info.result == 0`: cho qua. Giá trị khác 0: wrapper hiện chỉ ghi cảnh báo code -7 rồi trả về, không tự abort ở nhánh này.
- Không thấy triển khai llicense hay caller khác trong source đã rà, hoặc file mang tên llicense trong lịch sử Git hiện có. Lịch sử wrapper bắt đầu từ commit xuất source `6975b511`.
- Không có implementation nên không biết side effect của module khi nạp/chạy check. Không suy luận chỉ từ tên rằng nó chắc chắn chỉ kiểm license.

## Phần chưa xác minh

Gói Google Drive được README/manifest khai báo có scene/config server. Yêu cầu đọc trang file và endpoint tải lại bị proxy trả `Tunnel connection failed: 403 Forbidden`. Chưa đọc được central directory, DATA-FILES.json hoặc bất kỳ member nào trong ZIP; không kết luận llicense có hay không có trong gói đó. Domain đã có trong draft cấu hình không chứng minh chính sách đang chạy đã áp dụng.

## Kết luận

Không cần module này để build framework hoặc chạy bài smoke runtime đã thêm. Luồng game mặc định vẫn có phụ thuộc khởi động bắt buộc. Có thể thay đổi kiến trúc để tách phụ thuộc này, nhưng không có thư viện thay trực tiếp được xác minh, và chưa đủ source để tái tạo đúng kiểm tra hoặc side effect gốc. Sau yêu cầu dùng server riêng, wrapper có thêm cấu hình `skip_license_check = true` để bỏ qua việc nạp module; không cài module giả. Mặc định chưa bật cấu hình vẫn giữ đường kiểm tra cũ. Gateway Unity phát triển tự bật cấu hình này. Khả năng port framework sang macOS có cơ sở; full-game readiness trên ARM64 chưa được chứng minh.

## Bổ sung sau khi truy cập Drive được

Đã đọc central directory thật: 126.214 entries (126.212 dữ liệu + index/notice), không có tên file chứa `llicense`. Đã đọc DATA-FILES.json và tải chọn lọc dữ liệu hai map với CRC/member SHA-256. Chưa kiểm hash toàn ZIP hoặc phân tích mọi member để tìm module bị đổi tên.

````

## Docs/guide/server-macos-arm64.md

SHA-256: `65e4a2e9fac573c363582f7d64a824421431976745e7db7e64d57c63b1fd7fdf`

````markdown
# Server native trên macOS Apple Silicon

Đã chuẩn bị nhánh build macOS ARM64; **chưa nghiệm thu trên Mac hoặc gameplay đầy đủ**.
Môi trường thực hiện thay đổi là Linux x64. Không dùng Docker, VM hay Rosetta.

## Source tìm thấy và tái sử dụng

- `Server/GameServer/framework`: Skynet đã có target `macosx`, socket `kqueue`,
  Lua 5.4.2 và native module. Giữ nguyên Lua tùy biến và các file hiện có.
- Framework công bố bị thiếu 27 file lõi C/header. Không có bản sao trong các
  thư mục được rà dưới `/workspace`, kể cả `Src`, `Tools`, `Docs`, `Registry`.
  Đã bổ sung **chỉ file thiếu** từ cloudwu/skynet v1.4.0, commit
  `4faa6499e819e4b5463d0b1efda7cf9d9f6dabcc`.
  Danh sách/SHA-256 ở `Server/GameServer/framework/RESTORED-SOURCES.json`.
  MIT license gốc ở `framework/LICENSE`.
- Căn cứ chọn baseline: `skynet.h`, `socket_server.h`, `atomic.h`,
  `lua-skynet.c` trùng v1.4.0. `socket_server.c` chỉ khác nhánh đóng kết nối;
  `service_snlua.c` thêm trường profiler. Đây là bằng chứng tương thích cho
  việc khôi phục, không chứng minh mọi hành vi gameplay giống bản server gốc.
- `lualib-src`: có source các module trong target mặc định: netpack, gbk, map,
  ldump, lnavmesh, laiscript, lprofile, lfs, rax.
- `3rd/behaviortree_cpp` có source nhưng `lbt` không thuộc target mặc định;
  chưa build/kiểm thử module tùy chọn đó.
- `Src/` chủ yếu là client/engine Windows, không cung cấp lõi Skynet bị thiếu.
- `services/license_check.lua` yêu cầu `llicense`; không tìm thấy source hay
  module đó trong checkout/lịch sử Git hiện có. Cần lấy đúng source từ tác giả
  để build ARM64; giữ nguyên đường kiểm tra hiện tại.

## Thay đổi nền tảng

- Module game dùng cờ bundle/dynamic lookup trên Darwin, giữ đuôi `.so` đúng
  đường nạp Lua; tất cả binary phải build riêng cho ARM64.
- Đường OpenSSL có thể truyền từ Homebrew; liên kết rõ cả SSL và Crypto.
- macOS dùng allocator hệ thống theo target có sẵn, không cần archive jemalloc
  Linux. Không khẳng định allocator này tương đương về hiệu năng/bộ nhớ.
- Profiler trên macOS dùng `CLOCK_MONOTONIC`, không dùng lệnh x86 `rdtsc`;
  bỏ việc cắt phần giây xuống 16 bit để tránh quay vòng đồng hồ.
- Lua CLI trên macOS không bắt buộc readline. Không đổi gameplay Lua/giao thức.

## Build và smoke test trên Mac

Cài Xcode Command Line Tools (`xcode-select --install`), Homebrew ARM64 và:

```bash
brew install openssl@3 python
cd /duong/dan/372dragon
bash Tools/server/build_native.sh
```

Script từ chối terminal chạy qua Rosetta, dùng clang/clang++, build lại các
output để không dùng nhầm object Linux/x64, kiểm `lipo` và chạy smoke test.
Mặc định dùng 2 build jobs; chỉnh bằng `NATIVE_JOBS` nếu cần.
Không tự tải data, cài database hay khởi động cụm game.

Smoke test khởi động Skynet thật, nạp module framework/game, kiểm GBK, tạo
navmesh point, TCP loopback ping/pong, profiler và timer. Có timeout 45 giây;
phải có `NATIVE_SMOKE_OK` và exit 0. Không chỉ kiểm cổng hoặc PID.

Workflow `.github/workflows/server-native.yml` chạy cùng bài kiểm trên Linux
và runner `macos-15`, có assertion `uname -m = arm64`. Workflow mới chỉ được
thêm vào source; chưa push hoặc chạy GitHub Actions trong phiên này.

## Điều kiện để chạy game đầy đủ

```bash
python3 Tools/server/check_native_game.py
```

Hiện thiếu:

1. Mặc định cần `llicense` tương thích ARM64. Với server phát triển riêng, có thể đặt `skip_license_check = true` trong cấu hình Skynet để bỏ phụ thuộc này. Gateway Unity tự bật cấu hình đó.
2. Data ngoài Git: `Server/configs`, `Server/Game_2/Scene`. Xem `DATA_DOWNLOAD.md`.
3. Cấu hình riêng từ template, database user và credential cục bộ.
4. MongoDB 4.4.31 và Mosquitto. Cần xác minh riêng khả năng cài MongoDB 4.4.31
   trên macOS/Apple Silicon thực tế. Không tự nâng major hoặc dùng binary x64
   rồi gọi là native ARM64. Đây có thể là blocker độc lập.

Sau khi ghép source/data vào root server riêng, dùng
`python3 Publication/init_config.py --server-root /duong/dan/Server`
để sinh cấu hình; không ghi đè file riêng đã có. Không đưa credential vào Git/chat.
Các script `start_all.sh`, `start_zone.sh`, `r.sh` lịch sử còn đường dẫn Linux
cố định và lệnh build Linux: **không chạy nguyên trạng trên Mac**.

Kiểm tra trước khi chạy chỉ xác nhận một số input cục bộ, không kiểm đầy đủ
kết nối/auth database, MQTT, license hoặc hành vi game. Sau khi giải quyết các
điều kiện trên vẫn phải nghiệm thu đăng nhập, tạo nhân vật, nạp scene, di chuyển,
chiến đấu/giao dịch và lưu sau thoát/đăng nhập lại.

## Kết quả đã đo trong cloud Linux

- Build framework với allocator hệ thống và toàn bộ module target mặc định: đạt.
- Build C++17 không dùng `-fpermissive`: đạt (vẫn có warning từ source kế thừa).
- Smoke runtime/module/GBK/navmesh/TCP/timer và profiler monotonic: đạt.
  Log: `Build/cloud/native-build-smoke.log`.
- Kiểm hash 27 file khôi phục: đạt.
- macOS ARM64, MongoDB/MQTT và gameplay đầy đủ: **chưa nghiệm thu**.

## Client Unity mới

Xem [gateway JSON/TCP cho Unity](unity-gateway.md). Gateway phát triển không cần data game, MongoDB, MQTT hoặc llicense; hiện mới cung cấp hello/ping, chưa nối gameplay.

````

## Docs/guide/server-setup.md

SHA-256: `7b70d257a50e44b2c1f15844ebf48e7ff3fc6f484019e4340e17fb09cd28e7f8`

````markdown
# Chuẩn bị server Linux/WSL2

[← Tài liệu](README.md) · [Trạng thái và nghiệm thu →](status.md)

Server ở `Server/`, dùng Skynet/Lua và module C/C++. Nó không được build bởi CMake
client. Chưa có bộ provision/cài dịch vụ hoàn chỉnh được nghiệm thu trên máy mới.

Hướng port riêng: [macOS Apple Silicon native](server-macos-arm64.md) (chưa nghiệm thu trên Mac).

## 1. Bố cục và phụ thuộc

| Đường dẫn | Nội dung |
|---|---|
| `Server/GameServer/framework` | Skynet, Lua, service và module native |
| `Server/GameServer` | Logic server, native module riêng và Makefile |
| `Server/Game_2/Script` | Gameplay/scene script |
| `Server/Game_2/Scene` | Scene lấy thêm từ data |
| `Server/configs` | Bảng tĩnh lấy thêm từ data |
| `Server/confs/publish_yu` | Cấu hình mẫu |

Chuẩn bị compiler C/C++, make, Python 3, MongoDB **4.4.31** và Mosquitto.
Giữ MongoDB trong giai đoạn tương thích này; chưa xác nhận đổi major. OpenSSL,
jemalloc và native module phải phù hợp source/Makefile hiện có.

## 2. Dùng root Linux riêng

Ghép source/data đúng bố cục, đặt bản cài ở root của bạn, ví dụ `~/372dragon/Server`.
Ví dụ dưới giả định root đó đã tồn tại. Không chạy script quản lý lên server khác
đang phục vụ người dùng. Từ root source trong Linux:

```bash
python3 Publication/init_config.py --server-root "$HOME/372dragon/Server"
```

Công cụ tạo **10 cấu hình** từ `.template`, sinh bí mật ngẫu nhiên và lưu tại
`.local/setup-secrets.json` của server root, quyền file `0600` trên Linux.
Nếu file đích đã tồn tại, thao tác bị từ chối. Công cụ chỉ thay placeholder đã biết;
rà lại các đường dẫn, IP và tài khoản còn lại theo bản cài.

Công cụ không cài dịch vụ, tạo user database/tài khoản game hay khởi động server.
Không đưa file bí mật, cấu hình đã sinh, database hoặc log phiên chơi vào Git.

## 3. Build native: những điểm phải giải quyết

| Vị trí | Cần đối chiếu |
|---|---|
| `GameServer/framework/Makefile` | Yêu cầu `3rd/jemalloc/lib/libjemalloc_pic.a`; bản xuất chưa có bộ source/dependency jemalloc hoàn chỉnh |
| `GameServer/framework/platform.mk` | Có target `linux`, `linux_nojemalloc`; thay allocator cần kiểm riêng |
| `GameServer/framework/Makefile` | `TLS_LIB=/usr/lib64/openssl` cần khớp distro/ABI thực tế |
| `GameServer/Makefile` | Các module `gbk`, `map`, `lnavmesh`, `laiscript`, `lprofile` và module khác |

Lệnh tham khảo chỉ áp dụng **sau khi** giải quyết đúng phụ thuộc/đường dẫn; chạy từ server root:

```bash
make -C GameServer/framework linux
make -C GameServer
```

Đây là lệnh từ Makefile, chưa phải xác nhận build sạch đạt. Không đổi sang
`linux_nojemalloc` để bỏ qua lỗi rồi kết luận tương đương. Dùng `ldd` trên
executable/module đã build để kiểm thư viện còn thiếu.

## 4. Dịch vụ và kết nối

| Thành phần | Cổng profile CY | Phạm vi |
|---|---:|---|
| Login | 15733 | Client truy cập được địa chỉ quảng bá |
| Game | 15734 | Client truy cập được địa chỉ quảng bá |
| MongoDB | 27018 | Loopback; không mở trực tiếp ra LAN |
| MQTT | 1884 | Theo cấu hình bản cài riêng |

Đây là cổng profile, không phải khẳng định dịch vụ đã lắng nghe. Tạo user MongoDB
phù hợp bí mật mới, thư mục lưu trữ/log và quyền truy cập trước khi khởi động.
Phân biệt IP nội bộ WSL/loopback với IP client nhìn thấy. Chỉ cấu hình khu 1 cho lần dựng đầu.

Các script `Tools/server/provision_test_wsl.py` và `cys_server.sh` còn giả định root
của máy phát triển. Đọc, điều chỉnh rõ đích trước khi dùng. Không nhập nguyên
database hay bản export WSL của người khác để thay bước cài đặt.

## 5. Phiên chạy đầu tiên

1. Kiểm MongoDB, MQTT và process game của **bản cài mới**.
2. Kiểm cổng thực và địa chỉ client dùng.
3. Theo dõi log scene: trước đây nạp khoảng 75 giây, có cửa sổ chờ tới 900 giây.
4. Tạo tài khoản mới qua đường đăng ký server; kiểm allow-list profile client
   lịch sử (`test00`–`test15`) nếu tài khoản bị từ chối.
5. Đăng nhập, tạo nhân vật, vào Đại Lý, di chuyển, giao dịch một lần, thoát sạch
   và đăng nhập lại để kiểm lưu trạng thái.

Ghi rõ lỗi baseline và lỗi mới. Xem [trạng thái](status.md), [xử lý lỗi](troubleshooting.md)
và [ghi chú cài đặt](../../Publication/INSTALL-NOTES.md).

````

## Docs/guide/unity-gateway.md

SHA-256: `08df9ad8e6de7b00d4be801722fadbbe84352776dcaa87ddd4a043bc3c971183`

````markdown
> Cập nhật mesh/animation và combat: xem [ART-COMBAT.md](../../Tools/unity/Package/ART-COMBAT.md). Gateway hiện có adapter PvE cơ bản có thẩm quyền ở server; các API world.* bên dưới vẫn là snapshot nguồn. Chưa port toàn bộ skill/gameplay cũ, chưa kiểm Unity Editor/macOS.

# Gateway native cho client Unity mới

Đây là điểm kết nối phát triển chạy bằng Skynet thật, dùng JSON UTF-8 qua TCP.
Không cần giao thức TLBB cũ, MongoDB, MQTT, data scene hay `llicense` để thử hello/ping.
Logic gameplay cũ vẫn còn nguyên trong source, nhưng **chưa được nối vào gateway**.
Không có đăng nhập, tạo nhân vật, di chuyển, chiến đấu hoặc lưu dữ liệu trong API mới.

## Chạy server

Từ root repository sau khi cài toolchain/OpenSSL theo hướng dẫn macOS:

```bash
bash Tools/server/build_native.sh
python3 Tools/server/run_unity_gateway.py
```

Mặc định bind `127.0.0.1:15800`, chạy foreground, Ctrl+C để dừng. Khi sẵn sàng:
`UNITY_GATEWAY_READY 15800`. Không chạy các script start_all/start_zone cũ cho workflow này.
`--host` và `--port` cho phép đổi địa chỉ. Gateway hiện không có authentication/TLS;
phạm vi mặc định là client Unity chạy cùng máy phát triển.

Launcher tự đặt `skip_license_check = true` trong cấu hình tạm. Không tạo llicense giả.
Luồng game cũ cũng có thể dùng cấu hình đó, nhưng vẫn cần data/database và các bước
nghiệm thu riêng. Tắt kiểm llicense không tắt kiểm tài khoản hoặc quyền của gameplay.

## Unity

Copy `Tools/unity/NativeServerConnection.cs` vào `Assets/Scripts`, gắn component
`NativeServerConnection` lên GameObject rồi Play. Console phải hiện hai phản hồi
thành công cho `hello` và `ping`. Script đóng kết nối sau hai yêu cầu thử nghiệm;
đây chưa phải client phiên chơi lâu dài. Host mặc định đúng khi Unity Editor và
server chạy trên cùng Mac. Chưa compile/chạy mẫu trong Unity tại cloud Linux này.

## Giao thức v1

Mỗi thông điệp là một JSON object, kết thúc bằng byte LF (`\n`). Không thêm BOM.
TCP có thể chia hoặc gộp các thông điệp; không coi mỗi lần đọc socket là một packet.
Giới hạn dòng/buffer nhận là 64 KiB. `id` là chuỗi không rỗng, tối đa 64 byte.

Yêu cầu:

```json
{"v":1,"id":"1","method":"hello"}
{"v":1,"id":"2","method":"ping"}
```

Phản hồi ví dụ (thứ tự key có thể khác):

```json
{"v":1,"id":"1","ok":true,"result":{"protocol":"372dragon.unity","version":1,"capabilities":["hello","ping"],"gameplayReady":false}}
{"v":1,"id":"2","ok":true,"result":{"pong":true}}
```

Method khác trả `METHOD_NOT_IMPLEMENTED`; không trả đăng nhập/di chuyển thành công giả.
Lỗi khác: `INVALID_JSON`, `INVALID_REQUEST`, `INVALID_ID`, `UNSUPPORTED_VERSION`.
Phản hồi chỉ có `id` khi yêu cầu có ID hợp lệ. Dòng vượt giới hạn làm đóng kết nối.

## Kiểm thử đã thực hiện

- 5 trường hợp bật/tắt cấu hình bỏ llicense: đạt.
- Skynet thực khởi động và gọi wrapper trong chế độ không có llicense: đạt.
- 9 kiểm tra gateway: hello, ping, method chưa có, JSON lỗi, null, thiếu ID,
  version sai, frame quá lớn, kết nối lại: đạt trên Linux.
- Bao gồm yêu cầu bị chia thành nhiều lần gửi và nhiều yêu cầu gửi chung một lần.
- macOS ARM64 và Unity Editor: chưa chạy tại môi trường hiện tại.

Chạy lại:

```bash
python3 Tests/server/test_unity_gateway.py
```

Bước gameplay tiếp theo là thiết kế API đăng nhập/nhân vật/di chuyển và adapter tới
logic server cũ hoặc chọn mô hình gameplay mới. Không cần xóa logic cũ để mở cổng mới.

## World adapter

Đã thêm `world.list`, `world.enter` và `world.entities` để đọc bundle xuất bởi
`Tools/unity/export_world.py`. Launcher nhận `--world-root` (mặc định Build/unity-world).
`world.enter` trả metadata, không tạo phiên gameplay. Ví dụ:

```json
{"v":1,"id":"worlds","method":"world.list"}
{"v":1,"id":"map","method":"world.enter","params":{"sceneId":2}}
{"v":1,"id":"spawns","method":"world.entities","params":{"sceneId":2,"offset":0,"limit":50}}
```

Giới hạn page 1..100; dừng khi nextOffset == total, yêu cầu vượt cuối trả
PAGE_OUT_OF_RANGE. Chưa có bundle trả WORLD_DATA_UNAVAILABLE. World ID không có
trả WORLD_NOT_FOUND. Mọi phản hồi world ghi simulationReady=false. Unity loader và
client đồng bộ mẫu nằm trong Tools/unity/Package; xem hướng dẫn world-unity-port.md.

Bản nhiều map: world.list cũng nhận offset/limit như world.entities và trả total/nextOffset. Không giả định phản hồi đầu tiên chứa toàn bộ catalog. Gateway lazy-load, giữ tối đa bốn world.

````

## Docs/guide/world-unity-port.md

SHA-256: `492d7b464f419989eacd00cd50a84873fcb0720976de969729ddf00535e5ca1e`

````markdown
> Cập nhật mesh/animation và combat: xem [ART-COMBAT.md](../../Tools/unity/Package/ART-COMBAT.md). Gateway hiện có adapter PvE cơ bản có thẩm quyền ở server; các API world.* bên dưới vẫn là snapshot nguồn. Chưa port toàn bộ skill/gameplay cũ, chưa kiểm Unity Editor/macOS.

# Port map, NPC và quái sang Unity

Dữ liệu thật đã lấy chọn lọc từ ZIP được dự án chia sẻ trên Google Drive,
không phải map/NPC dựng mẫu. Đã đọc danh sách 126.214 ZIP entries và index 126.212
file dữ liệu; không có tên member chứa llicense. Xác minh CRC và SHA-256 từng
member lấy về, cùng hash notice; chưa tải/kiểm hash toàn bộ ZIP 12 GB.

Source chuyển đổi: `Tools/unity/export_world.py`. Unity import/runtime:
`Tools/unity/Package/Assets/DragonPort`. Hướng dẫn nhập vào project khác:
`Tools/unity/Package/README.md`.

## Bằng chứng hai map đầu tiên

- Đại Lý (2): terrain 320×320, 172 NPC tương tác + 8 entity không tương tác,
  5.662 static placements. Bỏ qua 37 section spawn thiếu/đã tắt trong dải đếm,
  tương ứng cách đọc source server; danh sách nằm trong JSON xuất.
- Vô Lượng Sơn (6): terrain 320×320, 22 NPC + 317 entity không tương tác,
  2.274 static placements. Không có section bị bỏ qua.
- Không có spawn nằm ngoài biên terrain trong hai bản xuất.
- Tọa độ được đối chiếu `Src/Engine/WXRender/RenderSystem.cpp:Axis_Trans`;
  terrain/height/grid định dạng theo TerrainData và TerrainDataSerializer.
- Giữ grid diagonal/hole flags. MeshCollider terrain là hiển thị/va chạm ground,
  không phải navmesh server và chưa có walk collision của cầu/nhà.
- Giữ template/model ID, tên, script/AI ID, stats và thời gian respawn bằng ms.
  Thời gian được đối chiếu `scenecore:monster_die` chia cho 10 trước skynet.timeout.
- Static resource references và transform đã xuất. Chưa chuyển OGRE mesh, rig,
  animation, terrain texture splat/lightmap, particle hay building collision.
- Runtime Unity có prefab mapping; không có prefab thì NPC/quái dùng capsule.
  Scenery chưa có binding được đếm và bỏ vẽ, dữ liệu vẫn giữ trong JSON.
- Native gateway mới có world.list/enter/entities theo trang, lấy dữ liệu nguồn;
  chưa chạy AI/aggro/combat/respawn/NPC dialogue. Không ghi nhận đây là full game.

## Tái tạo và kiểm tra

```bash
python3 Tools/unity/fetch_world_data.py
python3 Tools/unity/export_world.py --server-root Server --client-data Assets/CanonicalCY/Data --out Build/unity-world
python3 Tests/server/test_unity_world.py
python3 Tests/server/test_unity_gateway.py
python3 Tools/unity/package_world.py
```

Downloader từ chối ghi đè input cục bộ nếu hash khác gói nguồn; không chạy code từ ZIP.
Exporter không thay byte input GBK, đầu ra JSON UTF-8. Tài nguyên tải về ở các
thư mục ignored, output ở Build; không đưa toàn bộ data vào Git.

6 test cases mới kiểm format hỏng, nội suy hai loại diagonal, hole flags, path
traversal, bundle thật và gateway thực. Gateway test so toàn bộ 519 spawn IDs,
template và độ cao qua các trang, đồng thời kiểm world/pagination lỗi.

Unity Editor/macOS ARM64 chưa có trong cloud Linux. Bộ C# chưa compile/run trong
Unity tại đây; cần import trên project của người dùng để chốt compatibility và
kiểm hình. Đây là phần tiếp tục bắt buộc, không được ghi là đã nghiệm thu.

## Bản mở rộng: 289 map

- Xuất 289 map đang bật: 198 map thường (type 0), 90 template phó bản (type 1),
  1 template thành bang (type 4). Không tạo phiên instance hay thành bang đang chạy.
- Tổng 27.400 spawn: 3.502 NPC tương tác và 23.898 entity không tương tác;
  399.983 static scenery placements. Danh sách đầy đủ ở Tools/unity/Package/MAPS.md.
- 226 scene đang bật chưa xuất được: 220 slot thành bang và 6 scene thiếu hoặc
  không khớp tài nguyên (42,153,154,155,316,1327). Không dùng map khác thế vào.
- Giữ ngoài catalog 284 scene đang tắt; không sửa trạng thái source server.
- 5 entity thiếu template ở scene 9/13/15 bị bỏ qua tương tự server gốc;
  scene 575/1328 có một cảnh báo tọa độ ngoài biên mỗi map. Ghi trong bundle.
- Sửa parser để hiểu pos_x=;... là mục đã tắt theo inireader gốc.
- Scene 2220–2223 dùng alias lấy từ DBC client, chỉ khi hash navmesh server
  bằng navmesh phía client của resource đó. Không đoán chỉ từ clientres.
- Đã kiểm member CRC/SHA-256 của 6.666 file nguồn; tải chọn lọc bằng HTTP Range.
  Chưa kiểm hash toàn archive. Source audit nằm trong gói ZIP.
- Map Browser mới: Tools → Dragon Port → Browse Maps, tìm theo ID/tên.
- world.list có offset/limit (default 50, max 100), total/nextOffset. Gateway
  chỉ giữ tối đa bốn world trong cache và nạp theo yêu cầu.

Tái tạo bản mở rộng:

```bash
python3 Tools/unity/port_all_worlds.py
python3 Tests/server/test_unity_world.py
python3 Tests/server/test_world_batch.py
python3 Tools/unity/package_world.py
```

Nếu đã có input verified, dùng port_all_worlds.py --no-download. Báo cáo phân loại
đủ 799 scene ở Build/unity-world/port-report.json và PORT-REPORT.json trong ZIP.
7 test format/world gốc và 2 test batch đã đạt trên Linux. Bài batch kiểm mọi
bundle, đối chiếu đủ 799 trạng thái và đi qua gateway của cả 289 map với phản hồi
dưới 64 KiB. Unity Editor/macOS vẫn chưa được kiểm thử tại môi trường này.

````

## SOURCE-DELTA.json

SHA-256: `63037ea7ddbd738c79976bdc91c5613c2c279d457ed20f58ce5e968b900c0173`

````json
{
  "baseCommit": "436a12317f0408f303692078790f48537a33fd20",
  "repository": "a002lamlam-ship-it/372dragon",
  "instructions": "Apply onto the base checkout. Contains source changes and world/combat data, not compiled macOS binaries. See Tools/unity/Package/ART-COMBAT.md."
}
````

## Server/GameServer/Makefile

SHA-256: `5afa96360ccbb49009083dba0820cf8abb25b07aef6675684a0429dbfaa809a9`

````makefile
LUA_CLIB_PATH ?= luaclib
CSERVICE_PATH ?= cservice

SKYNET_INC = framework/skynet-src
LUA_INC = framework/3rd/lua
SHARED ?= -fPIC --shared
PROFILE_FLAGS ?= -DUSE_RDTSC
CFLAGS = -g -O0 -Wall
CXXFLAGS = -g -fpermissive -std=c++17
ifeq ($(shell uname -s),Darwin)
SHARED = -fPIC -bundle -Wl,-undefined,dynamic_lookup
CXXFLAGS = -g -std=c++17
PROFILE_FLAGS =
endif

BT_STATICLIB := 3rd/behaviortree_cpp/lib/libbehaviortree_cpp.a
BT_LIB ?= $(BT_STATICLIB)
BT_INC ?= 3rd/behaviortree_cpp/include
SOL2_INC  ?= lualib-src/sol/

NAV_MESH_SRC ?= lualib-src/navmesh/*.cpp
AI_SCRIPT_SRC ?= lualib-src/ai/*.cpp
PROFILE_SRC ?=lualib-src/profile/*.c
LFS_SRC ?=lualib-src/lfs/*.c
RAX_SRC ?=lualib-src/rax/*.c

LUA_CLIB = unitynav \
  netpack \
  gbk \
  map \
  ldump \
  lnavmesh \
  laiscript \
  lprofile \
  lfs \
  rax

CSERVICE = caoi

all : \
  $(foreach v, $(CSERVICE), $(CSERVICE_PATH)/$(v).so) \
  $(foreach v, $(LUA_CLIB), $(LUA_CLIB_PATH)/$(v).so) 

$(LUA_CLIB_PATH)/netpack.so : lualib-src/lua-netpack.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/gbk.so : lualib-src/gbk/lgbk.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/map.so : lualib-src/map/lmap.cc lualib-src/map/Map.cc lualib-src/map/PathFinder.cc | $(LUA_CLIB_PATH)
	$(CXX) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/ldump.so : lualib-src/ldump.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/lbt.so : lualib-src/lbt.cc $(BT_LIB) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) -I$(SOL2_INC) -I$(BT_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/lnavmesh.so : lualib-src/lnavmesh.cc $(NAV_MESH_SRC) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) -I$(SOL2_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/laiscript.so : lualib-src/laiscript.cc $(AI_SCRIPT_SRC) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) -I$(SOL2_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/lprofile.so : $(PROFILE_SRC) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $(PROFILE_FLAGS) $^ -o $@

$(LUA_CLIB_PATH)/lfs.so : $(LFS_SRC) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH)/rax.so : $(RAX_SRC) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) -I$(LUA_INC) -I$(SKYNET_INC) $(SHARED) $^ -o $@

$(LUA_CLIB_PATH) :
	mkdir -p $(LUA_CLIB_PATH)
$(CSERVICE_PATH) :
	mkdir -p $(CSERVICE_PATH)

define CSERVICE_TEMP
  $$(CSERVICE_PATH)/$(1).so : service-src/service_$(1).c | $$(CSERVICE_PATH)
	$$(CC) $$(CFLAGS) $$(SHARED) $$< -o $$@ -Iframework/skynet-src
endef

$(foreach v, $(CSERVICE), $(eval $(call CSERVICE_TEMP,$(v))))

clean :
	rm -f $(LUA_CLIB_PATH)/*.so



UNITY_NAV_SRC = lualib-src/lunitynav.cc ../../Src/Client/WXClient/World/CysNavMesh.cpp $(wildcard ../../Src/Engine/PathLib/*.cpp)
$(LUA_CLIB_PATH)/unitynav.so : $(UNITY_NAV_SRC) | $(LUA_CLIB_PATH)
	$(CXX) $(CXXFLAGS) $(SHARED) -I$(LUA_INC) -I../../Src/Engine/PathLib -I../../Src/Client/WXClient/World $^ -o $@

````

## Server/GameServer/framework/.gitignore

SHA-256: `baae23769dbcc145abbdfe7d3421ddf27c10feecf840b480dda5d054766979d9`

````text
*.o
*.a
/skynet
/skynet.pid
3rd/lua/lua
3rd/lua/luac
GameSvr*
/cservice
/luaclib
/log
*.so
*.dSYM
.DS_Store

````

## Server/GameServer/framework/3rd/lua/Makefile

SHA-256: `0914466e474ea7b9649229051b14cc35dfc63944f71573b9e2d3f11c66226b1b`

````makefile
# Makefile for building Lua
# See ../doc/readme.html for installation and customization instructions.

# == CHANGE THE SETTINGS BELOW TO SUIT YOUR ENVIRONMENT =======================

# Your platform. See PLATS for possible values.
PLAT= guess

CC= gcc -std=gnu99
CFLAGS= -O2 -Wall -Wextra $(SYSCFLAGS) $(MYCFLAGS)
LDFLAGS= $(SYSLDFLAGS) $(MYLDFLAGS)
LIBS= -lm $(SYSLIBS) $(MYLIBS)

AR= ar rcu
RANLIB= ranlib
RM= rm -f
UNAME= uname

SYSCFLAGS=
SYSLDFLAGS=
SYSLIBS=

MYCFLAGS=-I../../skynet-src -g
MYLDFLAGS=
MYLIBS=
MYOBJS=

# Special flags for compiler modules; -Os reduces code size.
CMCFLAGS= -Os

# == END OF USER SETTINGS -- NO NEED TO CHANGE ANYTHING BELOW THIS LINE =======

PLATS= guess aix bsd c89 freebsd generic linux linux-readline macosx mingw posix solaris

LUA_A=	liblua.a
CORE_O=	lapi.o lcode.o lctype.o ldebug.o ldo.o ldump.o lfunc.o lgc.o llex.o lmem.o lobject.o lopcodes.o lparser.o lstate.o lstring.o ltable.o ltm.o lundump.o lvm.o lzio.o
LIB_O=	lauxlib.o lbaselib.o lcorolib.o ldblib.o liolib.o lmathlib.o loadlib.o loslib.o lstrlib.o ltablib.o lutf8lib.o linit.o
BASE_O= $(CORE_O) $(LIB_O) $(MYOBJS)

LUA_T=	lua
LUA_O=	lua.o

LUAC_T=	luac
LUAC_O=	luac.o

ALL_O= $(BASE_O) $(LUA_O) $(LUAC_O)
ALL_T= $(LUA_A) $(LUA_T) $(LUAC_T)
ALL_A= $(LUA_A)

# Targets start here.
default: $(PLAT)

all:	$(ALL_T)

o:	$(ALL_O)

a:	$(ALL_A)

$(LUA_A): $(BASE_O)
	$(AR) $@ $(BASE_O)
	$(RANLIB) $@

$(LUA_T): $(LUA_O) $(LUA_A)
	$(CC) -o $@ $(LDFLAGS) $(LUA_O) $(LUA_A) $(LIBS)

$(LUAC_T): $(LUAC_O) $(LUA_A)
	$(CC) -o $@ $(LDFLAGS) $(LUAC_O) $(LUA_A) $(LIBS)

test:
	./lua -v

clean:
	$(RM) $(ALL_T) $(ALL_O)

depend:
	@$(CC) $(CFLAGS) -MM l*.c

echo:
	@echo "PLAT= $(PLAT)"
	@echo "CC= $(CC)"
	@echo "CFLAGS= $(CFLAGS)"
	@echo "LDFLAGS= $(SYSLDFLAGS)"
	@echo "LIBS= $(LIBS)"
	@echo "AR= $(AR)"
	@echo "RANLIB= $(RANLIB)"
	@echo "RM= $(RM)"
	@echo "UNAME= $(UNAME)"

# Convenience targets for popular platforms.
ALL= all

help:
	@echo "Do 'make PLATFORM' where PLATFORM is one of these:"
	@echo "   $(PLATS)"
	@echo "See doc/readme.html for complete instructions."

guess:
	@echo Guessing `$(UNAME)`
	@$(MAKE) `$(UNAME)`

AIX aix:
	$(MAKE) $(ALL) CC="xlc" CFLAGS="-O2 -DLUA_USE_POSIX -DLUA_USE_DLOPEN" SYSLIBS="-ldl" SYSLDFLAGS="-brtl -bexpall"

bsd:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_POSIX -DLUA_USE_DLOPEN" SYSLIBS="-Wl,-E"

c89:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_C89" CC="gcc -std=c89"
	@echo ''
	@echo '*** C89 does not guarantee 64-bit integers for Lua.'
	@echo ''

FreeBSD NetBSD OpenBSD freebsd:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_LINUX -DLUA_USE_READLINE -I/usr/include/edit" SYSLIBS="-Wl,-E -ledit" CC="cc"

generic: $(ALL)

Linux linux:	linux-noreadline

linux-noreadline:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_LINUX" SYSLIBS="-Wl,-E -ldl"

linux-readline:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_LINUX -DLUA_USE_READLINE" SYSLIBS="-Wl,-E -ldl -lreadline"

Darwin macos macosx:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_MACOSX" SYSLIBS=""

mingw:
	$(MAKE) "LUA_A=lua54.dll" "LUA_T=lua.exe" \
	"AR=$(CC) -shared -o" "RANLIB=strip --strip-unneeded" \
	"SYSCFLAGS=-DLUA_BUILD_AS_DLL" "SYSLIBS=" "SYSLDFLAGS=-s" lua.exe
	$(MAKE) "LUAC_T=luac.exe" luac.exe

posix:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_POSIX"

SunOS solaris:
	$(MAKE) $(ALL) SYSCFLAGS="-DLUA_USE_POSIX -DLUA_USE_DLOPEN -D_REENTRANT" SYSLIBS="-ldl"

# Targets that do not create files (not all makes understand .PHONY).
.PHONY: all $(PLATS) help test clean default o a depend echo

# Compiler modules may use special flags.
llex.o:
	$(CC) $(CFLAGS) $(CMCFLAGS) -c llex.c

lparser.o:
	$(CC) $(CFLAGS) $(CMCFLAGS) -c lparser.c

lcode.o:
	$(CC) $(CFLAGS) $(CMCFLAGS) -c lcode.c

# DO NOT DELETE

lapi.o: lapi.c lprefix.h lua.h luaconf.h lapi.h llimits.h lstate.h \
 lobject.h ltm.h lzio.h lmem.h ldebug.h ldo.h lfunc.h lgc.h lstring.h \
 ltable.h lundump.h lvm.h
lauxlib.o: lauxlib.c lprefix.h lua.h luaconf.h lauxlib.h
lbaselib.o: lbaselib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
lcode.o: lcode.c lprefix.h lua.h luaconf.h lcode.h llex.h lobject.h \
 llimits.h lzio.h lmem.h lopcodes.h lparser.h ldebug.h lstate.h ltm.h \
 ldo.h lgc.h lstring.h ltable.h lvm.h
lcorolib.o: lcorolib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
lctype.o: lctype.c lprefix.h lctype.h lua.h luaconf.h llimits.h
ldblib.o: ldblib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
ldebug.o: ldebug.c lprefix.h lua.h luaconf.h lapi.h llimits.h lstate.h \
 lobject.h ltm.h lzio.h lmem.h lcode.h llex.h lopcodes.h lparser.h \
 ldebug.h ldo.h lfunc.h lstring.h lgc.h ltable.h lvm.h
ldo.o: ldo.c lprefix.h lua.h luaconf.h lapi.h llimits.h lstate.h \
 lobject.h ltm.h lzio.h lmem.h ldebug.h ldo.h lfunc.h lgc.h lopcodes.h \
 lparser.h lstring.h ltable.h lundump.h lvm.h
ldump.o: ldump.c lprefix.h lua.h luaconf.h lobject.h llimits.h lstate.h \
 ltm.h lzio.h lmem.h lundump.h
lfunc.o: lfunc.c lprefix.h lua.h luaconf.h ldebug.h lstate.h lobject.h \
 llimits.h ltm.h lzio.h lmem.h ldo.h lfunc.h lgc.h
lgc.o: lgc.c lprefix.h lua.h luaconf.h ldebug.h lstate.h lobject.h \
 llimits.h ltm.h lzio.h lmem.h ldo.h lfunc.h lgc.h lstring.h ltable.h
linit.o: linit.c lprefix.h lua.h luaconf.h lualib.h lauxlib.h
liolib.o: liolib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
llex.o: llex.c lprefix.h lua.h luaconf.h lctype.h llimits.h ldebug.h \
 lstate.h lobject.h ltm.h lzio.h lmem.h ldo.h lgc.h llex.h lparser.h \
 lstring.h ltable.h
lmathlib.o: lmathlib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
lmem.o: lmem.c lprefix.h lua.h luaconf.h ldebug.h lstate.h lobject.h \
 llimits.h ltm.h lzio.h lmem.h ldo.h lgc.h
loadlib.o: loadlib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
lobject.o: lobject.c lprefix.h lua.h luaconf.h lctype.h llimits.h \
 ldebug.h lstate.h lobject.h ltm.h lzio.h lmem.h ldo.h lstring.h lgc.h \
 lvm.h
lopcodes.o: lopcodes.c lprefix.h lopcodes.h llimits.h lua.h luaconf.h
loslib.o: loslib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
lparser.o: lparser.c lprefix.h lua.h luaconf.h lcode.h llex.h lobject.h \
 llimits.h lzio.h lmem.h lopcodes.h lparser.h ldebug.h lstate.h ltm.h \
 ldo.h lfunc.h lstring.h lgc.h ltable.h
lstate.o: lstate.c lprefix.h lua.h luaconf.h lapi.h llimits.h lstate.h \
 lobject.h ltm.h lzio.h lmem.h ldebug.h ldo.h lfunc.h lgc.h llex.h \
 lstring.h ltable.h
lstring.o: lstring.c lprefix.h lua.h luaconf.h ldebug.h lstate.h \
 lobject.h llimits.h ltm.h lzio.h lmem.h ldo.h lstring.h lgc.h
lstrlib.o: lstrlib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
ltable.o: ltable.c lprefix.h lua.h luaconf.h ldebug.h lstate.h lobject.h \
 llimits.h ltm.h lzio.h lmem.h ldo.h lgc.h lstring.h ltable.h lvm.h
ltablib.o: ltablib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
ltm.o: ltm.c lprefix.h lua.h luaconf.h ldebug.h lstate.h lobject.h \
 llimits.h ltm.h lzio.h lmem.h ldo.h lgc.h lstring.h ltable.h lvm.h
lua.o: lua.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
luac.o: luac.c lprefix.h lua.h luaconf.h lauxlib.h ldebug.h lstate.h \
 lobject.h llimits.h ltm.h lzio.h lmem.h lopcodes.h lopnames.h lundump.h
lundump.o: lundump.c lprefix.h lua.h luaconf.h ldebug.h lstate.h \
 lobject.h llimits.h ltm.h lzio.h lmem.h ldo.h lfunc.h lstring.h lgc.h \
 lundump.h
lutf8lib.o: lutf8lib.c lprefix.h lua.h luaconf.h lauxlib.h lualib.h
lvm.o: lvm.c lprefix.h lua.h luaconf.h ldebug.h lstate.h lobject.h \
 llimits.h ltm.h lzio.h lmem.h ldo.h lfunc.h lgc.h lopcodes.h lstring.h \
 ltable.h lvm.h ljumptab.h
lzio.o: lzio.c lprefix.h lua.h luaconf.h llimits.h lmem.h lstate.h \
 lobject.h ltm.h lzio.h

# (end of Makefile)

````

## Server/GameServer/framework/Makefile

SHA-256: `026b129fcdb143d84442446b86c32d43d47c3967cc94081a29918bd3890f0577`

````makefile
include platform.mk

LUA_CLIB_PATH ?= luaclib
CSERVICE_PATH ?= cservice

SKYNET_BUILD_PATH ?= .

CFLAGS = -g -O2 -Wall -I$(LUA_INC) $(MYCFLAGS)
# CFLAGS += -DUSE_PTHREAD_LOCK

# lua

LUA_STATICLIB := 3rd/lua/liblua.a
LUA_LIB ?= $(LUA_STATICLIB)
LUA_INC ?= 3rd/lua

$(LUA_STATICLIB) :
	cd 3rd/lua && $(MAKE) CC='$(CC) -std=gnu99' $(if $(filter linux_nojemalloc,$(PLAT)),linux,$(PLAT))

# https : turn on TLS_MODULE to add https support
TLS_MODULE=ltls
TLS_LIB ?= /usr/lib64/openssl
TLS_INC ?= /usr/include/openssl

## cipher: use openssl cipher 
CIPHER_MODULE = lcipher

# jemalloc

JEMALLOC_STATICLIB := 3rd/jemalloc/lib/libjemalloc_pic.a
JEMALLOC_INC := 3rd/jemalloc/include/jemalloc

MALLOC_STATICLIB := $(JEMALLOC_STATICLIB)
# skynet

CSERVICE = snlua logger gate harbor
LUA_CLIB = skynet \
  client \
  bson md5 pb sproto lpeg cjson luarsa textfilter zlib skiplist $(TLS_MODULE) $(CIPHER_MODULE)

LUA_CLIB_SKYNET = \
  lua-skynet.c lua-seri.c \
  lua-socket.c \
  lua-mongo.c \
  lua-netpack.c \
  lua-memory.c \
  lua-multicast.c \
  lua-cluster.c \
  lua-crypt.c lsha1.c lcrc.c lsha1.c lsha2.c\
  lua-sharedata.c \
  lua-stm.c \
  lua-debugchannel.c \
  lua-datasheet.c \
  lua-sharetable.c \
  lua-vscdebugaux.c \
  \

LUA_CLIB_PROTOBUF = \
  pb.c \

SKYNET_SRC = skynet_main.c skynet_handle.c skynet_module.c skynet_mq.c \
  skynet_server.c skynet_start.c skynet_timer.c skynet_error.c \
  skynet_harbor.c skynet_env.c skynet_monitor.c skynet_socket.c socket_server.c \
  malloc_hook.c skynet_daemon.c skynet_log.c

all : \
  $(SKYNET_BUILD_PATH)/skynet \
  $(foreach v, $(CSERVICE), $(CSERVICE_PATH)/$(v).so) \
  $(foreach v, $(LUA_CLIB), $(LUA_CLIB_PATH)/$(v).so) 

$(SKYNET_BUILD_PATH)/skynet : $(foreach v, $(SKYNET_SRC), skynet-src/$(v)) $(LUA_LIB) $(MALLOC_STATICLIB)
	$(CC) $(CFLAGS) -o $@ $^ -Iskynet-src -I$(JEMALLOC_INC) $(LDFLAGS) $(EXPORT) $(SKYNET_LIBS) $(SKYNET_DEFINES)

$(LUA_CLIB_PATH) :
	mkdir -p $(LUA_CLIB_PATH)

$(CSERVICE_PATH) :
	mkdir -p $(CSERVICE_PATH)

define CSERVICE_TEMP
  $$(CSERVICE_PATH)/$(1).so : service-src/service_$(1).c | $$(CSERVICE_PATH)
	$$(CC) $$(CFLAGS) $$(SHARED) $$< -o $$@ -Iskynet-src
endef

$(foreach v, $(CSERVICE), $(eval $(call CSERVICE_TEMP,$(v))))

$(LUA_CLIB_PATH)/skynet.so : $(addprefix lualib-src/,$(LUA_CLIB_SKYNET)) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) $^ -o $@ -Iskynet-src -Iservice-src -Ilualib-src

$(LUA_CLIB_PATH)/bson.so : lualib-src/lua-bson.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -Iskynet-src $^ -o $@ -Iskynet-src

$(LUA_CLIB_PATH)/md5.so : 3rd/lua-md5/md5.c 3rd/lua-md5/md5lib.c 3rd/lua-md5/compat-5.2.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -I3rd/lua-md5 $^ -o $@ 

$(LUA_CLIB_PATH)/client.so : lualib-src/lua-clientsocket.c lualib-src/lua-crypt.c lualib-src/lcrc.c lualib-src/lsha1.c lualib-src/lsha2.c| $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) $^ -o $@ -lpthread

$(LUA_CLIB_PATH)/sproto.so : lualib-src/sproto/sproto.c lualib-src/sproto/lsproto.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -Ilualib-src/sproto $^ -o $@ 

$(LUA_CLIB_PATH)/ltls.so : lualib-src/ltls.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -Iskynet-src -L$(TLS_LIB) -I$(TLS_INC) $^ -o $@ -lssl -lcrypto

$(LUA_CLIB_PATH)/lcipher.so : lualib-src/lcipher.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -Iskynet-src -L$(TLS_LIB) -I$(TLS_INC) $^ -o $@ -lssl -lcrypto

$(LUA_CLIB_PATH)/lpeg.so : 3rd/lpeg/lpcap.c 3rd/lpeg/lpcode.c 3rd/lpeg/lpprint.c 3rd/lpeg/lptree.c 3rd/lpeg/lpvm.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -I3rd/lpeg $^ -o $@ 

$(LUA_CLIB_PATH)/cjson.so : 3rd/lua-cjson/lua_cjson.c 3rd/lua-cjson/fpconv.c 3rd/lua-cjson/strbuf.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -I3rd/lua-cjson $^ -o $@ 

$(LUA_CLIB_PATH)/pb.so : $(addprefix 3rd/lua-pbc/,$(LUA_CLIB_PROTOBUF)) | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -I3rd/lua-pbc $^ -o $@ 

$(LUA_CLIB_PATH)/luarsa.so : 3rd/lua-rsa/luarsa.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -I3rd/lua-rsa -L$(TLS_LIB) -I$(TLS_INC) $^ -o $@ -lssl -lcrypto

$(LUA_CLIB_PATH)/zlib.so : 3rd/lua-zlib/lua_zlib.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -I3rd/lua-zlib $^ -o $@ -lz

$(LUA_CLIB_PATH)/skiplist.so : 3rd/lua-zset/skiplist.c 3rd/lua-zset/lua-skiplist.c | $(LUA_CLIB_PATH)
	$(CC) $(CFLAGS) $(SHARED) -I3rd/lua-zset $^ -o $@ -lz

$(LUA_CLIB_PATH)/textfilter.so : 3rd/lua-textfilter/lua-textfilter.cc | $(LUA_CLIB_PATH)
	$(CXX) $(CFLAGS) $(SHARED) $^ -o $@	

clean :
	rm -f $(SKYNET_BUILD_PATH)/skynet $(CSERVICE_PATH)/*.so $(LUA_CLIB_PATH)/*.so

cleanall: clean
ifneq (,$(wildcard 3rd/jemalloc/Makefile))
	cd 3rd/jemalloc && $(MAKE) clean && rm Makefile
endif
	cd 3rd/lua && $(MAKE) clean
	rm -f $(LUA_STATICLIB)


````

## Server/GameServer/framework/RESTORED-SOURCES.json

SHA-256: `68b368330610d3ded6edf6453a1694597839fe28c34ef87ffb459dcce23be6c5`

````json
{
  "upstream": "https://github.com/cloudwu/skynet",
  "commit": "4faa6499e819e4b5463d0b1efda7cf9d9f6dabcc",
  "tag": "v1.4.0",
  "note": "Missing files only; existing customized files retained. Compatibility requires runtime validation.",
  "files": [
    {
      "path": "skynet-src/skynet_daemon.c",
      "sha256": "2be34f5b7809f6c4319469216c61c3d9d943c5aa09c9e4ed7e57ea7aad971382"
    },
    {
      "path": "skynet-src/skynet_daemon.h",
      "sha256": "8dc30f6180b47f467d2c571e3d55d97f756bf75c11d8e57d297d34499b1a12a9"
    },
    {
      "path": "skynet-src/skynet_env.c",
      "sha256": "83c1a68d0711dda4cbb05373a21f5c0b56d31f725b62048e8a6713d953812852"
    },
    {
      "path": "skynet-src/skynet_env.h",
      "sha256": "71382d1d902dcf59965de2439b13758a78bcdf713c7c7d9edad530586888906d"
    },
    {
      "path": "skynet-src/skynet_error.c",
      "sha256": "234bab2ab7010d991d0099e499700a0dec25ef77079260d129730e94ac7eca91"
    },
    {
      "path": "skynet-src/skynet_handle.c",
      "sha256": "670b6e0dee728670aa52f502fff44f0784911400384b4deeedc99567efe50027"
    },
    {
      "path": "skynet-src/skynet_handle.h",
      "sha256": "9381325d3f93758ac36dd36e8f177cd09e4e1dbfabebbb2cd25f6e10aa2aa2ab"
    },
    {
      "path": "skynet-src/skynet_harbor.c",
      "sha256": "0752f0967ec6e13b71ae12b8452aa35a8f41c1ad746ac658ef05db82570eb3ed"
    },
    {
      "path": "skynet-src/skynet_harbor.h",
      "sha256": "c387da20d598b59de3ff809fe43eefd93e620e552c1d97de170a7cefaae029b5"
    },
    {
      "path": "skynet-src/skynet_imp.h",
      "sha256": "433f1fe3d93771652ff9a8543eb9af46d69032db6c12cb5950314f8523224ee4"
    },
    {
      "path": "skynet-src/skynet_log.c",
      "sha256": "472b8fab48bfafc8dd871fb490005d232fec3cbed09e39ac3c95ac0d0b22b7ed"
    },
    {
      "path": "skynet-src/skynet_log.h",
      "sha256": "71d1553f5893b13a17f2581cf0e3c2104df90ec8c6f16d81a195c8b6236f774a"
    },
    {
      "path": "skynet-src/skynet_main.c",
      "sha256": "f76c917f3dfa283e3b8aefc6a49e145c921fb3b866bae81097dadc14ab2d9703"
    },
    {
      "path": "skynet-src/skynet_malloc.h",
      "sha256": "1e41039e9321beed4e288538a34dcfb082d320a1d65e5369cecf635be2955da9"
    },
    {
      "path": "skynet-src/skynet_module.c",
      "sha256": "5317a8ddcb882d88022432367b158fc23400002cacc10fc711617d2e2f3dfe63"
    },
    {
      "path": "skynet-src/skynet_module.h",
      "sha256": "95473fc43187f45bb3cb5300d861608336f60783562b37318c2683853a491925"
    },
    {
      "path": "skynet-src/skynet_monitor.c",
      "sha256": "879fedeb811acd9bc9ca98fc011ed5a809b8c4131a3647c2d826ab3b3a0c0a12"
    },
    {
      "path": "skynet-src/skynet_monitor.h",
      "sha256": "2297e8ef506bf331f0bb098c5854021a6e5532e1279c2d205db62cc178be9c89"
    },
    {
      "path": "skynet-src/skynet_mq.c",
      "sha256": "11eb445405e59b419d20a17c35a15308ff3b84672410bfcdb00b7d53acc8008a"
    },
    {
      "path": "skynet-src/skynet_mq.h",
      "sha256": "422aaad1e86a90037c9da472a5bd38f9f379868439c42a2e5870bb5c35c9ad33"
    },
    {
      "path": "skynet-src/skynet_server.c",
      "sha256": "8d9202d8d0341312fa347282988defa604a81221dab63ba6497ed3d13c5484ef"
    },
    {
      "path": "skynet-src/skynet_server.h",
      "sha256": "fb7ea33829ff4f47379fc5e706deaa949699c5e2d544d77c9086a047158aa51e"
    },
    {
      "path": "skynet-src/skynet_socket.c",
      "sha256": "3ee755e6be3dff9c60e079406ade5e09bcc762ec4d6a46342a0ba573988b613e"
    },
    {
      "path": "skynet-src/skynet_socket.h",
      "sha256": "2dc8583a604cb95e7d189e64522c5027e11d637f77779aed766caada94eae097"
    },
    {
      "path": "skynet-src/skynet_start.c",
      "sha256": "5551b4343e3953346e677c74fd30ed24d06a6790b9c05b69af5878addaf50ca2"
    },
    {
      "path": "skynet-src/skynet_timer.c",
      "sha256": "9307cfcdcbb5606706deb1a7101d49f2f95631050b1a79f1f49ed72098596af6"
    },
    {
      "path": "skynet-src/skynet_timer.h",
      "sha256": "6ed1e209893bf3d479c864ad980564980d48b67a6ab69af6cd623300ba41c708"
    }
  ]
}

````

## Server/GameServer/framework/platform.mk

SHA-256: `b83178f068d0ca62c331f0ca79e398a4e51587c83a63c55e17821eec595fe598`

````text
PLAT ?= none
PLATS = linux freebsd macosx

CC ?= gcc

.PHONY : none $(PLATS) clean all cleanall

#ifneq ($(PLAT), none)

.PHONY : default

default :
	$(MAKE) $(PLAT)

#endif

none :
	@echo "Please do 'make PLATFORM' where PLATFORM is one of these:"
	@echo "   $(PLATS)"

SKYNET_LIBS := -lpthread -lm
SHARED := -fPIC --shared
EXPORT := -Wl,-E

linux : PLAT = linux
macosx : PLAT = macosx
freebsd : PLAT = freebsd

macosx : SHARED := -fPIC -dynamiclib -Wl,-undefined,dynamic_lookup
macosx : EXPORT :=
linux linux_nojemalloc : SKYNET_LIBS += -ldl
linux freebsd linux_nojemalloc : SKYNET_LIBS += -lrt

# Turn off jemalloc and malloc hook on macosx

macosx : MALLOC_STATICLIB :=
macosx : SKYNET_DEFINES :=-DNOUSE_JEMALLOC

linux_nojemalloc : PLAT = linux
linux_nojemalloc : MALLOC_STATICLIB :=
linux_nojemalloc : SKYNET_DEFINES :=-DNOUSE_JEMALLOC

linux macosx freebsd linux_nojemalloc :
	$(MAKE) all PLAT=$@ SKYNET_LIBS="$(SKYNET_LIBS)" SHARED="$(SHARED)" EXPORT="$(EXPORT)" MALLOC_STATICLIB="$(MALLOC_STATICLIB)" SKYNET_DEFINES="$(SKYNET_DEFINES)"

````

## Server/GameServer/framework/skynet-src/skynet_daemon.c

SHA-256: `2be34f5b7809f6c4319469216c61c3d9d943c5aa09c9e4ed7e57ea7aad971382`

````c
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/file.h>
#include <signal.h>
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>

#include "skynet_daemon.h"

static int
check_pid(const char *pidfile) {
	int pid = 0;
	FILE *f = fopen(pidfile,"r");
	if (f == NULL)
		return 0;
	int n = fscanf(f,"%d", &pid);
	fclose(f);

	if (n !=1 || pid == 0 || pid == getpid()) {
		return 0;
	}

	if (kill(pid, 0) && errno == ESRCH)
		return 0;

	return pid;
}

static int
write_pid(const char *pidfile) {
	FILE *f;
	int pid = 0;
	int fd = open(pidfile, O_RDWR|O_CREAT, 0644);
	if (fd == -1) {
		fprintf(stderr, "Can't create pidfile [%s].\n", pidfile);
		return 0;
	}
	f = fdopen(fd, "w+");
	if (f == NULL) {
		fprintf(stderr, "Can't open pidfile [%s].\n", pidfile);
		return 0;
	}

	if (flock(fd, LOCK_EX|LOCK_NB) == -1) {
		int n = fscanf(f, "%d", &pid);
		fclose(f);
		if (n != 1) {
			fprintf(stderr, "Can't lock and read pidfile.\n");
		} else {
			fprintf(stderr, "Can't lock pidfile, lock is held by pid %d.\n", pid);
		}
		return 0;
	}

	pid = getpid();
	if (!fprintf(f,"%d\n", pid)) {
		fprintf(stderr, "Can't write pid.\n");
		close(fd);
		return 0;
	}
	fflush(f);

	return pid;
}

static int
redirect_fds() {
	int nfd = open("/dev/null", O_RDWR);
	if (nfd == -1) {
		perror("Unable to open /dev/null: ");
		return -1;
	}
	if (dup2(nfd, 0) < 0) {
		perror("Unable to dup2 stdin(0): ");
		return -1;
	}
	if (dup2(nfd, 1) < 0) {
		perror("Unable to dup2 stdout(1): ");
		return -1;
	}
	if (dup2(nfd, 2) < 0) {
		perror("Unable to dup2 stderr(2): ");
		return -1;
	}

	close(nfd);

	return 0;
}

int
daemon_init(const char *pidfile) {
	int pid = check_pid(pidfile);

	if (pid) {
		fprintf(stderr, "Skynet is already running, pid = %d.\n", pid);
		return 1;
	}

#ifdef __APPLE__
	fprintf(stderr, "'daemon' is deprecated: first deprecated in OS X 10.5 , use launchd instead.\n");
#else
	if (daemon(1,1)) {
		fprintf(stderr, "Can't daemonize.\n");
		return 1;
	}
#endif

	pid = write_pid(pidfile);
	if (pid == 0) {
		return 1;
	}

	if (redirect_fds()) {
		return 1;
	}

	return 0;
}

int
daemon_exit(const char *pidfile) {
	return unlink(pidfile);
}

````

## Server/GameServer/framework/skynet-src/skynet_daemon.h

SHA-256: `8dc30f6180b47f467d2c571e3d55d97f756bf75c11d8e57d297d34499b1a12a9`

````c
#ifndef skynet_daemon_h
#define skynet_daemon_h

int daemon_init(const char *pidfile);
int daemon_exit(const char *pidfile);

#endif

````

## Server/GameServer/framework/skynet-src/skynet_env.c

SHA-256: `83c1a68d0711dda4cbb05373a21f5c0b56d31f725b62048e8a6713d953812852`

````c
#include "skynet.h"
#include "skynet_env.h"
#include "spinlock.h"

#include <lua.h>
#include <lauxlib.h>

#include <stdlib.h>
#include <assert.h>

struct skynet_env {
	struct spinlock lock;
	lua_State *L;
};

static struct skynet_env *E = NULL;

const char * 
skynet_getenv(const char *key) {
	SPIN_LOCK(E)

	lua_State *L = E->L;
	
	lua_getglobal(L, key);
	const char * result = lua_tostring(L, -1);
	lua_pop(L, 1);

	SPIN_UNLOCK(E)

	return result;
}

void 
skynet_setenv(const char *key, const char *value) {
	SPIN_LOCK(E)
	
	lua_State *L = E->L;
	lua_getglobal(L, key);
	assert(lua_isnil(L, -1));
	lua_pop(L,1);
	lua_pushstring(L,value);
	lua_setglobal(L,key);

	SPIN_UNLOCK(E)
}

void
skynet_env_init() {
	E = skynet_malloc(sizeof(*E));
	SPIN_INIT(E)
	E->L = luaL_newstate();
}

````

## Server/GameServer/framework/skynet-src/skynet_env.h

SHA-256: `71382d1d902dcf59965de2439b13758a78bcdf713c7c7d9edad530586888906d`

````c
#ifndef SKYNET_ENV_H
#define SKYNET_ENV_H

const char * skynet_getenv(const char *key);
void skynet_setenv(const char *key, const char *value);

void skynet_env_init();

#endif

````

## Server/GameServer/framework/skynet-src/skynet_error.c

SHA-256: `234bab2ab7010d991d0099e499700a0dec25ef77079260d129730e94ac7eca91`

````c
#include "skynet.h"
#include "skynet_handle.h"
#include "skynet_mq.h"
#include "skynet_server.h"

#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LOG_MESSAGE_SIZE 256

void 
skynet_error(struct skynet_context * context, const char *msg, ...) {
	static uint32_t logger = 0;
	if (logger == 0) {
		logger = skynet_handle_findname("logger");
	}
	if (logger == 0) {
		return;
	}

	char tmp[LOG_MESSAGE_SIZE];
	char *data = NULL;

	va_list ap;

	va_start(ap,msg);
	int len = vsnprintf(tmp, LOG_MESSAGE_SIZE, msg, ap);
	va_end(ap);
	if (len >=0 && len < LOG_MESSAGE_SIZE) {
		data = skynet_strdup(tmp);
	} else {
		int max_size = LOG_MESSAGE_SIZE;
		for (;;) {
			max_size *= 2;
			data = skynet_malloc(max_size);
			va_start(ap,msg);
			len = vsnprintf(data, max_size, msg, ap);
			va_end(ap);
			if (len < max_size) {
				break;
			}
			skynet_free(data);
		}
	}
	if (len < 0) {
		skynet_free(data);
		perror("vsnprintf error :");
		return;
	}


	struct skynet_message smsg;
	if (context == NULL) {
		smsg.source = 0;
	} else {
		smsg.source = skynet_context_handle(context);
	}
	smsg.session = 0;
	smsg.data = data;
	smsg.sz = len | ((size_t)PTYPE_TEXT << MESSAGE_TYPE_SHIFT);
	skynet_context_push(logger, &smsg);
}


````

## Server/GameServer/framework/skynet-src/skynet_handle.c

SHA-256: `670b6e0dee728670aa52f502fff44f0784911400384b4deeedc99567efe50027`

````c
#include "skynet.h"

#include "skynet_handle.h"
#include "skynet_server.h"
#include "rwlock.h"

#include <stdlib.h>
#include <assert.h>
#include <string.h>

#define DEFAULT_SLOT_SIZE 4
#define MAX_SLOT_SIZE 0x40000000

struct handle_name {
	char * name;
	uint32_t handle;
};

struct handle_storage {
	struct rwlock lock;

	uint32_t harbor;
	uint32_t handle_index;
	int slot_size;
	struct skynet_context ** slot;
	
	int name_cap;
	int name_count;
	struct handle_name *name;
};

static struct handle_storage *H = NULL;

uint32_t
skynet_handle_register(struct skynet_context *ctx) {
	struct handle_storage *s = H;

	rwlock_wlock(&s->lock);
	
	for (;;) {
		int i;
		uint32_t handle = s->handle_index;
		for (i=0;i<s->slot_size;i++,handle++) {
			if (handle > HANDLE_MASK) {
				// 0 is reserved
				handle = 1;
			}
			int hash = handle & (s->slot_size-1);
			if (s->slot[hash] == NULL) {
				s->slot[hash] = ctx;
				s->handle_index = handle + 1;

				rwlock_wunlock(&s->lock);

				handle |= s->harbor;
				return handle;
			}
		}
		assert((s->slot_size*2 - 1) <= HANDLE_MASK);
		struct skynet_context ** new_slot = skynet_malloc(s->slot_size * 2 * sizeof(struct skynet_context *));
		memset(new_slot, 0, s->slot_size * 2 * sizeof(struct skynet_context *));
		for (i=0;i<s->slot_size;i++) {
			int hash = skynet_context_handle(s->slot[i]) & (s->slot_size * 2 - 1);
			assert(new_slot[hash] == NULL);
			new_slot[hash] = s->slot[i];
		}
		skynet_free(s->slot);
		s->slot = new_slot;
		s->slot_size *= 2;
	}
}

int
skynet_handle_retire(uint32_t handle) {
	int ret = 0;
	struct handle_storage *s = H;

	rwlock_wlock(&s->lock);

	uint32_t hash = handle & (s->slot_size-1);
	struct skynet_context * ctx = s->slot[hash];

	if (ctx != NULL && skynet_context_handle(ctx) == handle) {
		s->slot[hash] = NULL;
		ret = 1;
		int i;
		int j=0, n=s->name_count;
		for (i=0; i<n; ++i) {
			if (s->name[i].handle == handle) {
				skynet_free(s->name[i].name);
				continue;
			} else if (i!=j) {
				s->name[j] = s->name[i];
			}
			++j;
		}
		s->name_count = j;
	} else {
		ctx = NULL;
	}

	rwlock_wunlock(&s->lock);

	if (ctx) {
		// release ctx may call skynet_handle_* , so wunlock first.
		skynet_context_release(ctx);
	}

	return ret;
}

void 
skynet_handle_retireall() {
	struct handle_storage *s = H;
	for (;;) {
		int n=0;
		int i;
		for (i=0;i<s->slot_size;i++) {
			rwlock_rlock(&s->lock);
			struct skynet_context * ctx = s->slot[i];
			uint32_t handle = 0;
			if (ctx)
				handle = skynet_context_handle(ctx);
			rwlock_runlock(&s->lock);
			if (handle != 0) {
				if (skynet_handle_retire(handle)) {
					++n;
				}
			}
		}
		if (n==0)
			return;
	}
}

struct skynet_context * 
skynet_handle_grab(uint32_t handle) {
	struct handle_storage *s = H;
	struct skynet_context * result = NULL;

	rwlock_rlock(&s->lock);

	uint32_t hash = handle & (s->slot_size-1);
	struct skynet_context * ctx = s->slot[hash];
	if (ctx && skynet_context_handle(ctx) == handle) {
		result = ctx;
		skynet_context_grab(result);
	}

	rwlock_runlock(&s->lock);

	return result;
}

uint32_t 
skynet_handle_findname(const char * name) {
	struct handle_storage *s = H;

	rwlock_rlock(&s->lock);

	uint32_t handle = 0;

	int begin = 0;
	int end = s->name_count - 1;
	while (begin<=end) {
		int mid = (begin+end)/2;
		struct handle_name *n = &s->name[mid];
		int c = strcmp(n->name, name);
		if (c==0) {
			handle = n->handle;
			break;
		}
		if (c<0) {
			begin = mid + 1;
		} else {
			end = mid - 1;
		}
	}

	rwlock_runlock(&s->lock);

	return handle;
}

static void
_insert_name_before(struct handle_storage *s, char *name, uint32_t handle, int before) {
	if (s->name_count >= s->name_cap) {
		s->name_cap *= 2;
		assert(s->name_cap <= MAX_SLOT_SIZE);
		struct handle_name * n = skynet_malloc(s->name_cap * sizeof(struct handle_name));
		int i;
		for (i=0;i<before;i++) {
			n[i] = s->name[i];
		}
		for (i=before;i<s->name_count;i++) {
			n[i+1] = s->name[i];
		}
		skynet_free(s->name);
		s->name = n;
	} else {
		int i;
		for (i=s->name_count;i>before;i--) {
			s->name[i] = s->name[i-1];
		}
	}
	s->name[before].name = name;
	s->name[before].handle = handle;
	s->name_count ++;
}

static const char *
_insert_name(struct handle_storage *s, const char * name, uint32_t handle) {
	int begin = 0;
	int end = s->name_count - 1;
	while (begin<=end) {
		int mid = (begin+end)/2;
		struct handle_name *n = &s->name[mid];
		int c = strcmp(n->name, name);
		if (c==0) {
			return NULL;
		}
		if (c<0) {
			begin = mid + 1;
		} else {
			end = mid - 1;
		}
	}
	char * result = skynet_strdup(name);

	_insert_name_before(s, result, handle, begin);

	return result;
}

const char * 
skynet_handle_namehandle(uint32_t handle, const char *name) {
	rwlock_wlock(&H->lock);

	const char * ret = _insert_name(H, name, handle);

	rwlock_wunlock(&H->lock);

	return ret;
}

void 
skynet_handle_init(int harbor) {
	assert(H==NULL);
	struct handle_storage * s = skynet_malloc(sizeof(*H));
	s->slot_size = DEFAULT_SLOT_SIZE;
	s->slot = skynet_malloc(s->slot_size * sizeof(struct skynet_context *));
	memset(s->slot, 0, s->slot_size * sizeof(struct skynet_context *));

	rwlock_init(&s->lock);
	// reserve 0 for system
	s->harbor = (uint32_t) (harbor & 0xff) << HANDLE_REMOTE_SHIFT;
	s->handle_index = 1;
	s->name_cap = 2;
	s->name_count = 0;
	s->name = skynet_malloc(s->name_cap * sizeof(struct handle_name));

	H = s;

	// Don't need to free H
}


````

## Server/GameServer/framework/skynet-src/skynet_handle.h

SHA-256: `9381325d3f93758ac36dd36e8f177cd09e4e1dbfabebbb2cd25f6e10aa2aa2ab`

````c
#ifndef SKYNET_CONTEXT_HANDLE_H
#define SKYNET_CONTEXT_HANDLE_H

#include <stdint.h>

// reserve high 8 bits for remote id
#define HANDLE_MASK 0xffffff
#define HANDLE_REMOTE_SHIFT 24

struct skynet_context;

uint32_t skynet_handle_register(struct skynet_context *);
int skynet_handle_retire(uint32_t handle);
struct skynet_context * skynet_handle_grab(uint32_t handle);
void skynet_handle_retireall();

uint32_t skynet_handle_findname(const char * name);
const char * skynet_handle_namehandle(uint32_t handle, const char *name);

void skynet_handle_init(int harbor);

#endif

````

## Server/GameServer/framework/skynet-src/skynet_harbor.c

SHA-256: `0752f0967ec6e13b71ae12b8452aa35a8f41c1ad746ac658ef05db82570eb3ed`

````c
#include "skynet.h"
#include "skynet_harbor.h"
#include "skynet_server.h"
#include "skynet_mq.h"
#include "skynet_handle.h"

#include <string.h>
#include <stdio.h>
#include <assert.h>

static struct skynet_context * REMOTE = 0;
static unsigned int HARBOR = ~0;

static inline int
invalid_type(int type) {
	return type != PTYPE_SYSTEM && type != PTYPE_HARBOR;
}

void 
skynet_harbor_send(struct remote_message *rmsg, uint32_t source, int session) {
	assert(invalid_type(rmsg->type) && REMOTE);
	skynet_context_send(REMOTE, rmsg, sizeof(*rmsg) , source, PTYPE_SYSTEM , session);
}

int 
skynet_harbor_message_isremote(uint32_t handle) {
	assert(HARBOR != ~0);
	int h = (handle & ~HANDLE_MASK);
	return h != HARBOR && h !=0;
}

void
skynet_harbor_init(int harbor) {
	HARBOR = (unsigned int)harbor << HANDLE_REMOTE_SHIFT;
}

void
skynet_harbor_start(void *ctx) {
	// the HARBOR must be reserved to ensure the pointer is valid.
	// It will be released at last by calling skynet_harbor_exit
	skynet_context_reserve(ctx);
	REMOTE = ctx;
}

void
skynet_harbor_exit() {
	struct skynet_context * ctx = REMOTE;
	REMOTE= NULL;
	if (ctx) {
		skynet_context_release(ctx);
	}
}

````

## Server/GameServer/framework/skynet-src/skynet_harbor.h

SHA-256: `c387da20d598b59de3ff809fe43eefd93e620e552c1d97de170a7cefaae029b5`

````c
#ifndef SKYNET_HARBOR_H
#define SKYNET_HARBOR_H

#include <stdint.h>
#include <stdlib.h>

#define GLOBALNAME_LENGTH 16
#define REMOTE_MAX 256

struct remote_name {
	char name[GLOBALNAME_LENGTH];
	uint32_t handle;
};

struct remote_message {
	struct remote_name destination;
	const void * message;
	size_t sz;
	int type;
};

void skynet_harbor_send(struct remote_message *rmsg, uint32_t source, int session);
int skynet_harbor_message_isremote(uint32_t handle);
void skynet_harbor_init(int harbor);
void skynet_harbor_start(void * ctx);
void skynet_harbor_exit();

#endif

````

## Server/GameServer/framework/skynet-src/skynet_imp.h

SHA-256: `433f1fe3d93771652ff9a8543eb9af46d69032db6c12cb5950314f8523224ee4`

````c
#ifndef SKYNET_IMP_H
#define SKYNET_IMP_H

struct skynet_config {
	int thread;
	int harbor;
	int profile;
	const char * daemon;
	const char * module_path;
	const char * bootstrap;
	const char * logger;
	const char * logservice;
};

#define THREAD_WORKER 0
#define THREAD_MAIN 1
#define THREAD_SOCKET 2
#define THREAD_TIMER 3
#define THREAD_MONITOR 4

void skynet_start(struct skynet_config * config);

#endif

````

## Server/GameServer/framework/skynet-src/skynet_log.c

SHA-256: `472b8fab48bfafc8dd871fb490005d232fec3cbed09e39ac3c95ac0d0b22b7ed`

````c
#include "skynet_log.h"
#include "skynet_timer.h"
#include "skynet.h"
#include "skynet_socket.h"
#include <string.h>
#include <time.h>

FILE * 
skynet_log_open(struct skynet_context * ctx, uint32_t handle) {
	const char * logpath = skynet_getenv("logpath");
	if (logpath == NULL)
		return NULL;
	size_t sz = strlen(logpath);
	char tmp[sz + 16];
	sprintf(tmp, "%s/%08x.log", logpath, handle);
	FILE *f = fopen(tmp, "ab");
	if (f) {
		uint32_t starttime = skynet_starttime();
		uint64_t currenttime = skynet_now();
		time_t ti = starttime + currenttime/100;
		skynet_error(ctx, "Open log file %s", tmp);
		fprintf(f, "open time: %u %s", (uint32_t)currenttime, ctime(&ti));
		fflush(f);
	} else {
		skynet_error(ctx, "Open log file %s fail", tmp);
	}
	return f;
}

void
skynet_log_close(struct skynet_context * ctx, FILE *f, uint32_t handle) {
	skynet_error(ctx, "Close log file :%08x", handle);
	fprintf(f, "close time: %u\n", (uint32_t)skynet_now());
	fclose(f);
}

static void
log_blob(FILE *f, void * buffer, size_t sz) {
	size_t i;
	uint8_t * buf = buffer;
	for (i=0;i!=sz;i++) {
		fprintf(f, "%02x", buf[i]);
	}
}

static void
log_socket(FILE * f, struct skynet_socket_message * message, size_t sz) {
	fprintf(f, "[socket] %d %d %d ", message->type, message->id, message->ud);

	if (message->buffer == NULL) {
		const char *buffer = (const char *)(message + 1);
		sz -= sizeof(*message);
		const char * eol = memchr(buffer, '\0', sz);
		if (eol) {
			sz = eol - buffer;
		}
		fprintf(f, "[%*s]", (int)sz, (const char *)buffer);
	} else {
		sz = message->ud;
		log_blob(f, message->buffer, sz);
	}
	fprintf(f, "\n");
	fflush(f);
}

void 
skynet_log_output(FILE *f, uint32_t source, int type, int session, void * buffer, size_t sz) {
	if (type == PTYPE_SOCKET) {
		log_socket(f, buffer, sz);
	} else {
		uint32_t ti = (uint32_t)skynet_now();
		fprintf(f, ":%08x %d %d %u ", source, type, session, ti);
		log_blob(f, buffer, sz);
		fprintf(f,"\n");
		fflush(f);
	}
}

````

## Server/GameServer/framework/skynet-src/skynet_log.h

SHA-256: `71d1553f5893b13a17f2581cf0e3c2104df90ec8c6f16d81a195c8b6236f774a`

````c
#ifndef skynet_log_h
#define skynet_log_h

#include "skynet_env.h"
#include "skynet.h"

#include <stdio.h>
#include <stdint.h>

FILE * skynet_log_open(struct skynet_context * ctx, uint32_t handle);
void skynet_log_close(struct skynet_context * ctx, FILE *f, uint32_t handle);
void skynet_log_output(FILE *f, uint32_t source, int type, int session, void * buffer, size_t sz);

#endif
````

## Server/GameServer/framework/skynet-src/skynet_main.c

SHA-256: `f76c917f3dfa283e3b8aefc6a49e145c921fb3b866bae81097dadc14ab2d9703`

````c
#include "skynet.h"

#include "skynet_imp.h"
#include "skynet_env.h"
#include "skynet_server.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
#include <signal.h>
#include <assert.h>

static int
optint(const char *key, int opt) {
	const char * str = skynet_getenv(key);
	if (str == NULL) {
		char tmp[20];
		sprintf(tmp,"%d",opt);
		skynet_setenv(key, tmp);
		return opt;
	}
	return strtol(str, NULL, 10);
}

static int
optboolean(const char *key, int opt) {
	const char * str = skynet_getenv(key);
	if (str == NULL) {
		skynet_setenv(key, opt ? "true" : "false");
		return opt;
	}
	return strcmp(str,"true")==0;
}

static const char *
optstring(const char *key,const char * opt) {
	const char * str = skynet_getenv(key);
	if (str == NULL) {
		if (opt) {
			skynet_setenv(key, opt);
			opt = skynet_getenv(key);
		}
		return opt;
	}
	return str;
}

static void
_init_env(lua_State *L) {
	lua_pushnil(L);  /* first key */
	while (lua_next(L, -2) != 0) {
		int keyt = lua_type(L, -2);
		if (keyt != LUA_TSTRING) {
			fprintf(stderr, "Invalid config table\n");
			exit(1);
		}
		const char * key = lua_tostring(L,-2);
		if (lua_type(L,-1) == LUA_TBOOLEAN) {
			int b = lua_toboolean(L,-1);
			skynet_setenv(key,b ? "true" : "false" );
		} else {
			const char * value = lua_tostring(L,-1);
			if (value == NULL) {
				fprintf(stderr, "Invalid config table key = %s\n", key);
				exit(1);
			}
			skynet_setenv(key,value);
		}
		lua_pop(L,1);
	}
	lua_pop(L,1);
}

int sigign() {
	struct sigaction sa;
	sa.sa_handler = SIG_IGN;
	sa.sa_flags = 0;
	sigemptyset(&sa.sa_mask);
	sigaction(SIGPIPE, &sa, 0);
	return 0;
}

static const char * load_config = "\
	local result = {}\n\
	local function getenv(name) return assert(os.getenv(name), [[os.getenv() failed: ]] .. name) end\n\
	local sep = package.config:sub(1,1)\n\
	local current_path = [[.]]..sep\n\
	local function include(filename)\n\
		local last_path = current_path\n\
		local path, name = filename:match([[(.*]]..sep..[[)(.*)$]])\n\
		if path then\n\
			if path:sub(1,1) == sep then	-- root\n\
				current_path = path\n\
			else\n\
				current_path = current_path .. path\n\
			end\n\
		else\n\
			name = filename\n\
		end\n\
		local f = assert(io.open(current_path .. name))\n\
		local code = assert(f:read [[*a]])\n\
		code = string.gsub(code, [[%$([%w_%d]+)]], getenv)\n\
		f:close()\n\
		assert(load(code,[[@]]..filename,[[t]],result))()\n\
		current_path = last_path\n\
	end\n\
	setmetatable(result, { __index = { include = include } })\n\
	local config_name = ...\n\
	include(config_name)\n\
	setmetatable(result, nil)\n\
	return result\n\
";

int
main(int argc, char *argv[]) {
	const char * config_file = NULL ;
	if (argc > 1) {
		config_file = argv[1];
	} else {
		fprintf(stderr, "Need a config file. Please read skynet wiki : https://github.com/cloudwu/skynet/wiki/Config\n"
			"usage: skynet configfilename\n");
		return 1;
	}

	skynet_globalinit();
	skynet_env_init();

	sigign();

	struct skynet_config config;

#ifdef LUA_CACHELIB
	// init the lock of code cache
	luaL_initcodecache();
#endif

	struct lua_State *L = luaL_newstate();
	luaL_openlibs(L);	// link lua lib

	int err =  luaL_loadbufferx(L, load_config, strlen(load_config), "=[skynet config]", "t");
	assert(err == LUA_OK);
	lua_pushstring(L, config_file);

	err = lua_pcall(L, 1, 1, 0);
	if (err) {
		fprintf(stderr,"%s\n",lua_tostring(L,-1));
		lua_close(L);
		return 1;
	}
	_init_env(L);

	config.thread =  optint("thread",8);
	config.module_path = optstring("cpath","./cservice/?.so");
	config.harbor = optint("harbor", 1);
	config.bootstrap = optstring("bootstrap","snlua bootstrap");
	config.daemon = optstring("daemon", NULL);
	config.logger = optstring("logger", NULL);
	config.logservice = optstring("logservice", "logger");
	config.profile = optboolean("profile", 1);

	lua_close(L);

	skynet_start(&config);
	skynet_globalexit();

	return 0;
}

````

## Server/GameServer/framework/skynet-src/skynet_malloc.h

SHA-256: `1e41039e9321beed4e288538a34dcfb082d320a1d65e5369cecf635be2955da9`

````c
#ifndef skynet_malloc_h
#define skynet_malloc_h

#include <stddef.h>

#define skynet_malloc malloc
#define skynet_calloc calloc
#define skynet_realloc realloc
#define skynet_free free
#define skynet_memalign memalign
#define skynet_aligned_alloc aligned_alloc
#define skynet_posix_memalign posix_memalign

void * skynet_malloc(size_t sz);
void * skynet_calloc(size_t nmemb,size_t size);
void * skynet_realloc(void *ptr, size_t size);
void skynet_free(void *ptr);
char * skynet_strdup(const char *str);
void * skynet_lalloc(void *ptr, size_t osize, size_t nsize);	// use for lua
void * skynet_memalign(size_t alignment, size_t size);
void * skynet_aligned_alloc(size_t alignment, size_t size);
int skynet_posix_memalign(void **memptr, size_t alignment, size_t size);

#endif

````

## Server/GameServer/framework/skynet-src/skynet_module.c

SHA-256: `5317a8ddcb882d88022432367b158fc23400002cacc10fc711617d2e2f3dfe63`

````c
#include "skynet.h"

#include "skynet_module.h"
#include "spinlock.h"

#include <assert.h>
#include <string.h>
#include <dlfcn.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define MAX_MODULE_TYPE 32

struct modules {
	int count;
	struct spinlock lock;
	const char * path;
	struct skynet_module m[MAX_MODULE_TYPE];
};

static struct modules * M = NULL;

static void *
_try_open(struct modules *m, const char * name) {
	const char *l;
	const char * path = m->path;
	size_t path_size = strlen(path);
	size_t name_size = strlen(name);

	int sz = path_size + name_size;
	//search path
	void * dl = NULL;
	char tmp[sz];
	do
	{
		memset(tmp,0,sz);
		while (*path == ';') path++;
		if (*path == '\0') break;
		l = strchr(path, ';');
		if (l == NULL) l = path + strlen(path);
		int len = l - path;
		int i;
		for (i=0;path[i]!='?' && i < len ;i++) {
			tmp[i] = path[i];
		}
		memcpy(tmp+i,name,name_size);
		if (path[i] == '?') {
			strncpy(tmp+i+name_size,path+i+1,len - i - 1);
		} else {
			fprintf(stderr,"Invalid C service path\n");
			exit(1);
		}
		dl = dlopen(tmp, RTLD_NOW | RTLD_GLOBAL);
		path = l;
	}while(dl == NULL);

	if (dl == NULL) {
		fprintf(stderr, "try open %s failed : %s\n",name,dlerror());
	}

	return dl;
}

static struct skynet_module * 
_query(const char * name) {
	int i;
	for (i=0;i<M->count;i++) {
		if (strcmp(M->m[i].name,name)==0) {
			return &M->m[i];
		}
	}
	return NULL;
}

static void *
get_api(struct skynet_module *mod, const char *api_name) {
	size_t name_size = strlen(mod->name);
	size_t api_size = strlen(api_name);
	char tmp[name_size + api_size + 1];
	memcpy(tmp, mod->name, name_size);
	memcpy(tmp+name_size, api_name, api_size+1);
	char *ptr = strrchr(tmp, '.');
	if (ptr == NULL) {
		ptr = tmp;
	} else {
		ptr = ptr + 1;
	}
	return dlsym(mod->module, ptr);
}

static int
open_sym(struct skynet_module *mod) {
	mod->create = get_api(mod, "_create");
	mod->init = get_api(mod, "_init");
	mod->release = get_api(mod, "_release");
	mod->signal = get_api(mod, "_signal");

	return mod->init == NULL;
}

struct skynet_module * 
skynet_module_query(const char * name) {
	struct skynet_module * result = _query(name);
	if (result)
		return result;

	SPIN_LOCK(M)

	result = _query(name); // double check

	if (result == NULL && M->count < MAX_MODULE_TYPE) {
		int index = M->count;
		void * dl = _try_open(M,name);
		if (dl) {
			M->m[index].name = name;
			M->m[index].module = dl;

			if (open_sym(&M->m[index]) == 0) {
				M->m[index].name = skynet_strdup(name);
				M->count ++;
				result = &M->m[index];
			}
		}
	}

	SPIN_UNLOCK(M)

	return result;
}

void 
skynet_module_insert(struct skynet_module *mod) {
	SPIN_LOCK(M)

	struct skynet_module * m = _query(mod->name);
	assert(m == NULL && M->count < MAX_MODULE_TYPE);
	int index = M->count;
	M->m[index] = *mod;
	++M->count;

	SPIN_UNLOCK(M)
}

void * 
skynet_module_instance_create(struct skynet_module *m) {
	if (m->create) {
		return m->create();
	} else {
		return (void *)(intptr_t)(~0);
	}
}

int
skynet_module_instance_init(struct skynet_module *m, void * inst, struct skynet_context *ctx, const char * parm) {
	return m->init(inst, ctx, parm);
}

void 
skynet_module_instance_release(struct skynet_module *m, void *inst) {
	if (m->release) {
		m->release(inst);
	}
}

void
skynet_module_instance_signal(struct skynet_module *m, void *inst, int signal) {
	if (m->signal) {
		m->signal(inst, signal);
	}
}

void 
skynet_module_init(const char *path) {
	struct modules *m = skynet_malloc(sizeof(*m));
	m->count = 0;
	m->path = skynet_strdup(path);

	SPIN_INIT(m)

	M = m;
}

````

## Server/GameServer/framework/skynet-src/skynet_module.h

SHA-256: `95473fc43187f45bb3cb5300d861608336f60783562b37318c2683853a491925`

````c
#ifndef SKYNET_MODULE_H
#define SKYNET_MODULE_H

struct skynet_context;

typedef void * (*skynet_dl_create)(void);
typedef int (*skynet_dl_init)(void * inst, struct skynet_context *, const char * parm);
typedef void (*skynet_dl_release)(void * inst);
typedef void (*skynet_dl_signal)(void * inst, int signal);

struct skynet_module {
	const char * name;
	void * module;
	skynet_dl_create create;
	skynet_dl_init init;
	skynet_dl_release release;
	skynet_dl_signal signal;
};

void skynet_module_insert(struct skynet_module *mod);
struct skynet_module * skynet_module_query(const char * name);
void * skynet_module_instance_create(struct skynet_module *);
int skynet_module_instance_init(struct skynet_module *, void * inst, struct skynet_context *ctx, const char * parm);
void skynet_module_instance_release(struct skynet_module *, void *inst);
void skynet_module_instance_signal(struct skynet_module *, void *inst, int signal);

void skynet_module_init(const char *path);

#endif

````

## Server/GameServer/framework/skynet-src/skynet_monitor.c

SHA-256: `879fedeb811acd9bc9ca98fc011ed5a809b8c4131a3647c2d826ab3b3a0c0a12`

````c
#include "skynet.h"

#include "skynet_monitor.h"
#include "skynet_server.h"
#include "skynet.h"
#include "atomic.h"

#include <stdlib.h>
#include <string.h>

struct skynet_monitor {
	int version;
	int check_version;
	uint32_t source;
	uint32_t destination;
};

struct skynet_monitor * 
skynet_monitor_new() {
	struct skynet_monitor * ret = skynet_malloc(sizeof(*ret));
	memset(ret, 0, sizeof(*ret));
	return ret;
}

void 
skynet_monitor_delete(struct skynet_monitor *sm) {
	skynet_free(sm);
}

void 
skynet_monitor_trigger(struct skynet_monitor *sm, uint32_t source, uint32_t destination) {
	sm->source = source;
	sm->destination = destination;
	ATOM_INC(&sm->version);
}

void 
skynet_monitor_check(struct skynet_monitor *sm) {
	if (sm->version == sm->check_version) {
		if (sm->destination) {
			skynet_context_endless(sm->destination);
			skynet_error(NULL, "A message from [ :%08x ] to [ :%08x ] maybe in an endless loop (version = %d)", sm->source , sm->destination, sm->version);
		}
	} else {
		sm->check_version = sm->version;
	}
}

````

## Server/GameServer/framework/skynet-src/skynet_monitor.h

SHA-256: `2297e8ef506bf331f0bb098c5854021a6e5532e1279c2d205db62cc178be9c89`

````c
#ifndef SKYNET_MONITOR_H
#define SKYNET_MONITOR_H

#include <stdint.h>

struct skynet_monitor;

struct skynet_monitor * skynet_monitor_new();
void skynet_monitor_delete(struct skynet_monitor *);
void skynet_monitor_trigger(struct skynet_monitor *, uint32_t source, uint32_t destination);
void skynet_monitor_check(struct skynet_monitor *);

#endif

````

## Server/GameServer/framework/skynet-src/skynet_mq.c

SHA-256: `11eb445405e59b419d20a17c35a15308ff3b84672410bfcdb00b7d53acc8008a`

````c
#include "skynet.h"
#include "skynet_mq.h"
#include "skynet_handle.h"
#include "spinlock.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdbool.h>

#define DEFAULT_QUEUE_SIZE 64
#define MAX_GLOBAL_MQ 0x10000

// 0 means mq is not in global mq.
// 1 means mq is in global mq , or the message is dispatching.

#define MQ_IN_GLOBAL 1
#define MQ_OVERLOAD 1024

struct message_queue {
	struct spinlock lock;
	uint32_t handle;
	int cap;
	int head;
	int tail;
	int release;
	int in_global;
	int overload;
	int overload_threshold;
	struct skynet_message *queue;
	struct message_queue *next;
};

struct global_queue {
	struct message_queue *head;
	struct message_queue *tail;
	struct spinlock lock;
};

static struct global_queue *Q = NULL;

void 
skynet_globalmq_push(struct message_queue * queue) {
	struct global_queue *q= Q;

	SPIN_LOCK(q)
	assert(queue->next == NULL);
	if(q->tail) {
		q->tail->next = queue;
		q->tail = queue;
	} else {
		q->head = q->tail = queue;
	}
	SPIN_UNLOCK(q)
}

struct message_queue * 
skynet_globalmq_pop() {
	struct global_queue *q = Q;

	SPIN_LOCK(q)
	struct message_queue *mq = q->head;
	if(mq) {
		q->head = mq->next;
		if(q->head == NULL) {
			assert(mq == q->tail);
			q->tail = NULL;
		}
		mq->next = NULL;
	}
	SPIN_UNLOCK(q)

	return mq;
}

struct message_queue * 
skynet_mq_create(uint32_t handle) {
	struct message_queue *q = skynet_malloc(sizeof(*q));
	q->handle = handle;
	q->cap = DEFAULT_QUEUE_SIZE;
	q->head = 0;
	q->tail = 0;
	SPIN_INIT(q)
	// When the queue is create (always between service create and service init) ,
	// set in_global flag to avoid push it to global queue .
	// If the service init success, skynet_context_new will call skynet_mq_push to push it to global queue.
	q->in_global = MQ_IN_GLOBAL;
	q->release = 0;
	q->overload = 0;
	q->overload_threshold = MQ_OVERLOAD;
	q->queue = skynet_malloc(sizeof(struct skynet_message) * q->cap);
	q->next = NULL;

	return q;
}

static void 
_release(struct message_queue *q) {
	assert(q->next == NULL);
	SPIN_DESTROY(q)
	skynet_free(q->queue);
	skynet_free(q);
}

uint32_t 
skynet_mq_handle(struct message_queue *q) {
	return q->handle;
}

int
skynet_mq_length(struct message_queue *q) {
	int head, tail,cap;

	SPIN_LOCK(q)
	head = q->head;
	tail = q->tail;
	cap = q->cap;
	SPIN_UNLOCK(q)
	
	if (head <= tail) {
		return tail - head;
	}
	return tail + cap - head;
}

int
skynet_mq_overload(struct message_queue *q) {
	if (q->overload) {
		int overload = q->overload;
		q->overload = 0;
		return overload;
	} 
	return 0;
}

int
skynet_mq_pop(struct message_queue *q, struct skynet_message *message) {
	int ret = 1;
	SPIN_LOCK(q)

	if (q->head != q->tail) {
		*message = q->queue[q->head++];
		ret = 0;
		int head = q->head;
		int tail = q->tail;
		int cap = q->cap;

		if (head >= cap) {
			q->head = head = 0;
		}
		int length = tail - head;
		if (length < 0) {
			length += cap;
		}
		while (length > q->overload_threshold) {
			q->overload = length;
			q->overload_threshold *= 2;
		}
	} else {
		// reset overload_threshold when queue is empty
		q->overload_threshold = MQ_OVERLOAD;
	}

	if (ret) {
		q->in_global = 0;
	}
	
	SPIN_UNLOCK(q)

	return ret;
}

static void
expand_queue(struct message_queue *q) {
	struct skynet_message *new_queue = skynet_malloc(sizeof(struct skynet_message) * q->cap * 2);
	int i;
	for (i=0;i<q->cap;i++) {
		new_queue[i] = q->queue[(q->head + i) % q->cap];
	}
	q->head = 0;
	q->tail = q->cap;
	q->cap *= 2;
	
	skynet_free(q->queue);
	q->queue = new_queue;
}

void 
skynet_mq_push(struct message_queue *q, struct skynet_message *message) {
	assert(message);
	SPIN_LOCK(q)

	q->queue[q->tail] = *message;
	if (++ q->tail >= q->cap) {
		q->tail = 0;
	}

	if (q->head == q->tail) {
		expand_queue(q);
	}

	if (q->in_global == 0) {
		q->in_global = MQ_IN_GLOBAL;
		skynet_globalmq_push(q);
	}
	
	SPIN_UNLOCK(q)
}

void 
skynet_mq_init() {
	struct global_queue *q = skynet_malloc(sizeof(*q));
	memset(q,0,sizeof(*q));
	SPIN_INIT(q);
	Q=q;
}

void 
skynet_mq_mark_release(struct message_queue *q) {
	SPIN_LOCK(q)
	assert(q->release == 0);
	q->release = 1;
	if (q->in_global != MQ_IN_GLOBAL) {
		skynet_globalmq_push(q);
	}
	SPIN_UNLOCK(q)
}

static void
_drop_queue(struct message_queue *q, message_drop drop_func, void *ud) {
	struct skynet_message msg;
	while(!skynet_mq_pop(q, &msg)) {
		drop_func(&msg, ud);
	}
	_release(q);
}

void 
skynet_mq_release(struct message_queue *q, message_drop drop_func, void *ud) {
	SPIN_LOCK(q)
	
	if (q->release) {
		SPIN_UNLOCK(q)
		_drop_queue(q, drop_func, ud);
	} else {
		skynet_globalmq_push(q);
		SPIN_UNLOCK(q)
	}
}

````

## Server/GameServer/framework/skynet-src/skynet_mq.h

SHA-256: `422aaad1e86a90037c9da472a5bd38f9f379868439c42a2e5870bb5c35c9ad33`

````c
#ifndef SKYNET_MESSAGE_QUEUE_H
#define SKYNET_MESSAGE_QUEUE_H

#include <stdlib.h>
#include <stdint.h>

struct skynet_message {
	uint32_t source;
	int session;
	void * data;
	size_t sz;
};

// type is encoding in skynet_message.sz high 8bit
#define MESSAGE_TYPE_MASK (SIZE_MAX >> 8)
#define MESSAGE_TYPE_SHIFT ((sizeof(size_t)-1) * 8)

struct message_queue;

void skynet_globalmq_push(struct message_queue * queue);
struct message_queue * skynet_globalmq_pop(void);

struct message_queue * skynet_mq_create(uint32_t handle);
void skynet_mq_mark_release(struct message_queue *q);

typedef void (*message_drop)(struct skynet_message *, void *);

void skynet_mq_release(struct message_queue *q, message_drop drop_func, void *ud);
uint32_t skynet_mq_handle(struct message_queue *);

// 0 for success
int skynet_mq_pop(struct message_queue *q, struct skynet_message *message);
void skynet_mq_push(struct message_queue *q, struct skynet_message *message);

// return the length of message queue, for debug
int skynet_mq_length(struct message_queue *q);
int skynet_mq_overload(struct message_queue *q);

void skynet_mq_init();

#endif

````

## Server/GameServer/framework/skynet-src/skynet_server.c

SHA-256: `8d9202d8d0341312fa347282988defa604a81221dab63ba6497ed3d13c5484ef`

````c
#include "skynet.h"

#include "skynet_server.h"
#include "skynet_module.h"
#include "skynet_handle.h"
#include "skynet_mq.h"
#include "skynet_timer.h"
#include "skynet_harbor.h"
#include "skynet_env.h"
#include "skynet_monitor.h"
#include "skynet_imp.h"
#include "skynet_log.h"
#include "skynet_timer.h"
#include "spinlock.h"
#include "atomic.h"

#include <pthread.h>

#include <string.h>
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>

#ifdef CALLING_CHECK

#define CHECKCALLING_BEGIN(ctx) if (!(spinlock_trylock(&ctx->calling))) { assert(0); }
#define CHECKCALLING_END(ctx) spinlock_unlock(&ctx->calling);
#define CHECKCALLING_INIT(ctx) spinlock_init(&ctx->calling);
#define CHECKCALLING_DESTROY(ctx) spinlock_destroy(&ctx->calling);
#define CHECKCALLING_DECL struct spinlock calling;

#else

#define CHECKCALLING_BEGIN(ctx)
#define CHECKCALLING_END(ctx)
#define CHECKCALLING_INIT(ctx)
#define CHECKCALLING_DESTROY(ctx)
#define CHECKCALLING_DECL

#endif

struct skynet_context {
	void * instance;
	struct skynet_module * mod;
	void * cb_ud;
	skynet_cb cb;
	struct message_queue *queue;
	FILE * logfile;
	uint64_t cpu_cost;	// in microsec
	uint64_t cpu_start;	// in microsec
	char result[32];
	uint32_t handle;
	int session_id;
	int ref;
	int message_count;
	bool init;
	bool endless;
	bool profile;

	CHECKCALLING_DECL
};

struct skynet_node {
	int total;
	int init;
	uint32_t monitor_exit;
	pthread_key_t handle_key;
	bool profile;	// default is off
};

static struct skynet_node G_NODE;

int 
skynet_context_total() {
	return G_NODE.total;
}

static void
context_inc() {
	ATOM_INC(&G_NODE.total);
}

static void
context_dec() {
	ATOM_DEC(&G_NODE.total);
}

uint32_t 
skynet_current_handle(void) {
	if (G_NODE.init) {
		void * handle = pthread_getspecific(G_NODE.handle_key);
		return (uint32_t)(uintptr_t)handle;
	} else {
		uint32_t v = (uint32_t)(-THREAD_MAIN);
		return v;
	}
}

static void
id_to_hex(char * str, uint32_t id) {
	int i;
	static char hex[16] = { '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F' };
	str[0] = ':';
	for (i=0;i<8;i++) {
		str[i+1] = hex[(id >> ((7-i) * 4))&0xf];
	}
	str[9] = '\0';
}

struct drop_t {
	uint32_t handle;
};

static void
drop_message(struct skynet_message *msg, void *ud) {
	struct drop_t *d = ud;
	skynet_free(msg->data);
	uint32_t source = d->handle;
	assert(source);
	// report error to the message source
	skynet_send(NULL, source, msg->source, PTYPE_ERROR, 0, NULL, 0);
}

struct skynet_context * 
skynet_context_new(const char * name, const char *param) {
	struct skynet_module * mod = skynet_module_query(name);

	if (mod == NULL)
		return NULL;

	void *inst = skynet_module_instance_create(mod);
	if (inst == NULL)
		return NULL;
	struct skynet_context * ctx = skynet_malloc(sizeof(*ctx));
	CHECKCALLING_INIT(ctx)

	ctx->mod = mod;
	ctx->instance = inst;
	ctx->ref = 2;
	ctx->cb = NULL;
	ctx->cb_ud = NULL;
	ctx->session_id = 0;
	ctx->logfile = NULL;

	ctx->init = false;
	ctx->endless = false;

	ctx->cpu_cost = 0;
	ctx->cpu_start = 0;
	ctx->message_count = 0;
	ctx->profile = G_NODE.profile;
	// Should set to 0 first to avoid skynet_handle_retireall get an uninitialized handle
	ctx->handle = 0;	
	ctx->handle = skynet_handle_register(ctx);
	struct message_queue * queue = ctx->queue = skynet_mq_create(ctx->handle);
	// init function maybe use ctx->handle, so it must init at last
	context_inc();

	CHECKCALLING_BEGIN(ctx)
	int r = skynet_module_instance_init(mod, inst, ctx, param);
	CHECKCALLING_END(ctx)
	if (r == 0) {
		struct skynet_context * ret = skynet_context_release(ctx);
		if (ret) {
			ctx->init = true;
		}
		skynet_globalmq_push(queue);
		if (ret) {
			skynet_error(ret, "LAUNCH %s %s", name, param ? param : "");
		}
		return ret;
	} else {
		skynet_error(ctx, "FAILED launch %s", name);
		uint32_t handle = ctx->handle;
		skynet_context_release(ctx);
		skynet_handle_retire(handle);
		struct drop_t d = { handle };
		skynet_mq_release(queue, drop_message, &d);
		return NULL;
	}
}

int
skynet_context_newsession(struct skynet_context *ctx) {
	// session always be a positive number
	int session = ++ctx->session_id;
	if (session <= 0) {
		ctx->session_id = 1;
		return 1;
	}
	return session;
}

void 
skynet_context_grab(struct skynet_context *ctx) {
	ATOM_INC(&ctx->ref);
}

void
skynet_context_reserve(struct skynet_context *ctx) {
	skynet_context_grab(ctx);
	// don't count the context reserved, because skynet abort (the worker threads terminate) only when the total context is 0 .
	// the reserved context will be release at last.
	context_dec();
}

static void 
delete_context(struct skynet_context *ctx) {
	if (ctx->logfile) {
		fclose(ctx->logfile);
	}
	skynet_module_instance_release(ctx->mod, ctx->instance);
	skynet_mq_mark_release(ctx->queue);
	CHECKCALLING_DESTROY(ctx)
	skynet_free(ctx);
	context_dec();
}

struct skynet_context * 
skynet_context_release(struct skynet_context *ctx) {
	if (ATOM_DEC(&ctx->ref) == 0) {
		delete_context(ctx);
		return NULL;
	}
	return ctx;
}

int
skynet_context_push(uint32_t handle, struct skynet_message *message) {
	struct skynet_context * ctx = skynet_handle_grab(handle);
	if (ctx == NULL) {
		return -1;
	}
	skynet_mq_push(ctx->queue, message);
	skynet_context_release(ctx);

	return 0;
}

void 
skynet_context_endless(uint32_t handle) {
	struct skynet_context * ctx = skynet_handle_grab(handle);
	if (ctx == NULL) {
		return;
	}
	ctx->endless = true;
	skynet_context_release(ctx);
}

int 
skynet_isremote(struct skynet_context * ctx, uint32_t handle, int * harbor) {
	int ret = skynet_harbor_message_isremote(handle);
	if (harbor) {
		*harbor = (int)(handle >> HANDLE_REMOTE_SHIFT);
	}
	return ret;
}

static void
dispatch_message(struct skynet_context *ctx, struct skynet_message *msg) {
	assert(ctx->init);
	CHECKCALLING_BEGIN(ctx)
	pthread_setspecific(G_NODE.handle_key, (void *)(uintptr_t)(ctx->handle));
	int type = msg->sz >> MESSAGE_TYPE_SHIFT;
	size_t sz = msg->sz & MESSAGE_TYPE_MASK;
	if (ctx->logfile) {
		skynet_log_output(ctx->logfile, msg->source, type, msg->session, msg->data, sz);
	}
	++ctx->message_count;
	int reserve_msg;
	if (ctx->profile) {
		ctx->cpu_start = skynet_thread_time();
		reserve_msg = ctx->cb(ctx, ctx->cb_ud, type, msg->session, msg->source, msg->data, sz);
		uint64_t cost_time = skynet_thread_time() - ctx->cpu_start;
		ctx->cpu_cost += cost_time;
	} else {
		reserve_msg = ctx->cb(ctx, ctx->cb_ud, type, msg->session, msg->source, msg->data, sz);
	}
	if (!reserve_msg) {
		skynet_free(msg->data);
	}
	CHECKCALLING_END(ctx)
}

void 
skynet_context_dispatchall(struct skynet_context * ctx) {
	// for skynet_error
	struct skynet_message msg;
	struct message_queue *q = ctx->queue;
	while (!skynet_mq_pop(q,&msg)) {
		dispatch_message(ctx, &msg);
	}
}

struct message_queue * 
skynet_context_message_dispatch(struct skynet_monitor *sm, struct message_queue *q, int weight) {
	if (q == NULL) {
		q = skynet_globalmq_pop();
		if (q==NULL)
			return NULL;
	}

	uint32_t handle = skynet_mq_handle(q);

	struct skynet_context * ctx = skynet_handle_grab(handle);
	if (ctx == NULL) {
		struct drop_t d = { handle };
		skynet_mq_release(q, drop_message, &d);
		return skynet_globalmq_pop();
	}

	int i,n=1;
	struct skynet_message msg;

	for (i=0;i<n;i++) {
		if (skynet_mq_pop(q,&msg)) {
			skynet_context_release(ctx);
			return skynet_globalmq_pop();
		} else if (i==0 && weight >= 0) {
			n = skynet_mq_length(q);
			n >>= weight;
		}
		int overload = skynet_mq_overload(q);
		if (overload) {
			skynet_error(ctx, "May overload, message queue length = %d", overload);
		}

		skynet_monitor_trigger(sm, msg.source , handle);

		if (ctx->cb == NULL) {
			skynet_free(msg.data);
		} else {
			dispatch_message(ctx, &msg);
		}

		skynet_monitor_trigger(sm, 0,0);
	}

	assert(q == ctx->queue);
	struct message_queue *nq = skynet_globalmq_pop();
	if (nq) {
		// If global mq is not empty , push q back, and return next queue (nq)
		// Else (global mq is empty or block, don't push q back, and return q again (for next dispatch)
		skynet_globalmq_push(q);
		q = nq;
	} 
	skynet_context_release(ctx);

	return q;
}

static void
copy_name(char name[GLOBALNAME_LENGTH], const char * addr) {
	int i;
	for (i=0;i<GLOBALNAME_LENGTH && addr[i];i++) {
		name[i] = addr[i];
	}
	for (;i<GLOBALNAME_LENGTH;i++) {
		name[i] = '\0';
	}
}

uint32_t 
skynet_queryname(struct skynet_context * context, const char * name) {
	switch(name[0]) {
	case ':':
		return strtoul(name+1,NULL,16);
	case '.':
		return skynet_handle_findname(name + 1);
	}
	skynet_error(context, "Don't support query global name %s",name);
	return 0;
}

static void
handle_exit(struct skynet_context * context, uint32_t handle) {
	if (handle == 0) {
		handle = context->handle;
		skynet_error(context, "KILL self");
	} else {
		skynet_error(context, "KILL :%0x", handle);
	}
	if (G_NODE.monitor_exit) {
		skynet_send(context,  handle, G_NODE.monitor_exit, PTYPE_CLIENT, 0, NULL, 0);
	}
	skynet_handle_retire(handle);
}

// skynet command

struct command_func {
	const char *name;
	const char * (*func)(struct skynet_context * context, const char * param);
};

static const char *
cmd_timeout(struct skynet_context * context, const char * param) {
	char * session_ptr = NULL;
	int ti = strtol(param, &session_ptr, 10);
	int session = skynet_context_newsession(context);
	skynet_timeout(context->handle, ti, session);
	sprintf(context->result, "%d", session);
	return context->result;
}

static const char *
cmd_reg(struct skynet_context * context, const char * param) {
	if (param == NULL || param[0] == '\0') {
		sprintf(context->result, ":%x", context->handle);
		return context->result;
	} else if (param[0] == '.') {
		return skynet_handle_namehandle(context->handle, param + 1);
	} else {
		skynet_error(context, "Can't register global name %s in C", param);
		return NULL;
	}
}

static const char *
cmd_query(struct skynet_context * context, const char * param) {
	if (param[0] == '.') {
		uint32_t handle = skynet_handle_findname(param+1);
		if (handle) {
			sprintf(context->result, ":%x", handle);
			return context->result;
		}
	}
	return NULL;
}

static const char *
cmd_name(struct skynet_context * context, const char * param) {
	int size = strlen(param);
	char name[size+1];
	char handle[size+1];
	sscanf(param,"%s %s",name,handle);
	if (handle[0] != ':') {
		return NULL;
	}
	uint32_t handle_id = strtoul(handle+1, NULL, 16);
	if (handle_id == 0) {
		return NULL;
	}
	if (name[0] == '.') {
		return skynet_handle_namehandle(handle_id, name + 1);
	} else {
		skynet_error(context, "Can't set global name %s in C", name);
	}
	return NULL;
}

static const char *
cmd_exit(struct skynet_context * context, const char * param) {
	handle_exit(context, 0);
	return NULL;
}

static uint32_t
tohandle(struct skynet_context * context, const char * param) {
	uint32_t handle = 0;
	if (param[0] == ':') {
		handle = strtoul(param+1, NULL, 16);
	} else if (param[0] == '.') {
		handle = skynet_handle_findname(param+1);
	} else {
		skynet_error(context, "Can't convert %s to handle",param);
	}

	return handle;
}

static const char *
cmd_kill(struct skynet_context * context, const char * param) {
	uint32_t handle = tohandle(context, param);
	if (handle) {
		handle_exit(context, handle);
	}
	return NULL;
}

static const char *
cmd_launch(struct skynet_context * context, const char * param) {
	size_t sz = strlen(param);
	char tmp[sz+1];
	strcpy(tmp,param);
	char * args = tmp;
	char * mod = strsep(&args, " \t\r\n");
	args = strsep(&args, "\r\n");
	struct skynet_context * inst = skynet_context_new(mod,args);
	if (inst == NULL) {
		return NULL;
	} else {
		id_to_hex(context->result, inst->handle);
		return context->result;
	}
}

static const char *
cmd_getenv(struct skynet_context * context, const char * param) {
	return skynet_getenv(param);
}

static const char *
cmd_setenv(struct skynet_context * context, const char * param) {
	size_t sz = strlen(param);
	char key[sz+1];
	int i;
	for (i=0;param[i] != ' ' && param[i];i++) {
		key[i] = param[i];
	}
	if (param[i] == '\0')
		return NULL;

	key[i] = '\0';
	param += i+1;
	
	skynet_setenv(key,param);
	return NULL;
}

static const char *
cmd_starttime(struct skynet_context * context, const char * param) {
	uint32_t sec = skynet_starttime();
	sprintf(context->result,"%u",sec);
	return context->result;
}

static const char *
cmd_abort(struct skynet_context * context, const char * param) {
	skynet_handle_retireall();
	return NULL;
}

static const char *
cmd_monitor(struct skynet_context * context, const char * param) {
	uint32_t handle=0;
	if (param == NULL || param[0] == '\0') {
		if (G_NODE.monitor_exit) {
			// return current monitor serivce
			sprintf(context->result, ":%x", G_NODE.monitor_exit);
			return context->result;
		}
		return NULL;
	} else {
		handle = tohandle(context, param);
	}
	G_NODE.monitor_exit = handle;
	return NULL;
}

static const char *
cmd_stat(struct skynet_context * context, const char * param) {
	if (strcmp(param, "mqlen") == 0) {
		int len = skynet_mq_length(context->queue);
		sprintf(context->result, "%d", len);
	} else if (strcmp(param, "endless") == 0) {
		if (context->endless) {
			strcpy(context->result, "1");
			context->endless = false;
		} else {
			strcpy(context->result, "0");
		}
	} else if (strcmp(param, "cpu") == 0) {
		double t = (double)context->cpu_cost / 1000000.0;	// microsec
		sprintf(context->result, "%lf", t);
	} else if (strcmp(param, "time") == 0) {
		if (context->profile) {
			uint64_t ti = skynet_thread_time() - context->cpu_start;
			double t = (double)ti / 1000000.0;	// microsec
			sprintf(context->result, "%lf", t);
		} else {
			strcpy(context->result, "0");
		}
	} else if (strcmp(param, "message") == 0) {
		sprintf(context->result, "%d", context->message_count);
	} else {
		context->result[0] = '\0';
	}
	return context->result;
}

static const char *
cmd_logon(struct skynet_context * context, const char * param) {
	uint32_t handle = tohandle(context, param);
	if (handle == 0)
		return NULL;
	struct skynet_context * ctx = skynet_handle_grab(handle);
	if (ctx == NULL)
		return NULL;
	FILE *f = NULL;
	FILE * lastf = ctx->logfile;
	if (lastf == NULL) {
		f = skynet_log_open(context, handle);
		if (f) {
			if (!ATOM_CAS_POINTER(&ctx->logfile, NULL, f)) {
				// logfile opens in other thread, close this one.
				fclose(f);
			}
		}
	}
	skynet_context_release(ctx);
	return NULL;
}

static const char *
cmd_logoff(struct skynet_context * context, const char * param) {
	uint32_t handle = tohandle(context, param);
	if (handle == 0)
		return NULL;
	struct skynet_context * ctx = skynet_handle_grab(handle);
	if (ctx == NULL)
		return NULL;
	FILE * f = ctx->logfile;
	if (f) {
		// logfile may close in other thread
		if (ATOM_CAS_POINTER(&ctx->logfile, f, NULL)) {
			skynet_log_close(context, f, handle);
		}
	}
	skynet_context_release(ctx);
	return NULL;
}

static const char *
cmd_signal(struct skynet_context * context, const char * param) {
	uint32_t handle = tohandle(context, param);
	if (handle == 0)
		return NULL;
	struct skynet_context * ctx = skynet_handle_grab(handle);
	if (ctx == NULL)
		return NULL;
	param = strchr(param, ' ');
	int sig = 0;
	if (param) {
		sig = strtol(param, NULL, 0);
	}
	// NOTICE: the signal function should be thread safe.
	skynet_module_instance_signal(ctx->mod, ctx->instance, sig);

	skynet_context_release(ctx);
	return NULL;
}

static struct command_func cmd_funcs[] = {
	{ "TIMEOUT", cmd_timeout },
	{ "REG", cmd_reg },
	{ "QUERY", cmd_query },
	{ "NAME", cmd_name },
	{ "EXIT", cmd_exit },
	{ "KILL", cmd_kill },
	{ "LAUNCH", cmd_launch },
	{ "GETENV", cmd_getenv },
	{ "SETENV", cmd_setenv },
	{ "STARTTIME", cmd_starttime },
	{ "ABORT", cmd_abort },
	{ "MONITOR", cmd_monitor },
	{ "STAT", cmd_stat },
	{ "LOGON", cmd_logon },
	{ "LOGOFF", cmd_logoff },
	{ "SIGNAL", cmd_signal },
	{ NULL, NULL },
};

const char * 
skynet_command(struct skynet_context * context, const char * cmd , const char * param) {
	struct command_func * method = &cmd_funcs[0];
	while(method->name) {
		if (strcmp(cmd, method->name) == 0) {
			return method->func(context, param);
		}
		++method;
	}

	return NULL;
}

static void
_filter_args(struct skynet_context * context, int type, int *session, void ** data, size_t * sz) {
	int needcopy = !(type & PTYPE_TAG_DONTCOPY);
	int allocsession = type & PTYPE_TAG_ALLOCSESSION;
	type &= 0xff;

	if (allocsession) {
		assert(*session == 0);
		*session = skynet_context_newsession(context);
	}

	if (needcopy && *data) {
		char * msg = skynet_malloc(*sz+1);
		memcpy(msg, *data, *sz);
		msg[*sz] = '\0';
		*data = msg;
	}

	*sz |= (size_t)type << MESSAGE_TYPE_SHIFT;
}

int
skynet_send(struct skynet_context * context, uint32_t source, uint32_t destination , int type, int session, void * data, size_t sz) {
	if ((sz & MESSAGE_TYPE_MASK) != sz) {
		skynet_error(context, "The message to %x is too large", destination);
		if (type & PTYPE_TAG_DONTCOPY) {
			skynet_free(data);
		}
		return -2;
	}
	_filter_args(context, type, &session, (void **)&data, &sz);

	if (source == 0) {
		source = context->handle;
	}

	if (destination == 0) {
		if (data) {
			skynet_error(context, "Destination address can't be 0");
			skynet_free(data);
			return -1;
		}

		return session;
	}
	if (skynet_harbor_message_isremote(destination)) {
		struct remote_message * rmsg = skynet_malloc(sizeof(*rmsg));
		rmsg->destination.handle = destination;
		rmsg->message = data;
		rmsg->sz = sz & MESSAGE_TYPE_MASK;
		rmsg->type = sz >> MESSAGE_TYPE_SHIFT;
		skynet_harbor_send(rmsg, source, session);
	} else {
		struct skynet_message smsg;
		smsg.source = source;
		smsg.session = session;
		smsg.data = data;
		smsg.sz = sz;

		if (skynet_context_push(destination, &smsg)) {
			skynet_free(data);
			return -1;
		}
	}
	return session;
}

int
skynet_sendname(struct skynet_context * context, uint32_t source, const char * addr , int type, int session, void * data, size_t sz) {
	if (source == 0) {
		source = context->handle;
	}
	uint32_t des = 0;
	if (addr[0] == ':') {
		des = strtoul(addr+1, NULL, 16);
	} else if (addr[0] == '.') {
		des = skynet_handle_findname(addr + 1);
		if (des == 0) {
			if (type & PTYPE_TAG_DONTCOPY) {
				skynet_free(data);
			}
			return -1;
		}
	} else {
		if ((sz & MESSAGE_TYPE_MASK) != sz) {
			skynet_error(context, "The message to %s is too large", addr);
			if (type & PTYPE_TAG_DONTCOPY) {
				skynet_free(data);
			}
			return -2;
		}
		_filter_args(context, type, &session, (void **)&data, &sz);

		struct remote_message * rmsg = skynet_malloc(sizeof(*rmsg));
		copy_name(rmsg->destination.name, addr);
		rmsg->destination.handle = 0;
		rmsg->message = data;
		rmsg->sz = sz & MESSAGE_TYPE_MASK;
		rmsg->type = sz >> MESSAGE_TYPE_SHIFT;

		skynet_harbor_send(rmsg, source, session);
		return session;
	}

	return skynet_send(context, source, des, type, session, data, sz);
}

uint32_t 
skynet_context_handle(struct skynet_context *ctx) {
	return ctx->handle;
}

void 
skynet_callback(struct skynet_context * context, void *ud, skynet_cb cb) {
	context->cb = cb;
	context->cb_ud = ud;
}

void
skynet_context_send(struct skynet_context * ctx, void * msg, size_t sz, uint32_t source, int type, int session) {
	struct skynet_message smsg;
	smsg.source = source;
	smsg.session = session;
	smsg.data = msg;
	smsg.sz = sz | (size_t)type << MESSAGE_TYPE_SHIFT;

	skynet_mq_push(ctx->queue, &smsg);
}

void 
skynet_globalinit(void) {
	G_NODE.total = 0;
	G_NODE.monitor_exit = 0;
	G_NODE.init = 1;
	if (pthread_key_create(&G_NODE.handle_key, NULL)) {
		fprintf(stderr, "pthread_key_create failed");
		exit(1);
	}
	// set mainthread's key
	skynet_initthread(THREAD_MAIN);
}

void 
skynet_globalexit(void) {
	pthread_key_delete(G_NODE.handle_key);
}

void
skynet_initthread(int m) {
	uintptr_t v = (uint32_t)(-m);
	pthread_setspecific(G_NODE.handle_key, (void *)v);
}

void
skynet_profile_enable(int enable) {
	G_NODE.profile = (bool)enable;
}

````

## Server/GameServer/framework/skynet-src/skynet_server.h

SHA-256: `fb7ea33829ff4f47379fc5e706deaa949699c5e2d544d77c9086a047158aa51e`

````c
#ifndef SKYNET_SERVER_H
#define SKYNET_SERVER_H

#include <stdint.h>
#include <stdlib.h>

struct skynet_context;
struct skynet_message;
struct skynet_monitor;

struct skynet_context * skynet_context_new(const char * name, const char * parm);
void skynet_context_grab(struct skynet_context *);
void skynet_context_reserve(struct skynet_context *ctx);
struct skynet_context * skynet_context_release(struct skynet_context *);
uint32_t skynet_context_handle(struct skynet_context *);
int skynet_context_push(uint32_t handle, struct skynet_message *message);
void skynet_context_send(struct skynet_context * context, void * msg, size_t sz, uint32_t source, int type, int session);
int skynet_context_newsession(struct skynet_context *);
struct message_queue * skynet_context_message_dispatch(struct skynet_monitor *, struct message_queue *, int weight);	// return next queue
int skynet_context_total();
void skynet_context_dispatchall(struct skynet_context * context);	// for skynet_error output before exit

void skynet_context_endless(uint32_t handle);	// for monitor

void skynet_globalinit(void);
void skynet_globalexit(void);
void skynet_initthread(int m);

void skynet_profile_enable(int enable);

#endif

````

## Server/GameServer/framework/skynet-src/skynet_socket.c

SHA-256: `3ee755e6be3dff9c60e079406ade5e09bcc762ec4d6a46342a0ba573988b613e`

````c
#include "skynet.h"

#include "skynet_socket.h"
#include "socket_server.h"
#include "skynet_server.h"
#include "skynet_mq.h"
#include "skynet_harbor.h"

#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

static struct socket_server * SOCKET_SERVER = NULL;

void 
skynet_socket_init() {
	SOCKET_SERVER = socket_server_create(skynet_now());
}

void
skynet_socket_exit() {
	socket_server_exit(SOCKET_SERVER);
}

void
skynet_socket_free() {
	socket_server_release(SOCKET_SERVER);
	SOCKET_SERVER = NULL;
}

void
skynet_socket_updatetime() {
	socket_server_updatetime(SOCKET_SERVER, skynet_now());
}

// mainloop thread
static void
forward_message(int type, bool padding, struct socket_message * result) {
	struct skynet_socket_message *sm;
	size_t sz = sizeof(*sm);
	if (padding) {
		if (result->data) {
			size_t msg_sz = strlen(result->data);
			if (msg_sz > 128) {
				msg_sz = 128;
			}
			sz += msg_sz;
		} else {
			result->data = "";
		}
	}
	sm = (struct skynet_socket_message *)skynet_malloc(sz);
	sm->type = type;
	sm->id = result->id;
	sm->ud = result->ud;
	if (padding) {
		sm->buffer = NULL;
		memcpy(sm+1, result->data, sz - sizeof(*sm));
	} else {
		sm->buffer = result->data;
	}

	struct skynet_message message;
	message.source = 0;
	message.session = 0;
	message.data = sm;
	message.sz = sz | ((size_t)PTYPE_SOCKET << MESSAGE_TYPE_SHIFT);
	
	if (skynet_context_push((uint32_t)result->opaque, &message)) {
		// todo: report somewhere to close socket
		// don't call skynet_socket_close here (It will block mainloop)
		skynet_free(sm->buffer);
		skynet_free(sm);
	}
}

int 
skynet_socket_poll() {
	struct socket_server *ss = SOCKET_SERVER;
	assert(ss);
	struct socket_message result;
	int more = 1;
	int type = socket_server_poll(ss, &result, &more);
	switch (type) {
	case SOCKET_EXIT:
		return 0;
	case SOCKET_DATA:
		forward_message(SKYNET_SOCKET_TYPE_DATA, false, &result);
		break;
	case SOCKET_CLOSE:
		forward_message(SKYNET_SOCKET_TYPE_CLOSE, false, &result);
		break;
	case SOCKET_OPEN:
		forward_message(SKYNET_SOCKET_TYPE_CONNECT, true, &result);
		break;
	case SOCKET_ERR:
		forward_message(SKYNET_SOCKET_TYPE_ERROR, true, &result);
		break;
	case SOCKET_ACCEPT:
		forward_message(SKYNET_SOCKET_TYPE_ACCEPT, true, &result);
		break;
	case SOCKET_UDP:
		forward_message(SKYNET_SOCKET_TYPE_UDP, false, &result);
		break;
	case SOCKET_WARNING:
		forward_message(SKYNET_SOCKET_TYPE_WARNING, false, &result);
		break;
	default:
		skynet_error(NULL, "Unknown socket message type %d.",type);
		return -1;
	}
	if (more) {
		return -1;
	}
	return 1;
}

int
skynet_socket_sendbuffer(struct skynet_context *ctx, struct socket_sendbuffer *buffer) {
	return socket_server_send(SOCKET_SERVER, buffer);
}

int
skynet_socket_sendbuffer_lowpriority(struct skynet_context *ctx, struct socket_sendbuffer *buffer) {
	return socket_server_send_lowpriority(SOCKET_SERVER, buffer);
}

int 
skynet_socket_listen(struct skynet_context *ctx, const char *host, int port, int backlog) {
	uint32_t source = skynet_context_handle(ctx);
	return socket_server_listen(SOCKET_SERVER, source, host, port, backlog);
}

int 
skynet_socket_connect(struct skynet_context *ctx, const char *host, int port) {
	uint32_t source = skynet_context_handle(ctx);
	return socket_server_connect(SOCKET_SERVER, source, host, port);
}

int 
skynet_socket_bind(struct skynet_context *ctx, int fd) {
	uint32_t source = skynet_context_handle(ctx);
	return socket_server_bind(SOCKET_SERVER, source, fd);
}

void 
skynet_socket_close(struct skynet_context *ctx, int id) {
	uint32_t source = skynet_context_handle(ctx);
	socket_server_close(SOCKET_SERVER, source, id);
}

void 
skynet_socket_shutdown(struct skynet_context *ctx, int id) {
	uint32_t source = skynet_context_handle(ctx);
	socket_server_shutdown(SOCKET_SERVER, source, id);
}

void 
skynet_socket_start(struct skynet_context *ctx, int id) {
	uint32_t source = skynet_context_handle(ctx);
	socket_server_start(SOCKET_SERVER, source, id);
}

void
skynet_socket_pause(struct skynet_context *ctx, int id) {
	uint32_t source = skynet_context_handle(ctx);
	socket_server_pause(SOCKET_SERVER, source, id);
}


void
skynet_socket_nodelay(struct skynet_context *ctx, int id) {
	socket_server_nodelay(SOCKET_SERVER, id);
}

int 
skynet_socket_udp(struct skynet_context *ctx, const char * addr, int port) {
	uint32_t source = skynet_context_handle(ctx);
	return socket_server_udp(SOCKET_SERVER, source, addr, port);
}

int 
skynet_socket_udp_connect(struct skynet_context *ctx, int id, const char * addr, int port) {
	return socket_server_udp_connect(SOCKET_SERVER, id, addr, port);
}

int 
skynet_socket_udp_sendbuffer(struct skynet_context *ctx, const char * address, struct socket_sendbuffer *buffer) {
	return socket_server_udp_send(SOCKET_SERVER, (const struct socket_udp_address *)address, buffer);
}

const char *
skynet_socket_udp_address(struct skynet_socket_message *msg, int *addrsz) {
	if (msg->type != SKYNET_SOCKET_TYPE_UDP) {
		return NULL;
	}
	struct socket_message sm;
	sm.id = msg->id;
	sm.opaque = 0;
	sm.ud = msg->ud;
	sm.data = msg->buffer;
	return (const char *)socket_server_udp_address(SOCKET_SERVER, &sm, addrsz);
}

struct socket_info *
skynet_socket_info() {
	return socket_server_info(SOCKET_SERVER);
}

````

## Server/GameServer/framework/skynet-src/skynet_socket.h

SHA-256: `2dc8583a604cb95e7d189e64522c5027e11d637f77779aed766caada94eae097`

````c
#ifndef skynet_socket_h
#define skynet_socket_h

#include "socket_info.h"
#include "socket_buffer.h"

struct skynet_context;

#define SKYNET_SOCKET_TYPE_DATA 1
#define SKYNET_SOCKET_TYPE_CONNECT 2
#define SKYNET_SOCKET_TYPE_CLOSE 3
#define SKYNET_SOCKET_TYPE_ACCEPT 4
#define SKYNET_SOCKET_TYPE_ERROR 5
#define SKYNET_SOCKET_TYPE_UDP 6
#define SKYNET_SOCKET_TYPE_WARNING 7

struct skynet_socket_message {
	int type;
	int id;
	int ud;
	char * buffer;
};

void skynet_socket_init();
void skynet_socket_exit();
void skynet_socket_free();
int skynet_socket_poll();
void skynet_socket_updatetime();

int skynet_socket_sendbuffer(struct skynet_context *ctx, struct socket_sendbuffer *buffer);
int skynet_socket_sendbuffer_lowpriority(struct skynet_context *ctx, struct socket_sendbuffer *buffer);
int skynet_socket_listen(struct skynet_context *ctx, const char *host, int port, int backlog);
int skynet_socket_connect(struct skynet_context *ctx, const char *host, int port);
int skynet_socket_bind(struct skynet_context *ctx, int fd);
void skynet_socket_close(struct skynet_context *ctx, int id);
void skynet_socket_shutdown(struct skynet_context *ctx, int id);
void skynet_socket_start(struct skynet_context *ctx, int id);
void skynet_socket_pause(struct skynet_context *ctx, int id);
void skynet_socket_nodelay(struct skynet_context *ctx, int id);

int skynet_socket_udp(struct skynet_context *ctx, const char * addr, int port);
int skynet_socket_udp_connect(struct skynet_context *ctx, int id, const char * addr, int port);
int skynet_socket_udp_sendbuffer(struct skynet_context *ctx, const char * address, struct socket_sendbuffer *buffer);
const char * skynet_socket_udp_address(struct skynet_socket_message *, int *addrsz);

struct socket_info * skynet_socket_info();

// legacy APIs

static inline void sendbuffer_init_(struct socket_sendbuffer *buf, int id, const void *buffer, int sz) {
	buf->id = id;
	buf->buffer = buffer;
	if (sz < 0) {
		buf->type = SOCKET_BUFFER_OBJECT;
	} else {
		buf->type = SOCKET_BUFFER_MEMORY;
	}
	buf->sz = (size_t)sz;
}

static inline int skynet_socket_send(struct skynet_context *ctx, int id, void *buffer, int sz) {
	struct socket_sendbuffer tmp;
	sendbuffer_init_(&tmp, id, buffer, sz);
	return skynet_socket_sendbuffer(ctx, &tmp);
}

static inline int skynet_socket_send_lowpriority(struct skynet_context *ctx, int id, void *buffer, int sz) {
	struct socket_sendbuffer tmp;
	sendbuffer_init_(&tmp, id, buffer, sz);
	return skynet_socket_sendbuffer_lowpriority(ctx, &tmp);
}

static inline int skynet_socket_udp_send(struct skynet_context *ctx, int id, const char * address, const void *buffer, int sz) {
	struct socket_sendbuffer tmp;
	sendbuffer_init_(&tmp, id, buffer, sz);
	return skynet_socket_udp_sendbuffer(ctx, address, &tmp);
}

#endif

````

## Server/GameServer/framework/skynet-src/skynet_start.c

SHA-256: `5551b4343e3953346e677c74fd30ed24d06a6790b9c05b69af5878addaf50ca2`

````c
#include "skynet.h"
#include "skynet_server.h"
#include "skynet_imp.h"
#include "skynet_mq.h"
#include "skynet_handle.h"
#include "skynet_module.h"
#include "skynet_timer.h"
#include "skynet_monitor.h"
#include "skynet_socket.h"
#include "skynet_daemon.h"
#include "skynet_harbor.h"

#include <pthread.h>
#include <unistd.h>
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

struct monitor {
	int count;
	struct skynet_monitor ** m;
	pthread_cond_t cond;
	pthread_mutex_t mutex;
	int sleep;
	int quit;
};

struct worker_parm {
	struct monitor *m;
	int id;
	int weight;
};

static volatile int SIG = 0;

static void
handle_hup(int signal) {
	if (signal == SIGHUP) {
		SIG = 1;
	}
}

#define CHECK_ABORT if (skynet_context_total()==0) break;

static void
create_thread(pthread_t *thread, void *(*start_routine) (void *), void *arg) {
	if (pthread_create(thread,NULL, start_routine, arg)) {
		fprintf(stderr, "Create thread failed");
		exit(1);
	}
}

static void
wakeup(struct monitor *m, int busy) {
	if (m->sleep >= m->count - busy) {
		// signal sleep worker, "spurious wakeup" is harmless
		pthread_cond_signal(&m->cond);
	}
}

static void *
thread_socket(void *p) {
	struct monitor * m = p;
	skynet_initthread(THREAD_SOCKET);
	for (;;) {
		int r = skynet_socket_poll();
		if (r==0)
			break;
		if (r<0) {
			CHECK_ABORT
			continue;
		}
		wakeup(m,0);
	}
	return NULL;
}

static void
free_monitor(struct monitor *m) {
	int i;
	int n = m->count;
	for (i=0;i<n;i++) {
		skynet_monitor_delete(m->m[i]);
	}
	pthread_mutex_destroy(&m->mutex);
	pthread_cond_destroy(&m->cond);
	skynet_free(m->m);
	skynet_free(m);
}

static void *
thread_monitor(void *p) {
	struct monitor * m = p;
	int i;
	int n = m->count;
	skynet_initthread(THREAD_MONITOR);
	for (;;) {
		CHECK_ABORT
		for (i=0;i<n;i++) {
			skynet_monitor_check(m->m[i]);
		}
		for (i=0;i<5;i++) {
			CHECK_ABORT
			sleep(1);
		}
	}

	return NULL;
}

static void
signal_hup() {
	// make log file reopen

	struct skynet_message smsg;
	smsg.source = 0;
	smsg.session = 0;
	smsg.data = NULL;
	smsg.sz = (size_t)PTYPE_SYSTEM << MESSAGE_TYPE_SHIFT;
	uint32_t logger = skynet_handle_findname("logger");
	if (logger) {
		skynet_context_push(logger, &smsg);
	}
}

static void *
thread_timer(void *p) {
	struct monitor * m = p;
	skynet_initthread(THREAD_TIMER);
	for (;;) {
		skynet_updatetime();
		skynet_socket_updatetime();
		CHECK_ABORT
		wakeup(m,m->count-1);
		usleep(2500);
		if (SIG) {
			signal_hup();
			SIG = 0;
		}
	}
	// wakeup socket thread
	skynet_socket_exit();
	// wakeup all worker thread
	pthread_mutex_lock(&m->mutex);
	m->quit = 1;
	pthread_cond_broadcast(&m->cond);
	pthread_mutex_unlock(&m->mutex);
	return NULL;
}

static void *
thread_worker(void *p) {
	struct worker_parm *wp = p;
	int id = wp->id;
	int weight = wp->weight;
	struct monitor *m = wp->m;
	struct skynet_monitor *sm = m->m[id];
	skynet_initthread(THREAD_WORKER);
	struct message_queue * q = NULL;
	while (!m->quit) {
		q = skynet_context_message_dispatch(sm, q, weight);
		if (q == NULL) {
			if (pthread_mutex_lock(&m->mutex) == 0) {
				++ m->sleep;
				// "spurious wakeup" is harmless,
				// because skynet_context_message_dispatch() can be call at any time.
				if (!m->quit)
					pthread_cond_wait(&m->cond, &m->mutex);
				-- m->sleep;
				if (pthread_mutex_unlock(&m->mutex)) {
					fprintf(stderr, "unlock mutex error");
					exit(1);
				}
			}
		}
	}
	return NULL;
}

static void
start(int thread) {
	pthread_t pid[thread+3];

	struct monitor *m = skynet_malloc(sizeof(*m));
	memset(m, 0, sizeof(*m));
	m->count = thread;
	m->sleep = 0;

	m->m = skynet_malloc(thread * sizeof(struct skynet_monitor *));
	int i;
	for (i=0;i<thread;i++) {
		m->m[i] = skynet_monitor_new();
	}
	if (pthread_mutex_init(&m->mutex, NULL)) {
		fprintf(stderr, "Init mutex error");
		exit(1);
	}
	if (pthread_cond_init(&m->cond, NULL)) {
		fprintf(stderr, "Init cond error");
		exit(1);
	}

	create_thread(&pid[0], thread_monitor, m);
	create_thread(&pid[1], thread_timer, m);
	create_thread(&pid[2], thread_socket, m);

	static int weight[] = { 
		-1, -1, -1, -1, 0, 0, 0, 0,
		1, 1, 1, 1, 1, 1, 1, 1, 
		2, 2, 2, 2, 2, 2, 2, 2, 
		3, 3, 3, 3, 3, 3, 3, 3, };
	struct worker_parm wp[thread];
	for (i=0;i<thread;i++) {
		wp[i].m = m;
		wp[i].id = i;
		if (i < sizeof(weight)/sizeof(weight[0])) {
			wp[i].weight= weight[i];
		} else {
			wp[i].weight = 0;
		}
		create_thread(&pid[i+3], thread_worker, &wp[i]);
	}

	for (i=0;i<thread+3;i++) {
		pthread_join(pid[i], NULL); 
	}

	free_monitor(m);
}

static void
bootstrap(struct skynet_context * logger, const char * cmdline) {
	int sz = strlen(cmdline);
	char name[sz+1];
	char args[sz+1];
	sscanf(cmdline, "%s %s", name, args);
	struct skynet_context *ctx = skynet_context_new(name, args);
	if (ctx == NULL) {
		skynet_error(NULL, "Bootstrap error : %s\n", cmdline);
		skynet_context_dispatchall(logger);
		exit(1);
	}
}

void 
skynet_start(struct skynet_config * config) {
	// register SIGHUP for log file reopen
	struct sigaction sa;
	sa.sa_handler = &handle_hup;
	sa.sa_flags = SA_RESTART;
	sigfillset(&sa.sa_mask);
	sigaction(SIGHUP, &sa, NULL);

	if (config->daemon) {
		if (daemon_init(config->daemon)) {
			exit(1);
		}
	}
	skynet_harbor_init(config->harbor);
	skynet_handle_init(config->harbor);
	skynet_mq_init();
	skynet_module_init(config->module_path);
	skynet_timer_init();
	skynet_socket_init();
	skynet_profile_enable(config->profile);

	struct skynet_context *ctx = skynet_context_new(config->logservice, config->logger);
	if (ctx == NULL) {
		fprintf(stderr, "Can't launch %s service\n", config->logservice);
		exit(1);
	}

	skynet_handle_namehandle(skynet_context_handle(ctx), "logger");

	bootstrap(ctx, config->bootstrap);

	start(config->thread);

	// harbor_exit may call socket send, so it should exit before socket_free
	skynet_harbor_exit();
	skynet_socket_free();
	if (config->daemon) {
		daemon_exit(config->daemon);
	}
}

````

## Server/GameServer/framework/skynet-src/skynet_timer.c

SHA-256: `9307cfcdcbb5606706deb1a7101d49f2f95631050b1a79f1f49ed72098596af6`

````c
#include "skynet.h"

#include "skynet_timer.h"
#include "skynet_mq.h"
#include "skynet_server.h"
#include "skynet_handle.h"
#include "spinlock.h"

#include <time.h>
#include <assert.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

#if defined(__APPLE__)
#include <AvailabilityMacros.h>
#include <sys/time.h>
#include <mach/task.h>
#include <mach/mach.h>
#endif

typedef void (*timer_execute_func)(void *ud,void *arg);

#define TIME_NEAR_SHIFT 8
#define TIME_NEAR (1 << TIME_NEAR_SHIFT)
#define TIME_LEVEL_SHIFT 6
#define TIME_LEVEL (1 << TIME_LEVEL_SHIFT)
#define TIME_NEAR_MASK (TIME_NEAR-1)
#define TIME_LEVEL_MASK (TIME_LEVEL-1)

struct timer_event {
	uint32_t handle;
	int session;
};

struct timer_node {
	struct timer_node *next;
	uint32_t expire;
};

struct link_list {
	struct timer_node head;
	struct timer_node *tail;
};

struct timer {
	struct link_list near[TIME_NEAR];
	struct link_list t[4][TIME_LEVEL];
	struct spinlock lock;
	uint32_t time;
	uint32_t starttime;
	uint64_t current;
	uint64_t current_point;
};

static struct timer * TI = NULL;

static inline struct timer_node *
link_clear(struct link_list *list) {
	struct timer_node * ret = list->head.next;
	list->head.next = 0;
	list->tail = &(list->head);

	return ret;
}

static inline void
link(struct link_list *list,struct timer_node *node) {
	list->tail->next = node;
	list->tail = node;
	node->next=0;
}

static void
add_node(struct timer *T,struct timer_node *node) {
	uint32_t time=node->expire;
	uint32_t current_time=T->time;
	
	if ((time|TIME_NEAR_MASK)==(current_time|TIME_NEAR_MASK)) {
		link(&T->near[time&TIME_NEAR_MASK],node);
	} else {
		int i;
		uint32_t mask=TIME_NEAR << TIME_LEVEL_SHIFT;
		for (i=0;i<3;i++) {
			if ((time|(mask-1))==(current_time|(mask-1))) {
				break;
			}
			mask <<= TIME_LEVEL_SHIFT;
		}

		link(&T->t[i][((time>>(TIME_NEAR_SHIFT + i*TIME_LEVEL_SHIFT)) & TIME_LEVEL_MASK)],node);	
	}
}

static void
timer_add(struct timer *T,void *arg,size_t sz,int time) {
	struct timer_node *node = (struct timer_node *)skynet_malloc(sizeof(*node)+sz);
	memcpy(node+1,arg,sz);

	SPIN_LOCK(T);

		node->expire=time+T->time;
		add_node(T,node);

	SPIN_UNLOCK(T);
}

static void
move_list(struct timer *T, int level, int idx) {
	struct timer_node *current = link_clear(&T->t[level][idx]);
	while (current) {
		struct timer_node *temp=current->next;
		add_node(T,current);
		current=temp;
	}
}

static void
timer_shift(struct timer *T) {
	int mask = TIME_NEAR;
	uint32_t ct = ++T->time;
	if (ct == 0) {
		move_list(T, 3, 0);
	} else {
		uint32_t time = ct >> TIME_NEAR_SHIFT;
		int i=0;

		while ((ct & (mask-1))==0) {
			int idx=time & TIME_LEVEL_MASK;
			if (idx!=0) {
				move_list(T, i, idx);
				break;				
			}
			mask <<= TIME_LEVEL_SHIFT;
			time >>= TIME_LEVEL_SHIFT;
			++i;
		}
	}
}

static inline void
dispatch_list(struct timer_node *current) {
	do {
		struct timer_event * event = (struct timer_event *)(current+1);
		struct skynet_message message;
		message.source = 0;
		message.session = event->session;
		message.data = NULL;
		message.sz = (size_t)PTYPE_RESPONSE << MESSAGE_TYPE_SHIFT;

		skynet_context_push(event->handle, &message);
		
		struct timer_node * temp = current;
		current=current->next;
		skynet_free(temp);	
	} while (current);
}

static inline void
timer_execute(struct timer *T) {
	int idx = T->time & TIME_NEAR_MASK;
	
	while (T->near[idx].head.next) {
		struct timer_node *current = link_clear(&T->near[idx]);
		SPIN_UNLOCK(T);
		// dispatch_list don't need lock T
		dispatch_list(current);
		SPIN_LOCK(T);
	}
}

static void 
timer_update(struct timer *T) {
	SPIN_LOCK(T);

	// try to dispatch timeout 0 (rare condition)
	timer_execute(T);

	// shift time first, and then dispatch timer message
	timer_shift(T);

	timer_execute(T);

	SPIN_UNLOCK(T);
}

static struct timer *
timer_create_timer() {
	struct timer *r=(struct timer *)skynet_malloc(sizeof(struct timer));
	memset(r,0,sizeof(*r));

	int i,j;

	for (i=0;i<TIME_NEAR;i++) {
		link_clear(&r->near[i]);
	}

	for (i=0;i<4;i++) {
		for (j=0;j<TIME_LEVEL;j++) {
			link_clear(&r->t[i][j]);
		}
	}

	SPIN_INIT(r)

	r->current = 0;

	return r;
}

int
skynet_timeout(uint32_t handle, int time, int session) {
	if (time <= 0) {
		struct skynet_message message;
		message.source = 0;
		message.session = session;
		message.data = NULL;
		message.sz = (size_t)PTYPE_RESPONSE << MESSAGE_TYPE_SHIFT;

		if (skynet_context_push(handle, &message)) {
			return -1;
		}
	} else {
		struct timer_event event;
		event.handle = handle;
		event.session = session;
		timer_add(TI, &event, sizeof(event), time);
	}

	return session;
}

// centisecond: 1/100 second
static void
systime(uint32_t *sec, uint32_t *cs) {
#if !defined(__APPLE__) || defined(AVAILABLE_MAC_OS_X_VERSION_10_12_AND_LATER)
	struct timespec ti;
	clock_gettime(CLOCK_REALTIME, &ti);
	*sec = (uint32_t)ti.tv_sec;
	*cs = (uint32_t)(ti.tv_nsec / 10000000);
#else
	struct timeval tv;
	gettimeofday(&tv, NULL);
	*sec = tv.tv_sec;
	*cs = tv.tv_usec / 10000;
#endif
}

static uint64_t
gettime() {
	uint64_t t;
#if !defined(__APPLE__) || defined(AVAILABLE_MAC_OS_X_VERSION_10_12_AND_LATER)
	struct timespec ti;
	clock_gettime(CLOCK_MONOTONIC, &ti);
	t = (uint64_t)ti.tv_sec * 100;
	t += ti.tv_nsec / 10000000;
#else
	struct timeval tv;
	gettimeofday(&tv, NULL);
	t = (uint64_t)tv.tv_sec * 100;
	t += tv.tv_usec / 10000;
#endif
	return t;
}

void
skynet_updatetime(void) {
	uint64_t cp = gettime();
	if(cp < TI->current_point) {
		skynet_error(NULL, "time diff error: change from %lld to %lld", cp, TI->current_point);
		TI->current_point = cp;
	} else if (cp != TI->current_point) {
		uint32_t diff = (uint32_t)(cp - TI->current_point);
		TI->current_point = cp;
		TI->current += diff;
		int i;
		for (i=0;i<diff;i++) {
			timer_update(TI);
		}
	}
}

uint32_t
skynet_starttime(void) {
	return TI->starttime;
}

uint64_t 
skynet_now(void) {
	return TI->current;
}

void 
skynet_timer_init(void) {
	TI = timer_create_timer();
	uint32_t current = 0;
	systime(&TI->starttime, &current);
	TI->current = current;
	TI->current_point = gettime();
}

// for profile

#define NANOSEC 1000000000
#define MICROSEC 1000000

uint64_t
skynet_thread_time(void) {
#if  !defined(__APPLE__) || defined(AVAILABLE_MAC_OS_X_VERSION_10_12_AND_LATER)
	struct timespec ti;
	clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ti);

	return (uint64_t)ti.tv_sec * MICROSEC + (uint64_t)ti.tv_nsec / (NANOSEC / MICROSEC);
#else
	struct task_thread_times_info aTaskInfo;
	mach_msg_type_number_t aTaskInfoCount = TASK_THREAD_TIMES_INFO_COUNT;
	if (KERN_SUCCESS != task_info(mach_task_self(), TASK_THREAD_TIMES_INFO, (task_info_t )&aTaskInfo, &aTaskInfoCount)) {
		return 0;
	}

	return (uint64_t)(aTaskInfo.user_time.seconds) + (uint64_t)aTaskInfo.user_time.microseconds;
#endif
}

````

## Server/GameServer/framework/skynet-src/skynet_timer.h

SHA-256: `6ed1e209893bf3d479c864ad980564980d48b67a6ab69af6cd623300ba41c708`

````c
#ifndef SKYNET_TIMER_H
#define SKYNET_TIMER_H

#include <stdint.h>

int skynet_timeout(uint32_t handle, int time, int session);
void skynet_updatetime(void);
uint32_t skynet_starttime(void);
uint64_t skynet_thread_time(void);	// for profile, in micro second

void skynet_timer_init(void);

#endif

````

## Server/GameServer/lualib-src/lunitynav.cc

SHA-256: `07fa3d46e40e4a68e1e07945326fee1dadb6abc75424a7a135febfe2e431afb5`

````cpp
// Portable Lua binding to the existing clean-room PathLib/CysNavMesh reader.
// The old grid-only map reader cannot parse the published triangle .path images.
#include "CysNavMesh.h"
#include <cmath>
#include <vector>
extern "C" {
#include "lua.h"
#include "lauxlib.h"
}
static const char* META="dragon_unity_nav";
static cys::NavMesh* self(lua_State* L){auto p=(cys::NavMesh**)luaL_checkudata(L,1,META);luaL_argcheck(L,*p!=nullptr,1,"closed navmesh");return *p;}
static cys::NavPoint point(lua_State* L,int index){
    luaL_checktype(L,index,LUA_TTABLE);lua_getfield(L,index,"x");double x=luaL_checknumber(L,-1);lua_pop(L,1);lua_getfield(L,index,"y");double z=luaL_checknumber(L,-1);lua_pop(L,1);
    luaL_argcheck(L,std::isfinite(x)&&std::isfinite(z)&&std::fabs(x)<1e7&&std::fabs(z)<1e7,index,"invalid nav coordinate");return {(float)x,(float)z};
}
static int create(lua_State* L){auto p=(cys::NavMesh**)lua_newuserdata(L,sizeof(cys::NavMesh*));*p=new cys::NavMesh();luaL_setmetatable(L,META);return 1;}
static int close(lua_State* L){auto p=(cys::NavMesh**)luaL_checkudata(L,1,META);delete *p;*p=nullptr;return 0;}
static int load(lua_State* L){auto nav=self(L);bool ok=nav->LoadFromFile(luaL_checkstring(L,2));ok=ok&&nav->Stats().points>=3&&nav->Stats().tris>0;if(!ok)nav->Unload();lua_pushboolean(L,ok);return 1;}
static int walkable(lua_State* L){auto nav=self(L);auto p=point(L,2);lua_pushboolean(L,nav->IsWalkable(p.x,p.z));return 1;}
static int visible(lua_State* L){auto nav=self(L);auto a=point(L,2),b=point(L,3);lua_pushboolean(L,nav->LineOfSight(a,b));return 1;}
static void push(lua_State* L,const cys::NavPoint& p){lua_newtable(L);lua_pushnumber(L,p.x);lua_setfield(L,-2,"x");lua_pushnumber(L,p.z);lua_setfield(L,-2,"y");}
static int findpath(lua_State* L){auto nav=self(L);auto a=point(L,2),b=point(L,3);std::vector<cys::NavPoint> points;nav->FindPath(a,b,points);lua_newtable(L);int index=1;for(const auto& p:points){push(L,p);lua_rawseti(L,-2,index++);}return 1;}
static int empty(lua_State* L){auto nav=self(L);auto p=point(L,2);if(nav->IsWalkable(p.x,p.z)){push(L,p);return 1;}
    for(int radius=1;radius<=8;++radius)for(int x=-radius;x<=radius;++x)for(int z=-radius;z<=radius;++z){
        if(std::abs(x)!=radius&&std::abs(z)!=radius)continue;cys::NavPoint candidate={p.x+x*.5f,p.z+z*.5f};if(nav->IsWalkable(candidate.x,candidate.z)){push(L,candidate);return 1;}}
    lua_pushnil(L);return 1;
}
extern "C" int luaopen_unitynav(lua_State* L){
    luaL_newmetatable(L,META);luaL_Reg methods[]={{"__gc",close},{"load",load},{"walkable",walkable},{"lineofsight",visible},{"findpath",findpath},{"findempty",empty},{nullptr,nullptr}};luaL_setfuncs(L,methods,0);lua_pushvalue(L,-1);lua_setfield(L,-2,"__index");lua_pop(L,1);
    luaL_Reg functions[]={{"new",create},{nullptr,nullptr}};luaL_newlib(L,functions);return 1;
}

````

## Server/GameServer/lualib-src/profile/profile.c

SHA-256: `7c9963a1038d9575bc6b0f46b2f027f5dcb95cb9e69c1c2131648f97079dbcb8`

````c
#include "profile.h"
#include "imap.h"
#include "icallpath.h"
#include "lobject.h"
#include "lstate.h"
#include <pthread.h>

// #include <google/profiler.h>

#define MAX_CALL_SIZE               1024
#define MAX_CO_SIZE                 1024
#define NANOSEC                     1000000000
#define MICROSEC                    1000000

#if defined(USE_RDTSC) && (defined(__i386__) || defined(__x86_64__))
    #include "rdtsc.h"
    static inline uint64_t
    gettime() {
        return rdtsc();
    }

    static inline double
    realtime(uint64_t t) {
        return (double) t / (2000000000);
    }
#else
    static inline uint64_t
    gettime() {
        struct timespec ti;
        clock_gettime(CLOCK_MONOTONIC, &ti);
        return (uint64_t)ti.tv_sec * NANOSEC + (uint64_t)ti.tv_nsec;
    }

    static inline double
    realtime(uint64_t t) {
        return (double)t / NANOSEC;
    }
#endif


struct callpath_node;
struct call_frame {
    const void* point;
    const void* prototype;
    struct icallpath_context*   path;
    bool  tail;
    uint64_t call_time;
    uint64_t ret_time;
    uint64_t sub_cost;
    uint64_t real_cost;
    uint64_t alloc_co_cost;
    uint64_t alloc_start;
};

struct call_state {
    lua_State*  co;
    uint64_t    leave_time;
    uint64_t    leave_alloc;
    int         top;
    struct call_frame   call_list[0];
};

struct profile_context {
    uint64_t    start;
    bool        increment_alloc_count;
    uint64_t    alloc_count;
    lua_Alloc   last_alloc_f;
    void*       last_alloc_ud;
    struct imap_context*        cs_map;
    struct icallpath_context*   callpath;
    struct call_state*          cur_cs;
};

struct callpath_node {
    struct callpath_node*   parent;
    const void* point;
    const char* source;
    const char* name;
    int     line;
    int     depth;
    uint64_t ret_time;
    uint64_t count;
    uint64_t record_time;
    uint64_t alloc_count;
};

static struct callpath_node*
callpath_node_create() {
    struct callpath_node* node = (struct callpath_node*)pmalloc(sizeof(*node));
    node->parent = NULL;
    node->point = NULL;
    node->source = NULL;
    node->name = NULL;
    node->line = 0;
    node->depth = 0;
    node->ret_time = 0;
    node->count = 0;
    node->record_time = 0;
    node->alloc_count = 0;
    return node;
}

static struct profile_context *
profile_create() {
    struct profile_context* context = (struct profile_context*)pmalloc(sizeof(*context));
    
    context->start = 0;
    context->cs_map = imap_create();
    context->callpath = NULL;
    context->cur_cs = NULL;
    context->increment_alloc_count = false;
    context->alloc_count = 0;
    context->last_alloc_f = NULL;
    context->last_alloc_ud = NULL;
    return context;
}

static void
_ob_free_call_state(uint64_t key, void* value, void* ud) {
    pfree(value);
}
static void
profile_free(struct profile_context* context) {
    if (context->callpath) {
        icallpath_free(context->callpath);
        context->callpath = NULL;
    }

    imap_dump(context->cs_map, _ob_free_call_state, NULL);
    imap_free(context->cs_map);
    pfree(context);
}


static inline struct call_frame *
push_callframe(struct call_state* cs) {
    if(cs->top >= MAX_CALL_SIZE) {
        assert(false);
    }
    return &cs->call_list[cs->top++];
}

static inline struct call_frame *
pop_callframe(struct call_state* cs) {
    if(cs->top<=0) {
        assert(false);
    }
    return &cs->call_list[--cs->top];
}

static inline struct call_frame *
cur_callframe(struct call_state* cs) {
    if(cs->top<=0) {
        return NULL;
    }

    uint64_t idx = cs->top-1;
    return &cs->call_list[idx];
}

struct snlua {
    struct profile_context * context;
};

static inline struct profile_context *
_get_profile(lua_State* L) {
    void *ud = NULL;
    lua_getallocf(L, &ud);
    return ((struct snlua*)(ud))->context;
}

static struct icallpath_context*
get_frame_path(struct profile_context* context, lua_State* co, lua_Debug* far, struct icallpath_context* pre_callpath, struct call_frame* frame) {
    if (!context->callpath) {
        struct callpath_node* node = callpath_node_create();
        node->name = "total";
        node->source = node->name;
        context->callpath = icallpath_create(0, node);
    }
    struct icallpath_context* path = pre_callpath;
    if (!path) {
        path = context->callpath;
    }

    struct call_frame* cur_cf = frame;
    uint64_t k = (uint64_t)((uintptr_t)cur_cf->prototype);
    struct icallpath_context* child_path = icallpath_get_child(path, k);
    if (!child_path) {
        struct callpath_node* path_parent = (struct callpath_node*)icallpath_getvalue(path);
        struct callpath_node* node = callpath_node_create();

        node->parent = path_parent;
        node->point = cur_cf->prototype;
        node->depth = path_parent->depth + 1;
        node->ret_time = 0;
        node->record_time = 0;
        node->count = 0;
        node->alloc_count = 0;
        child_path = icallpath_add_child(path, k, node);
    }
    path = child_path;

    struct callpath_node* cur_node = (struct callpath_node*)icallpath_getvalue(path);
    if (cur_node->name == NULL) {
        const char* name = NULL;
        #ifdef USE_EXPORT_NAME
            lua_getinfo(co, "nSl", far);
            name = far->name;
        #else
            lua_getinfo(co, "Sl", far);
        #endif
        int line = far->linedefined;
        const char* source = far->source;
        char flag = far->what[0];
        if (flag == 'C') {
            lua_Debug ar2;
            int i=0;
            int ret = 0;
            do {
                i++;
                ret = lua_getstack(co, i, &ar2);
                flag = 'C';
                if(ret) {
                    lua_getinfo(co, "Sl", &ar2);
                    if(ar2.what[0] != 'C') {
                        line = ar2.currentline;
                        source = ar2.source;
                        break;
                    }
                }
            }while(ret);
        }

        cur_node->name = name ? name : "null";
        cur_node->source = source ? source : "null";
        cur_node->line = line;
    }
    
    return path;
}

static void*
_resolve_alloc(void *ud, void *ptr, size_t osize, size_t nsize) {
    struct profile_context* context = ((struct snlua*)ud)->context;
    size_t old = ptr == NULL ? 0 : osize;
    if (nsize > 0 && nsize > old && context->increment_alloc_count) {
        context->alloc_count += (nsize - old);
    }

    void* p = context->last_alloc_f(context->last_alloc_ud, ptr, osize, nsize);
    return p;
}

static void
_resolve_hook(lua_State* L, lua_Debug* far) {
    struct profile_context* context = _get_profile(L);
    if(context->start == 0) {
        return;
    }

    uint64_t cur_time = gettime();
    context->increment_alloc_count = false;
    int event = far->event;
    struct call_state* cs = context->cur_cs;
    if (!context->cur_cs || context->cur_cs->co != L) {
        uint64_t key = (uint64_t)((uintptr_t)L);
        cs = imap_query(context->cs_map, key);
        if (cs == NULL) {
            cs = (struct call_state*)pmalloc(sizeof(struct call_state) + sizeof(struct call_frame)*MAX_CALL_SIZE);
            cs->co = L; 
            cs->top = 0;
            cs->leave_time = 0;
            cs->leave_alloc = 0;
            imap_set(context->cs_map, key, cs);
        }

        if (context->cur_cs) {
            context->cur_cs->leave_time = cur_time;
            context->cur_cs->leave_alloc = context->alloc_count;
        }
        context->cur_cs = cs;
    }
    if (cs->leave_time > 0) {
        assert(cur_time >= cs->leave_time);
        uint64_t co_cost = cur_time - cs->leave_time;
        uint64_t co_alloc = context->alloc_count - cs->leave_alloc;

        int i = 0;
        for (; i < cs->top; i++) {
            cs->call_list[i].sub_cost += co_cost;
            cs->call_list[i].alloc_co_cost += co_alloc;
        }
        cs->leave_time = 0;
        cs->leave_alloc = 0;
    }
    assert(cs->co == L);

    if (event == LUA_HOOKCALL || event == LUA_HOOKTAILCALL) {
        const void* point = NULL;
        if (far->i_ci && far->i_ci->func) {
            point = far->i_ci->func;
        } else {
            lua_getinfo(L, "f", far);
            point = lua_topointer(L, -1);
        }

        struct icallpath_context* pre_callpath = NULL;
        struct call_frame* pre_frame = cur_callframe(cs);
        if (pre_frame) {
            pre_callpath = pre_frame->path;
        }

        struct call_frame* frame = push_callframe(cs);
        frame->point = point;
        frame->tail = event == LUA_HOOKTAILCALL;
        frame->sub_cost = 0;
        frame->call_time = cur_time;
        frame->alloc_co_cost = 0;
        frame->alloc_start = context->alloc_count;
        frame->prototype = point;
        if (far->i_ci && ttisclosure(s2v(far->i_ci->func))) {
            Closure *cl = clvalue(s2v(far->i_ci->func));
            if (cl && cl->c.tt == LUA_VLCL) {
                frame->prototype = cl->l.p;
            }
        }
        frame->path = get_frame_path(context, L, far, pre_callpath, frame);
    } else if (event == LUA_HOOKRET) {
        int len = cs->top;
        if (len <= 0) {
            context->increment_alloc_count = true;
            return;
        }
        bool tail_call = false;
        do {
            struct call_frame* cur_frame = pop_callframe(cs);
            struct callpath_node* cur_path = (struct callpath_node*)icallpath_getvalue(cur_frame->path);
            uint64_t total_cost = cur_time - cur_frame->call_time;
            uint64_t real_cost = total_cost - cur_frame->sub_cost;
            uint64_t alloc_count = context->alloc_count - cur_frame->alloc_start - cur_frame->alloc_co_cost;
            assert(context->alloc_count >= (cur_frame->alloc_start + cur_frame->alloc_co_cost));
            assert(cur_time >= cur_frame->call_time && total_cost >= cur_frame->sub_cost);
            cur_frame->ret_time = cur_time;
            cur_frame->real_cost = real_cost;

            cur_path->ret_time = cur_path->ret_time == 0 ? cur_time : cur_path->ret_time;
            cur_path->record_time += real_cost;
            cur_path->count++;
            cur_path->alloc_count += alloc_count;

            struct call_frame* pre_frame = cur_callframe(cs);
            tail_call = pre_frame ? cur_frame->tail : false;
        }while(tail_call);
    }

    context->increment_alloc_count = true;
}


struct dump_call_path_arg {
    lua_State* L;
    uint64_t record_time;
    uint64_t count;
    uint64_t index;
    uint64_t alloc_count;
};

static void _dump_call_path(struct icallpath_context* path, struct dump_call_path_arg* arg);
static void _dump_call_path_child(uint64_t key, void* value, void* ud) {
    struct dump_call_path_arg* arg = (struct dump_call_path_arg*)ud;
    _dump_call_path((struct icallpath_context*)value, arg);
    lua_seti(arg->L, -2, ++arg->index);
}
static void _dump_call_path(struct icallpath_context* path, struct dump_call_path_arg* arg) {
    lua_checkstack(arg->L, 3);
    lua_newtable(arg->L);

    struct dump_call_path_arg child_arg;
    child_arg.L = arg->L;
    child_arg.record_time = 0;
    child_arg.count = 0;
    child_arg.index = 0;
    child_arg.alloc_count = 0;

    if (icallpath_children_size(path) > 0) {
        lua_newtable(arg->L);
        icallpath_dump_children(path, _dump_call_path_child, &child_arg);
        lua_setfield(arg->L, -2, "children");
    }

    struct callpath_node* node = (struct callpath_node*)icallpath_getvalue(path);
    uint64_t alloc_count = node->alloc_count > child_arg.alloc_count ? node->alloc_count : child_arg.alloc_count;
    uint64_t count = node->count > child_arg.count ? node->count : child_arg.count;
    uint64_t rt = realtime(node->record_time) * MICROSEC;
    uint64_t record_time = rt > child_arg.record_time ? rt : child_arg.record_time;

    arg->record_time += record_time;
    arg->count += count;
    arg->alloc_count += alloc_count;

    char name[512] = {0};
    snprintf(name, sizeof(name)-1, "%s %s:%d", node->name ? node->name : "", node->source ? node->source : "", node->line);
    lua_pushstring(arg->L, name);
    lua_setfield(arg->L, -2, "name");

    lua_pushinteger(arg->L, count);
    lua_setfield(arg->L, -2, "count");

    lua_pushinteger(arg->L, record_time);
    lua_setfield(arg->L, -2, "value");

    lua_pushinteger(arg->L, node->ret_time);
    lua_setfield(arg->L, -2, "rettime");

    lua_pushinteger(arg->L, alloc_count);
    lua_setfield(arg->L, -2, "alloc_count");
}
static void dump_call_path(lua_State* L, struct icallpath_context* path) {
    struct dump_call_path_arg arg;
    arg.L = L;
    arg.record_time = 0;
    arg.count = 0;
    arg.index = 0;
    arg.alloc_count = 0;
    _dump_call_path(path, &arg);
}


static int 
get_all_coroutines(lua_State* L, lua_State** result, int maxsize) {
    int i = 0;
    struct global_State* lG = L->l_G;
    result[i++] = lG->mainthread;

    struct GCObject* obj = lG->allgc;
    while (obj && i < maxsize) {
        if (obj->tt == LUA_TTHREAD) {
            result[i++] = gco2th(obj);
        }
        obj = obj->next;
    }
    return i;
}

static int
_lstart(lua_State* L) {
    struct profile_context* context = _get_profile(L);
    if (context) {
        return 0;
    }
    // ProfilerStart("my.prof");
    // init registry
    context = profile_create();

    context->start = gettime();
    context->last_alloc_f = lua_getallocf(L, &context->last_alloc_ud);
    ((struct snlua*)(context->last_alloc_ud))->context = context;
    lua_setallocf(L, _resolve_alloc, context->last_alloc_ud);

    lua_State* states[MAX_CO_SIZE] = {0};
    int i = get_all_coroutines(L, states, MAX_CO_SIZE);
    for (i = i - 1; i >= 0; i--) {
        lua_sethook(states[i], _resolve_hook, LUA_MASKCALL | LUA_MASKRET, 0);
    }
    context->increment_alloc_count = true;
    return 0;
}

static int
_lstop(lua_State* L) {
    struct profile_context* context = _get_profile(L);
    if (!context) {
        return 0;
    }
    context->increment_alloc_count = false;
    //ProfilerStop();

    void* current_ud = NULL;
    lua_getallocf(L, &current_ud);
     ((struct snlua*)(current_ud))->context = NULL;
    lua_setallocf(L, context->last_alloc_f, context->last_alloc_ud);

    lua_State* states[MAX_CO_SIZE] = {0};
    int i = get_all_coroutines(L, states, MAX_CO_SIZE);
    for (i = i - 1; i >= 0; i--) {
        lua_sethook(states[i], NULL, 0, 0);
    }
    profile_free(context);
    return 0;
}

static int
_lmark(lua_State* L) {
    struct profile_context* context = _get_profile(L);
    if (!context) {
        return 0;
    }
    lua_State* co = lua_tothread(L, 1);
    if(co == NULL) {
        co = L;
    }
    if(context->start != 0) {
        lua_sethook(co, _resolve_hook, LUA_MASKCALL | LUA_MASKRET, 0);
    }
    lua_pushboolean(L, context->start != 0);
    return 1;
}

static int
_lunmark(lua_State* L) {
    struct profile_context* context = _get_profile(L);
    if (!context) {
        return 0;
    }
    lua_State* co = lua_tothread(L, 1);
    if(co == NULL) {
        co = L;
    }
    lua_sethook(co, NULL, 0, 0);
    return 0;
}

static int
_ldump(lua_State* L) {
    struct profile_context* context = _get_profile(L);
    if (context && context->callpath) {
        context->increment_alloc_count = false;
        uint64_t record_time = realtime(gettime() - context->start) * MICROSEC;
        lua_pushinteger(L, record_time);
        dump_call_path(L, context->callpath);
        context->increment_alloc_count = true;
        return 2;
    }
    return 0;
}

int
luaopen_lprofile_c(lua_State* L) {
    luaL_checkversion(L);
     luaL_Reg l[] = {
        {"start", _lstart},
        {"stop", _lstop},
        {"mark", _lmark},
        {"unmark", _lunmark},
        {"dump", _ldump},
        {NULL, NULL},
    };
    luaL_newlib(L, l);
    return 1;
}
````

## Server/GameServer/lualib/unity_combat.lua

SHA-256: `44f03845024dbd01f6906a44e66b79f838ceb55adc031b9fba7515b109bfdded`

````lua
-- Authoritative development PvE adapter. Reuses source basic physical formulas/stats/nav;
-- does not claim the full TLBB skill/equipment/impact/mission systems are connected.
local json=require 'cjson'
local legacy=require 'unity_legacy_combat'
local M={}
local function read_json(path)
    local file=io.open(path,'rb');if not file then return nil end
    local raw=file:read('*a');file:close();local ok,data=pcall(json.decode,raw);if ok then return data end
end
local function finite(v)return type(v)=='number' and v==v and v~=math.huge and v~=-math.huge end
local function distance(a,b)local dx,dz=a.x-b.x,a.z-b.z;return math.sqrt(dx*dx+dz*dz)end
local function actor(stats,kind)
    return {stats=stats,get_attack_physics=function(self)return self.stats.attack end,
        get_defence_physics=function(self)return self.stats.defence end,
        get_obj_type=function()return kind end,get_skill_info=function()return nil end,item_value=function()return 0 end}
end
function M.new(world_provider,opts)
    opts=opts or {};local skynet=require 'skynet'
    local now=opts.now or function()return skynet.now()*10 end
    local roll=opts.random or math.random
    local root=world_provider.data_root()
    local data=root and read_json(root..'/combat-data.json')
    local sessions,worlds,order={},{},{}
    local engine={}
    local function event(world,kind,fields)
        world.sequence=world.sequence+1;fields.kind=kind;fields.sequence=world.sequence;fields.time=now()
        world.events[#world.events+1]=fields
        if #world.events>128 then table.remove(world.events,1)end
    end
    local function height(world,x,z)
        local w,d=world.source.width,world.source.depth
        x=math.max(0,math.min(w,x));z=math.max(0,math.min(d,z))
        local ix,iz=math.min(math.floor(x),w-1),math.min(math.floor(z),d-1)
        local u,v=x-ix,z-iz
        local function sample(a,b)return string.unpack('<f',world.heights,((b*(w+1)+a)*4)+1)end
        local a,b,c,e=sample(ix,iz),sample(ix+1,iz),sample(ix,iz+1),sample(ix+1,iz+1)
        if (world.flags:byte(iz*w+ix+1)&1)~=0 then
            if v<=u then return a+(b-a)*u+(e-b)*v else return a+(e-c)*u+(c-a)*v end
        end
        if u+v<=1 then return a+(b-a)*u+(c-a)*v end
        return e+(c-e)*(1-u)+(b-e)*(1-v)
    end
    local function valid(world,x,z)
        return finite(x) and finite(z) and x>=0 and z>=0 and x<world.source.width and z<world.source.depth
    end
    local function route(world,a,b)
        if not valid(world,a.x,a.z) or not valid(world,b.x,b.z)then return nil end
        if not world.nav:walkable({x=a.x,y=a.z}) or not world.nav:walkable({x=b.x,y=b.z})then return nil end
        if distance(a,b)<.01 then return {} end
        local nodes=world.nav:findpath({x=a.x,y=a.z},{x=b.x,y=b.z})
        if not nodes or #nodes==0 then return nil end
        return nodes
    end
    local function load_world(id)
        if worlds[id]then return worlds[id]end
        local source=world_provider.get_world(id)
        if not source then return nil,'WORLD_NOT_FOUND' end
        if not source.combatNavigationAvailable or not source.navFile then return nil,'COMBAT_NAV_UNAVAILABLE' end
        if #order>=4 then
            local evict
            for i,key in ipairs(order)do if next(worlds[key].players)==nil then evict=i;break end end
            if not evict then return nil,'COMBAT_WORLD_CAPACITY' end
            worlds[table.remove(order,evict)]=nil
        end
        local nav=(opts.nav_factory or function()return require('unitynav').new()end)()
        if not nav:load(root..'/'..source.navFile)then return nil,'COMBAT_NAV_UNAVAILABLE' end
        local function binary(suffix)
            local file=io.open(root..'/'..string.format('%d',id)..suffix,'rb');if not file then return nil end
            local result=file:read('*a');file:close();return result
        end
        local heights,flags=binary('.heights.bytes'),binary('.cells.bytes')
        if not heights or #heights~=(source.width+1)*(source.depth+1)*4 or not flags or #flags~=source.width*source.depth then return nil,'COMBAT_TERRAIN_UNAVAILABLE' end
        local world={source=source,nav=nav,heights=heights,flags=flags,mobs={},players={},events={},sequence=0,lastTick=now()}
        for _,spawn in ipairs(source.entities)do
            local stats=data.templates[string.format('%d',spawn.templateId)]
            if stats then
                local mob=actor(stats,'monster');mob.id=spawn.id;mob.spawn=spawn;mob.hp=stats.hp;mob.maxHp=stats.hp
                mob.x,mob.y,mob.z=spawn.x,spawn.y,spawn.z;mob.action='idle';mob.cooldown=0;mob.yaw=spawn.yaw or 0
                mob.hostile=spawn.kind=='monster' and not stats.isNpc and (spawn.aiType==1 or spawn.aiType==2) and stats.hp>0
                world.mobs[mob.id]=mob
            end
        end
        worlds[id]=world;order[#order+1]=id;return world
    end
    local function attack(world,sender,target)
        local t=now();sender.yaw=math.deg(math.atan(target.x-sender.x,target.z-sender.z));sender.cooldown=t+math.max(100,sender.stats.cooldownMilliseconds)
        sender.action='attack';sender.actionUntil=t+math.max(100,sender.stats.actionMilliseconds or 500)
        local accuracy=legacy:calculate_hit_rate(sender.stats.hit,target.stats.miss)
        local hit=legacy:is_hit(accuracy,roll(100));local damage=0;local critical=false
        if hit then
            local trait=sender.stats.traitId and data.physicalTraits[string.format('%d',sender.stats.traitId)] or 1000000
            if not trait then return nil,'COMBAT_TRAIT_UNAVAILABLE' end
            damage=legacy:physical_damage(sender,target,0,0,{[0]=trait})
            -- Original configs:get_fluctuation = 1.2; same random expression as combat_core.
            damage=damage*(1+(2*1.2*(50-roll(100))/100)/100)
            critical=legacy:is_critical_hit(legacy:calculate_critical_rate(sender.stats.critical,target.stats.criticalDefence),roll(100))
            if critical then damage=damage*2.2 end -- source std_impact_003 baseline +120%; equipment hooks excluded.
            damage=math.min(target.hp,math.max(0,math.floor(damage)))
            target.hp=target.hp-damage
            if target.hp<=0 then
                target.action='dead';target.path=nil;target.deadAt=t
                if target.spawn then
                    local delay=target.spawn.respawnMilliseconds
                    target.respawnAt=delay and delay>=0 and t+delay or nil
                end
                event(world,'death',{targetId=target.id,sourceId=sender.id})
            elseif damage>0 then target.action='hit';target.actionUntil=t+300 end
        end
        event(world,hit and 'damage' or 'miss',{sourceId=sender.id,targetId=target.id,damage=damage,critical=critical,hp=target.hp})
        return {damage=damage,hit=hit,critical=critical,targetId=target.id,targetHp=target.hp,dead=target.hp<=0,cooldownUntil=sender.cooldown}
    end
    local function advance(world,unit,dt)
        if not unit.path or unit.hp<=0 then return end
        local budget=math.max(0,unit.stats.speed or 0)*dt/1000
        local oldX,oldZ=unit.x,unit.z
        while budget>0 and unit.path[unit.pathIndex or 1]do
            unit.pathIndex=unit.pathIndex or 1
            local node=unit.path[unit.pathIndex];local goal={x=node.x,z=node.y};local length=distance(unit,goal)
            if length<=budget then unit.x,unit.z=goal.x,goal.z;budget=budget-length;unit.pathIndex=unit.pathIndex+1
            else local factor=budget/length;unit.x=unit.x+(goal.x-unit.x)*factor;unit.z=unit.z+(goal.z-unit.z)*factor;budget=0 end
        end
        unit.y=height(world,unit.x,unit.z)
        if math.abs(unit.x-oldX)+math.abs(unit.z-oldZ)>.0001 then unit.yaw=math.deg(math.atan(unit.x-oldX,unit.z-oldZ))end
        if not unit.path[unit.pathIndex or 1]then unit.path=nil;unit.pathIndex=nil end
        if not unit.actionUntil or now()>=unit.actionUntil then unit.action=unit.path and 'run' or 'idle' end
    end
    function engine:tick()
        local t=now()
        for _,world in pairs(worlds)do
            local dt=math.max(0,math.min(500,t-world.lastTick));world.lastTick=t
            for _,player in pairs(world.players)do advance(world,player,dt)end
            for _,mob in pairs(world.mobs)do
                if mob.hp<=0 then
                    if mob.respawnAt and t>=mob.respawnAt then
                        mob.hp=mob.maxHp;mob.x,mob.y,mob.z=mob.spawn.x,mob.spawn.y,mob.spawn.z;mob.action='idle';mob.respawnAt=nil;mob.target=nil
                        event(world,'respawn',{targetId=mob.id,hp=mob.hp})
                    end
                elseif mob.hostile and next(world.players)then
                    local target=mob.target and world.players[mob.target]
                    if not target or target.hp<=0 or distance(target,mob)>12 or distance(mob,mob.spawn)>16 then target=nil;mob.target=nil end
                    if not target and mob.spawn.aiType==1 then
                        local nearest=6
                        for id,player in pairs(world.players)do
                            local d=distance(mob,player)
                            if player.hp>0 and d<nearest then target=player;nearest=d;mob.target=id end
                        end
                    end
                    if target then
                        local d=distance(mob,target)
                        if d<=3 then
                            mob.path=nil
                            if t>=mob.cooldown then
                                local nodes=route(world,mob,target);local length=0;local previous=mob
                                if nodes then for _,node in ipairs(nodes)do local nextpos={x=node.x,z=node.y};length=length+distance(previous,nextpos);previous=nextpos end end
                                if nodes and length<=3.75 then attack(world,mob,target)end
                            end
                        elseif t>=(mob.repathAt or 0)then mob.path=route(world,mob,target);mob.pathIndex=1;mob.repathAt=t+1000 end
                    elseif distance(mob,mob.spawn)>.1 and t>=(mob.repathAt or 0)then mob.path=route(world,mob,mob.spawn);mob.pathIndex=1;mob.repathAt=t+1000 end
                    advance(world,mob,dt)
                end
                if mob.hp>0 and mob.actionUntil and t>=mob.actionUntil then mob.actionUntil=nil;mob.action=mob.path and 'run' or 'idle' end
            end
        end
    end
    local function view(unit)
        return {id=unit.id,x=unit.x,y=unit.y,z=unit.z,hp=unit.hp,maxHp=unit.maxHp,action=unit.action,yaw=unit.yaw or 0,alive=unit.hp>0,modelId=unit.spawn and unit.spawn.modelId or 0}
    end
    function engine:disconnect(connection)
        local player=sessions[connection]
        if player then player.world.players[player.id]=nil;sessions[connection]=nil end
    end
    function engine:call(connection,method,params)
        if not data then return nil,'COMBAT_DATA_UNAVAILABLE' end
        if type(params)~='table' then return nil,'INVALID_PARAMS' end
        self:tick()
        if method=='combat.join' then
            if sessions[connection]then return nil,'COMBAT_ALREADY_JOINED' end
            if not finite(params.sceneId) or params.sceneId%1~=0 then return nil,'WORLD_NOT_FOUND' end
            local sessionCount=0;for _ in pairs(sessions)do sessionCount=sessionCount+1 end
            if sessionCount>=32 then return nil,'COMBAT_SESSION_CAPACITY' end
            local world,error=load_world(params.sceneId);if not world then return nil,error end
            local anchor
            for _,spawn in ipairs(world.source.entities)do
                if valid(world,spawn.x,spawn.z) and world.nav:walkable({x=spawn.x,y=spawn.z})then anchor=spawn;break end
            end
            if not anchor then return nil,'COMBAT_NO_WALKABLE_SPAWN' end
            local player=actor(data.profile,'human');player.id='player:'..tostring(connection);player.world=world;player.hp=data.profile.hp;player.maxHp=player.hp
            local spawn=world.nav:findempty({x=math.min(world.source.width-.1,anchor.x+2.5),y=anchor.z}) or {x=anchor.x,y=anchor.z}
            player.x,player.z=spawn.x,spawn.y;player.y=height(world,player.x,player.z);player.home={x=player.x,z=player.z};player.action='idle';player.cooldown=0
            sessions[connection]=player;world.players[player.id]=player
            return {player=view(player),sceneId=world.source.sceneId,combatMode='legacy-basic-physical',persistent=false,fullLegacySkills=false}
        end
        local player=sessions[connection]
        if not player then return nil,'COMBAT_NOT_JOINED' end
        local world=player.world
        if method=='combat.leave' then self:disconnect(connection);return {left=true}end
        if method=='combat.snapshot' then
            local offset,limit=params.offset or 0,params.limit or 50
            if not finite(offset) or offset<0 or offset%1~=0 or not finite(limit) or limit<1 or limit>100 or limit%1~=0 then return nil,'INVALID_PAGINATION' end
            local nearby={}
            for _,mob in pairs(world.mobs)do if distance(mob,player)<=40 then nearby[#nearby+1]=mob end end
            table.sort(nearby,function(a,b)return a.id<b.id end)
            local items={};for i=offset+1,math.min(#nearby,offset+limit)do items[#items+1]=view(nearby[i])end
            local events={};local after=params.afterSequence or 0
            if not finite(after) or after<0 then return nil,'INVALID_PARAMS' end
            for _,item in ipairs(world.events)do if item.sequence>after then events[#events+1]=item;if #events>=64 then break end end end
            return {player=view(player),entities=#items>0 and items or json.null,total=#nearby,nextOffset=math.min(offset+limit,#nearby),events=#events>0 and events or json.null,sequence=#events>0 and events[#events].sequence or world.sequence,latestSequence=world.sequence,eventsTruncated=#world.events>0 and after<world.events[1].sequence-1 or false,combatMode='legacy-basic-physical',fullLegacySkills=false}
        end
        if method=='combat.respawn' then
            if player.hp>0 then return nil,'PLAYER_ALIVE' end
            if now()<(player.deadAt or now())+5000 then return nil,'RESPAWN_COOLDOWN' end
            player.hp=player.maxHp;player.x,player.z=player.home.x,player.home.z;player.y=height(world,player.x,player.z);player.action='idle';return {player=view(player)}
        end
        if player.hp<=0 then return nil,'PLAYER_DEAD' end
        if method=='combat.move' then
            if not valid(world,params.x,params.z)then return nil,'INVALID_POSITION' end
            if distance(player,params)>32 then return nil,'MOVE_TOO_FAR' end
            local path=route(world,player,params);if not path then return nil,'PATH_BLOCKED' end
            player.path=path;player.pathIndex=1;return {accepted=true,player=view(player)}
        end
        if method=='combat.attack' then
            if type(params.targetId)~='string' then return nil,'INVALID_TARGET' end
            local target=world.mobs[params.targetId]
            if not target or not target.hostile then return nil,'TARGET_NOT_HOSTILE' end
            if target.hp<=0 then return nil,'TARGET_DEAD' end
            if now()<player.cooldown then return nil,'ATTACK_COOLDOWN' end
            if distance(player,target)>data.profile.range then return nil,'OUT_OF_RANGE' end
            if not world.nav:lineofsight({x=player.x,y=player.z},{x=target.x,y=target.z})then return nil,'PATH_BLOCKED' end
            local nodes=route(world,player,target);if not nodes then return nil,'PATH_BLOCKED' end
            local length=0;local previous=player
            for _,node in ipairs(nodes)do local nextpos={x=node.x,z=node.y};length=length+distance(previous,nextpos);previous=nextpos end
            if length>data.profile.range*1.25 then return nil,'PATH_BLOCKED' end
            local result,error=attack(world,player,target)
            if result then target.target=player.id;player.path=nil end
            return result,error
        end
        return nil,'METHOD_NOT_IMPLEMENTED'
    end
    return engine
end
return M

````

## Server/GameServer/lualib/unity_legacy_combat.lua

SHA-256: `29759afc5b5db0b8a5e279919a810a356b03d056b76c86bb5ac175eecf280744`

````lua
-- Generated from combat_core.lua: verbatim basic methods, not the complete skill/impact system.
local define=require "define"
local enum_damage_type={IDX_DAMAGE_PHY=0}
local M={}

function M:calculate_hit_rate(hit, miss)
	if hit == 0 and miss == 0 then
		return 0.5  -- 如果没有数据，默认50%命中率
	end
    return hit / (hit + miss)
end

-- 计算暴击率
-- @param mind_attack 攻击者的精神属性
-- @param mind_defend 防御者的精神属性
-- @return 暴击率（0-1之间的小数）

function M:calculate_critical_rate(mind_attack, mind_defend)
	if not mind_defend or mind_defend == 0 then
		mind_defend = 1  -- 防止除零错误
	end
    return mind_attack / (mind_defend * 20)
    -- 备选公式: return mind_attack / (mind_defend + mind_attack)
end

-- 判断是否命中
-- @param accuracy 命中率（0-1之间的小数）
-- @param rand 随机数（0-100）
-- @return 是否命中

function M:is_hit(accuracy, rand)
    local result = rand <= accuracy * 100
    -- skynet.error("[DBG_COMBAT] is_hit: accuracy=", accuracy, " rand=", rand, " threshold=", accuracy and (accuracy * 100) or "nil", " result=", result)
    return result
end

-- 判断是否暴击
-- @param critical_rate 暴击率（0-1之间的小数）
-- @param rand 随机数（0-100）
-- @return 是否暴击

function M:is_critical_hit(critical_rate, rand)
	if critical_rate >= 1 then
		return true  -- 暴击率100%时必定暴击
	end
    return rand <= critical_rate * 100
end

-- 获取战斗结果
-- 计算攻击者对防御者造成的所有类型伤害，并返回伤害结果
-- @param attacker 攻击者对象
-- @param defencer 防御者对象
-- @param imp 伤害影响对象
-- @return 伤害影响对象

function M:physical_damage(attacker, defencer, addition_attack, addition_defence, traits)
    local damage
    local attack = attacker:get_attack_physics() + addition_attack
    local defence = defencer:get_defence_physics() + addition_defence
    local ignorerate = 0  -- 免伤率
    local trait = traits[enum_damage_type.IDX_DAMAGE_PHY]
    
    -- 获取防御者的物理免伤率（仅玩家）
    if defencer:get_obj_type() == "human" then
        ignorerate = defencer:item_value(define.ITEM_ATTRIBUTE.IATTRIBUTE_IMMUNITY_P)
    end
    
    -- 检查技能是否忽略防御
    local skill_info = attacker:get_skill_info()
	if skill_info and skill_info.id then
		local ignore_defence = skill_info:get_is_ignore_defence()
		if ignore_defence then
			defence = 0  -- 忽略防御，防御力设为0
		end
	end
	
    -- 获取攻击和防御的百分比加成（仅玩家）
    local kfs_wg_attack_rate = 0
    local kfs_wg_defence_rate = 0
    if attacker:get_obj_type() == "human" then
        kfs_wg_attack_rate = attacker:item_value(define.ITEM_ATTRIBUTE.IATTRIBUTE_POINT_ADD_ATTACK_PHYSIC_DAMAGE_RATE)
    end
    if defencer:get_obj_type() == "human" then
        kfs_wg_defence_rate = defencer:item_value(define.ITEM_ATTRIBUTE.IATTRIBUTE_POINT_ADD_PHYSIC_DEFENCE_RATE)
    end
    kfs_wg_attack_rate = kfs_wg_attack_rate - kfs_wg_defence_rate
    kfs_wg_attack_rate = math.max(-10000, kfs_wg_attack_rate)
    
    -- 计算基础伤害：攻击力平方除以攻击力与防御力之和
    if attack + defence == 0 then
        damage = 0
    else
        damage = attack * attack / (attack + defence) * trait / 1000000
    end
    
    -- 应用免伤率
    ignorerate = ignorerate < 0 and 0 or ignorerate
    ignorerate = ignorerate > 100 and 100 or ignorerate
    damage = damage - damage * ignorerate / 100
    
    -- 应用百分比加成
    damage = damage * (10000 + kfs_wg_attack_rate) / 10000
    damage = damage < 0 and 0 or damage
    return damage
end

-- 计算魔法伤害
-- @param attacker 攻击者对象
-- @param defencer 防御者对象
-- @param addition_attack 额外攻击力
-- @param addition_defence 额外防御力
-- @param traits 攻击特性配置
-- @return 魔法伤害值
return M

````

## Server/GameServer/lualib/unity_world.lua

SHA-256: `1a6bb7f30678cac2cf97a1b49ef0a887c5e8ad85df6694f4a5090127f723ce53`

````lua
-- Read-only exported placements, loaded lazily; not a legacy gameplay simulation.
local json = require 'cjson'
local skynet = require 'skynet'
local M = {}
local catalog, entries, worlds, order, root
local function load_json(path)
    local file=io.open(path,'rb')
    if not file then return nil end
    local raw=file:read('*a');file:close()
    local ok,value=pcall(json.decode,raw)
    if ok then return value end
end
local function initialize()
    if catalog then return end
    root=skynet.getenv('unity_world_root')
    catalog=root and load_json(root..'/catalog.json') or {schema=1,scenes={}}
    catalog=catalog or {schema=1,scenes={}}
    entries={};worlds={};order={}
    for _,info in ipairs(catalog.scenes) do entries[info.sceneId]=info end
end
local function pagination(params)
    local offset=params.offset or 0
    local limit=params.limit or 50
    if type(offset)~='number' or offset<0 or offset%1~=0 or type(limit)~='number' or limit<1 or limit>100 or limit%1~=0 then
        return nil,nil,'INVALID_PAGINATION'
    end
    return offset,limit
end
local function get_world(id)
    if not entries[id] then return nil end
    if worlds[id] then return worlds[id] end
    local world=load_json(root..'/'..string.format('%d',id)..'.json')
    if not world or world.schema~=1 then return nil end
    if #order>=4 then worlds[table.remove(order,1)]=nil end
    worlds[id]=world;order[#order+1]=id
    return world
end
function M.call(method,params)
    initialize()
    if method=='world.list' then
        if #catalog.scenes==0 then return nil,'WORLD_DATA_UNAVAILABLE' end
        if params~=nil and params~=json.null and type(params)~='table' then return nil,'INVALID_PARAMS' end
        local offset,limit,error=pagination(type(params)=='table' and params or {})
        if error then return nil,error end
        if offset>=#catalog.scenes then return nil,'PAGE_OUT_OF_RANGE' end
        local scenes={}
        for i=offset+1,math.min(offset+limit,#catalog.scenes) do scenes[#scenes+1]=catalog.scenes[i] end
        return {scenes=scenes,total=#catalog.scenes,nextOffset=math.min(offset+limit,#catalog.scenes),simulationReady=false}
    end
    if type(params)~='table' then return nil,'INVALID_PARAMS' end
    if type(params.sceneId)~='number' or params.sceneId%1~=0 then return nil,'WORLD_NOT_FOUND' end
    local world=get_world(params.sceneId)
    if not world then return nil,'WORLD_NOT_FOUND' end
    if method=='world.enter' then
        return {sceneId=world.sceneId,name=world.name,width=world.width,depth=world.depth,sceneType=world.sceneType,
            entityCount=#world.entities,simulationReady=false,coordinates=world.coordinates}
    end
    local offset,limit,error=pagination(params)
    if error then return nil,error end
    if offset>=#world.entities then return nil,'PAGE_OUT_OF_RANGE' end
    local items={}
    for i=offset+1,math.min(offset+limit,#world.entities) do items[#items+1]=world.entities[i] end
    return {sceneId=world.sceneId,items=items,total=#world.entities,nextOffset=math.min(offset+limit,#world.entities),simulationReady=false}
end
function M.get_world(id)
    initialize()
    return get_world(id)
end
function M.data_root()
    initialize()
    return root
end
return M

````

## Server/GameServer/services/license_check.lua

SHA-256: `cc128c90deb45c1088dbaec55100a6114c3c1cb1f0dfb7b1aa2eed6cfeff96a6`

````lua
local skynet = require "skynet"

local M = {}

function M.check_or_abort()
    -- Explicit development configuration; no replacement native module required.
    if skynet.getenv("skip_license_check") == "true" then
        skynet.error("[DEV] License module check disabled by configuration")
        return true
    end

    local ok, mod = pcall(require, "llicense")
    if not ok then
        skynet.error("[FATAL] Core service initialization failed (code -3)")
        skynet.abort()
        return
    end

    local ok2, info = pcall(mod.check)
    if not ok2 then
        skynet.error("[FATAL] Runtime environment validation error (code -5)")
        skynet.abort()
        return
    end

    if info.result == 0 then
        -- passed
    else
        -- 旧版本本地启动不因机器时间/运行环境校验失败中断，保留日志方便定位。
        skynet.error(string.format("[WARN] Runtime environment check skipped: system clock mismatch (code -7, result %s)", tostring(info.result)))
        return
    end
end

return M

````

## Server/GameServer/services/unity_gateway.lua

SHA-256: `d5514247e4ce73955f9049d19c8d666dd840d34fbc35a10921b5148a6e84a960`

````lua
-- Development transport for a new Unity client, with a basic server-owned PvE adapter.
local skynet = require 'skynet'
local socket = require 'skynet.socket'
local driver = require 'skynet.socketdriver'
local json = require 'cjson'
require 'skynet.manager'
local MAX_LINE = 65536
local combat
local function response(request,connection)
    if type(request) ~= 'table' or request == json.null then
        return {v=1, ok=false, error={code='INVALID_REQUEST'}}
    end
    local id = request.id
    if type(id) ~= 'string' or #id > 64 or id == '' then
        return {v=1, ok=false, error={code='INVALID_ID'}}
    end
    local reply = {v=1, id=id, ok=false}
    if request.v ~= 1 then
        reply.error = {code='UNSUPPORTED_VERSION'}
    elseif request.method == 'hello' then
        reply.ok = true
        reply.result = {protocol='372dragon.unity', version=1,
                        capabilities={'hello', 'ping', 'world.list', 'world.enter', 'world.entities', 'combat.join', 'combat.move', 'combat.attack', 'combat.snapshot', 'combat.respawn', 'combat.leave'}, gameplayReady=false, basicCombatAvailable=true, fullLegacySkills=false}
    elseif request.method == 'ping' then
        reply.ok = true
        reply.result = {pong=true}
    elseif request.method == 'world.list' or request.method == 'world.enter' or request.method == 'world.entities' then
        local result, code = require('unity_world').call(request.method, request.params)
        if result then reply.ok = true; reply.result = result else reply.error = {code=code} end
    elseif type(request.method)=='string' and request.method:match('^combat%.') then
        local result,code=combat:call(connection,request.method,request.params)
        if result then reply.ok=true;reply.result=result else reply.error={code=code}end
    else
        reply.error = {code='METHOD_NOT_IMPLEMENTED'}
    end
    return reply
end
skynet.start(function()
    assert(require('license_check').check_or_abort(), 'Gateway requires skip_license_check=true')
    combat=require('unity_combat').new(require('unity_world'))
    skynet.fork(function()while true do skynet.sleep(10);combat:tick()end end)
    local host = skynet.getenv('unity_host') or '127.0.0.1'
    local port = tonumber(skynet.getenv('unity_port') or '15800')
    local listener = socket.listen(host, port)
    socket.start(listener, function(fd)
        local ok, err = pcall(function()
            socket.start(fd)
            socket.limit(fd, MAX_LINE)
            while true do
                local line = socket.readline(fd, '\n')
                if not line then break end
                if #line > MAX_LINE then break end
                local decoded, request = pcall(json.decode, line)
                local reply = decoded and response(request,fd) or
                    {v=1, ok=false, error={code='INVALID_JSON'}}
                socket.write(fd, json.encode(reply)..'\n')
            end
        end)
        if not ok then skynet.error('Unity connection closed: '..tostring(err)) end
        combat:disconnect(fd)
        socket.close(fd)
    end)
    for _, info in pairs(driver.info()) do
        if info.id == listener then
            local actual = assert(info.sock:match(':(%d+)$'))
            io.stdout:write('UNITY_GATEWAY_READY '..actual..'\n')
            io.stdout:flush()
        end
    end
end)

````

## Tests/server/native/combat_clock.lua

SHA-256: `2886981f56bbd241fe34b1aea7c6a247f1fca86927923a52f8264e6c33516c02`

````lua
local skynet=require 'skynet'
require 'skynet.manager'
skynet.start(function()
 local ok,error=xpcall(function()
  local world=require 'unity_world'
  local legacy=require 'unity_legacy_combat'
  assert(legacy:calculate_hit_rate(0,0)==.5)
  assert(legacy:calculate_hit_rate(100,100)==.5)
  assert(legacy:calculate_critical_rate(20,1)==1)
  local attacker={get_attack_physics=function()return 100 end,get_obj_type=function()return 'monster'end,get_skill_info=function()return nil end}
  local defender={get_defence_physics=function()return 100 end,get_obj_type=function()return 'monster'end}
  assert(legacy:physical_damage(attacker,defender,0,0,{[0]=1000000})==50)
  local time=1000
  local engine=require('unity_combat').new(world,{now=function()return time end,random=function()return 1 end})
  local joined,code=engine:call(70,'combat.join',{sceneId=6});assert(joined,code)
  local target='6:monster0'
  local snapshot=assert(engine:call(70,'combat.snapshot',{limit=100}))
  local initial
  for _,mob in ipairs(snapshot.entities)do if mob.id==target then initial=mob.hp end end
  assert(initial and initial>0)
  local dead=false
  for i=1,30 do
   local result,why=engine:call(70,'combat.attack',{targetId=target,damage=99999999})
   assert(result,why)
   assert(result.damage<100 and result.targetHp>=0)
   local _,cooldown=engine:call(70,'combat.attack',{targetId=target})
   assert(cooldown=='ATTACK_COOLDOWN' or cooldown=='TARGET_DEAD')
   if result.dead then dead=true;break end
   time=time+600
  end
  assert(dead,'source monster did not die from authoritative attacks')
  local _,why=engine:call(70,'combat.attack',{targetId=target});assert(why=='TARGET_DEAD')
  local respawn
  for _,spawn in ipairs(world.get_world(6).entities)do if spawn.id==target then respawn=spawn.respawnMilliseconds end end
  time=time+respawn-1;engine:tick()
  local state=assert(engine:call(70,'combat.snapshot',{limit=100}))
  for _,mob in ipairs(state.entities)do if mob.id==target then assert(mob.hp==0)end end
  time=time+1;engine:tick()
  state=assert(engine:call(70,'combat.snapshot',{limit=100}))
  local found=false
  for _,mob in ipairs(state.entities)do if mob.id==target then assert(mob.hp==initial);found=true end end
  assert(found,'respawned monster snapshot missing')
  local moved,move_error=engine:call(70,'combat.move',{x=joined.player.x+.25,z=joined.player.z})
  assert(moved,move_error)
  local before=assert(engine:call(70,'combat.snapshot',{limit=100})).player
  time=time+100;engine:tick()
  local after=assert(engine:call(70,'combat.snapshot',{limit=100})).player
  assert(math.abs(after.x-before.x)<=.51 and math.abs(after.z-before.z)<=.51,'client movement exceeded server speed')
  engine:disconnect(70)
  local _,missing=engine:call(70,'combat.snapshot',{});assert(missing=='COMBAT_NOT_JOINED')
 end,debug.traceback)
 if ok then io.stdout:write('COMBAT_CLOCK_OK\n')else io.stdout:write('COMBAT_CLOCK_FAILED '..error..'\n')end
 io.stdout:flush();skynet.abort()
end)

````

## Tests/server/native/smoke.lua

SHA-256: `87f0cc2b77e79e3184b39e4a83257ca85f21b701ceb133bcaa256477be4a94ff`

````lua
local skynet = require 'skynet'
local socket = require 'skynet.socket'
require 'skynet.manager'
skynet.start(function()
    local ok, err = xpcall(function()
        assert(require('license_check').check_or_abort(), 'development startup without llicense')
        for _, name in ipairs({'unitynav', 'gbk', 'map', 'ldump', 'lnavmesh', 'laiscript', 'lfs', 'rax', 'lprofile.c', 'lcipher.c', 'ltls.c', 'bson', 'md5', 'pb', 'sproto', 'lpeg', 'cjson', 'zlib', 'skiplist.c', 'textfilter', 'luarsa'}) do
            assert(require(name), name)
        end
        local gbk = require 'gbk'
        assert(gbk.fromutf8(gbk.toutf8('native-test')) == 'native-test')
        local nav = require 'lnavmesh'
        local point = nav.Point.new(1, 2, 0)
        assert(point.x == 100 and point.y == 200)
        local received = false
        local listener = socket.listen('127.0.0.1', 0)
        socket.start(listener, function(id)
            socket.start(id)
            assert(socket.read(id, 4) == 'ping')
            socket.write(id, 'pong')
            received = true
            socket.close(id)
        end)
        local info = require('skynet.socketdriver').info()
        local port
        for _, s in pairs(info) do
            if s.id == listener then port = tonumber(s.sock:match(':(%d+)$')) end
        end
        assert(port, 'listener port')
        local client = assert(socket.open('127.0.0.1', port))
        socket.write(client, 'ping')
        assert(socket.read(client, 4) == 'pong')
        assert(received)
        socket.close(client)
        socket.close(listener)
        local profiler = require 'lprofile.c'
        profiler.start()
        local sum = 0
        for i = 1, 1000 do sum = sum + i end
        assert(sum == 500500)
        local elapsed = profiler.dump()
        profiler.stop()
        assert(type(elapsed) == 'number' and elapsed >= 0 and elapsed < 10000000, 'profiler clock')
        local before = skynet.now()
        skynet.sleep(2)
        assert(skynet.now() > before, 'timer must advance')
    end, debug.traceback)
    if ok then io.stdout:write('NATIVE_SMOKE_OK\n') else io.stdout:write('NATIVE_SMOKE_FAILED: '..err..'\n') end
    io.stdout:flush()
    skynet.abort()
end)

````

## Tests/server/run_combat_clock.py

SHA-256: `8ba77bd5ac978649293753947dbd7eccf0bb9488e79539c068c8b8629cd6d1a6`

````python
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

````

## Tests/server/run_native_smoke.py

SHA-256: `e3944d33c1bf4262484e35ecb038e33b6a9210091e9a040bf04d7bf0883d156a`

````python
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

````

## Tests/server/test_license_startup.lua

SHA-256: `bf42a56ae7292174f0cb133a6104b1ca209d8b7726d8d9524f7fe152ac4077d1`

````lua
-- Exercise the real wrapper with an isolated Skynet facade; no game/native license is needed.
local skipped, aborted, requested, logged
package.preload.skynet = function()
    return {
        getenv = function(name) assert(name == 'skip_license_check'); return skipped end,
        abort = function() aborted = true end,
        error = function() logged = true end,
    }
end
package.preload.llicense = function()
    requested = true
    error('license module unavailable in this fixture')
end
local check = dofile('Server/GameServer/services/license_check.lua')
for _, value in ipairs({'true', 'false', 'TRUE', ''}) do
    skipped, aborted, requested, logged = value, false, false, false
    check.check_or_abort()
    assert(logged)
    if value == 'true' then
        assert(not requested and not aborted, 'explicit development mode must avoid native dependency')
    else
        assert(requested and aborted, 'other values must preserve the default check')
    end
    package.loaded.llicense = nil
end
skipped, aborted, requested = nil, false, false
check.check_or_abort()
assert(requested and aborted, 'unset configuration must retain the default check')
print('PASS: 5 license startup configuration cases')

````

## Tests/server/test_original_art.py

SHA-256: `3b4be667cfd738ca93d126f3a98059ed921d79a10fbba6b86a74e891c6db2aa4`

````python
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

````

## Tests/server/test_unity_combat.py

SHA-256: `09d25c5aef7625d8b5245216e1ba82148ed19b82dd0c51d2d33e7ce293228b83`

````python
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

````

## Tests/server/test_unity_gateway.py

SHA-256: `13b2c7a22d5e17012e877c284dc125d70b43815831eff65d271017eb329e4439`

````python
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

````

## Tests/server/test_unity_nav.py

SHA-256: `cc60627f0005a9c8a5402c3887e167b371efa8b2286fe4a1204346eaddfeedbf`

````python
#!/usr/bin/env python3
"""Check every navigation image through the actual native Lua module and verify scene metadata."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Tools/unity/art'))
from native_navigation import inspect
WORLD=ROOT/'Build/unity-world'
status=inspect(WORLD)
expected={v[:24]+'.path' for v in json.loads((WORLD/'combat-data.json').read_text())['navigation'].values()}
assert set(status)==expected
blocked=[]
for entry in json.loads((WORLD/'catalog.json').read_text())['scenes']:
    data=json.loads((WORLD/(str(entry['sceneId'])+'.json')).read_text())
    assert data['combatNavigationAvailable']==status[Path(data['navFile']).name]
    if not data['combatNavigationAvailable']:blocked.append(data['sceneId'])
assert set(blocked)=={40,95,104},blocked
print('UNITY_NAV_AUDIT_OK',sum(status.values()),'of',len(status),'images; 289 scenes checked, unavailable combat scenes:',blocked)

````

## Tests/server/test_unity_world.py

SHA-256: `43d4d3bf62d565f5a54e410813b475b02933fd280d2a67e242cf1bd525d843d1`

````python
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

````

## Tests/server/test_world_batch.py

SHA-256: `2c88384fac331928f167d013aaf8b319becfb2e4ab8009825a4ce4d8031b950c`

````python
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

````

## Tools/server/build_native.sh

SHA-256: `60019eba77d90d380cde1e19d2d85c490c1bb3aa1e444a549ac3ba2d697116a8`

````bash
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

````

## Tools/server/check_native_game.py

SHA-256: `7891407a4b266e7d0a641a5e3ad581c56eed0aa401e97efecfcca0f141d95652`

````python
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

````

## Tools/server/run_unity_gateway.py

SHA-256: `25092ca3ad255adb2d5d6d47e4cc65028bdda2a2760a0beb2b2dc0a4fc6c3b4a`

````python
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

````

## Tools/unity/NativeServerConnection.cs

SHA-256: `63f024aebbc717605b09c317dca876acf5d1b163af386e7403ec00d224d5d59b`

````csharp
using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

// Attach to a GameObject. Requires a running run_unity_gateway.py process.
public sealed class NativeServerConnection : MonoBehaviour
{
    public string Host = "127.0.0.1";
    public int Port = 15800;
    private TcpClient client;
    private bool destroyed;

    [Serializable] private sealed class Request
    {
        public int v = 1;
        public string id;
        public string method;
    }

    [Serializable] private sealed class Response
    {
        public int v;
        public string id;
        public bool ok;
    }

    private async void Start()
    {
        try
        {
            client = new TcpClient();
            var connect = client.ConnectAsync(Host, Port);
            if (await Task.WhenAny(connect, Task.Delay(5000)) != connect)
                throw new TimeoutException("Server connection timed out");
            await connect;
            if (destroyed) return;
            using (var stream = client.GetStream())
            using (var reader = new StreamReader(stream, new UTF8Encoding(false)))
            using (var writer = new StreamWriter(stream, new UTF8Encoding(false)) { AutoFlush = true, NewLine = "\n" })
            {
                foreach (var method in new[] { "hello", "ping" })
                {
                    var request = new Request { id = Guid.NewGuid().ToString("N"), method = method };
                    await writer.WriteLineAsync(JsonUtility.ToJson(request));
                    var read = reader.ReadLineAsync();
                    if (await Task.WhenAny(read, Task.Delay(5000)) != read)
                        throw new TimeoutException("Server response timed out");
                    var response = await read;
                    if (response == null) throw new IOException("Server closed the connection");
                    var envelope = JsonUtility.FromJson<Response>(response);
                    if (envelope == null || envelope.v != 1 || envelope.id != request.id || !envelope.ok)
                        throw new IOException("Invalid or unsuccessful server response: " + response);
                    if (!destroyed) Debug.Log("Native server: " + response);
                }
            }
        }
        catch (Exception error)
        {
            if (!destroyed) Debug.LogError("Native server connection: " + error.Message);
        }
        finally { client?.Close(); }
    }

    private void OnDestroy()
    {
        destroyed = true;
        client?.Close();
    }
}

````

## Tools/unity/Package/ART-COMBAT.md

SHA-256: `4ef7f36f39e0c3141fefcea96c09dc47f6e95eb4db44a5cb2b128349a7652b56`

````markdown
# Mesh, animation gốc và chiến đấu phát triển

## Cài vào Unity (mục tiêu 2021.3 LTS trở lên)

1. Nhập `Assets/DragonPort` từ UnityMapPort.zip vào project đã sao lưu.
2. Để thử nhanh actor của Đại Lý/Vô Lượng Sơn: giải nén UnityOriginalActors-Starter.zip
   vào cùng project. Gói này không chứa vật thể cảnh. Để có toàn bộ art đã chuyển,
   tải và giải nén **tất cả** UnityOriginalArt-XX.zip vào cùng một thư mục Assets.
   Các ZIP độc lập, cùng cấu trúc thư mục. Không đặt mỗi gói vào thư mục riêng.
3. Chạy **Tools → Dragon Port → Import Original Meshes and Animations**, chọn
   `Assets/DragonPort/Art/art-catalog.json`. Chờ tạo prefab, mesh, material và clip.
   Importer hỗ trợ gói một phần; bỏ qua file chưa tải và giữ prefab/binding đã có.
   Nếu đã nhập starter, full pack sẽ thay catalog bằng catalog đầy đủ.
4. Dùng Browse Maps, import map 6 (Vô Lượng Sơn). Gán
   `Assets/DragonPort/GeneratedArt/OriginalPrefabs.asset` vào loader.Prefabs,
   rồi Build World lại để thay capsule bằng actor gốc có binding.
5. Chọn map root, chạy **Tools → Dragon Port → Enable Development Combat on Selected Map**.
   Menu tắt DragonWorldSession và thêm DragonCombatClient. Hai component không chạy cùng nhau.
6. Bổ sung camera/light của project; camera phải nhìn vào player/vùng spawn.
   Đặt InputCamera trên DragonCombatClient. Play khi gateway native đang chạy.
   Player hiện là capsule phát triển; có thể gán PlayerPrefab của project.
7. Với Legacy Input Manager: click nền để đi, click quái để đánh, R để hồi sinh.
   Với New Input System: nối input vào `MoveTo(Vector3)`, `Attack(spawnId)`, `Respawn()`.
   Đọc PlayerState/CombatEvent để nối UI HP, sát thương; client không tự tính damage.

## Chạy server

Từ repository server đã áp dụng NativeServerChanges.zip:

```bash
bash Tools/server/build_native.sh
python3 Tools/server/run_unity_gateway.py --world-root Build/unity-world
```

ZIP server là **source delta + dữ liệu đã export**, áp dụng lên repository
`a002lamlam-ship-it/372dragon` commit `436a12317f0408f303692078790f48537a33fd20`.
Không phải binary macOS dựng sẵn. macOS cần Xcode Command Line Tools, Python3,
GNU make, pkg-config và OpenSSL; xem Docs/guide/server-macos-arm64.md.
Mặc định gateway chỉ bind localhost:15800. Chưa có account/auth/TLS/persistence.

## Những gì đã chuyển

- 7.738 mesh nguồn, 875 mesh có animation; 7.584 binding scenery và 159 binding
  actor trong 914 model ID đang được map sử dụng. Giữ keyframe skeleton gốc;
  shader dùng material Unity gần đúng và texture màu nguồn, không tái hiện toàn bộ shader/effect cũ.
- Xuất thành Mesh/SkinnedMeshRenderer, rig, Legacy AnimationClip và prefab Unity.
  Tên clip gốc giữ nguyên; idle/run/attack/hit/death chọn theo tên và có thể chỉnh trên component.
- Tọa độ XYZ giữ nguyên, đổi đơn vị 0.01, đảo winding cho Unity; giữ auxiliary W
  của FLOAT4 trong dữ liệu audit. Normals lỗi được dựng lại; geometry không hữu hạn bị loại rõ ràng.
- Combat **PvE vật lý cơ bản cho phát triển**, server quyết định vị trí, HP, trúng,
  chí mạng, cooldown, sát thương, chết/hồi sinh. Tái sử dụng năm hàm tính gốc,
  chỉ số monster/AttackTraits nguồn và PathLib hiện có để đi theo navmesh thật.
  Nav thật nạp được cho 286/289 scene; scene 40/95/104 bị từ chối combat do nav nguồn
  rỗng/không được reader chấp nhận, vẫn import được map. Xem combat-navigation-report.json.
  Chí mạng cơ bản 2.2x theo hook gốc; chưa áp dụng modifier skill/equipment/impact.
- Aggro/chase/leash là adapter mới đơn giản. Player dùng profile thử nghiệm cố định,
  không phải nhân vật game cũ. Không có loot, exp, nhiệm vụ, inventory hay lưu nhân vật.

## Thiếu dữ liệu và mức xác minh

Archive không chứa `all.obj`, file ghép bộ phận, attachment và transform mà
CharModelEx tham chiếu. 755 model chưa thể tự gán đáng tin cậy: giữ capsule,
không tự bịa cấu trúc ghép. 159 binding là đối chiếu mesh cùng tên, chưa xác minh
composition/transform gốc. Cột 3 CharModelEx là fuse time, không phải scale.
Tổng 12 lỗi tài nguyên/geometry được ghi trong art-catalog.json; không bỏ qua âm thầm.

Nguồn tải được kiểm CRC và SHA-256 từng member theo index; chưa kiểm hash toàn bộ
archive 12 GB. Art có giấy phép dữ liệu riêng, xem DATA-NOTICE trong core package.
Đã kiểm server/native module trên Linux và render mesh khỉ trắng với pose đánh
bằng Blender. **Chưa compile/chạy Unity Editor và chưa chạy trên macOS ARM64**;
cần kiểm import, shader, hướng/tỉ lệ và gameplay trong project Unity thực tế.

## Tái tạo từ nguồn

```bash
python3 Tools/unity/port_all_worlds.py
python3 Tools/unity/art/export_combat_data.py
python3 Tools/unity/art/export_art.py
python3 Tests/server/test_original_art.py
python3 Tests/server/test_unity_combat.py
python3 Tests/server/run_combat_clock.py
python3 Tools/unity/package_world.py
python3 Tools/unity/art/package_art.py
python3 Tools/unity/package_server.py
```

Art đầy đủ cần nhiều GB đĩa và thời gian tải/chuyển; dùng cache đã kiểm checksum.
`Build/art-downloads.json` chứa hash từng ZIP giao cuối. Các Python tool chạy từ
repository gốc; gói Unity không phải bản sao đầy đủ repository để tái export.

````

## Tools/unity/Package/Assets/DragonPort/Editor/DragonArtImport.cs

SHA-256: `b61d56312e510dd4b6e02621f133ad35f9d9194b41b7bf120e61a8451a158b22`

````csharp
using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;
namespace DragonPort.Editor
{
    public static class DragonArtImport
    {
        [Serializable] private sealed class Asset { public string assetId,file; }
        [Serializable] private sealed class Actor { public int modelId; public string assetId; public float importScale=1; }
        [Serializable] private sealed class Scenery { public string resource,assetId; }
        [Serializable] private sealed class Catalog { public int schema; public Asset[] assets; public Actor[] actorBindings; public Scenery[] sceneryBindings; }
        private const string Destination="Assets/DragonPort/GeneratedArt";
        private static Vector3 V(float[] values){return new Vector3(values[0],values[1],values[2]);}
        private static Quaternion Q(float[] values){return new Quaternion(values[0],values[1],values[2],values[3]).normalized;}
        private static string BoneName(int id){return "Bone_"+id.ToString("D3");}
        [MenuItem("Tools/Dragon Port/Import Original Meshes and Animations")]
        public static void Import()
        {
            var file=EditorUtility.OpenFilePanel("Select art-catalog.json inside imported Assets/DragonPort/Art","Assets/DragonPort/Art","json");
            if(string.IsNullOrEmpty(file))return;
            var source=Path.GetDirectoryName(file);
            var absoluteAssets=Path.GetFullPath(Application.dataPath)+Path.DirectorySeparatorChar;
            if(!Path.GetFullPath(source).StartsWith(absoluteAssets,StringComparison.Ordinal))throw new InvalidOperationException("Copy the art pack under this project's Assets folder first");
            var catalog=JsonUtility.FromJson<Catalog>(File.ReadAllText(file));
            if(catalog==null || catalog.schema!=1)throw new InvalidDataException("Invalid art catalog");
            Directory.CreateDirectory(Destination);AssetDatabase.Refresh();
            var prefabs=new Dictionary<string,GameObject>();
            try
            {
                for(var i=0;i<catalog.assets.Length;++i)
                {
                    var asset=catalog.assets[i];
                    if(EditorUtility.DisplayCancelableProgressBar("Import original art",asset.assetId,(float)i/catalog.assets.Length))break;
                    var prefabPath=Destination+"/"+asset.assetId+".prefab";
                    var prefab=AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
                    // Preserve existing generated/user-edited assets on repeated imports.
                    try
                    {
                        if(!prefab && !File.Exists(Path.Combine(source,asset.file)))continue; // Partial art packs are supported.
                        if(!prefab)prefab=Build(Path.Combine(source,asset.file),source,asset.assetId,prefabPath);
                        prefabs[asset.assetId]=prefab;
                    }
                    catch(Exception error){Debug.LogError("Art import failed for "+asset.assetId+": "+error.Message);}
                }
            }
            finally{EditorUtility.ClearProgressBar();AssetDatabase.SaveAssets();}
            var libraryPath=Destination+"/OriginalPrefabs.asset";
            var library=AssetDatabase.LoadAssetAtPath<DragonPrefabLibrary>(libraryPath);
            if(!library){library=ScriptableObject.CreateInstance<DragonPrefabLibrary>();AssetDatabase.CreateAsset(library,libraryPath);}
            var actors=new List<DragonPrefabLibrary.ActorBinding>(library.actors);
            var knownActors=new HashSet<int>();foreach(var old in library.actors)knownActors.Add(old.modelId);
            foreach(var binding in catalog.actorBindings)
            {
                GameObject prefab;
                if(!knownActors.Contains(binding.modelId) && prefabs.TryGetValue(binding.assetId,out prefab))actors.Add(new DragonPrefabLibrary.ActorBinding{modelId=binding.modelId,prefab=prefab,scale=binding.importScale});
            }
            var scenery=new List<DragonPrefabLibrary.SceneryBinding>(library.scenery);
            var knownScenery=new HashSet<string>();foreach(var old in library.scenery)knownScenery.Add(old.resource);
            foreach(var binding in catalog.sceneryBindings)
            {
                GameObject prefab;
                if(!knownScenery.Contains(binding.resource) && prefabs.TryGetValue(binding.assetId,out prefab))scenery.Add(new DragonPrefabLibrary.SceneryBinding{resource=binding.resource,prefab=prefab});
            }
            library.actors=actors.ToArray();library.scenery=scenery.ToArray();EditorUtility.SetDirty(library);AssetDatabase.SaveAssets();
            Selection.activeObject=library;
            Debug.Log("Imported "+prefabs.Count+" original meshes. Assign OriginalPrefabs to DragonWorldLoader.Prefabs. See art-catalog.json for missing/unsupported assets and unverified object composition.");
        }
        private static GameObject Build(string file,string source,string id,string prefabPath)
        {
            var data=JsonUtility.FromJson<DragonArtData>(File.ReadAllText(file));
            if(data==null || data.schema!=1)throw new InvalidDataException("Invalid art data");
            var folder=Destination+"/"+id;
            if(Directory.Exists(folder))throw new InvalidOperationException("Existing partial asset folder preserved: "+folder);
            Directory.CreateDirectory(folder);AssetDatabase.Refresh();
            var root=new GameObject(id);
            try
            {
                var bones=new Dictionary<int,Transform>();var boneData=new Dictionary<int,DragonBone>();var boneOrder=new List<int>();
                Transform rigRoot=null;
                if(data.rig!=null && data.rig.bones!=null)
                {
                    rigRoot=new GameObject("Rig").transform;rigRoot.SetParent(root.transform,false);
                    foreach(var bone in data.rig.bones)
                    {
                        var t=new GameObject(BoneName(bone.id)).transform;bones.Add(bone.id,t);boneData.Add(bone.id,bone);boneOrder.Add(bone.id);
                    }
                    boneOrder.Sort();
                    foreach(var bone in data.rig.bones)
                    {
                        var t=bones[bone.id];t.SetParent(bone.parent<0?rigRoot:bones[bone.parent],false);
                        t.localPosition=V(bone.position);t.localRotation=Q(bone.rotation);t.localScale=V(bone.scale);
                    }
                }
                for(var partIndex=0;partIndex<data.parts.Length;++partIndex)
                {
                    var part=data.parts[partIndex];var count=part.positions.Length/3;
                    var vertices=new Vector3[count];for(var j=0;j<count;++j)vertices[j]=new Vector3(part.positions[j*3],part.positions[j*3+1],part.positions[j*3+2]);
                    var mesh=new Mesh{name=id+"_"+partIndex,indexFormat=count>65535?IndexFormat.UInt32:IndexFormat.UInt16};mesh.vertices=vertices;mesh.triangles=part.triangles;
                    if(part.normals!=null && part.normals.Length==count*3)
                    {
                        var normals=new Vector3[count];for(var j=0;j<count;++j)normals[j]=new Vector3(part.normals[j*3],part.normals[j*3+1],part.normals[j*3+2]);mesh.normals=normals;
                    }
                    else mesh.RecalculateNormals();
                    if(part.uv!=null && part.uvComponents>=2 && part.uv.Length==count*part.uvComponents)
                    {
                        var uv=new Vector2[count];for(var j=0;j<count;++j)uv[j]=new Vector2(part.uv[j*part.uvComponents],part.uv[j*part.uvComponents+1]);mesh.uv=uv;mesh.RecalculateTangents();
                    }
                    var child=new GameObject("Mesh_"+partIndex);child.transform.SetParent(root.transform,false);
                    Renderer renderer;
                    if(part.hasSkin)
                    {
                        if(!rigRoot)throw new InvalidDataException("Skin without rig");
                        var dense=new Dictionary<int,int>();var transforms=new Transform[boneOrder.Count];var bindposes=new Matrix4x4[boneOrder.Count];
                        for(var j=0;j<boneOrder.Count;++j){dense[boneOrder[j]]=j;transforms[j]=bones[boneOrder[j]];bindposes[j]=transforms[j].worldToLocalMatrix*child.transform.localToWorldMatrix;}
                        var weights=new BoneWeight[count];
                        for(var j=0;j<count;++j)
                        {
                            var k=j*4;
                            weights[j]=new BoneWeight{boneIndex0=part.weights[k]>0?dense[part.boneIds[k]]:0,boneIndex1=part.weights[k+1]>0?dense[part.boneIds[k+1]]:0,boneIndex2=part.weights[k+2]>0?dense[part.boneIds[k+2]]:0,boneIndex3=part.weights[k+3]>0?dense[part.boneIds[k+3]]:0,weight0=part.weights[k],weight1=part.weights[k+1],weight2=part.weights[k+2],weight3=part.weights[k+3]};
                        }
                        mesh.boneWeights=weights;mesh.bindposes=bindposes;
                        var skin=child.AddComponent<SkinnedMeshRenderer>();skin.bones=transforms;skin.rootBone=rigRoot;skin.sharedMesh=mesh;skin.updateWhenOffscreen=true;renderer=skin;
                    }
                    else
                    {
                        child.AddComponent<MeshFilter>().sharedMesh=mesh;renderer=child.AddComponent<MeshRenderer>();
                        child.AddComponent<MeshCollider>().sharedMesh=mesh;
                    }
                    mesh.RecalculateBounds();AssetDatabase.CreateAsset(mesh,folder+"/Mesh_"+partIndex+".asset");
                    var info=data.materials[partIndex];var shader=Shader.Find("Universal Render Pipeline/Lit")??Shader.Find("Standard")??Shader.Find("HDRP/Lit");
                    if(!shader)throw new InvalidOperationException("No supported lit shader found");
                    var material=new Material(shader){name=info.name};
                    if(!string.IsNullOrEmpty(info.textureFile))
                    {
                        var absolute=Path.GetFullPath(Path.Combine(source,info.textureFile)).Replace('\\','/');
                        var assetPath="Assets"+absolute.Substring(Path.GetFullPath(Application.dataPath).Replace('\\','/').Length);
                        var texture=AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
                        if(!texture)throw new InvalidDataException("Missing texture; copy all art packs before import: "+info.textureFile);
                        if(material.HasProperty("_BaseMap"))material.SetTexture("_BaseMap",texture);
                        if(material.HasProperty("_MainTex"))material.SetTexture("_MainTex",texture);
                    }
                    if(info.alphaCutoff>0)
                    {
                        material.EnableKeyword("_ALPHATEST_ON");material.SetFloat("_Cutoff",info.alphaCutoff);material.renderQueue=2450;
                        if(material.HasProperty("_AlphaClip"))material.SetFloat("_AlphaClip",1);
                        if(material.HasProperty("_Mode"))material.SetFloat("_Mode",1);
                    }
                    if(info.transparent)
                    {
                        if(material.HasProperty("_Surface"))material.SetFloat("_Surface",1);
                        if(material.HasProperty("_Mode"))material.SetFloat("_Mode",3);
                        material.SetInt("_SrcBlend",(int)BlendMode.SrcAlpha);material.SetInt("_DstBlend",(int)BlendMode.OneMinusSrcAlpha);material.SetInt("_ZWrite",0);material.EnableKeyword("_ALPHABLEND_ON");material.renderQueue=3000;
                    }
                    if(info.doubleSided && material.HasProperty("_Cull"))material.SetInt("_Cull",(int)CullMode.Off);
                    AssetDatabase.CreateAsset(material,folder+"/Material_"+partIndex+".mat");renderer.sharedMaterial=material;
                }
                if(data.rig!=null && data.rig.animations!=null && data.rig.animations.Length>0)
                {
                    var animation=root.AddComponent<Animation>();var names=new List<string>();
                    for(var index=0;index<data.rig.animations.Length;++index)
                    {
                        var original=data.rig.animations[index];var clip=new AnimationClip{name=original.name,legacy=true,frameRate=30};
                        foreach(var track in original.tracks)
                        {
                            var bone=boneData[track.boneId];var path=AnimationUtility.CalculateTransformPath(bones[track.boneId],root.transform);
                            var position=new[]{new AnimationCurve(),new AnimationCurve(),new AnimationCurve()};
                            var rotation=new[]{new AnimationCurve(),new AnimationCurve(),new AnimationCurve(),new AnimationCurve()};
                            var scale=new[]{new AnimationCurve(),new AnimationCurve(),new AnimationCurve()};
                            foreach(var key in track.keys)
                            {
                                var p=V(bone.position)+V(key.position);var q=Q(bone.rotation)*Q(key.rotation);var s=Vector3.Scale(V(bone.scale),V(key.scale));
                                for(var axis=0;axis<3;++axis){position[axis].AddKey(key.time,p[axis]);scale[axis].AddKey(key.time,s[axis]);}
                                for(var axis=0;axis<4;++axis)rotation[axis].AddKey(key.time,q[axis]);
                            }
                            for(var axis=0;axis<3;++axis){SetCurve(clip,path,"localPosition."+"xyz"[axis],position[axis]);SetCurve(clip,path,"localScale."+"xyz"[axis],scale[axis]);}
                            for(var axis=0;axis<4;++axis)SetCurve(clip,path,"localRotation."+"xyzw"[axis],rotation[axis]);
                        }
                        clip.EnsureQuaternionContinuity();AssetDatabase.CreateAsset(clip,folder+"/Clip_"+index+".anim");animation.AddClip(clip,original.name);names.Add(original.name);
                    }
                    var playback=root.AddComponent<DragonOriginalAnimation>();playback.Idle=Choose(names,"站立","idle","stand","休闲");playback.Run=Choose(names,"跑步","行走","run","walk");playback.Attack=Choose(names,"攻击","attack");playback.Hit=Choose(names,"受击","hit");playback.Death=Choose(names,"倒地","死亡","death","die");
                }
                return PrefabUtility.SaveAsPrefabAsset(root,prefabPath);
            }
            catch
            {
                // Only this newly created transaction folder is removed; pre-existing folders were rejected above.
                AssetDatabase.DeleteAsset(folder);throw;
            }
            finally{UnityEngine.Object.DestroyImmediate(root);}
        }
        private static void SetCurve(AnimationClip clip,string path,string property,AnimationCurve curve)
        {
            for(var i=0;i<curve.length;++i){AnimationUtility.SetKeyLeftTangentMode(curve,i,AnimationUtility.TangentMode.Linear);AnimationUtility.SetKeyRightTangentMode(curve,i,AnimationUtility.TangentMode.Linear);}
            clip.SetCurve(path,typeof(Transform),property,curve);
        }
        private static string Choose(List<string> names,params string[] choices)
        {
            foreach(var choice in choices)foreach(var name in names)if(name.Equals(choice,StringComparison.OrdinalIgnoreCase))return name;
            foreach(var choice in choices)foreach(var name in names)if(name.IndexOf(choice,StringComparison.OrdinalIgnoreCase)>=0)return name;
            return names.Count>0?names[0]:null;
        }
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Editor/DragonWorldBrowser.cs

SHA-256: `964916f9f83510dd9ffd8c84281eca494d3ab1d20805ac9253bdf9fbbdcc7fc4`

````csharp
using System;
using System.IO;
using UnityEditor;
using UnityEngine;
namespace DragonPort.Editor
{
    public sealed class DragonWorldBrowser : EditorWindow
    {
        [Serializable] private sealed class Map
        {
            public int sceneId,width,depth,entityCount,npcCount,monsterCount,warningCount,skippedEntityCount;
            public string name;
        }
        [Serializable] private sealed class Catalog { public int schema; public Map[] scenes; }
        private TextAsset catalogAsset;
        private Catalog catalog;
        private string query="";
        private Vector2 scroll;
        [MenuItem("Tools/Dragon Port/Browse Maps")]
        public static void Open(){GetWindow<DragonWorldBrowser>("Dragon Maps");}
        private void OnEnable()
        {
            catalogAsset=AssetDatabase.LoadAssetAtPath<TextAsset>("Assets/DragonPort/Data/catalog.json");
            Reload();
        }
        private void Reload()
        {
            catalog=catalogAsset ? JsonUtility.FromJson<Catalog>(catalogAsset.text) : null;
        }
        private void OnGUI()
        {
            EditorGUI.BeginChangeCheck();
            catalogAsset=(TextAsset)EditorGUILayout.ObjectField("Catalog",catalogAsset,typeof(TextAsset),false);
            if(EditorGUI.EndChangeCheck())Reload();
            query=EditorGUILayout.TextField("Find ID or name",query);
            if(catalog==null || catalog.schema!=1 || catalog.scenes==null)
            {EditorGUILayout.HelpBox("Choose the exported catalog.json from the map package.",MessageType.Info);return;}
            EditorGUILayout.LabelField(catalog.scenes.Length+" exported maps; source placements only, no live AI.");
            scroll=EditorGUILayout.BeginScrollView(scroll);
            foreach(var map in catalog.scenes)
            {
                if(query.Length>0 && map.name.IndexOf(query,StringComparison.OrdinalIgnoreCase)<0 && !map.sceneId.ToString().Contains(query))continue;
                EditorGUILayout.BeginVertical("box");
                EditorGUILayout.LabelField(map.sceneId+" — "+map.name,EditorStyles.boldLabel);
                EditorGUILayout.LabelField(map.width+"×"+map.depth+" | NPC "+map.npcCount+" | Other spawns "+map.monsterCount);
                if(map.warningCount>0 || map.skippedEntityCount>0)
                    EditorGUILayout.LabelField("Source warnings: "+map.warningCount+"; skipped entities: "+map.skippedEntityCount);
                if(GUILayout.Button("Import this map"))
                {
                    var directory=Path.GetDirectoryName(AssetDatabase.GetAssetPath(catalogAsset));
                    var path=Path.Combine(directory,map.sceneId.ToString(),map.sceneId+".json");
                    if(File.Exists(path))DragonWorldImport.ImportPath(path);
                    else Debug.LogError("Map bundle missing: "+path);
                }
                EditorGUILayout.EndVertical();
            }
            EditorGUILayout.EndScrollView();
        }
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Editor/DragonWorldImport.cs

SHA-256: `f84df9cee4e7954900e4fe4e4628ea348ebb7b8afa3549a330e7da157ca7c0ad`

````csharp
using System;
using System.IO;
using UnityEditor;
using UnityEngine;
namespace DragonPort.Editor
{
    public static class DragonWorldImport
    {
        private static Material MaterialAsset(string path,Shader shader,Color color)
        {
            var material=AssetDatabase.LoadAssetAtPath<Material>(path);
            if(material)return material;
            material=new Material(shader);
            if(material.HasProperty("_BaseColor"))material.SetColor("_BaseColor",color);
            if(material.HasProperty("_Color"))material.SetColor("_Color",color);
            AssetDatabase.CreateAsset(material,path);
            return material;
        }
        [MenuItem("Tools/Dragon Port/Enable Development Combat on Selected Map")]
        public static void EnableCombat()
        {
            var selected=Selection.activeGameObject;
            var loader=selected?selected.GetComponent<DragonWorldLoader>():null;
            if(!loader)throw new InvalidOperationException("Select the imported map root first");
            var snapshot=selected.GetComponent<DragonWorldSession>();
            if(snapshot){Undo.RecordObject(snapshot,"Disable source snapshot session");snapshot.enabled=false;EditorUtility.SetDirty(snapshot);}
            var combat=selected.GetComponent<DragonCombatClient>();
            if(!combat)combat=Undo.AddComponent<DragonCombatClient>(selected);
            combat.Loader=loader;combat.enabled=true;EditorUtility.SetDirty(combat);
        }
        [MenuItem("Tools/Dragon Port/Import Exported Map")]
        public static void Import()
        {
            var json=EditorUtility.OpenFilePanel("Select exported map JSON","","json");
            if(string.IsNullOrEmpty(json))return;
            ImportPath(json);
        }
        public static void ImportPath(string json)
        {
            var world=JsonUtility.FromJson<DragonWorldData>(File.ReadAllText(json));
            if(world==null || world.schema!=1 || world.width<=0)throw new InvalidDataException("Not a Dragon map export");
            var source=Path.GetDirectoryName(json);
            var destination="Assets/DragonPort/Imported/"+world.sceneId;
            Directory.CreateDirectory(destination);
            foreach(var suffix in new[]{".json",".heights.bytes",".cells.bytes"})
            {
                var input=Path.Combine(source,world.sceneId+suffix);
                var output=destination+"/"+world.sceneId+suffix;
                if(Path.GetFullPath(input)!=Path.GetFullPath(output)) File.Copy(input,output,true);
            }
            AssetDatabase.Refresh();
            var obj=new GameObject("Dragon Map "+world.sceneId+" "+world.name);
            Undo.RegisterCreatedObjectUndo(obj,"Import Dragon map");
            var loader=obj.AddComponent<DragonWorldLoader>();
            loader.WorldJson=AssetDatabase.LoadAssetAtPath<TextAsset>(destination+"/"+world.sceneId+".json");
            loader.HeightSamples=AssetDatabase.LoadAssetAtPath<TextAsset>(destination+"/"+world.sceneId+".heights.bytes");
            loader.CellFlags=AssetDatabase.LoadAssetAtPath<TextAsset>(destination+"/"+world.sceneId+".cells.bytes");
            var shader=Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Standard") ?? Shader.Find("HDRP/Lit");
            if(shader)
            {
                loader.GroundMaterial=MaterialAsset(destination+"/Ground.mat",shader,new Color(0.3f,0.4f,0.25f));
                loader.NpcMaterial=MaterialAsset(destination+"/Npc.mat",shader,Color.yellow);
                loader.MonsterMaterial=MaterialAsset(destination+"/Monster.mat",shader,Color.red);
            }
            obj.AddComponent<DragonWorldSession>().Loader=loader;
            EditorUtility.SetDirty(loader);
            Selection.activeGameObject=obj;
            Debug.Log("Assign a Ground Material (and optional Prefab Library), then use Build World or press Play.",obj);
        }
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonArtData.cs

SHA-256: `8ef218f998fe39770a8a3e104d3493540a84ff7de4eeee1a418d83421c4cbbc7`

````csharp
using System;
namespace DragonPort
{
    [Serializable] public sealed class DragonArtData
    {
        public int schema;
        public DragonArtPart[] parts;
        public DragonRig rig;
        public DragonArtMaterial[] materials;
    }
    [Serializable] public sealed class DragonArtPart
    {
        public string material;
        public float[] positions,normals,uv,weights;
        public int[] triangles,boneIds;
        public int uvComponents;
        public bool hasSkin;
    }
    [Serializable] public sealed class DragonRig
    {
        public DragonBone[] bones;
        public DragonClip[] animations;
    }
    [Serializable] public sealed class DragonBone
    {
        public int id,parent;
        public string name;
        public float[] position,rotation,scale;
    }
    [Serializable] public sealed class DragonClip
    {
        public string name;
        public float duration;
        public DragonTrack[] tracks;
    }
    [Serializable] public sealed class DragonTrack
    {
        public int boneId;
        public DragonKey[] keys;
    }
    [Serializable] public sealed class DragonKey
    {
        public float time;
        public float[] position,rotation,scale;
    }
    [Serializable] public sealed class DragonArtMaterial
    {
        public string name,textureFile;
        public bool transparent,doubleSided,sourceMaterialFound,shaderApproximation;
        public float alphaCutoff;
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonCombatClient.cs

SHA-256: `38b3df2ee8714586fc0026204a81bdc1902c4740364099c704e3ce8706d06d6f`

````csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
namespace DragonPort
{
    [Serializable] public sealed class DragonCombatActor
    {
        public string id,action;
        public float x,y,z,yaw;
        public double hp,maxHp;
        public int modelId;
        public bool alive;
    }
    [Serializable] public sealed class DragonCombatEvent
    {
        public string kind,sourceId,targetId;
        public double sequence,damage,hp;
        public bool critical;
    }
    public sealed class DragonCombatClient : MonoBehaviour
    {
        public DragonWorldLoader Loader;
        public string Host="127.0.0.1";
        public int Port=15800;
        public GameObject PlayerPrefab;
        public Camera InputCamera;
        public DragonCombatActor PlayerState {get;private set;}
        public event Action<DragonCombatEvent> CombatEvent;
        private TcpClient client;
        private bool stopped;
        private readonly Dictionary<string,DragonSpawn> actors=new Dictionary<string,DragonSpawn>();
        private GameObject playerVisual;
        private string pendingAttack;
        private Vector3? pendingMove;
        private bool pendingRespawn;
        private double sequence;
        [Serializable] private sealed class Parameters
        {
            public int sceneId,offset,limit=100;
            public string targetId;
            public float x,z;
            public double afterSequence;
        }
        [Serializable] private sealed class Request {public int v=1;public string id,method;public Parameters @params;}
        [Serializable] private sealed class Result
        {
            public DragonCombatActor player;
            public DragonCombatActor[] entities;
            public DragonCombatEvent[] events;
            public double sequence;
            public int total,nextOffset;
            public double damage,targetHp;
            public bool hit,critical,dead;
        }
        [Serializable] private sealed class Error {public string code;}
        [Serializable] private sealed class Reply {public int v;public string id;public bool ok;public Result result;public Error error;}
        public void Attack(string sourceSpawnId){pendingAttack=sourceSpawnId;}
        public void MoveTo(Vector3 localGridPosition){pendingMove=localGridPosition;}
        public void Respawn(){pendingRespawn=true;}
        private async Task<Reply> Call(StreamReader input,StreamWriter output,string method,Parameters parameters)
        {
            var request=new Request{id=Guid.NewGuid().ToString("N"),method=method,@params=parameters};
            await output.WriteLineAsync(JsonUtility.ToJson(request));
            var read=input.ReadLineAsync();
            if(await Task.WhenAny(read,Task.Delay(5000))!=read)throw new TimeoutException("Combat response timed out");
            var line=await read;
            if(line==null)throw new IOException("Combat server disconnected");
            var reply=JsonUtility.FromJson<Reply>(line);
            if(reply==null || reply.v!=1 || reply.id!=request.id)throw new InvalidDataException("Invalid combat response");
            if(!reply.ok && !stopped)Debug.Log("Combat: "+(reply.error!=null?reply.error.code:"unknown error"),this);
            return reply;
        }
        private void Apply(DragonCombatActor state,Transform target)
        {
            var old=target.localPosition;var next=new Vector3(state.x,state.y,state.z);
            target.localRotation=Quaternion.Euler(0,state.yaw,0);
            target.localPosition=next;
            var playback=target.GetComponentInChildren<DragonOriginalAnimation>();
            if(playback)playback.PlayState(state.action);
        }
        private async void Start()
        {
            try
            {
                if(!Loader)Loader=GetComponent<DragonWorldLoader>();
                if(!Loader)throw new InvalidOperationException("Assign DragonWorldLoader");
                // WorldSession is a one-off source snapshot client; it must not race live combat updates.
                var sourceSession=Loader.GetComponent<DragonWorldSession>();
                if(sourceSession && sourceSession.enabled)throw new InvalidOperationException("Disable DragonWorldSession when enabling DragonCombatClient");
                if(Loader.World==null)Loader.BuildWorld();
                foreach(var spawn in Loader.GetComponentsInChildren<DragonSpawn>())actors[spawn.Data.id]=spawn;
                client=new TcpClient();var connect=client.ConnectAsync(Host,Port);
                if(await Task.WhenAny(connect,Task.Delay(5000))!=connect)throw new TimeoutException("Combat connection timed out");
                await connect;if(stopped)return;
                using(var stream=client.GetStream())
                using(var input=new StreamReader(stream,new UTF8Encoding(false)))
                using(var output=new StreamWriter(stream,new UTF8Encoding(false)){AutoFlush=true,NewLine="\n"})
                {
                    var joined=await Call(input,output,"combat.join",new Parameters{sceneId=Loader.World.sceneId});
                    if(!joined.ok)throw new IOException("Could not join development combat world");
                    PlayerState=joined.result.player;
                    playerVisual=PlayerPrefab?Instantiate(PlayerPrefab,Loader.transform):new GameObject("Development Player");
                    if(!PlayerPrefab)
                    {
                        playerVisual.transform.SetParent(Loader.transform,false);
                        var marker=GameObject.CreatePrimitive(PrimitiveType.Capsule);marker.transform.SetParent(playerVisual.transform,false);marker.transform.localPosition=Vector3.up;
                    }
                    playerVisual.name="Development Player "+PlayerState.id;Apply(PlayerState,playerVisual.transform);
                    Debug.Log("Connected: source basic physical damage, source nav/stats, server-owned HP/cooldown. Development player profile; not full TLBB skills or account persistence.",this);
                    while(!stopped)
                    {
                        if(pendingMove.HasValue)
                        {
                            var move=pendingMove.Value;pendingMove=null;
                            await Call(input,output,"combat.move",new Parameters{x=move.x,z=move.z});
                        }
                        if(pendingAttack!=null)
                        {
                            var target=pendingAttack;pendingAttack=null;
                            var reply=await Call(input,output,"combat.attack",new Parameters{targetId=target});
                            if(reply.ok)Debug.Log("Attack: "+(reply.result.hit?reply.result.damage.ToString():"miss")+"; target HP "+reply.result.targetHp,this);
                        }
                        if(pendingRespawn){pendingRespawn=false;await Call(input,output,"combat.respawn",new Parameters());}
                        var offset=0;
                        do
                        {
                            var snapshot=await Call(input,output,"combat.snapshot",new Parameters{offset=offset,afterSequence=sequence});
                            if(!snapshot.ok)throw new IOException("Combat snapshot rejected");
                            var result=snapshot.result;PlayerState=result.player;Apply(PlayerState,playerVisual.transform);
                            if(result.entities!=null)foreach(var state in result.entities)
                            {
                                DragonSpawn actor;if(actors.TryGetValue(state.id,out actor))Apply(state,actor.transform);
                            }
                            if(result.events!=null)foreach(var item in result.events)CombatEvent?.Invoke(item);
                            sequence=result.sequence;
                            if(result.nextOffset>=result.total)break;
                            if(result.nextOffset<=offset)throw new InvalidDataException("Combat page did not advance");
                            offset=result.nextOffset;
                        }while(!stopped);
                        await Task.Delay(100);
                    }
                }
            }
            catch(Exception error){if(!stopped)Debug.LogError("Dragon combat: "+error.Message,this);}
            finally{client?.Close();}
        }
        private void Update()
        {
#if ENABLE_LEGACY_INPUT_MANAGER
            if(!Loader || PlayerState==null)return;
            if(Input.GetKeyDown(KeyCode.R))Respawn();
            if(!Input.GetMouseButtonDown(0))return;
            var camera=InputCamera?InputCamera:Camera.main;if(!camera)return;
            RaycastHit hit;if(!Physics.Raycast(camera.ScreenPointToRay(Input.mousePosition),out hit,2000))return;
            var spawn=hit.collider.GetComponentInParent<DragonSpawn>();
            if(spawn)Attack(spawn.Data.id);
            else MoveTo(Loader.transform.InverseTransformPoint(hit.point));
#endif
        }
        private void OnDestroy(){stopped=true;client?.Close();if(playerVisual)Destroy(playerVisual);}
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonOriginalAnimation.cs

SHA-256: `f615349658e78a73925fb8d1f898cb1df313fe47bb5983405f99390e1f365268`

````csharp
using UnityEngine;
namespace DragonPort
{
    public sealed class DragonOriginalAnimation : MonoBehaviour
    {
        public string Idle,Run,Attack,Hit,Death;
        private Animation animationComponent;
        private string current;
        private void Awake(){animationComponent=GetComponent<Animation>();}
        private void Start(){PlayState("idle");}
        public void PlayState(string state)
        {
            if(!animationComponent)animationComponent=GetComponent<Animation>();
            if(!animationComponent)return;
            var clip=state=="dead"?Death:state=="attack"?Attack:state=="hit"?Hit:state=="run"?Run:Idle;
            if(string.IsNullOrEmpty(clip) || !animationComponent[clip])return;
            if(current==state && animationComponent.IsPlaying(clip))return;
            current=state;
            animationComponent[clip].wrapMode=(state=="idle" || state=="run")?WrapMode.Loop:WrapMode.ClampForever;
            animationComponent.CrossFade(clip,.08f);
        }
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonPrefabLibrary.cs

SHA-256: `f201c295c485dfc0627eac1f0778b497b5c73b557fb03bf5e61bba15139d5de3`

````csharp
using System;
using UnityEngine;
namespace DragonPort
{
    [CreateAssetMenu(menuName="Dragon Port/Prefab Library")]
    public sealed class DragonPrefabLibrary : ScriptableObject
    {
        [Serializable] public sealed class ActorBinding
        {
            public int modelId;
            public float scale=1;
            public GameObject prefab;
        }
        [Serializable] public sealed class SceneryBinding
        {
            public string resource;
            public GameObject prefab;
        }
        public ActorBinding[] actors = new ActorBinding[0];
        public SceneryBinding[] scenery = new SceneryBinding[0];
        public GameObject Actor(int modelId)
        {
            foreach (var binding in actors) if (binding.modelId == modelId) return binding.prefab;
            return null;
        }
        public float ActorScale(int modelId)
        {
            foreach(var binding in actors)if(binding.modelId==modelId)return binding.scale;
            return 1;
        }
        public GameObject Scenery(string resource)
        {
            foreach (var binding in scenery) if (binding.resource == resource) return binding.prefab;
            return null;
        }
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonSpawn.cs

SHA-256: `5720dd28e00215cab31519bbee9b5da9d9693938df879ba16eb2541f6a6f1917`

````csharp
using UnityEngine;
namespace DragonPort
{
    // Stable source identity; no client-side damage, AI or respawn authority.
    public sealed class DragonSpawn : MonoBehaviour
    {
        public DragonEntityData Data;
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonWorldData.cs

SHA-256: `a52b409724e1dc70f0adf8f66961ddf42e4a25b95c8b3bad4881d5f233539c51`

````csharp
using System;
using UnityEngine;
namespace DragonPort
{
    [Serializable] public sealed class DragonWorldData
    {
        public int schema, sceneId, clientResourceId, width, depth;
        public string name, coordinates;
        public bool simulationReady;
        public DragonEntityData[] entities;
        public DragonStaticData[] staticObjects;
    }
    [Serializable] public sealed class DragonEntityData
    {
        public string id, kind, name, title, sourceSection;
        public int templateId, modelId, level, hp, scriptId, aiType, respawnMilliseconds;
        public float x, y, z, yaw;
    }
    [Serializable] public sealed class DragonStaticData
    {
        public string resource;
        public float x, y, z;
        public Quaternion rotation;
        public float[] sourceScale;
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonWorldLoader.cs

SHA-256: `d169144213d75ed96cce273d2defa7509efaca397990787f198e48d2455332a3`

````csharp
using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
namespace DragonPort
{
    [DefaultExecutionOrder(-100)]
    public sealed class DragonWorldLoader : MonoBehaviour
    {
        public TextAsset WorldJson, HeightSamples, CellFlags;
        public DragonPrefabLibrary Prefabs;
        public Material GroundMaterial, NpcMaterial, MonsterMaterial;
        public bool ShowLabels = true;
        [Range(8,128)] public int TileSize = 64;
        private readonly List<Mesh> meshes = new List<Mesh>();
        public DragonWorldData World { get; private set; }
        private void Start() { if(World==null || !transform.Find("__DragonWorld"))BuildWorld(); }
        private void Clear()
        {
            var old = transform.Find("__DragonWorld");
            if (old != null) Remove(old.gameObject);
            foreach (var mesh in meshes) if (mesh != null) Remove(mesh);
            meshes.Clear();
        }
        private static void Remove(UnityEngine.Object value)
        {
            if (Application.isPlaying) Destroy(value); else DestroyImmediate(value);
        }
        [ContextMenu("Build World")]
        public void BuildWorld()
        {
            if (!WorldJson || !HeightSamples || !CellFlags) throw new InvalidOperationException("Assign all three exported data assets");
            World = JsonUtility.FromJson<DragonWorldData>(WorldJson.text);
            if (World == null || World.schema != 1 || World.width < 1 || World.depth < 1 || World.width > 4096 || World.depth > 4096)
                throw new InvalidDataException("Unsupported world schema/dimensions");
            var heights = HeightSamples.bytes;
            var flags = CellFlags.bytes;
            if (heights.Length != checked((World.width+1)*(World.depth+1)*4) || flags.Length != World.width*World.depth)
                throw new InvalidDataException("Terrain byte count mismatch");
            var samples = new float[heights.Length/4];
            using (var reader = new BinaryReader(new MemoryStream(heights)))
                for (var i=0; i<samples.Length; ++i)
                {
                    samples[i] = reader.ReadSingle();
                    if (float.IsNaN(samples[i]) || float.IsInfinity(samples[i])) throw new InvalidDataException("Invalid height");
                }
            Clear();
            var root = new GameObject("__DragonWorld"); root.transform.SetParent(transform,false);
            if (!Application.isPlaying) root.hideFlags = HideFlags.DontSave;
            var tileSize = Mathf.Clamp(TileSize,8,128);
            for (var z=0; z<World.depth; z+=tileSize)
                for (var x=0; x<World.width; x+=tileSize)
                    MakeTile(root.transform, samples, flags, x,z,Math.Min(tileSize,World.width-x),Math.Min(tileSize,World.depth-z));
            foreach (var entity in World.entities ?? new DragonEntityData[0])
            {
                var prefab = Prefabs ? Prefabs.Actor(entity.modelId) : null;
                GameObject actor;
                if (prefab)
                {
                    actor = Instantiate(prefab,root.transform);
                    actor.transform.localScale *= Prefabs.ActorScale(entity.modelId);
                }
                else
                {
                    actor = new GameObject(); actor.transform.SetParent(root.transform,false);
                    var marker = GameObject.CreatePrimitive(PrimitiveType.Capsule);
                    marker.transform.SetParent(actor.transform,false); marker.transform.localPosition = Vector3.up;
                    var material = entity.kind == "npc" ? NpcMaterial : MonsterMaterial;
                    if (material) marker.GetComponent<Renderer>().sharedMaterial = material;
                }
                actor.name = entity.kind+" "+entity.name+" ["+entity.id+"]";
                actor.transform.localPosition = new Vector3(entity.x,entity.y,entity.z);
                actor.transform.localRotation = Quaternion.Euler(0,entity.yaw,0);
                actor.AddComponent<DragonSpawn>().Data = entity;
                if(prefab)
                {
                    var hitbox=actor.AddComponent<CapsuleCollider>();hitbox.center=Vector3.up;hitbox.height=2;hitbox.radius=.5f;
                }
                if (ShowLabels)
                {
                    var label = new GameObject("Name"); label.transform.SetParent(actor.transform,false);
                    label.transform.localPosition = new Vector3(0,2.3f,0);
                    var text = label.AddComponent<TextMesh>(); text.text = entity.name;
                    text.anchor = TextAnchor.LowerCenter; text.characterSize = 0.15f; text.fontSize = 32;
                    text.color = entity.kind == "npc" ? Color.yellow : Color.red;
                }
            }
            var unresolved=0;
            foreach (var item in World.staticObjects ?? new DragonStaticData[0])
            {
                var prefab = Prefabs ? Prefabs.Scenery(item.resource) : null;
                if (!prefab) { ++unresolved; continue; }
                var scenery = Instantiate(prefab,root.transform);
                scenery.transform.localPosition = new Vector3(item.x,item.y,item.z);
                scenery.transform.localRotation = item.rotation;
                // Bind prefabs authored in server-grid units; preserve each placement's source scale.
                if (item.sourceScale != null && item.sourceScale.Length == 3)
                    scenery.transform.localScale = Vector3.Scale(scenery.transform.localScale,new Vector3(item.sourceScale[0],item.sourceScale[1],item.sourceScale[2]));
            }
            Debug.Log("Loaded "+World.name+": "+World.entities.Length+" spawn placements; "+unresolved+" scenery prefab bindings missing. Enable DragonCombatClient for development PvE.",this);
        }
        private void MakeTile(Transform root,float[] heights,byte[] flags,int startX,int startZ,int w,int d)
        {
            var vertices=new Vector3[(w+1)*(d+1)]; var uv=new Vector2[vertices.Length];
            for(var z=0;z<=d;++z) for(var x=0;x<=w;++x)
            {
                var i=z*(w+1)+x; var gx=startX+x; var gz=startZ+z;
                vertices[i]=new Vector3(gx,heights[gz*(World.width+1)+gx],gz);
                uv[i]=new Vector2((float)gx/World.width,(float)gz/World.depth);
            }
            var triangles=new List<int>(w*d*6);
            for(var z=0;z<d;++z) for(var x=0;x<w;++x)
            {
                var flag=flags[(startZ+z)*World.width+startX+x];
                if((flag&2)!=0)continue;
                var a=z*(w+1)+x; var b=a+1; var c=a+w+1; var e=c+1;
                if((flag&1)!=0) triangles.AddRange(new[]{a,c,e,a,e,b});
                else triangles.AddRange(new[]{a,c,b,b,c,e});
            }
            var mesh=new Mesh {name="Terrain "+startX+","+startZ};
            mesh.vertices=vertices;mesh.uv=uv;mesh.triangles=triangles.ToArray();mesh.RecalculateNormals();mesh.RecalculateBounds();meshes.Add(mesh);
            var tile=new GameObject(mesh.name);tile.transform.SetParent(root,false);
            tile.AddComponent<MeshFilter>().sharedMesh=mesh;
            tile.AddComponent<MeshRenderer>().sharedMaterial=GroundMaterial;
            tile.AddComponent<MeshCollider>().sharedMesh=mesh;
        }
        private void OnDestroy() { foreach(var mesh in meshes) if(mesh) Remove(mesh); }
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/DragonWorldSession.cs

SHA-256: `afede0a4af3662d730346ea79e29aca6ab7c29d33da121f34044a3574dc693d9`

````csharp
using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
namespace DragonPort
{
    // Fetches real source placements from the native gateway; not a multiplayer simulation client.
    public sealed class DragonWorldSession : MonoBehaviour
    {
        public string Host="127.0.0.1";
        public int Port=15800;
        public DragonWorldLoader Loader;
        private TcpClient client;
        private bool destroyed;
        [Serializable] private sealed class Parameters { public int sceneId,offset,limit=50; }
        [Serializable] private sealed class Request { public int v=1; public string id,method; public Parameters @params; }
        [Serializable] private sealed class Result { public int sceneId,width,depth,entityCount,total,nextOffset; public bool simulationReady; public DragonEntityData[] items; }
        [Serializable] private sealed class Error { public string code; }
        [Serializable] private sealed class Reply { public int v; public string id; public bool ok; public Result result; public Error error; }
        private async Task<Reply> Call(StreamReader input,StreamWriter output,string method,Parameters parameters)
        {
            var request=new Request {id=Guid.NewGuid().ToString("N"),method=method,@params=parameters};
            await output.WriteLineAsync(JsonUtility.ToJson(request));
            var read=input.ReadLineAsync();
            if(await Task.WhenAny(read,Task.Delay(5000))!=read)throw new TimeoutException("World response timeout");
            var line=await read;
            if(line==null)throw new IOException("Gateway disconnected");
            var reply=JsonUtility.FromJson<Reply>(line);
            if(reply==null || reply.v!=1 || reply.id!=request.id || !reply.ok)
                throw new IOException(reply!=null && reply.error!=null ? reply.error.code : "Invalid world response");
            return reply;
        }
        private async void Start()
        {
            try
            {
                if(!Loader)Loader=GetComponent<DragonWorldLoader>();
                if(!Loader)throw new InvalidOperationException("Assign DragonWorldLoader");
                if(Loader.World==null)Loader.BuildWorld();
                client=new TcpClient();
                var connect=client.ConnectAsync(Host,Port);
                if(await Task.WhenAny(connect,Task.Delay(5000))!=connect)throw new TimeoutException("Gateway connection timeout");
                await connect;
                if(destroyed)return;
                using(var stream=client.GetStream())
                using(var input=new StreamReader(stream,new UTF8Encoding(false)))
                using(var output=new StreamWriter(stream,new UTF8Encoding(false)){AutoFlush=true,NewLine="\n"})
                {
                    var p=new Parameters {sceneId=Loader.World.sceneId};
                    var entered=await Call(input,output,"world.enter",p);
                    if(entered.result.sceneId!=Loader.World.sceneId || entered.result.width!=Loader.World.width || entered.result.depth!=Loader.World.depth)
                        throw new InvalidDataException("Local terrain and server world do not match");
                    var actors=Loader.GetComponentsInChildren<DragonSpawn>();
                    var known=new System.Collections.Generic.Dictionary<string,DragonSpawn>();
                    foreach(var actor in actors)known[actor.Data.id]=actor;
                    var count=0;
                    while(p.offset<entered.result.entityCount)
                    {
                        var page=await Call(input,output,"world.entities",p);
                        if(page.result.nextOffset<=p.offset || page.result.nextOffset>page.result.total)throw new InvalidDataException("Invalid pagination");
                        foreach(var entity in page.result.items)
                        {
                            DragonSpawn actor;
                            if(!known.TryGetValue(entity.id,out actor))throw new InvalidDataException("Local spawn bundle differs from server");
                            actor.Data=entity;
                            actor.transform.localPosition=new Vector3(entity.x,entity.y,entity.z);
                            actor.transform.localRotation=Quaternion.Euler(0,entity.yaw,0);
                            ++count;
                        }
                        p.offset=page.result.nextOffset;
                    }
                    if(!destroyed)Debug.Log("Native world synchronized: "+count+" placements. Live AI/combat are not connected.",this);
                }
            }
            catch(Exception error){if(!destroyed)Debug.LogError("Dragon world: "+error.Message,this);}
            finally{client?.Close();}
        }
        private void OnDestroy(){destroyed=true;client?.Close();}
    }
}

````

## Tools/unity/Package/Assets/DragonPort/Runtime/NativeServerConnection.cs

SHA-256: `63f024aebbc717605b09c317dca876acf5d1b163af386e7403ec00d224d5d59b`

````csharp
using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

// Attach to a GameObject. Requires a running run_unity_gateway.py process.
public sealed class NativeServerConnection : MonoBehaviour
{
    public string Host = "127.0.0.1";
    public int Port = 15800;
    private TcpClient client;
    private bool destroyed;

    [Serializable] private sealed class Request
    {
        public int v = 1;
        public string id;
        public string method;
    }

    [Serializable] private sealed class Response
    {
        public int v;
        public string id;
        public bool ok;
    }

    private async void Start()
    {
        try
        {
            client = new TcpClient();
            var connect = client.ConnectAsync(Host, Port);
            if (await Task.WhenAny(connect, Task.Delay(5000)) != connect)
                throw new TimeoutException("Server connection timed out");
            await connect;
            if (destroyed) return;
            using (var stream = client.GetStream())
            using (var reader = new StreamReader(stream, new UTF8Encoding(false)))
            using (var writer = new StreamWriter(stream, new UTF8Encoding(false)) { AutoFlush = true, NewLine = "\n" })
            {
                foreach (var method in new[] { "hello", "ping" })
                {
                    var request = new Request { id = Guid.NewGuid().ToString("N"), method = method };
                    await writer.WriteLineAsync(JsonUtility.ToJson(request));
                    var read = reader.ReadLineAsync();
                    if (await Task.WhenAny(read, Task.Delay(5000)) != read)
                        throw new TimeoutException("Server response timed out");
                    var response = await read;
                    if (response == null) throw new IOException("Server closed the connection");
                    var envelope = JsonUtility.FromJson<Response>(response);
                    if (envelope == null || envelope.v != 1 || envelope.id != request.id || !envelope.ok)
                        throw new IOException("Invalid or unsuccessful server response: " + response);
                    if (!destroyed) Debug.Log("Native server: " + response);
                }
            }
        }
        catch (Exception error)
        {
            if (!destroyed) Debug.LogError("Native server connection: " + error.Message);
        }
        finally { client?.Close(); }
    }

    private void OnDestroy()
    {
        destroyed = true;
        client?.Close();
    }
}

````

## Tools/unity/Package/MAPS.md

SHA-256: `4b647dc14d14981701a54c4310ea2a93e84f886f76c4c30811d43a10078c1d78`

````markdown
# Danh sách map đã xuất

289 map; 27,400 vị trí spawn (3,502 NPC tương tác, 23,898 entity không tương tác).

Đây là terrain và vị trí ban đầu, không phải AI/gameplay đang chạy. Tên giữ theo bảng server.

| ID | Map | Loại scene | Kích thước | NPC | Entity khác | Cảnh báo / entity thiếu template |
|---:|---|---:|---|---:|---:|---|
| 0 | 洛阳 | 0 | 512×512 | 214 | 5 | 0 / 0 |
| 1 | 苏州 | 0 | 512×512 | 152 | 16 | 0 / 0 |
| 2 | 大理 | 0 | 320×320 | 172 | 8 | 0 / 0 |
| 3 | 嵩山 | 0 | 320×320 | 11 | 277 | 0 / 0 |
| 4 | 太湖 | 0 | 320×320 | 21 | 0 | 0 / 0 |
| 5 | 镜湖 | 0 | 320×320 | 5 | 0 | 0 / 0 |
| 6 | 无量山 | 0 | 320×320 | 22 | 317 | 0 / 0 |
| 7 | 剑阁 | 0 | 320×320 | 15 | 385 | 0 / 0 |
| 8 | 敦煌 | 0 | 320×320 | 21 | 265 | 0 / 0 |
| 9 | 少林寺 | 0 | 192×192 | 23 | 6 | 0 / 2 |
| 10 | 丐帮总舵 | 0 | 192×192 | 20 | 8 | 0 / 0 |
| 11 | 光明殿 | 0 | 192×192 | 30 | 8 | 0 / 0 |
| 12 | 武当山 | 0 | 144×224 | 23 | 6 | 0 / 0 |
| 13 | 天龙寺 | 0 | 192×192 | 28 | 2 | 0 / 2 |
| 14 | 淩波洞 | 0 | 192×192 | 19 | 6 | 0 / 0 |
| 15 | 峨嵋山 | 0 | 192×192 | 28 | 7 | 0 / 1 |
| 16 | 星宿海 | 0 | 192×192 | 21 | 8 | 0 / 0 |
| 17 | 天山 | 0 | 192×192 | 33 | 7 | 0 / 0 |
| 18 | 雁南 | 0 | 320×320 | 17 | 126 | 0 / 0 |
| 19 | 雁北 | 0 | 320×320 | 24 | 101 | 0 / 0 |
| 20 | 草原 | 0 | 320×320 | 15 | 161 | 0 / 0 |
| 21 | 辽西 | 0 | 320×320 | 13 | 140 | 0 / 0 |
| 22 | 长白山 | 0 | 320×320 | 17 | 133 | 0 / 0 |
| 23 | 黄龙府 | 0 | 320×320 | 13 | 133 | 0 / 0 |
| 24 | 洱海 | 0 | 320×320 | 11 | 135 | 0 / 0 |
| 25 | 苍山 | 0 | 320×320 | 14 | 153 | 0 / 0 |
| 26 | 石林 | 0 | 320×320 | 11 | 139 | 0 / 0 |
| 27 | 玉溪 | 0 | 320×320 | 9 | 136 | 0 / 0 |
| 28 | 南诏 | 0 | 320×320 | 18 | 113 | 0 / 0 |
| 29 | 苗疆 | 0 | 320×320 | 16 | 143 | 0 / 0 |
| 30 | 西湖 | 0 | 320×320 | 17 | 127 | 0 / 0 |
| 31 | 龙泉 | 0 | 320×320 | 13 | 133 | 0 / 0 |
| 32 | 武夷 | 0 | 320×320 | 14 | 140 | 0 / 0 |
| 33 | 梅岭 | 0 | 320×320 | 17 | 143 | 0 / 0 |
| 34 | 南海 | 0 | 320×320 | 11 | 108 | 0 / 0 |
| 35 | 琼州 | 0 | 320×320 | 11 | 110 | 0 / 0 |
| 36 | 聚贤庄 | 1 | 128×128 | 47 | 0 | 0 / 0 |
| 37 | 燕子坞 | 1 | 128×128 | 18 | 0 | 0 / 0 |
| 38 | 一品堂 | 1 | 128×128 | 27 | 0 | 0 / 0 |
| 39 | 玄武岛 | 0 | 320×320 | 2 | 257 | 0 / 0 |
| 40 | 预留2 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 43 | 木人巷 | 1 | 128×128 | 0 | 89 | 0 / 0 |
| 44 | 珍珑棋局 | 1 | 128×128 | 1 | 0 | 0 / 0 |
| 45 | 水牢 | 1 | 192×192 | 0 | 12 | 0 / 0 |
| 46 | 沙漠要塞 | 1 | 128×128 | 0 | 0 | 0 / 0 |
| 47 | 宋辽边境 | 1 | 128×128 | 0 | 51 | 0 / 0 |
| 48 | 野外匪寨 | 1 | 128×128 | 0 | 0 | 0 / 0 |
| 49 | 竹林 | 1 | 128×128 | 0 | 81 | 0 / 0 |
| 50 | 小木人巷2 | 0 | 96×96 | 0 | 82 | 0 / 0 |
| 51 | 光明洞 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 52 | 逍遥谷底 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 53 | 灵性峰 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 54 | 丐帮酒窖 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 55 | 桃花阵 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 56 | 塔林 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 57 | 五神洞 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 58 | 墓穴 | 1 | 64×64 | 0 | 6 | 0 / 0 |
| 59 | 塔底 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 60 | 折梅峰 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 61 | 小木人巷 | 0 | 96×96 | 0 | 82 | 0 / 0 |
| 62 | 后花园 | 0 | 128×128 | 0 | 57 | 0 / 0 |
| 63 | 集市 | 1 | 64×64 | 0 | 11 | 0 / 0 |
| 64 | 矿场 | 1 | 64×64 | 0 | 20 | 0 / 0 |
| 65 | 牧场 | 1 | 128×128 | 1 | 16 | 0 / 0 |
| 66 | 书阁 | 1 | 64×64 | 0 | 20 | 0 / 0 |
| 67 | 市集 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 68 | 聚贤庄 | 1 | 128×128 | 13 | 0 | 0 / 0 |
| 69 | 燕子坞 | 1 | 128×128 | 26 | 0 | 0 / 0 |
| 70 | 一品堂 | 1 | 128×128 | 4 | 0 | 0 / 0 |
| 71 | 大理2 | 0 | 320×320 | 172 | 8 | 0 / 0 |
| 72 | 大理3 | 0 | 320×320 | 172 | 8 | 0 / 0 |
| 73 | 无量山2 | 0 | 320×320 | 22 | 317 | 0 / 0 |
| 74 | 无量山3 | 0 | 320×320 | 22 | 317 | 0 / 0 |
| 75 | 剑阁2 | 0 | 320×320 | 15 | 385 | 0 / 0 |
| 76 | 剑阁3 | 0 | 320×320 | 15 | 385 | 0 / 0 |
| 77 | 地府 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 81 | 小木人巷3 | 0 | 96×96 | 0 | 82 | 0 / 0 |
| 82 | 后花园2 | 0 | 128×128 | 0 | 57 | 0 / 0 |
| 84 | 万劫谷 | 1 | 128×128 | 14 | 0 | 0 / 0 |
| 85 | 擂鼓山 | 1 | 128×128 | 27 | 0 | 0 / 0 |
| 86 | 雁南山洞 | 0 | 128×192 | 0 | 111 | 0 / 0 |
| 87 | 雁北山洞 | 0 | 128×192 | 0 | 118 | 0 / 0 |
| 88 | 西湖山洞 | 0 | 128×192 | 0 | 118 | 0 / 0 |
| 89 | 苍山山洞 | 0 | 128×192 | 0 | 118 | 0 / 0 |
| 90 | 光明洞 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 91 | 逍遥谷底 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 92 | 灵性峰 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 93 | 丐帮酒窖 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 94 | 桃花阵 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 95 | 塔林 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 96 | 五神洞 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 97 | 折梅峰 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 98 | 塔底 | 1 | 64×64 | 0 | 12 | 0 / 0 |
| 99 | 光明洞 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 100 | 逍遥谷底 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 101 | 灵性峰 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 102 | 丐帮酒窖 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 103 | 桃花阵 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 104 | 塔林 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 105 | 五神洞 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 106 | 折梅峰 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 107 | 塔底 | 1 | 64×64 | 0 | 9 | 0 / 0 |
| 108 | 市集 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 109 | 市集 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 110 | 工地 | 1 | 64×64 | 0 | 10 | 0 / 0 |
| 111 | 校场 | 1 | 64×64 | 0 | 20 | 0 / 0 |
| 112 | 衙门 | 1 | 64×64 | 0 | 15 | 0 / 0 |
| 113 | 三春幻境 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 114 | 三夏幻境 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 115 | 三秋幻境 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 116 | 三冬幻境 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 117 | 边关阵地山头 | 1 | 64×64 | 0 | 11 | 0 / 0 |
| 118 | 边关阵地山头 | 1 | 64×64 | 0 | 11 | 0 / 0 |
| 119 | 边关阵地山头 | 1 | 64×64 | 0 | 11 | 0 / 0 |
| 120 | 边关阵地山头 | 1 | 64×64 | 0 | 11 | 0 / 0 |
| 121 | 西湖 | 0 | 320×320 | 31 | 1 | 0 / 0 |
| 122 | 藏经阁 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 123 | 宝藏洞一层 | 0 | 256×256 | 3 | 316 | 0 / 0 |
| 124 | 考场 | 1 | 64×64 | 0 | 5 | 0 / 0 |
| 125 | 华山绝顶 | 0 | 256×256 | 37 | 0 | 0 / 0 |
| 126 | 宝藏洞二层 | 0 | 256×256 | 1 | 184 | 0 / 0 |
| 127 | 贼寇营地 | 1 | 128×128 | 0 | 30 | 0 / 0 |
| 128 | 藏经阁 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 129 | 藏经阁 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 130 | 少林寺 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 131 | 丐帮总舵 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 132 | 光明殿 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 133 | 武当山 | 1 | 144×224 | 0 | 30 | 0 / 0 |
| 134 | 天龙寺 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 135 | 淩波洞 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 136 | 峨嵋山 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 137 | 星宿海 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 138 | 天山 | 1 | 192×192 | 0 | 30 | 0 / 0 |
| 139 | 少林寺 | 0 | 192×192 | 0 | 85 | 0 / 0 |
| 140 | 丐帮总舵 | 0 | 192×192 | 0 | 111 | 0 / 0 |
| 141 | 光明殿 | 0 | 192×192 | 0 | 94 | 0 / 0 |
| 142 | 武当山 | 0 | 144×224 | 0 | 82 | 0 / 0 |
| 143 | 天龙寺 | 0 | 192×192 | 0 | 83 | 0 / 0 |
| 144 | 淩波洞 | 0 | 192×192 | 0 | 50 | 0 / 0 |
| 145 | 峨嵋山 | 0 | 192×192 | 0 | 92 | 0 / 0 |
| 146 | 星宿海 | 0 | 192×192 | 0 | 81 | 0 / 0 |
| 147 | 天山 | 0 | 192×192 | 0 | 67 | 0 / 0 |
| 148 | 宝藏洞三层 | 0 | 256×256 | 1 | 248 | 0 / 0 |
| 149 | 宝藏洞四层 | 0 | 256×256 | 1 | 245 | 0 / 0 |
| 150 | 宝藏洞五层 | 0 | 256×256 | 1 | 205 | 0 / 0 |
| 151 | 监狱 | 0 | 96×96 | 1 | 0 | 0 / 0 |
| 152 | 比武会场 | 1 | 256×256 | 0 | 0 | 0 / 0 |
| 156 | 大军草料场 | 0 | 256×256 | 0 | 412 | 0 / 0 |
| 157 | 苗人洞 | 0 | 256×256 | 1 | 371 | 0 / 0 |
| 158 | 圣兽山 | 0 | 256×256 | 0 | 188 | 0 / 0 |
| 159 | 燕王古墓一层 | 0 | 128×128 | 1 | 40 | 0 / 0 |
| 160 | 燕王古墓二层 | 0 | 128×128 | 0 | 35 | 0 / 0 |
| 161 | 燕王古墓三层 | 0 | 128×128 | 0 | 50 | 0 / 0 |
| 162 | 燕王古墓四层 | 0 | 128×128 | 0 | 70 | 0 / 0 |
| 163 | 燕王古墓五层 | 0 | 128×128 | 1 | 81 | 0 / 0 |
| 164 | 燕王古墓六层 | 0 | 128×128 | 0 | 65 | 0 / 0 |
| 165 | 燕王古墓七层 | 0 | 128×128 | 0 | 71 | 0 / 0 |
| 166 | 燕王古墓八层 | 0 | 128×128 | 0 | 99 | 0 / 0 |
| 167 | 燕王古墓九层 | 0 | 128×128 | 0 | 45 | 0 / 0 |
| 168 | 山洞船坞 | 0 | 256×256 | 0 | 277 | 0 / 0 |
| 169 | 剑冢 | 0 | 256×256 | 0 | 215 | 0 / 0 |
| 170 | 摩崖洞 | 0 | 256×256 | 2 | 311 | 0 / 0 |
| 171 | 野人沟 | 0 | 256×256 | 0 | 271 | 0 / 0 |
| 172 | 温泉洞 | 0 | 256×256 | 0 | 257 | 0 / 0 |
| 173 | 黄龙洞 | 0 | 256×256 | 0 | 494 | 0 / 0 |
| 174 | 水晶湖 | 0 | 256×256 | 0 | 351 | 0 / 0 |
| 175 | 先王坟 | 0 | 256×256 | 1 | 269 | 0 / 0 |
| 176 | 天坑树洞 | 0 | 256×256 | 0 | 283 | 0 / 0 |
| 177 | 桃花源 | 0 | 256×256 | 1 | 437 | 0 / 0 |
| 178 | 海贼洞 | 0 | 256×256 | 0 | 327 | 0 / 0 |
| 179 | 雪狼湖 | 0 | 256×256 | 0 | 538 | 0 / 0 |
| 181 | 钱庄 | 0 | 128×128 | 4 | 0 | 0 / 0 |
| 182 | 后花园3 | 0 | 128×128 | 0 | 57 | 0 / 0 |
| 183 | 藏经阁 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 185 | 藏经阁 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 186 | 楼兰 | 0 | 320×320 | 86 | 2 | 0 / 0 |
| 187 | 擂台 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 188 | 银皑雪原 | 0 | 256×256 | 5 | 326 | 0 / 0 |
| 189 | 镜湖匪寨 | 1 | 192×192 | 1 | 0 | 0 / 0 |
| 190 | 燕子坞 | 1 | 256×256 | 0 | 0 | 0 / 0 |
| 191 | 凤凰古城 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 192 | 擂台 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 193 | 大理休息室 | 0 | 64×64 | 2 | 0 | 0 / 0 |
| 194 | 寒玉谷 | 0 | 96×96 | 1 | 3 | 0 / 0 |
| 195 | 擂台 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 196 | 擂台 | 1 | 64×64 | 0 | 0 | 0 / 0 |
| 200 | 古铜雀台 | 0 | 192×192 | 0 | 0 | 0 / 0 |
| 201 | 撒马尔罕 | 0 | 256×256 | 0 | 134 | 0 / 0 |
| 202 | 圣火宫 | 0 | 128×128 | 0 | 98 | 0 / 0 |
| 203 | 千仞黄山 | 0 | 128×128 | 0 | 0 | 0 / 0 |
| 313 | 帮会BOSS | 0 | 64×64 | 0 | 20 | 0 / 0 |
| 314 | 金猪赠礼 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 315 | 尸王争夺 | 0 | 64×64 | 0 | 0 | 0 / 0 |
| 317 | 擂台 | 0 | 64×64 | 0 | 0 | 0 / 0 |
| 377 | 西湖1 | 0 | 320×320 | 31 | 1 | 0 / 0 |
| 394 | 圣兽山1 | 0 | 256×256 | 0 | 188 | 0 / 0 |
| 400 | 秦皇地宫一层 | 0 | 256×256 | 3 | 202 | 0 / 0 |
| 401 | 秦皇地宫二层 | 0 | 256×256 | 3 | 300 | 0 / 0 |
| 402 | 秦皇地宫三层 | 0 | 256×256 | 0 | 156 | 0 / 0 |
| 404 | 毒障泽地 | 1 | 256×256 | 1 | 0 | 0 / 0 |
| 405 | 熔岩之地 | 1 | 256×256 | 0 | 0 | 0 / 0 |
| 406 | 玄武岛 | 1 | 320×320 | 0 | 0 | 0 / 0 |
| 407 | 楼兰藏宝洞 | 1 | 128×128 | 1 | 0 | 0 / 0 |
| 409 | 亮马驿 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 410 | 生死擂台 | 0 | 64×64 | 0 | 1 | 0 / 0 |
| 414 | 竞技场 | 0 | 192×192 | 17 | 0 | 0 / 0 |
| 415 | 盐湖 | 0 | 256×256 | 9 | 245 | 0 / 0 |
| 416 | 缥缈峰 | 1 | 192×192 | 0 | 0 | 0 / 0 |
| 418 | 洛阳第一休息室 | 0 | 64×64 | 2 | 0 | 0 / 0 |
| 419 | 洛阳第二休息室 | 0 | 64×64 | 2 | 0 | 0 / 0 |
| 420 | 束河古镇 | 0 | 320×320 | 58 | 4 | 0 / 0 |
| 423 | 火焰山 | 0 | 256×256 | 18 | 114 | 0 / 0 |
| 424 | 高昌 | 0 | 256×256 | 10 | 127 | 0 / 0 |
| 425 | 塔里木 | 0 | 256×256 | 10 | 98 | 0 / 0 |
| 427 | 塔克拉玛干 | 0 | 128×128 | 0 | 90 | 0 / 0 |
| 431 | 大宛 | 0 | 256×256 | 4 | 122 | 0 / 0 |
| 432 | 汗血岭 | 0 | 128×128 | 0 | 84 | 0 / 0 |
| 433 | 昆仑山 | 0 | 256×256 | 0 | 325 | 0 / 0 |
| 434 | 昆仑福地 | 0 | 128×128 | 0 | 79 | 0 / 0 |
| 492 | 擂台 | 0 | 64×64 | 0 | 0 | 0 / 0 |
| 495 | 唐家堡 | 0 | 192×192 | 14 | 8 | 0 / 0 |
| 514 | 野猪农场 | 1 | 128×128 | 0 | 0 | 0 / 0 |
| 515 | 圣兽山 | 1 | 256×256 | 0 | 0 | 0 / 0 |
| 516 | 牡丹碗 | 1 | 128×128 | 1 | 0 | 0 / 0 |
| 517 | 白沙盐坑 | 0 | 128×128 | 1 | 110 | 0 / 0 |
| 518 | 苏州休息室 | 0 | 64×64 | 2 | 0 | 0 / 0 |
| 519 | 火焰谷 | 0 | 128×128 | 0 | 0 | 0 / 0 |
| 520 | 高昌迷宫 | 0 | 128×128 | 0 | 0 | 0 / 0 |
| 531 | 清源 | 0 | 320×320 | 0 | 0 | 0 / 0 |
| 532 | 清源山洞 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 538 | 秦皇地宫四层 | 0 | 256×256 | 0 | 317 | 0 / 0 |
| 539 | 凤凰陵墓 | 1 | 128×128 | 0 | 0 | 0 / 0 |
| 548 | 宋辽战场 | 0 | 320×320 | 0 | 4 | 0 / 0 |
| 550 | 宋辽战场休息室 | 0 | 64×64 | 2 | 0 | 0 / 0 |
| 560 | 钧天城 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 561 | 罗浮城 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 562 | 潮京城 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 573 | 漠南青原 | 0 | 256×256 | 1 | 101 | 0 / 0 |
| 574 | 忘川花海 | 0 | 256×256 | 1 | 101 | 0 / 0 |
| 575 | 天岐南淮 | 0 | 256×256 | 1 | 137 | 1 / 0 |
| 581 | 通天塔地宫 | 0 | 512×512 | 0 | 1176 | 0 / 0 |
| 582 | 通天塔一层 | 0 | 512×512 | 0 | 133 | 0 / 0 |
| 583 | 通天塔二层 | 0 | 512×512 | 0 | 115 | 0 / 0 |
| 584 | 通天塔三层 | 0 | 512×512 | 0 | 180 | 0 / 0 |
| 585 | 通天塔塔顶 | 0 | 512×512 | 0 | 5 | 0 / 0 |
| 713 | 翠云山 | 0 | 256×256 | 1 | 0 | 0 / 0 |
| 714 | 水帘洞 | 0 | 192×192 | 1 | 0 | 0 / 0 |
| 715 | 永宁城 | 0 | 256×256 | 1 | 0 | 0 / 0 |
| 814 | 凌云窟 | 0 | 192×192 | 0 | 0 | 0 / 0 |
| 818 | 天下会 | 0 | 512×512 | 0 | 0 | 0 / 0 |
| 819 | 剑池 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 1299 | 秦皇地宫四层 | 4 | 256×256 | 0 | 317 | 0 / 0 |
| 1303 | 秦皇地宫四层-2 | 0 | 256×256 | 0 | 317 | 0 / 0 |
| 1311 | 洛阳-2 | 0 | 512×512 | 214 | 5 | 0 / 0 |
| 1312 | 苏州-2 | 0 | 512×512 | 152 | 16 | 0 / 0 |
| 1313 | 敦煌-2 | 0 | 320×320 | 21 | 265 | 0 / 0 |
| 1314 | 敦煌-3 | 0 | 320×320 | 21 | 265 | 0 / 0 |
| 1315 | 洛阳-3 | 0 | 512×512 | 214 | 5 | 0 / 0 |
| 1316 | 洛阳-4 | 0 | 512×512 | 214 | 5 | 0 / 0 |
| 1317 | 敦煌-4 | 0 | 320×320 | 21 | 265 | 0 / 0 |
| 1318 | 敦煌-5 | 0 | 320×320 | 21 | 265 | 0 / 0 |
| 1319 | 敦煌-6 | 0 | 320×320 | 21 | 265 | 0 / 0 |
| 1320 | 大理4 | 0 | 320×320 | 172 | 8 | 0 / 0 |
| 1321 | 大理5 | 0 | 320×320 | 172 | 8 | 0 / 0 |
| 1322 | 嵩山2 | 0 | 320×320 | 11 | 277 | 0 / 0 |
| 1326 | 恶人谷 | 1 | 256×256 | 12 | 13 | 0 / 0 |
| 1328 | 慕容山庄 | 1 | 192×192 | 0 | 110 | 1 / 0 |
| 1358 | 慕容山庄 | 0 | 192×192 | 8 | 0 | 0 / 0 |
| 1500 | 地府-2 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 2218 | 地府-3 | 0 | 64×64 | 1 | 0 | 0 / 0 |
| 764 | 通天塔地宫 | 0 | 512×512 | 0 | 1176 | 0 / 0 |
| 765 | 通天塔一层 | 0 | 512×512 | 0 | 133 | 0 / 0 |
| 766 | 通天塔二层 | 0 | 512×512 | 0 | 115 | 0 / 0 |
| 767 | 通天塔三层 | 0 | 512×512 | 0 | 180 | 0 / 0 |
| 768 | 通天塔塔顶 | 0 | 512×512 | 0 | 5 | 0 / 0 |
| 1051 | 凌霄梦城 | 0 | 256×256 | 0 | 0 | 0 / 0 |
| 2220 | 唐门 | 0 | 192×192 | 24 | 0 | 0 / 0 |
| 2221 | 鬼谷 | 0 | 192×192 | 34 | 0 | 0 / 0 |
| 2222 | 桃花岛 | 0 | 320×320 | 27 | 0 | 0 / 0 |
| 2223 | 绝情谷 | 0 | 512×512 | 19 | 0 | 0 / 0 |
| 4511 | 汴京 | 0 | 1024×1024 | 1 | 0 | 0 / 0 |
| 987 | 恶人谷 | 0 | 256×256 | 12 | 13 | 0 / 0 |
| 755 | 汴京 | 0 | 1024×1024 | 1 | 0 | 0 / 0 |
| 775 | 汴京2线 | 0 | 1024×1024 | 1 | 0 | 0 / 0 |
| 776 | 汴京3线 | 0 | 1024×1024 | 1 | 0 | 0 / 0 |
| 779 | 汴京4线 | 0 | 1024×1024 | 1 | 0 | 0 / 0 |
| 780 | 汴京5线 | 0 | 1024×1024 | 1 | 0 | 0 / 0 |
| 785 | 汴京6线 | 0 | 1024×1024 | 1 | 0 | 0 / 0 |
| 1007 | 冰雪不夜城 | 0 | 320×320 | 1 | 0 | 0 / 0 |

## Scene đang bật chưa xuất được

226 mục: 220 slot thành bang (type 4) và 6 scene phó bản thiếu hoặc không khớp tài nguyên. Chi tiết đầy đủ trong PORT-REPORT.json.

284 scene đang tắt không được tự bật hay đưa vào catalog.

````

## Tools/unity/Package/README.md

SHA-256: `c773dc67b988872b7f59443c9eed29d68b6a84e0ba8fb095a50400584ebe391c`

````markdown
# Dragon Port — Unity map / NPC / monster import

Bản mở rộng gồm **289 map thật và 27,400 vị trí NPC/quái**.
Xem MAPS.md để chọn map theo ID. Không phải toàn bộ game TLBB đã chạy trong Unity.

## Import vào project đang có

1. Sao lưu/commit project Unity của bạn trước khi nhập.
2. Giải nén ZIP, copy thư mục `Assets/DragonPort` vào `Assets` của project.
   Bộ script dùng API Unity thông thường, không có dependency npm/NuGet.
   Mục tiêu Unity 2021.3 LTS trở lên; chưa compile/run trong Unity Editor ở cloud.
3. Chờ Unity compile. Menu **Tools → Dragon Port → Browse Maps**, tìm ID/tên rồi
   chọn **Import this map**. Importer tạo GameObject và material cơ bản.
4. Hoặc dùng **Import Exported Map** để chọn `<ID>.json` trực tiếp.
   Ví dụ 0=Lạc Dương, 1=Tô Châu, 2=Đại Lý, 6=Vô Lượng Sơn, 9=Thiếu Lâm.
5. Trên `DragonWorldLoader`, mở menu component → **Build World** để xem trong
   Scene view, hoặc bấm Play. Chọn terrain tile rồi F để focus.
   Thêm camera/light phù hợp scene của bạn; importer không sửa camera đang có.
6. Nếu chỉ xem map offline: tắt component `DragonWorldSession`.
   Nếu muốn lấy spawn qua server: chạy gateway bên repository server như dưới đây.

## Kết nối native server

Trên máy có source server, chạy từ root repository:

```bash
python3 Tools/server/run_unity_gateway.py --world-root Build/unity-world
```

Cần build native trước bằng `bash Tools/server/build_native.sh` nếu chưa có binary.
`DragonWorldSession` dùng mặc định `127.0.0.1:15800`; đổi Host nếu Unity chạy máy khác
và cấu hình địa chỉ bind gateway phù hợp mạng phát triển. Gateway chưa có auth/TLS.
Session kiểm map ID/kích thước, lấy spawn theo trang và cập nhật vị trí đã import.
Đây là snapshot ban đầu, không phải stream di chuyển/AI của server game cũ.

## Phạm vi bản mở rộng

- 289 map, 3.502 NPC tương tác + 23.898 entity không tương tác; 399.983 vị trí vật thể cảnh.
- 220 slot thành bang và 6 phó bản thiếu/không khớp tài nguyên được ghi rõ trong PORT-REPORT.json.
- Không tự bật 284 scene đang tắt. Loại 1 là template phó bản, chưa phải phiên instance đang chạy.
- Năm entity thiếu template ở ba map bị bỏ qua giống source server; hai map khác có tọa độ spawn ngoài biên.
  Cảnh báo giữ trong bundle và hiển thị ở map browser; không tự chỉnh dữ liệu nguồn.
- Bốn map môn phái 2220–2223 dùng resource alias từ DBC client, chỉ khi hash navmesh server/client trùng.

## Hai map của bản đầu (vẫn giữ trong gói)

| Map | Terrain | NPC tương tác | Entity loại monster | Vật thể cảnh có vị trí |
|---|---:|---:|---:|---:|
| Đại Lý | 320×320 ô | 172 | 8 | 5.662 |
| Vô Lượng Sơn | 320×320 ô | 22 | 317 | 2.274 |

- Terrain dựng thành mesh tile có MeshCollider; giữ height sample, đường chéo
  tam giác và lỗ theo `GridInfo`. Chưa chuyển lớp texture/lightmap terrain.
- NPC/quái giữ template/model ID, tên, tọa độ, hướng, script ID, AI type,
  HP/level và thời gian hồi sinh từ dữ liệu nguồn. Phân loại theo cờ
  `是否可以交互` mà server cũ dùng; không đảm bảo mọi entity không tương tác là địch.
- Đại Lý có 37 section spawn thiếu/đã tắt trong dải `monstercount`; exporter
  bỏ qua như vòng đọc server và ghi danh sách vào JSON. Vô Lượng Sơn không có.
- Tọa độ Unity dùng trực tiếp lưới game X/Z và raw height Y. Vị trí vật thể
  OGRE được chuyển bằng `(position-sourceOrigin)/sourceScale`.

## Prefab, đồ họa và animation

**Đã có gói mesh/animation gốc và combat PvE cơ bản riêng: xem [ART-COMBAT.md](ART-COMBAT.md).**
Gói core map này cần nhập thêm ZIP art để hiện model gốc. Nếu chưa có binding,
NPC/quái hiện bằng capsule vàng/đỏ để kiểm vị trí. Nhà cửa/cây chưa có binding
không được vẽ; vị trí và resource name vẫn có trong JSON, không bị bỏ khỏi data.
Tên tiếng Trung có thể cần font hỗ trợ glyph; có thể tắt Show Labels.

Tạo **Assets → Create → Dragon Port → Prefab Library**, gán cho loader:

- `actors`: modelId → prefab nhân vật đã có mesh/rig/animation Unity.
- `scenery`: resource nguyên gốc (`...mesh`) → prefab cảnh.

Prefab phải được chuẩn hóa về đơn vị game grid (100 đơn vị OGRE = 1 grid trong
hai map này), pivot ở chân/điểm gốc và hướng +Z. Cần kiểm hình thực tế trên Mac.
Không có NavMesh Unity trong gói; MeshCollider không thay thế walkability/nav server.

## Chưa port

Toàn bộ AI/skill game cũ, patrol, tương tác NPC/nhiệm vụ,
đăng nhập/lưu nhân vật và streaming AOI. Thông số đã được giữ để nối tiếp vào
logic server. Combat PvE phát triển được mô tả trong ART-COMBAT.md và có thẩm quyền ở server.
`simulationReady=false` trong giao thức và bundle là chủ ý.

## Export lại khi thêm map

Trong repository server:

```bash
python3 Tools/unity/fetch_world_data.py --maps dali_new_320,wuliang
python3 Tools/unity/export_world.py --server-root Server --client-data Assets/CanonicalCY/Data --scenes 2,6 --out Build/unity-world
python3 Tools/unity/package_world.py
```

Các Python tool trong ZIP là bản sao để tham khảo; lệnh trên giả định chạy từ
repository gốc. Gói cũng kèm manifest trong `Publication` cho downloader.
Downloader đọc ZIP qua HTTP Range, kiểm CRC và SHA-256 member theo index bên trong.
**Chưa tải/kiểm SHA-256 toàn bộ archive 12 GB.** Gói data ngoài giấy phép phần mềm;
xem DATA-NOTICE và SOURCE-AUDIT đi kèm. Không có credential hoặc database riêng.

## Tái tạo bản mở rộng

```bash
python3 Tools/unity/port_all_worlds.py
python3 Tests/server/test_world_batch.py
python3 Tools/unity/package_world.py
```

Dùng `--no-download` nếu các input đã có và đã kiểm checksum trong lần trước.
Bộ tải dùng khoảng 185 MiB range cho phần còn thiếu ở lần mở rộng này, kiểm
6.666 member; không tải hết 12 GB. `world.list` hiện phân trang giống entities
(default 50, tối đa 100), trả total/nextOffset. Gateway chỉ giữ tối đa 4 world
trong cache, tải khi được yêu cầu, không nạp tất cả map vào RAM lúc khởi động.

````

## Tools/unity/art/asset_source.py

SHA-256: `36acaa120b0a59644eadf629d4948ee66fb5dbb06f470dbd34e99cf1a7e5c8e3`

````python
"""Public archive access and GBK/mojibake resource resolution, preserving source bytes."""
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import zipfile
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cached_remote_zip import CachedRemoteZip

ROOT=Path(__file__).resolve().parents[3]

def variants(value):
    value=value.replace('\\','/').strip().strip('"')
    result={value.casefold()}
    for encoding in ['latin1','cp1252']:
        try:result.add(value.encode(encoding).decode('gb18030').casefold())
        except UnicodeError:pass
    return result

class AssetSource:
    def __init__(self,root=ROOT):
        self.root=root
        m=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
        endpoint='https://drive.usercontent.google.com/download'
        fid=re.search('/d/([^/]+)',m['google_drive_url'])[1]
        with urllib.request.urlopen(endpoint+'?'+urllib.parse.urlencode(dict(id=fid,export='download')),timeout=30) as r:page=r.read(100000).decode()
        params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
        if params.get('id')!=fid or params.get('confirm')!='t':raise ValueError('Unrecognized download form')
        self.remote=CachedRemoteZip(endpoint+'?'+urllib.parse.urlencode(params),m['bytes'],root/'Build/art-source-cache.zip')
        self.zip=zipfile.ZipFile(self.remote)
        self.index={r['path']:r for r in json.loads(self.zip.read('DATA-FILES.json'))}
        self.lookup={}
        for path in self.index:
            prefix='Assets/CanonicalCY/Data/'
            if not path.startswith(prefix):continue
            relative=path[len(prefix):];parts=relative.split('/',1)
            if len(parts)<2:continue
            for name in [parts[1],Path(relative).name]:
                for key in variants(name):self.lookup.setdefault(key,[]).append(path)
        self.ambiguities={};self.verified={}
    def resolve(self,name):
        matches=set()
        for key in variants(name):matches.update(self.lookup.get(key,[]))
        if not matches:return None
        def order(path):
            folder=path.split('/')[3]
            kind=re.match(r'(.*?)(\d*)(Folder)$',folder)
            rank=(int(kind[2]) if kind and kind[2] else 1)
            return rank,path.encode('utf8')
        chosen=sorted(matches,key=order)[-1]
        if len({self.index[p]['sha256'] for p in matches})>1:
            self.ambiguities[name]=dict(chosen=chosen,alternatives=sorted(matches),rule='last resource folder/location, as documented by existing validator')
        return chosen
    def fetch(self,names):
        paths=sorted(set(p for p in names if p))
        pending=[]
        for name in paths:
            if name not in self.index:raise ValueError('Unknown archive member: '+name)
            destination=(self.root/name).resolve()
            if not destination.is_relative_to(self.root.resolve()):raise ValueError('Unsafe archive path')
            if destination.exists():
                if hashlib.sha256(destination.read_bytes()).hexdigest()!=self.index[name]['sha256']:raise ValueError('Local file differs; refusing overwrite: '+name)
            else:pending.append(self.zip.getinfo(name))
        spans=[]
        for info in sorted(pending,key=lambda i:i.header_offset):
            a=info.header_offset;b=min(self.remote.size,a+30+len(info.filename.encode('utf8'))+len(info.extra)+info.compress_size+512)
            if spans and a-spans[-1][1]<=32768 and b-spans[-1][0]<=8*1024*1024:spans[-1]=(spans[-1][0],max(b,spans[-1][1]))
            else:spans.append((a,b))
        if spans:print(f'Fetching {len(pending)} art members in {len(spans)} ranges ({sum(b-a for a,b in spans)/1048576:.1f} MiB)',flush=True)
        self.remote.prefetch(spans)
        for i,name in enumerate(paths,1):
            destination=self.root/name
            if not destination.exists():
                data=self.zip.read(name)
                if len(data)!=self.index[name]['bytes'] or hashlib.sha256(data).hexdigest()!=self.index[name]['sha256']:raise ValueError('Art member checksum mismatch: '+name)
                destination.parent.mkdir(parents=True,exist_ok=True)
                with destination.open('xb') as stream:stream.write(data)
            self.verified[name]=self.index[name]
            if i%1000==0:print(f'Art members checked: {i}/{len(paths)}',flush=True)
    def close(self):
        self.zip.close()
        if self.remote.cache.exists():self.remote.cache.unlink()

````

## Tools/unity/art/export_art.py

SHA-256: `4395d5c9c27c24789ada6e4c75a9b40be7770f5a649436b2df2a769d1d1e6120`

````python
#!/usr/bin/env python3
"""Convert original referenced Ogre meshes and linked skeletal animations into Unity import data."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
from PIL import Image
from asset_source import AssetSource, ROOT, variants
from ogre_binary import mesh,skeleton,text


def dbc(path):
    raw=path.read_bytes();magic,nf,nr,poolsize=struct.unpack_from('<4I',raw)
    if magic!=0xDDBBCC00 or len(raw)!=16+nf*4+nf*nr*4+poolsize:raise ValueError('Invalid DBC: '+str(path))
    types=struct.unpack_from('<'+'I'*nf,raw,16);base=16+4*nf;pool=raw[base+nf*nr*4:];rows={}
    for r in range(nr):
        values=struct.unpack_from('<'+'I'*nf,raw,base+r*nf*4);out=[]
        for t,v in zip(types,values):
            if t==2:out.append(text(pool[v:pool.index(b'\0',v)]))
            elif t==1:out.append(struct.unpack('<f',struct.pack('<I',v))[0])
            else:out.append(struct.unpack('<i',struct.pack('<I',v))[0])
        rows[out[0]]=out
    return rows


def materials(raw):
    result={};header=None;body=[];depth=0;opened=False
    for line in raw.splitlines(keepends=True):
        clean=line.split(b'//',1)[0].strip()
        if header is None:
            if not clean.startswith(b'material '):continue
            header=clean[9:].split(b'{',1)[0].strip();body=[line];depth=clean.count(b'{')-clean.count(b'}');opened=b'{' in clean
        else:
            body.append(line);depth+=clean.count(b'{')-clean.count(b'}');opened=opened or b'{' in clean
        if opened and depth==0:
            try:
                parts=header.split(b':',1);name=text(parts[0].strip().strip(b'"'))
                base=text(parts[1].strip().strip(b'"')) if len(parts)>1 else ''
                result.setdefault(name,dict(body=b''.join(body),base=base))
            except UnicodeError:pass
            header=None;body=[];opened=False
    return result


def material_info(name,blocks):
    seen=set();parts=[];current=name
    while current and current not in seen:
        seen.add(current);block=blocks.get(current)
        if not block:break
        parts.append(block['body']);current=block['base']
    combined=b'\n'.join(parts)
    texture=''
    candidates=re.findall(rb'(?m)^\s*set_texture_alias\s+<baseTexture>\s+("[^"]+"|[^\r\n]+)',combined)
    if not candidates:candidates=re.findall(rb'(?m)^\s*texture\s+("[^"]+"|[^\r\n]+)',combined)
    if candidates:
        raw=candidates[0].strip();raw=raw[1:-1] if raw.startswith(b'"') else raw.split()[0]
        try:texture=text(raw)
        except UnicodeError:pass
    alpha=re.search(rb'alpha_rejection\s+greater(?:_equal)?\s+(\d+)',combined)
    transparent=bool(re.search(rb'scene_blend\s+(alpha_blend|src_alpha)',combined))
    return dict(name=name,textureReference=texture,textureFile='',alphaCutoff=int(alpha[1])/255 if alpha else 0,
                transparent=transparent,doubleSided=b'cull_hardware none' in combined,
                shaderApproximation=True,sourceMaterialFound=name in blocks)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--world-root',type=Path,default=ROOT/'Build/unity-world')
    ap.add_argument('--out',type=Path,default=ROOT/'Build/unity-art')
    ap.add_argument('--limit',type=int,help='Optional mesh limit for format diagnostics only')
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    source=AssetSource();failures=[]
    try:
        source.fetch(['Assets/CanonicalCY/Data/ConfigFolder/CharModelEx.txt','Assets/CanonicalCY/Data/MaterialFolder/all.material'])
        models=dbc(ROOT/'Assets/CanonicalCY/Data/ConfigFolder/CharModelEx.txt')
        scenery=set();used_models=set()
        for summary in json.loads((args.world_root/'catalog.json').read_text())['scenes']:
            world=json.loads((args.world_root/f"{summary['sceneId']}.json").read_text())
            scenery.update(r['resource'] for r in world['staticObjects']);used_models.update(r['modelId'] for r in world['entities'])
        requests={};scenery_bindings=[];actor_bindings=[];unresolved_actors=[]
        for name in sorted(scenery):
            path=source.resolve(name)
            if path:requests[path]=name;scenery_bindings.append(dict(resource=name,path=path))
            else:failures.append(dict(kind='missing-scenery-mesh',resource=name))
        for model_id in sorted(used_models):
            row=models.get(model_id)
            if not row:
                unresolved_actors.append(dict(modelId=model_id,reason='CharModelEx row absent'));continue
            object_name=row[1];name=str(Path(object_name).with_suffix('.mesh'))
            path=source.resolve(name)
            if not path:
                unresolved_actors.append(dict(modelId=model_id,objectReference=object_name,reason='all.obj absent and no exact same-name single mesh; multipart composition not inferred'));continue
            requests[path]=name
            actor_bindings.append(dict(modelId=model_id,path=path,objectReference=object_name,importScale=1.0,actionSetFileId=row[20],bindingEvidence='CharModelEx object stem matches mesh name; original all.obj composition/transforms unavailable; unit import scale 1, CharModelEx column 3 is fuse time, not model scale'))
        # Always retain a concrete original animated monster for the combat/animation smoke workflow.
        ape=source.resolve('高山白猿.mesh')
        if ape:requests[ape]='高山白猿.mesh'
        paths=sorted(requests)
        if args.limit:
            paths=([ape] if ape else [])+[p for p in paths if p!=ape][:max(0,args.limit-1)]
        source.fetch(paths)
        converted={};parsed={};skeleton_paths=set()
        for i,path in enumerate(paths,1):
            try:
                result=mesh((ROOT/path).read_bytes());parsed[path]=result
                if result['skeleton']:
                    skel_path=source.resolve(result['skeleton'])
                    if not skel_path:raise ValueError('Linked skeleton missing: '+result['skeleton'])
                    skeleton_paths.add(skel_path)
            except (ValueError,KeyError,IndexError,UnicodeError,struct.error) as e:failures.append(dict(kind='mesh-conversion',path=path,reason=str(e)))
            if i%500==0:print(f'Meshes decoded {i}/{len(paths)}',flush=True)
        source.fetch(skeleton_paths)
        skeletons={};pending=set(skeleton_paths)
        while pending:
            next_paths=set()
            for path in sorted(pending):
                if path in skeletons:continue
                try:
                    result=skeleton((ROOT/path).read_bytes());skeletons[path]=result
                    for link in result['links']:
                        linked=source.resolve(link['name'])
                        if not linked:raise ValueError('Animation link absent: '+link['name'])
                        if linked not in skeletons:next_paths.add(linked)
                except (ValueError,KeyError,IndexError,UnicodeError,struct.error) as e:failures.append(dict(kind='skeleton-conversion',path=path,reason=str(e)))
            source.fetch(next_paths);pending=next_paths
        blocks=materials((ROOT/'Assets/CanonicalCY/Data/MaterialFolder/all.material').read_bytes())
        mats={};textures=set()
        for result in parsed.values():
            for part in result['parts']:
                name=part['material']
                if name not in mats:
                    info=material_info(name,blocks);mats[name]=info
                    if info['textureReference']:
                        path=source.resolve(info['textureReference'])
                        if path:textures.add(path);info['texturePath']=path
        source.fetch(textures)
        texture_errors=[]
        for i,path in enumerate(sorted(textures),1):
            name=source.index[path]['sha256'][:24]+'.png'
            try:
                target=args.out/name
                if target.exists():
                    with Image.open(target) as cached:cached.verify()
                else:
                    with Image.open(ROOT/path) as image:image.convert('RGBA').save(target)
                for info in mats.values():
                    if info.get('texturePath')==path:info['textureFile']=name
            except (ValueError,OSError) as e:texture_errors.append(dict(path=path,reason=str(e)))
            if i%500==0:print(f'Textures converted {i}/{len(textures)}',flush=True)
        def merge_animations(base,path,visited):
            if path in visited:raise ValueError('Cyclic skeleton animation link')
            visited=visited|{path}
            result=skeletons.get(path)
            if result is None:raise ValueError('Skeleton conversion failed')
            names={a['name'] for a in base['animations']}
            base_names={b['id']:b['name'] for b in base['bones']}
            for link in result['links']:
                linked=source.resolve(link['name']);child=skeletons.get(linked)
                if not child or {b['id']:b['name'] for b in child['bones']}!=base_names:raise ValueError('Linked skeleton bone layout mismatch')
                for animation in child['animations']:
                    if animation['name'] in names:continue
                    copied=json.loads(json.dumps(animation));factor=link['scale']
                    for track in copied['tracks']:
                        for key in track['keys']:key['position']=[v*factor for v in key['position']]
                    base['animations'].append(copied);names.add(copied['name'])
                merge_animations(base,linked,visited)
        for i,(path,result) in enumerate(parsed.items(),1):
            try:
                skel=None
                if result['skeleton']:
                    skel_path=source.resolve(result['skeleton']);skel=json.loads(json.dumps(skeletons.get(skel_path)))
                    if skel is None:raise ValueError('Referenced skeleton failed conversion')
                    merge_animations(skel,skel_path,set())
                    handles={b['id'] for b in skel['bones']}
                    for part in result['parts']:
                        if part['hasSkin']:
                            if any(b not in handles for b,w in zip(part['boneIds'],part['weights']) if w>0):raise ValueError('Skin references missing bone')
                            if any(sum(part['weights'][n:n+4])<.999 for n in range(0,len(part['weights']),4)):raise ValueError('Unweighted vertex in skinned part')
                result['rig']=skel
                result['materials']=[mats[part['material']] for part in result['parts']]
                result['source']=dict(path=path,sha256=source.index[path]['sha256'],unitScale=.01,winding='reversed-for-Unity',axes='XYZ-preserved')
                asset_id=source.index[path]['sha256'][:24];output=args.out/(asset_id+'.dragon.json')
                output.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf8')
                converted[path]=dict(assetId=asset_id,file=output.name,source=path,parts=len(result['parts']),vertices=sum(len(p['positions'])//3 for p in result['parts']),animationCount=len(skel['animations']) if skel else 0)
            except (ValueError,KeyError,IndexError,UnicodeError,TypeError) as e:failures.append(dict(kind='asset-assembly',path=path,reason=str(e)))
            if i%500==0:print(f'Unity art exported {i}/{len(parsed)}',flush=True)
        scenery_bindings=[dict(resource=b['resource'],assetId=converted[b['path']]['assetId']) for b in scenery_bindings if b['path'] in converted]
        actor_bindings=[dict(modelId=b['modelId'],assetId=converted[b['path']]['assetId'],importScale=b['importScale'],actionSetFileId=b['actionSetFileId'],objectReference=b['objectReference'],bindingEvidence=b['bindingEvidence']) for b in actor_bindings if b['path'] in converted]
        report=dict(schema=1,assets=list(converted.values()),sceneryBindings=scenery_bindings,actorBindings=actor_bindings,
            failures=failures,unresolvedActors=unresolved_actors,textureFailures=texture_errors,ambiguities=source.ambiguities,
            allObjPresent=any(p.casefold().endswith('/all.obj') for p in source.index),diagnosticLimit=args.limit,
            integrity='Source member CRC and SHA-256 verified; full archive hash not verified')
        (args.out/'art-catalog.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
        (args.out/'art-source-audit.json').write_text(json.dumps(list(source.verified.values()),ensure_ascii=False,indent=2))
        print(json.dumps(dict(meshes=len(converted),animatedMeshes=sum(v['animationCount']>0 for v in converted.values()),sceneryBindings=len(scenery_bindings),actorBindings=len(actor_bindings),unresolvedActors=len(unresolved_actors),failures=len(failures),textures=len(textures),textureFailures=len(texture_errors),allObjPresent=report['allObjPresent']),ensure_ascii=False),flush=True)
    finally:source.close()

if __name__=='__main__':main()

````

## Tools/unity/art/export_combat_data.py

SHA-256: `56d2a9b5f85a72c62b8c05bc7eeab3245d4791b17e9725daea67d3e3926fb855`

````python
#!/usr/bin/env python3
"""Export source combat stats/nav and verbatim basic combat functions for the new server adapter."""
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
import urllib.request
import urllib.parse
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from export_world import templates,ini,contained
from remote_zip import RemoteZip
ROOT=Path(__file__).resolve().parents[3]

def main():
    source=ROOT/'Server/GameServer/services/scene/skill/combat_core.lua'
    raw=source.read_text()
    methods=['calculate_hit_rate','calculate_critical_rate','is_hit','is_critical_hit','physical_damage']
    functions=[];hashes={}
    for name in methods:
        start=raw.index('function combat_core:'+name+'(')
        next_method=raw.find('\nfunction combat_core:',start+1)
        body=raw[start:next_method if next_method>=0 else len(raw)].rstrip()
        functions.append(body.replace('function combat_core:','function M:',1))
        hashes[name]=hashlib.sha256(body.encode()).hexdigest()
    output=ROOT/'Server/GameServer/lualib/unity_legacy_combat.lua'
    output.write_text('-- Generated from combat_core.lua: verbatim basic methods, not the complete skill/impact system.\nlocal define=require "define"\nlocal enum_damage_type={IDX_DAMAGE_PHY=0}\nlocal M={}\n\n'+'\n\n'.join(functions)+'\nreturn M\n')
    trait_path=ROOT/'Server/configs/AttackTraits.txt'
    if not trait_path.exists():
        manifest=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
        endpoint='https://drive.usercontent.google.com/download'
        fid=re.search('/d/([^/]+)',manifest['google_drive_url'])[1]
        with urllib.request.urlopen(endpoint+'?'+urllib.parse.urlencode(dict(id=fid,export='download')),timeout=30) as response:page=response.read(100000).decode()
        params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
        if params.get('id')!=fid or params.get('confirm')!='t':raise ValueError('Unrecognized Drive form')
        url=endpoint+'?'+urllib.parse.urlencode(params)
        with zipfile.ZipFile(RemoteZip(url,manifest['bytes'])) as archive:
            name='Server/configs/AttackTraits.txt';data=archive.read(name)
            index={r['path']:r for r in json.loads(archive.read('DATA-FILES.json'))}
            if hashlib.sha256(data).hexdigest()!=index[name]['sha256']:raise ValueError('Combat traits checksum mismatch')
            trait_path.write_bytes(data)
    source_traits=templates(trait_path)
    traits={str(k):float(v.get('C-phy') or 0) for k,v in source_traits.items()}
    monsters={}
    for key,row in templates(ROOT/'Server/configs/MonsterAttrExTable.txt').items():
        def n(field,default=0):return float(row.get(field) or default)
        monsters[str(key)]=dict(hp=n('HP上限'),attack=n('物理攻击'),defence=n('物理防御'),hit=n('命中率'),miss=n('闪避'),critical=n('会心率'),criticalDefence=n('会心防御'),speed=n('移动速度')/1000,cooldownMilliseconds=n('攻击冷却时间',2400),actionMilliseconds=n('攻击动作时间',1200),traitId=10,sourceTraitId=n('攻击特性ID'),camp=n('阵营'),isNpc=n('是否可以交互')==1)
    world_root=ROOT/'Build/unity-world';config=ini(ROOT/'Server/configs/SceneInfo.ini');nav_root=world_root/'nav';nav_root.mkdir(exist_ok=True)
    nav_checked={}
    for summary in json.loads((world_root/'catalog.json').read_text())['scenes']:
        sid=summary['sceneId'];path=world_root/f'{sid}.json';world=json.loads(path.read_text())
        scn=ini(contained(ROOT/'Server/Game_2/Scene',config['scene'+str(sid)]['file']))['System']
        name=scn.get('navmapname')
        world['combatNavigationAvailable']=False
        if name:
            original=contained(ROOT/'Server/Game_2/Scene',name)
            if original.is_file():
                digest=hashlib.sha256(original.read_bytes()).hexdigest();filename=digest[:24]+'.path'
                target=nav_root/filename
                if not target.exists():target.write_bytes(original.read_bytes())
                if hashlib.sha256(target.read_bytes()).hexdigest()!=digest:raise ValueError('Altered exported nav image: '+str(target))
                world['navFile']='nav/'+filename;world['combatNavigationAvailable']=True
                nav_checked[name]=digest
        path.write_text(json.dumps(world,ensure_ascii=False,separators=(',',':'),allow_nan=False))
    from native_navigation import validate
    navigation_report=validate(world_root)
    print('Native navigation:',json.dumps(navigation_report,ensure_ascii=False))
    data=dict(schema=1,templates=monsters,physicalTraits=traits,sourceFunctions=hashes,sourceCoreSha256=hashlib.sha256(source.read_bytes()).hexdigest(),sourceMonsterSha256=hashlib.sha256((ROOT/'Server/configs/MonsterAttrExTable.txt').read_bytes()).hexdigest(),sourceTraitsSha256=hashlib.sha256(trait_path.read_bytes()).hexdigest(),navigation=nav_checked,
        profile=dict(id='unity-development',hp=100,attack=10,defence=5,hit=1000,miss=0,critical=0,criticalDefence=1,speed=5,cooldownMilliseconds=600,range=3),
        scope='Development basic physical combat only; original formulas/stats/nav are reused, full skills/equipment/buffs/progression are not connected')
    (world_root/'combat-data.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False))
    print(f'Exported {len(monsters)} source templates, {len(traits)} physical traits, {len(nav_checked)} source nav files and {len(methods)} verbatim combat methods')
if __name__=='__main__':main()

````

## Tools/unity/art/native_navigation.py

SHA-256: `48ce7f42711f73de1c591a36f103b2f05ccc16b527386eebd879788cd646326d`

````python
"""Validate exported navigation using the built source native reader, never infer from file existence."""
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[3]

def inspect(root):
    files=sorted((root/'nav').glob('*.path'))
    lua='package.cpath='+json.dumps(str(ROOT/'Server/GameServer/luaclib/?.so'))+';local nav=require("unitynav");'
    for p in files:
        lua+='do local n=nav.new();print('+json.dumps(p.name)+',n:load('+json.dumps(str(p.resolve()))+'))end;'
    result=subprocess.run([str(ROOT/'Server/GameServer/framework/3rd/lua/lua'),'-e',lua],capture_output=True,text=True,timeout=120,check=True)
    status={}
    for line in result.stdout.splitlines():
        name,ok=line.split('\t');status[name]=ok=='true'
    if set(status)!={p.name for p in files}:raise ValueError('Incomplete native nav validation')
    return status

def validate(root):
    status=inspect(root);blocked=[]
    for summary in json.loads((root/'catalog.json').read_text())['scenes']:
        p=root/(str(summary['sceneId'])+'.json');w=json.loads(p.read_text())
        ok=status.get(Path(w.get('navFile','')).name,False)
        w['combatNavigationAvailable']=ok
        if not ok:
            w['combatNavigationError']='Source nav image rejected by native triangle reader (empty or unsupported geometry)'
            blocked.append(dict(sceneId=w['sceneId'],name=w['name'],navFile=w.get('navFile'),reason=w['combatNavigationError']))
        else:w.pop('combatNavigationError',None)
        p.write_text(json.dumps(w,ensure_ascii=False,separators=(',',':'),allow_nan=False))
    report=dict(schema=1,images=len(status),loaded=sum(status.values()),blockedScenes=blocked)
    (root/'combat-navigation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return report

````

## Tools/unity/art/ogre_binary.py

SHA-256: `7a6e9488d2787460fc00c6b1a09a37400eed85d0a3cee6336288b15097bbeff9`

````python
"""Strict sequential readers for Ogre/Fairy mesh 1.30/1.40 and skeleton 1.10, from bundled serializers."""
import math
import struct

def text(data):
    # OGRE resource keys in this source snapshot are GBK bytes, even when also valid UTF-8.
    try:return data.decode('gb18030')
    except UnicodeError:return data.decode('utf8')

def unpack(fmt,data,p):
    size=struct.calcsize(fmt)
    if p<0 or p+size>len(data):raise ValueError('Truncated binary data')
    return struct.unpack_from(fmt,data,p)

def line(data,p):
    end=data.index(b'\n',p,min(p+4096,len(data)))
    return text(data[p:end]),end+1

def finite(values):
    if not all(math.isfinite(v) for v in values):raise ValueError('Nonfinite asset data')
    return list(values)

def mesh(data):
    if data[:2]!=b'\x00\x10':raise ValueError('Invalid mesh header/endian')
    version,p=line(data,2)
    if version not in ['[MeshSerializer_v1.40]','[MeshSerializer_v1.30]']:raise ValueError('Unsupported mesh version '+version)
    shared=None;geo=None;sub=None;parts=[];skeleton='';binding=0;stride=0
    skipped=[]
    def geometry(count):
        if not 0<=count<=10000000:raise ValueError('Unreasonable vertex count')
        return dict(count=count,decl=[],buffers={},assignments=[])
    while p+6<=len(data):
        cid,size=unpack('<HI',data,p);q=p+6
        if cid==0x3000:p=q+1
        elif cid==0x4000:
            material,q=line(data,q);use_shared,count,wide=unpack('<?I?',data,q);q+=6
            if count>30000000:raise ValueError('Unreasonable index count')
            indices=list(unpack('<'+('I' if wide else 'H')*count,data,q));p=q+count*(4 if wide else 2)
            sub=dict(material=material,shared=use_shared,indices=indices,operation=4,geometry=None);parts.append(sub);geo=None
        elif cid==0x4010:
            if sub is None:raise ValueError('Operation without submesh')
            sub['operation']=unpack('<H',data,q)[0];p=q+2
        elif cid==0x5000:
            geo=geometry(unpack('<I',data,q)[0]);p=q+4
            if sub is None:shared=geo
            else:sub['geometry']=geo
        elif cid==0x5100:p=q
        elif cid==0x5110:
            if geo is None:raise ValueError('Declaration without geometry')
            geo['decl'].append(unpack('<5H',data,q));p=q+10
        elif cid==0x5200:binding,stride=unpack('<2H',data,q);p=q+4
        elif cid==0x5210:
            if geo is None or stride==0:raise ValueError('Invalid vertex buffer')
            end=q+geo['count']*stride
            if end>len(data):raise ValueError('Truncated vertex buffer')
            geo['buffers'][binding]=(stride,data[q:end]);p=end
        elif cid in (0x4100,0x7000):
            vertex,bone,weight=unpack('<IHf',data,q);p=q+10
            target=shared if cid==0x7000 else (sub['geometry'] if sub else None)
            if target is None:raise ValueError('Bone assignment without geometry')
            if vertex>=target['count'] or not math.isfinite(weight) or weight<0:raise ValueError('Invalid skin assignment')
            target['assignments'].append((vertex,bone,weight))
        elif cid==0x6000:skeleton,p=line(data,q)
        elif cid==0x4200:
            _,q=line(data,q);_,p=line(data,q)
        elif cid==0x9000:p=q+28
        elif cid==0xA000:p=q
        elif cid==0xA100:_,p=line(data,q+2)
        elif cid in {0x8000,0xB000,0xC000,0xD000,0xE000} and 6<=size<=len(data)-p:
            skipped.append(hex(cid));p+=size
        elif all(v==0 for v in data[p:]) and len(data)-p<=64:break
        else:raise ValueError(f'Unsupported mesh chunk {cid:#x} at {p}')
        if p>len(data):raise ValueError('Mesh chunk exceeds file')
    if p<len(data) and any(data[p:]):raise ValueError('Unparsed mesh tail')
    result=[]
    for part in parts:
        g=shared if part['shared'] else part['geometry']
        if g is None:raise ValueError('Submesh geometry missing')
        count=g['count'];attrs={}
        for source,typ,semantic,offset,index in g['decl']:
            if semantic not in [1,4,7] or (semantic==7 and index!=0):continue
            if typ not in [0,1,2,3]:raise ValueError('Unsupported vertex attribute type '+str(typ))
            components=typ+1;vertex_stride,buffer=g['buffers'][source]
            if offset+components*4>vertex_stride:raise ValueError('Vertex element exceeds stride')
            values=[]
            for i in range(count):values+=unpack('<'+'f'*components,buffer,i*vertex_stride+offset)
            if semantic==4 and not all(math.isfinite(v) for v in values):
                attrs[semantic]=(components,[])
            else:attrs[semantic]=(components,finite(values))
        if 1 not in attrs or attrs[1][0] not in [3,4]:raise ValueError('FLOAT3/FLOAT4 positions required')
        indices=part['indices']
        if indices and max(indices)>=count:raise ValueError('Mesh index out of bounds')
        if part['operation']==4:
            if len(indices)%3:raise ValueError('Invalid triangle list')
            triangles=[v for i in range(0,len(indices),3) for v in [indices[i],indices[i+2],indices[i+1]]]
        elif part['operation'] in [5,6]:
            triangles=[]
            for i in range(2,len(indices)):
                a,b,c=(indices[i-2],indices[i-1],indices[i]) if part['operation']==5 else (indices[0],indices[i-1],indices[i])
                if part['operation']==5 and i%2:a,b=b,a
                if len({a,b,c})==3:triangles.extend([a,c,b])
        else:raise ValueError('Unsupported primitive operation '+str(part['operation']))
        weights=[[] for _ in range(count)]
        for vertex,bone,weight in g['assignments']:weights[vertex].append((bone,weight))
        ids=[];normalized=[];trimmed=0
        for row in weights:
            row=sorted(row,key=lambda v:-v[1]);trimmed+=max(0,len(row)-4);row=row[:4]
            total=sum(w for _,w in row)
            ids.extend([b for b,_ in row]+[0]*(4-len(row)))
            normalized.extend([w/total if total else 0 for _,w in row]+[0]*(4-len(row)))
        result.append(dict(material=part['material'],positions=[attrs[1][1][i*attrs[1][0]+j]*.01 for i in range(count) for j in range(3)],sourcePositionW=attrs[1][1][3::4] if attrs[1][0]==4 else [],normalRepair=4 in attrs and not attrs[4][1],
            normals=attrs.get(4,(3,[]))[1],uv=attrs.get(7,(2,[]))[1],uvComponents=attrs.get(7,(2,[]))[0],
            triangles=triangles,boneIds=ids,weights=normalized,trimmedWeights=trimmed,hasSkin=bool(g['assignments'])))
    if not result:raise ValueError('Mesh has no submeshes')
    return dict(schema=1,version=version,parts=result,skeleton=skeleton,skippedChunks=skipped)

def skeleton(data):
    if data[:2]!=b'\x00\x10':raise ValueError('Invalid skeleton endian/header')
    version,p=line(data,2)
    if version!='[Serializer_v1.10]':raise ValueError('Unsupported skeleton version '+version)
    bones=[];parents={};animations=[];links=[];animation=None;track=None
    def key(time,rotation=(0,0,0,1),position=(0,0,0),scale=(1,1,1)):
        finite([time]);return dict(time=time,rotation=finite(rotation),position=[v*.01 for v in finite(position)],scale=finite(scale))
    while p+6<=len(data):
        cid,size=unpack('<HI',data,p);q=p+6
        if cid==0x1010:p=q+2
        elif cid==0x2000:
            name,q=line(data,q);handle=unpack('<H',data,q)[0];q+=2
            vals=finite(unpack('<7f',data,q));q+=28
            scale=finite(unpack('<3f',data,q)) if size>36 else [1,1,1]
            if size>36:q+=12
            bones.append(dict(id=handle,name=name,parent=-1,position=[v*.01 for v in vals[:3]],rotation=vals[3:],scale=scale));p=q
        elif cid==0x3000:
            child,parent=unpack('<HH',data,q);parents[child]=parent;p=q+4
        elif cid==0x4000:
            name,q=line(data,q);duration=unpack('<f',data,q)[0];p=q+4
            finite([duration]);animation=dict(name=name,duration=duration,tracks=[]);animations.append(animation)
        elif cid==0x4010:raise ValueError('Animation base-keyframe rebasing requires explicit support')
        elif cid==0x4100:
            if animation is None:raise ValueError('Track without animation')
            track=dict(boneId=unpack('<H',data,q)[0],keys=[]);animation['tracks'].append(track);p=q+2
        elif cid==0x4110:
            if track is None:raise ValueError('Key without track')
            vals=unpack('<8f',data,q);q+=32
            scale=unpack('<3f',data,q) if size>38 else (1,1,1)
            if size>38:q+=12
            track['keys'].append(key(vals[0],vals[1:5],vals[5:8],scale));p=q
        elif cid==0x4120:
            if track is None:raise ValueError('Keys without track')
            count,flags=unpack('<HH',data,q);q+=4
            if flags&~7:raise ValueError('Unsupported compact key flags')
            for _ in range(count):
                t=unpack('<f',data,q)[0];q+=4;r=(0,0,0,1);v=(0,0,0);s=(1,1,1)
                if flags&1:r=unpack('<4f',data,q);q+=16
                if flags&2:v=unpack('<3f',data,q);q+=12
                if flags&4:s=unpack('<3f',data,q);q+=12
                track['keys'].append(key(t,r,v,s))
            p=q
        elif cid==0x5000:
            name,q=line(data,q);scale=unpack('<f',data,q)[0];p=q+4;links.append(dict(name=name,scale=scale))
        elif all(v==0 for v in data[p:]) and len(data)-p<=64:break
        else:raise ValueError(f'Unsupported skeleton chunk {cid:#x} at {p}')
        if p>len(data):raise ValueError('Skeleton chunk exceeds file')
    if p<len(data) and any(data[p:]):raise ValueError('Unparsed skeleton tail')
    handles={b['id'] for b in bones}
    if len(handles)!=len(bones) or not bones:raise ValueError('Missing/duplicate bones')
    for bone in bones:
        bone['parent']=parents.get(bone['id'],-1)
        visited={bone['id']};parent=bone['parent']
        while parent!=-1:
            if parent not in handles or parent in visited:raise ValueError('Invalid/cyclic bone hierarchy')
            visited.add(parent);parent=parents.get(parent,-1)
    for a in animations:
        for t in a['tracks']:
            if t['boneId'] not in handles:raise ValueError('Animation references absent bone')
            t['keys'].sort(key=lambda k:k['time'])
    return dict(schema=1,version=version,bones=bones,animations=animations,links=links)

````

## Tools/unity/art/package_art.py

SHA-256: `54e00dfb1fbb60f1543d9eff023d6847a25b531ea732095f8efa93faa3844415`

````python
#!/usr/bin/env python3
"""Package converted original art into mergeable, bounded ZIP downloads and a complete starter."""
import hashlib
import json
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parents[3]
ART=ROOT/'Build/unity-art'
OUT=ROOT/'Build'
PREFIX='Assets/DragonPort/Art/'

def archive(path,files,catalog):
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        z.writestr(PREFIX+'art-catalog.json',json.dumps(catalog,ensure_ascii=False,separators=(',',':')))
        for name in sorted(files):z.write(ART/name,PREFIX+name)
    with zipfile.ZipFile(path) as z:
        if z.testzip():raise ValueError('Bad ZIP '+str(path))
    return dict(file=path.name,bytes=path.stat().st_size,sha256=hashlib.file_digest(path.open('rb'),'sha256').hexdigest())

def main():
    c=json.loads((ART/'art-catalog.json').read_text())
    required=set();starter_ids=set()
    models=set()
    for sid in [2,6]:
        w=json.loads((OUT/f'unity-world/{sid}.json').read_text())
        models.update(e['modelId'] for e in w['entities'])
    starter_ids.update(a['assetId'] for a in c['actorBindings'] if a['modelId'] in models)
    starter_files=set()
    for a in c['assets']:
        required.add(a['file'])
        data=json.loads((ART/a['file']).read_text())
        deps={m['textureFile'] for m in data['materials'] if m.get('textureFile')}
        required.update(deps)
        if a['assetId'] in starter_ids:starter_files.update(deps|{a['file']})
    starter=dict(c)
    starter['assets']=[a for a in c['assets'] if a['assetId'] in starter_ids]
    starter['actorBindings']=[a for a in c['actorBindings'] if a['assetId'] in starter_ids]
    starter['sceneryBindings']=[]
    first=archive(OUT/'UnityOriginalActors-Starter.zip',starter_files,starter)
    print('Starter:',first,flush=True)
    # Bound by uncompressed size too, to keep imports/downloads manageable.
    packs=[];files=[];size=0
    for name in sorted(required):
        n=(ART/name).stat().st_size
        if files and size+n>250*1024*1024:
            packs.append(archive(OUT/f'UnityOriginalArt-{len(packs)+1:02d}.zip',files,c));print(packs[-1],flush=True);files=[];size=0
        files.append(name);size+=n
    if files:packs.append(archive(OUT/f'UnityOriginalArt-{len(packs)+1:02d}.zip',files,c));print(packs[-1],flush=True)
    manifest=dict(schema=1,starter=first,packs=packs,assetCount=len(c['assets']),files=len(required),instructions='Merge all full packs into the same Unity project Assets folder; starter is an optional self-contained actor subset for scenes 2 and 6. Full packs include the full catalog. Import skips missing assets until remaining packs are copied.')
    (OUT/'art-downloads.json').write_text(json.dumps(manifest,indent=2))
    lines=['# Original art downloads','','Start with [UnityMapPort.zip](UnityMapPort.zip), [starter actors](UnityOriginalActors-Starter.zip) and [server source/data](NativeServerChanges.zip).','',
        'Copy Assets folders into your Unity project. Starter contains only bindable actors used in maps 2 and 6, without scenery. For all converted scenery/actors, merge **every full pack below**; these are separate ZIPs, not multipart ZIP volumes. Run Tools → Dragon Port → Import Original Meshes and Animations after copying.','',
        'Missing all.obj composition data prevents reliable automatic binding for 755 of 914 referenced actor models. These retain capsule placeholders. Original shader effects and full legacy skill logic are not ported. See ART-COMBAT.md at the root of the core ZIP.','', '| Download | MiB |','|---|---:|']
    for p in packs:lines.append(f"| [{p['file']}]({p['file']}) | {p['bytes']/1024**2:.1f} |")
    lines+=['','Checksums and exact byte counts: [art-downloads.json](art-downloads.json).','', 'Preview rendered in Blender from converted original mesh and original attack keys: [rest](art-render/rest.png), [attack](art-render/attack.png). Unity Editor and macOS execution remain untested.']
    (OUT/'ART-DOWNLOADS.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':main()

````

## Tools/unity/art/render_original_smoke.py

SHA-256: `6e40e12ce2ad80c37f41132a5c21f251db7044a22c2fbea3d5b152b2cc42ef11`

````python
"""Blender headless validation of an original skinned asset/rest and attack pose; not a Unity screenshot."""
import bpy
import json
from pathlib import Path
import sys
from mathutils import Matrix,Quaternion,Vector
args=sys.argv[sys.argv.index('--')+1:]
file=Path(args[0]);out=Path(args[1]);out.mkdir(parents=True,exist_ok=True)
asset=json.loads(file.read_text());bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
rig_data=bpy.data.armatures.new('OriginalRig');rig=bpy.data.objects.new('OriginalRig',rig_data);bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True)
bpy.ops.object.mode_set(mode='EDIT')
bones={b['id']:b for b in asset['rig']['bones']};global_matrices={}
def rest(handle):
 if handle in global_matrices:return global_matrices[handle]
 b=bones[handle];q=b['rotation'];local=Matrix.LocRotScale(Vector(b['position']),Quaternion((q[3],q[0],q[1],q[2])),Vector(b['scale']))
 matrix=rest(b['parent'])@local if b['parent']>=0 else local;global_matrices[handle]=matrix;return matrix
for handle,b in bones.items():
 edit=rig_data.edit_bones.new('Bone_'+str(handle));matrix=rest(handle);edit.head=matrix.translation;edit.tail=edit.head+matrix.to_3x3()@Vector((0,.08,0));edit.matrix=matrix;edit.length=.08
for handle,b in bones.items():
 if b['parent']>=0:rig_data.edit_bones['Bone_'+str(handle)].parent=rig_data.edit_bones['Bone_'+str(b['parent'])]
bpy.ops.object.mode_set(mode='OBJECT')
objects=[]
for index,part in enumerate(asset['parts']):
 points=[part['positions'][i:i+3] for i in range(0,len(part['positions']),3)]
 # The converter reverses winding for Unity; reverse back for Blender's right-handed renderer.
 faces=[(part['triangles'][i],part['triangles'][i+2],part['triangles'][i+1]) for i in range(0,len(part['triangles']),3)]
 mesh=bpy.data.meshes.new('OriginalMesh');mesh.from_pydata(points,[],faces);mesh.update()
 obj=bpy.data.objects.new('OriginalMesh_'+str(index),mesh);bpy.context.collection.objects.link(obj);objects.append(obj)
 if part['uv']:
  layer=mesh.uv_layers.new();stride=part['uvComponents']
  for polygon in mesh.polygons:
   for loop_index in polygon.loop_indices:
    v=mesh.loops[loop_index].vertex_index;layer.data[loop_index].uv=part['uv'][v*stride:v*stride+2]
 for handle in bones:obj.vertex_groups.new(name='Bone_'+str(handle))
 if part['hasSkin']:
  for vertex in range(len(points)):
   for k in range(4):
    weight=part['weights'][vertex*4+k]
    if weight>0:obj.vertex_groups['Bone_'+str(part['boneIds'][vertex*4+k])].add([vertex],weight,'REPLACE')
  modifier=obj.modifiers.new('OriginalSkin','ARMATURE');modifier.object=rig
 mat=bpy.data.materials.new(part['material']);mat.use_nodes=True;bsdf=mat.node_tree.nodes.get('Principled BSDF')
 texture=asset['materials'][index]['textureFile']
 if texture:
  node=mat.node_tree.nodes.new('ShaderNodeTexImage');node.image=bpy.data.images.load(str(file.parent/texture));mat.node_tree.links.new(node.outputs['Color'],bsdf.inputs['Base Color'])
 bsdf.inputs['Roughness'].default_value=.75;mesh.materials.append(mat)
# Ogre/Unity use Y up; Blender uses Z up. Rotate the whole source scene for the preview.
from math import radians
rig.rotation_euler.x=radians(90)
for obj in objects:obj.rotation_euler.x=radians(90)
bpy.context.view_layer.update()
points=[obj.matrix_world@Vector(corner) for obj in objects for corner in obj.bound_box];center=sum(points,Vector())/len(points);span=max((p-center).length for p in points)
world=bpy.context.scene.world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.12,.12,1)
bpy.ops.object.camera_add(location=center+Vector((span*2.3,-span*3,span*1.2)));camera=bpy.context.object;camera.rotation_euler=(center-camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.camera=camera
for location,power,size in [(center+Vector((3,-4,6)),700,5),(center+Vector((-4,0,3)),400,4)]:
 bpy.ops.object.light_add(type='AREA',location=location);light=bpy.context.object;light.data.energy=power;light.data.shape='DISK';light.data.size=size;light.rotation_euler=(center-light.location).to_track_quat('-Z','Y').to_euler()
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.use_denoising=False;scene.cycles.samples=16;scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.filepath=str(out/'rest.png');bpy.ops.render.render(write_still=True)
clip=next(a for a in asset['rig']['animations'] if a['name']=='攻击')
for track in clip['tracks']:
 keys=track['keys'];key=min(keys,key=lambda k:abs(k['time']-.5));q=key['rotation'];bone=bones[track['boneId']];rest_q=bone['rotation'];pose=rig.pose.bones['Bone_'+str(track['boneId'])];pose.rotation_mode='QUATERNION';pose.rotation_quaternion=Quaternion((q[3],q[0],q[1],q[2]));pose.location=Quaternion((rest_q[3],rest_q[0],rest_q[1],rest_q[2])).inverted()@Vector(key['position']);pose.scale=Vector(key['scale'])
bpy.context.view_layer.update();scene.render.filepath=str(out/'attack.png');bpy.ops.render.render(write_still=True)
print('ORIGINAL_ART_RENDER_OK',len(bones),len(clip['tracks']),clip['duration'])

````

## Tools/unity/cached_remote_zip.py

SHA-256: `5fe1ba51a36f146964e648ac42d442e6f7b4dff4af9168411187ec2e77d72eeb`

````python
"""Verified HTTP range cache in a sparse file; supports bounded parallel prefetch."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from remote_zip import RemoteZip

class CachedRemoteZip(RemoteZip):
    def __init__(self,url,size,cache):
        super().__init__(url,size)
        self.cache=Path(cache)
        self.cache.parent.mkdir(parents=True,exist_ok=True)
        self.intervals=[]
        with self.cache.open('wb') as stream:stream.truncate(size)
    def record(self,start,end):
        ranges=sorted(self.intervals+[(start,end)])
        merged=[]
        for a,b in ranges:
            if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
            else:merged.append((a,b))
        self.intervals=merged
    def read(self,n=-1):
        n=self.size-self.pos if n<0 else min(n,self.size-self.pos)
        if n<=0:return b''
        start=self.pos;end=start+n
        if any(a<=start and end<=b for a,b in self.intervals):
            with self.cache.open('rb') as stream:stream.seek(start);data=stream.read(n)
            self.pos=end
            return data
        data=super().read(n)
        with self.cache.open('r+b') as stream:stream.seek(start);stream.write(data)
        self.record(start,end)
        return data
    def prefetch(self,ranges,workers=4):
        def fetch(bounds):
            start,end=bounds
            reader=RemoteZip(self.url,self.size);reader.seek(start)
            data=reader.read(end-start)
            with self.cache.open('r+b') as stream:stream.seek(start);stream.write(data)
            return start,end,len(data)
        with ThreadPoolExecutor(max_workers=workers) as pool:
            jobs=[pool.submit(fetch,bounds) for bounds in ranges]
            for count,job in enumerate(as_completed(jobs),1):
                start,end,size=job.result();self.transferred+=size;self.record(start,end)
                if count%20==0 or count==len(jobs):print(f'Ranges {count}/{len(jobs)}; fetched {self.transferred/1048576:.1f} MiB',flush=True)

````

## Tools/unity/export_world.py

SHA-256: `ca22fa6d1fa48ab7af08fc0252142ed9052cc0cf37ecc1d830ee8b6f0f8a596a`

````python
#!/usr/bin/env python3
"""Export real TLBB scene/spawn/terrain data to a Unity-neutral bundle; source files stay unchanged."""
import argparse
import configparser
import hashlib
import json
import math
from pathlib import Path
import struct
import xml.etree.ElementTree as ET
from functools import lru_cache


def ini(path):
    parser = configparser.ConfigParser(interpolation=None, inline_comment_prefixes=(';',), strict=False)
    text=Path(path).read_bytes().decode('gb18030')
    # Match legacy inireader: semicolon starts a comment even directly after '='.
    parser.read_string('\n'.join(line.split(';',1)[0] for line in text.splitlines()))
    return parser


def contained(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Reference escapes data root: '+relative)
    return path


def number(value, label):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('Nonfinite '+label)
    return result


@lru_cache(maxsize=4)
def templates(path):
    lines = [s for s in Path(path).read_bytes().decode('gb18030').splitlines() if s and not s.startswith('#')]
    keys = lines[1].split('\t')
    result = {}
    for line in lines[2:]:
        cells = line.split('\t')
        if not cells[0].lstrip('-').isdigit():
            continue
        row = dict(zip(keys, cells))
        result[int(cells[0])] = row
    return result


def heightmap(path, width, depth):
    raw = Path(path).read_bytes()
    if len(raw) < 16 or struct.unpack('<4I', raw[:16]) != (0x4645484D, 0x100000, width+1, depth+1):
        raise ValueError('Heightmap header/dimensions mismatch: '+str(path))
    if len(raw) != 16+4*(width+1)*(depth+1):
        raise ValueError('Heightmap payload size mismatch')
    values = struct.unpack('<'+'f'*((width+1)*(depth+1)), raw[16:])
    if not all(math.isfinite(v) for v in values):
        raise ValueError('Nonfinite height sample')
    return values, raw[16:]


def gridinfo(path, width, depth):
    raw = Path(path).read_bytes()
    magic, version, w, d = struct.unpack('<4I', raw[:16])
    if magic != 0x46454749 or not 0x100000 <= version <= 0x100002 or (w,d)!=(width,depth):
        raise ValueError('Invalid GridInfo header')
    offset = 16
    wide = False
    if version >= 0x100002:
        wide = bool(raw[offset]); offset += 1
    layer_size = 3 if wide else 2
    stride = 2*layer_size + (1 if version >= 0x100001 else 0)
    if len(raw) != offset+stride*w*d:
        raise ValueError('Invalid GridInfo size')
    result = bytearray()
    for i in range(w*d):
        row = raw[offset+i*stride:offset+(i+1)*stride]
        first = int.from_bytes(row[:2], 'little') if wide else row[0]
        second = int.from_bytes(row[layer_size:layer_size+2], 'little') if wide else row[layer_size]
        flip = row[-1]&1 if version >= 0x100001 else 0
        result.append(flip | (2 if first == 0 else 0))
    return bytes(result)


def sample(values, flags, width, depth, x, z):
    x = min(max(x,0),width); z = min(max(z,0),depth)
    ix = min(int(x),width-1); iz = min(int(z),depth-1)
    u,v = x-ix,z-iz
    a,b = values[iz*(width+1)+ix:iz*(width+1)+ix+2]
    c,d = values[(iz+1)*(width+1)+ix:(iz+1)*(width+1)+ix+2]
    if flags[iz*width+ix]&1:
        return a+(b-a)*u+(d-b)*v if v<=u else a+(d-c)*u+(c-a)*v
    return a+(b-a)*u+(c-a)*v if u+v<=1 else d+(c-d)*(1-u)+(b-d)*(1-v)


@lru_cache(maxsize=4)
def resource_index(data):
    lookup = {}
    for path in data.rglob('*'):
        if path.is_file() and path.suffix.lower() in ('.scene', '.terrain', '.heightmap', '.gridinfo'):
            lookup.setdefault(path.name.casefold(), []).append(path)
    return lookup


def resource(data, reference, preferred=None):
    relative = reference.replace('\\','/')
    contained(data, relative)  # Reject absolute or escaping references before lookup.
    if preferred:
        direct = contained(preferred, relative)
        if direct.is_file(): return direct
    matches = resource_index(data).get(Path(relative).name.casefold(), [])
    if len(matches)==1: return matches[0]
    if not matches: raise FileNotFoundError('Client resource missing: '+reference)
    raise ValueError('Ambiguous client resource: '+reference)


def export_scene(server, data, scene_id, output, aliases=None):
    source_paths = []
    def source(path):
        path=Path(path); source_paths.append(path); return path
    info_path=source(server/'configs/SceneInfo.ini')
    info=ini(info_path)['scene'+str(scene_id)]
    scene_root=server/'Game_2/Scene'
    config=ini(source(contained(scene_root, info['file'])))['System']
    visual_name=Path(info['file']).stem
    folder=data/'SceneFolder'
    resolution={'kind':'scene-file-stem'}
    try:
        visual=source(resource(data,visual_name+'.Scene',folder))
    except FileNotFoundError:
        nav_name=Path(config.get('navmapname','')).stem
        try:
            if not nav_name or nav_name.casefold()==visual_name.casefold(): raise FileNotFoundError('Client resource missing: '+visual_name+'.Scene')
            visual=source(resource(data,nav_name+'.Scene',folder))
            resolution={'kind':'navigation-file-stem'}
        except FileNotFoundError:
            alias=(aliases or {}).get(scene_id)
            if not alias: raise
            visual=source(resource(data,alias['resource'],data))
            resolution=alias
            source(data/'ConfigFolder/SceneDefineEx.txt')
    scene_xml=ET.parse(visual).getroot()
    terrain_ref=scene_xml.find('Terrain')
    if terrain_ref is None: raise ValueError('Scene has no terrain')
    terrain_path=source(resource(data,terrain_ref.attrib['filename'],visual.parent))
    terrain_xml=ET.parse(terrain_path).getroot()
    width,depth=int(terrain_xml.attrib['xsize']),int(terrain_xml.attrib['zsize'])
    if not 0<width<=4096 or not 0<depth<=4096: raise ValueError('Terrain dimensions outside supported bounds')
    scale=None; origin=None
    for child in terrain_xml:
        if child.tag in ('scale','size'):
            v=[number(child.attrib[k],k) for k in ('x','y','z')]
            scale=v if child.tag=='scale' else [v[0]/width,v[1],v[2]/depth]
            if min(scale)<=0: raise ValueError('Scale must be positive')
            origin=[-scale[0]*width/2,0,-scale[2]*depth/2]
        elif child.tag in ('position','centre','center'):
            if scale is None: raise ValueError('Position before scale')
            origin=[number(child.attrib[k],k) for k in ('x','y','z')]
            if child.tag!='position': origin=[origin[0]-scale[0]*width/2,origin[1],origin[2]-scale[2]*depth/2]
    if scale is None: raise ValueError('Terrain scale is required')
    ref=terrain_xml.find('heightmap')
    if ref is None or ref.get('type','standard')!='standard':raise ValueError('Only standard FEHM heightmaps supported')
    values,height_bytes=heightmap(source(resource(data,ref.attrib['filename'],terrain_path.parent)),width,depth)
    grid=terrain_xml.find('gridInfo')
    flags=gridinfo(source(resource(data,grid.attrib['filename'],terrain_path.parent)),width,depth) if grid is not None else bytes(width*depth)
    attr=templates(source(server/'configs/MonsterAttrExTable.txt'))
    spawns=ini(source(contained(scene_root,config['monsterfile']))) if config.get('monsterfile') else None
    entities=[]; skipped=[]; warnings=[]; skipped_entities=[]
    angles={0:0,5:135,9:270,14:315,18:180,23:45,27:90,32:225}
    for i in range(int(spawns['info']['monstercount']) if spawns else 0):
        key='monster'+str(i)
        if key not in spawns:
            skipped.append(key); continue
        row=spawns[key]
        if not row.get('pos_x') or not row.get('pos_z'):
            skipped.append(key); continue
        type_id=int(row['type'])
        if type_id not in attr:
            skipped_entities.append(dict(section=key,reason=f'template {type_id} missing; legacy server also skips this entity'))
            continue
        template=attr[type_id]
        x,z=number(row['pos_x'],key),number(row['pos_z'],key)
        if not 0<=x<=width or not 0<=z<=depth:
            warnings.append(f'{key}: spawn outside terrain bounds ({x},{z})')
        direction=number(row.get('dir','27'),key)
        radians=direction if direction>=100 else math.pi/2-math.radians(angles.get(direction,90))
        entities.append(dict(id=f'{scene_id}:{key}',templateId=type_id,
            modelId=int(template.get('外型ID') or 0),kind='npc' if template.get('是否可以交互')=='1' else 'monster',
            name=row.get('name') or template.get('名称$1$',''),title=row.get('title',''),
            x=x,y=sample(values,flags,width,depth,x,z),z=z,yaw=math.degrees(radians),
            level=int(template.get('等级') or 0),hp=int(template.get('HP上限') or 0),
            scriptId=int(row.get('script_id','-1')),aiType=int(row.get('base_ai',template.get('基础AI') or '0')),
            respawnMilliseconds=int(row.get('respawn_time','-1')),sourceSection=key))
    objects=[]
    for obj in scene_xml.iter('Object'):
        if obj.get('type')!='StaticEntity':continue
        props={p.get('name'):p.get('value') for p in obj.findall('Property')}
        if 'mesh name' not in props:continue
        position=[float(v) for v in props.get('position','0 0 0').split()]
        q=[float(v) for v in props.get('orientation','1 0 0 0').split()]
        objects.append(dict(resource=props['mesh name'],x=(position[0]-origin[0])/scale[0],
            y=(position[1]-origin[1])/scale[1],z=(position[2]-origin[2])/scale[2],
            rotation=dict(x=q[1],y=q[2],z=q[3],w=q[0]),
            sourceScale=[float(v) for v in props.get('scale','1 1 1').split()]))
    world=dict(schema=1,sceneId=scene_id,sceneType=int(info.get('type',0)),clientResourceId=int(info.get('clientres',scene_id)),name=info.get('name',''),
        coordinates='server-grid-XZ-height-samples-Y',width=width,depth=depth,
        sourceScale=scale,sourceOrigin=origin,resourceResolution=resolution,entities=entities,staticObjects=objects,
        skippedSections=skipped,skippedEntities=skipped_entities,warnings=warnings,simulationReady=False,
        sources=[dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in dict.fromkeys(source_paths)])
    output.mkdir(parents=True,exist_ok=True)
    (output/f'{scene_id}.heights.bytes').write_bytes(height_bytes)
    (output/f'{scene_id}.cells.bytes').write_bytes(flags)
    (output/f'{scene_id}.json').write_text(json.dumps(world,ensure_ascii=False,separators=(',',':'),allow_nan=False),encoding='utf-8')
    return dict(sceneId=scene_id,name=world['name'],width=width,depth=depth,entityCount=len(entities),
                npcCount=sum(e['kind']=='npc' for e in entities),monsterCount=sum(e['kind']=='monster' for e in entities),staticObjectCount=len(objects),warningCount=len(warnings),skippedEntityCount=len(skipped_entities),sceneType=int(info.get('type',0)))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--server-root',type=Path,required=True)
    ap.add_argument('--client-data',type=Path,required=True)
    ap.add_argument('--scenes',default='2,6')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    catalog=[export_scene(args.server_root.resolve(),args.client_data.resolve(),int(s),args.out.resolve()) for s in args.scenes.split(',')]
    (args.out/'catalog.json').write_text(json.dumps(dict(schema=1,scenes=catalog),ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(catalog,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

````

## Tools/unity/fetch_world_data.py

SHA-256: `697e328f66cadd4fbe7cdfbb4de18292c872d464945c81a7e56e1d46e7cff0fa`

````python
#!/usr/bin/env python3
"""Fetch selected world inputs from the published ZIP using range reads, CRC and member SHA-256."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import zipfile
from remote_zip import RemoteZip

ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--maps',default='dali_new_320,wuliang')
    ap.add_argument('--root',type=Path,default=ROOT)
    args=ap.parse_args()
    root=args.root.resolve()
    manifest=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
    file_id=re.search(r'/d/([^/]+)',manifest['google_drive_url'])[1]
    endpoint='https://drive.usercontent.google.com/download'
    initial=endpoint+'?'+urllib.parse.urlencode({'id':file_id,'export':'download'})
    with urllib.request.urlopen(initial,timeout=30) as response:
        if 'text/html' not in response.headers.get('Content-Type',''):
            raise ValueError('Expected Drive download confirmation')
        page=response.read(100000).decode('utf-8')
    params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
    if params.get('id')!=file_id or params.get('confirm')!='t':
        raise ValueError('Unrecognized public download form')
    remote=RemoteZip(endpoint+'?'+urllib.parse.urlencode(params),manifest['bytes'])
    maps=args.maps.split(',')
    if any(not re.fullmatch(r'[A-Za-z0-9_]+',m) for m in maps):raise ValueError('Invalid map name')
    checked=[]
    with zipfile.ZipFile(remote) as archive:
        records=json.loads(archive.read('DATA-FILES.json'))
        index={r['path']:r for r in records}
        names=archive.namelist()
        license_names=[n for n in names if 'llicense' in n.lower()]
        selected=[]
        for name in names:
            base=name.rsplit('/',1)[-1].lower()
            if name in ['Server/configs/SceneInfo.ini','Server/configs/MonsterAttrExTable.txt']:
                selected.append(name)
            elif name.startswith('Server/Game_2/Scene/') and any(base.startswith(m+'.') or base.startswith(m+'_') for m in maps):
                selected.append(name)
            elif name.startswith('Assets/CanonicalCY/Data/SceneFolder/') and any(base==m+ext for m in maps for ext in ['.scene','.terrain','.heightmap','.gridinfo']):
                selected.append(name)
        for name in selected:
            destination=(root/name).resolve()
            if not destination.is_relative_to(root):raise ValueError('Unsafe archive path')
            expected=index[name]
            if destination.exists():
                if hashlib.sha256(destination.read_bytes()).hexdigest()!=expected['sha256']:
                    raise ValueError('Existing local file differs; refusing overwrite: '+name)
            else:
                data=archive.read(name) # zipfile checks CRC on complete member reads.
                if len(data)!=expected['bytes'] or hashlib.sha256(data).hexdigest()!=expected['sha256']:
                    raise ValueError('Member checksum mismatch: '+name)
                destination.parent.mkdir(parents=True,exist_ok=True)
                with destination.open('xb') as stream:stream.write(data)
            checked.append(dict(path=name,sha256=expected['sha256'],bytes=expected['bytes']))
    report=root/'Build/unity-world-source-audit.json'
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(dict(archive=manifest['name'],archiveMemberCount=len(names),
        llicenseNamedMembers=license_names,checkedMembers=checked,rangeBytesTransferred=remote.transferred,
        integrityScope='ZIP member CRC and SHA-256 from embedded index; full archive SHA-256 not verified'),ensure_ascii=False,indent=2))
    print(f'Checked {len(checked)} files; archive has {len(names)} entries; llicense-named entries: {len(license_names)}. Full archive hash not verified.')

if __name__=='__main__':main()

````

## Tools/unity/package_server.py

SHA-256: `86f4102d87ebbb6efa8d974156f2f7f584e52463ff7c4bd205fb81cd64eee441`

````python
#!/usr/bin/env python3
"""Package this checkout's source delta and exported world/combat data, never native binaries."""
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile
ROOT=Path(__file__).resolve().parents[2]

def main():
    paths=set()
    for arguments in [['git','diff','--name-only','-z','HEAD'],['git','ls-files','--others','--exclude-standard','-z']]:
        paths.update(p for p in subprocess.check_output(arguments,cwd=ROOT).decode().split('\0') if p)
    target=ROOT/'Build/NativeServerChanges.zip'
    temporary=tempfile.NamedTemporaryFile(prefix='server-delta-',suffix='.zip',dir=target.parent,delete=False)
    pending=Path(temporary.name);temporary.close()
    with zipfile.ZipFile(pending,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name in sorted(paths):
            p=ROOT/name
            if p.is_file() and not any(part in ['Build','__pycache__','.git'] for part in p.parts) and p.suffix not in ['.so','.o','.pyc']:
                z.write(p,name)
        for p in sorted((ROOT/'Build/unity-world').rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(ROOT)))
        z.writestr('SOURCE-DELTA.json',json.dumps(dict(baseCommit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),repository='a002lamlam-ship-it/372dragon',instructions='Apply onto the base checkout. Contains source changes and world/combat data, not compiled macOS binaries. See Tools/unity/Package/ART-COMBAT.md.'),indent=2))
    with zipfile.ZipFile(pending) as z:
        assert z.testzip() is None
        assert 'Build/unity-world/combat-data.json' in z.namelist()
        expected={v[:24]+'.path' for v in json.loads((ROOT/'Build/unity-world/combat-data.json').read_text())['navigation'].values()}
        assert {n.rsplit('/',1)[-1] for n in z.namelist() if n.startswith('Build/unity-world/nav/')}==expected
    pending.replace(target)
    print(target,target.stat().st_size)
if __name__=='__main__':main()

````

## Tools/unity/package_world.py

SHA-256: `70fe6b211dd0d91028bc769a3e7062fbb2131da6b0f296afc5a18c70a2c228ca`

````python
#!/usr/bin/env python3
"""Create a self-contained Unity import ZIP from tested scripts and source-backed exported worlds."""
import argparse
import json
from pathlib import Path
import shutil
import zipfile
ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--world-root',type=Path,default=ROOT/'Build/unity-world')
    ap.add_argument('--out',type=Path,default=ROOT/'Build/UnityMapPort.zip')
    args=ap.parse_args()
    catalog=json.loads((args.world_root/'catalog.json').read_text())
    args.out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.out,'w',zipfile.ZIP_DEFLATED) as archive:
        package=ROOT/'Tools/unity/Package'
        for path in sorted(package.rglob('*')):
            if path.is_file():archive.write(path,str(path.relative_to(package)))
        for scene in catalog['scenes']:
            sid=scene['sceneId']
            for suffix in ['.json','.heights.bytes','.cells.bytes']:
                path=args.world_root/(str(sid)+suffix)
                archive.write(path,f'Assets/DragonPort/Data/{sid}/{path.name}')
        report=args.world_root/'port-report.json'
        if report.exists(): archive.write(report,'PORT-REPORT.json')
        for preview in args.world_root.glob('*.preview.png'):
            archive.write(preview,'Previews/'+preview.name)
        archive.write(args.world_root/'catalog.json','Assets/DragonPort/Data/catalog.json')
        for name in ['export_world.py','fetch_world_data.py','remote_zip.py','cached_remote_zip.py','port_all_worlds.py']:
            archive.write(ROOT/'Tools/unity'/name,'Tools/unity/'+name)
        manifest=ROOT/'Publication/test-data-manifest.json'
        archive.write(manifest,'Publication/test-data-manifest.json')
        audit=ROOT/'Build/unity-world-source-audit.json'
        if audit.exists():archive.write(audit,'SOURCE-AUDIT.json')
        notice=ROOT/'Build/cloud/recheck/DATA-NOTICE.txt'
        if notice.exists():archive.write(notice,'DATA-NOTICE.txt')
    print(args.out, args.out.stat().st_size,'bytes')
    with zipfile.ZipFile(args.out) as archive:
        bad=archive.testzip()
        if bad:raise ValueError('Package CRC failed: '+bad)
        print('Package CRC verified:',len(archive.infolist()),'files')

if __name__=='__main__':main()

````

## Tools/unity/port_all_worlds.py

SHA-256: `415f2d4277cf0c0358af235df5f57657065501780e3544a1f693930fc35f926f`

````python
#!/usr/bin/env python3
"""Fetch source-backed scene inputs, export active maps, and report every failure explicitly."""
import argparse
import configparser
import xml.etree.ElementTree as ET
import hashlib
import json
from pathlib import Path
import re
import urllib.parse
import urllib.request
import zipfile
import struct
from cached_remote_zip import CachedRemoteZip
from export_world import ini,export_scene

ROOT=Path(__file__).resolve().parents[2]

def download(root):
    manifest=json.loads((ROOT/'Publication/test-data-manifest.json').read_text())
    file_id=re.search(r'/d/([^/]+)',manifest['google_drive_url'])[1]
    endpoint='https://drive.usercontent.google.com/download'
    with urllib.request.urlopen(endpoint+'?'+urllib.parse.urlencode(dict(id=file_id,export='download')),timeout=30) as response:
        page=response.read(100000).decode('utf-8')
    params=dict(re.findall(r'name="([^"]+)" value="([^"]+)"',page))
    if params.get('id')!=file_id or params.get('confirm')!='t':raise ValueError('Unrecognized public download form')
    remote=CachedRemoteZip(endpoint+'?'+urllib.parse.urlencode(params),manifest['bytes'],root/'Build/world-range-cache.zip')
    records=[]
    with zipfile.ZipFile(remote) as archive:
        index_bytes=archive.read('DATA-FILES.json')
        (root/'Build/world-data-index.json').write_bytes(index_bytes)
        index={r['path']:r for r in json.loads(index_bytes)}
        selected=[]
        for info in archive.infolist():
            name=info.filename
            if name in ['Server/configs/SceneInfo.ini','Server/configs/MonsterAttrExTable.txt','Assets/CanonicalCY/Data/ConfigFolder/SceneDefineEx.txt'] or name.startswith('Server/Game_2/Scene/') or (name.startswith('Assets/CanonicalCY/Data/') and name.lower().endswith(('.scene','.terrain','.heightmap','.gridinfo'))):
                selected.append(info)
        pending=[]
        for info in selected:
            expected=index[info.filename];dest=(root/info.filename).resolve()
            if not dest.is_relative_to(root):raise ValueError('Unsafe archive path')
            if dest.exists():
                if hashlib.sha256(dest.read_bytes()).hexdigest()!=expected['sha256']:raise ValueError('Local data differs; refusing overwrite: '+info.filename)
            else:pending.append(info)
        spans=[]
        for info in sorted(pending,key=lambda i:i.header_offset):
            start=info.header_offset;end=min(remote.size,start+30+len(info.filename.encode('utf8'))+len(info.extra)+info.compress_size+512)
            if spans and start-spans[-1][1]<=65536 and end-spans[-1][0]<=8*1024*1024:
                spans[-1]=(spans[-1][0],max(spans[-1][1],end))
            else:spans.append((start,end))
        print(f'Selected {len(selected)} members; {len(pending)} missing locally; {len(spans)} ranges, {sum(b-a for a,b in spans)/1048576:.1f} MiB',flush=True)
        remote.prefetch(spans)
        for i,info in enumerate(selected,1):
            path=root/info.filename;expected=index[info.filename]
            if not path.exists():
                data=archive.read(info)
                if len(data)!=expected['bytes'] or hashlib.sha256(data).hexdigest()!=expected['sha256']:raise ValueError('Member checksum mismatch: '+info.filename)
                path.parent.mkdir(parents=True,exist_ok=True)
                with path.open('xb') as stream:stream.write(data)
            records.append(dict(path=info.filename,sha256=expected['sha256'],bytes=expected['bytes']))
            if i%500==0:print(f'Verified {i}/{len(selected)} members',flush=True)
    (root/'Build/unity-world-source-audit.json').write_text(json.dumps(dict(archive=manifest['name'],archiveMemberCount=len(archive.infolist()),llicenseNamedMembers=[n for n in archive.namelist() if 'llicense' in n.lower()],checkedMembers=records,rangeBytesTransferred=remote.transferred,integrityScope='Member CRC and SHA-256 from embedded index; full archive hash not verified'),ensure_ascii=False,indent=2))
    # The cache holds compressed source ranges only; all selected members have verified retained copies.
    remote.cache.unlink()

def verified_aliases(root, config):
    index_path=root/'Build/world-data-index.json'
    if not index_path.exists(): index_path=root/'Build/cloud/recheck/DATA-FILES.json'
    if not index_path.exists(): return {}
    index={row['path'].casefold():row for row in json.loads(index_path.read_text())}
    data=root/'Assets/CanonicalCY/Data'
    raw=(data/'ConfigFolder/SceneDefineEx.txt').read_bytes()
    magic,columns,rows,pool_size=struct.unpack_from('<4I',raw)
    if magic!=0xDDBBCC00 or columns<5 or len(raw)!=16+columns*4+columns*rows*4+pool_size:raise ValueError('Invalid SceneDefineEx DBC')
    types=struct.unpack_from('<'+'I'*columns,raw,16)
    if types[4]!=2: raise ValueError('SceneDefineEx resource column is not STRING')
    base=16+4*columns;pool=raw[base+4*columns*rows:];definitions={}
    for r in range(rows):
        cells=struct.unpack_from('<'+'I'*columns,raw,base+4*columns*r)
        offset=cells[4]
        if offset>=len(pool):raise ValueError('Invalid DBC string offset')
        text=pool[offset:pool.index(b'\0',offset)]
        try: name=text.decode('utf8')
        except UnicodeDecodeError:name=text.decode('gb18030')
        definitions[cells[0]]=name
    aliases={}
    for section in config.sections():
        if not section.startswith('scene') or not section[5:].isdigit():continue
        sid=int(section[5:]);row=config[section]
        if row.get('active')!='1' or row.get('type')!='0':continue
        definition=definitions.get(sid)
        if not definition:continue
        source=root/'Server/Game_2/Scene'/row.get('file','')
        if not source.is_file():continue
        nav=ini(source)['System'].get('navmapname')
        if not nav:continue
        server_nav=root/'Server/Game_2/Scene'/nav
        if not server_nav.is_file():continue
        server_hash=hashlib.sha256(server_nav.read_bytes()).hexdigest()
        stem=Path(definition).stem
        matches=[v for key,v in index.items() if key.startswith('assets/canonicalcy/data/') and key.endswith('/'+stem.casefold()+'.path') and v['sha256']==server_hash]
        if len(matches)!=1:continue
        aliases[sid]=dict(kind='client-dbc-with-matching-navigation-sha256',resource=definition,
            navigationSha256=server_hash,clientNavigation=matches[0]['path'],serverNavigation=str(server_nav.relative_to(root)))
    return aliases


def export_all(root,out):
    config=ini(root/'Server/configs/SceneInfo.ini')
    aliases=verified_aliases(root,config)
    catalog=[];failed=[];inactive=[]
    for section in config.sections():
        if not section.startswith('scene') or not section[5:].isdigit():continue
        sid=int(section[5:]);row=config[section]
        if row.get('active')!='1':inactive.append(sid);continue
        try:
            catalog.append(export_scene(root/'Server',root/'Assets/CanonicalCY/Data',sid,out,aliases))
        except (ValueError,KeyError,OSError,IndexError,TypeError,UnicodeError,ET.ParseError,configparser.Error,OverflowError) as error:
            failed.append(dict(sceneId=sid,name=row.get('name',''),sceneType=row.get('type'),file=row.get('file'),reason=str(error)))
        if (len(catalog)+len(failed))%25==0:print(f'Processed {len(catalog)+len(failed)} active scenes: {len(catalog)} exported, {len(failed)} blocked',flush=True)
    out.mkdir(parents=True,exist_ok=True)
    (out/'catalog.json').write_text(json.dumps(dict(schema=1,scenes=catalog),ensure_ascii=False,indent=2))
    report=dict(exported=len(catalog),blocked=len(failed),inactive=len(inactive),entityCount=sum(s['entityCount'] for s in catalog),scenes=catalog,failures=failed,inactiveSceneIds=inactive)
    (out/'port-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k not in ['scenes','failures','inactiveSceneIds']},ensure_ascii=False),flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--out',type=Path,default=ROOT/'Build/unity-world')
    ap.add_argument('--no-download',action='store_true')
    args=ap.parse_args()
    if not args.no_download:download(args.root.resolve())
    export_all(args.root.resolve(),args.out.resolve())

if __name__=='__main__':main()

````

## Tools/unity/publish_release.py

SHA-256: `8b3bf6275ba087bb43cd855038b32a3a0e9438aa76426455801f93e79127b19c`

````python
#!/usr/bin/env python3
"""Resume and publish the user's authorized Unity port Release after GitHub API access is enabled."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
ROOT=Path(__file__).resolve().parents[2]
BUILD=ROOT/'Build'
REPO='a002lamlam-ship-it/372dragon'
TAG='unity-native-port-20261027'

def gh(*args):
    return subprocess.check_output(['gh',*args],cwd=ROOT,text=True)

def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    manifest=json.loads((BUILD/'release-assets.json').read_text())
    for item in manifest['assets']:
        p=BUILD/item['name']
        if not p.is_file() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
            raise RuntimeError('Asset changed; rebuild release manifest: '+item['name'])
    # API preflight before any remote mutation. Never replace platform authentication.
    info=json.loads(gh('api','repos/'+REPO))
    if not info.get('permissions',{}).get('push'):raise RuntimeError('GitHub contents/write permission is required')
    releases=json.loads(gh('api','repos/'+REPO+'/releases?per_page=100'))
    release=next((r for r in releases if r['tag_name']==TAG),None)
    if release is None:
        gh('release','create',TAG,'--repo',REPO,'--target',manifest['baseCommit'],'--draft','--prerelease','--latest=false','--title','Unity native port: maps, original art and development PvE','--notes-file',str(BUILD/'RELEASE-NOTES.md'))
        release=json.loads(gh('api',f'repos/{REPO}/releases/tags/{TAG}'))
    if not release['draft']:
        raise RuntimeError('Release already published; refusing to alter existing published assets')
    for item in manifest['assets']:
        remote=json.loads(gh('api',f'repos/{REPO}/releases/{release["id"]}/assets?per_page=100'))
        existing=next((a for a in remote if a['name']==item['name']),None)
        if existing:
            if existing['size']!=item['bytes']:raise RuntimeError('Existing remote asset differs: '+item['name'])
            digest=existing.get('digest')
            if digest and digest!='sha256:'+item['sha256']:raise RuntimeError('Existing remote asset checksum differs: '+item['name'])
            if not digest:
                with tempfile.TemporaryDirectory(prefix='dragon-verify-') as tmp:
                    gh('release','download',TAG,'--repo',REPO,'--pattern',item['name'],'--dir',tmp)
                    if sha(Path(tmp)/item['name'])!=item['sha256']:raise RuntimeError('Remote asset hash differs: '+item['name'])
            print('Verified existing:',item['name'],flush=True)
        else:
            gh('release','upload',TAG,str(BUILD/item['name']),'--repo',REPO)
            print('Uploaded:',item['name'],flush=True)
    remote=json.loads(gh('api',f'repos/{REPO}/releases/{release["id"]}/assets?per_page=100'))
    for item in manifest['assets']:
        a=next(a for a in remote if a['name']==item['name'])
        assert a['size']==item['bytes']
        if a.get('digest'):assert a['digest']=='sha256:'+item['sha256']
    gh('release','edit',TAG,'--repo',REPO,'--draft=false','--prerelease','--latest=false')
    # Verify an actual downloadable ZIP after publication, not only the release page.
    with tempfile.TemporaryDirectory(prefix='dragon-download-') as tmp:
        name='UnityOriginalActors-Starter.zip'
        gh('release','download',TAG,'--repo',REPO,'--pattern',name,'--dir',tmp)
        expected=next(i['sha256'] for i in manifest['assets'] if i['name']==name)
        assert sha(Path(tmp)/name)==expected
    print('RELEASE_PUBLISHED_AND_DOWNLOAD_VERIFIED',release['html_url'])
if __name__=='__main__':main()

````

## Tools/unity/remote_zip.py

SHA-256: `ae8de3fb992b87008c32ae7bca0f4beba23f7fe4bcb16dc3037f1ef462cd0b8d`

````python
"""Seekable HTTP byte-range ZIP reader. Refuses ignored or truncated ranges."""
import io,urllib.request
from pathlib import Path
class RemoteZip(io.RawIOBase):
 def __init__(self,url,size):self.url=url;self.size=size;self.pos=0;self.transferred=0
 def seekable(self):return True
 def readable(self):return True
 def tell(self):return self.pos
 def seek(self,offset,whence=0):
  self.pos=offset if whence==0 else (self.pos+offset if whence==1 else self.size+offset)
  return self.pos
 def read(self,n=-1):
  n=self.size-self.pos if n<0 else min(n,self.size-self.pos)
  if n<=0:return b''
  end=self.pos+n-1
  req=urllib.request.Request(self.url,headers={'Range':f'bytes={self.pos}-{end}'})
  with urllib.request.urlopen(req,timeout=60) as r:
   if r.status!=206 or r.headers.get('Content-Range')!=f'bytes {self.pos}-{end}/{self.size}':raise ValueError('Server did not honor byte range')
   data=r.read(n+1)
  if len(data)!=n:raise ValueError('Incomplete range')
  self.pos+=n;self.transferred+=n
  return data

````
