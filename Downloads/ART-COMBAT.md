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
