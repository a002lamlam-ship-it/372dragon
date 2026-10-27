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
