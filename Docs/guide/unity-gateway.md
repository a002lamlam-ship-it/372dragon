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
