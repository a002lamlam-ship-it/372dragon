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
