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
