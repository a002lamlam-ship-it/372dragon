# Unity native port — bản thử nghiệm

Tải UnityMapPort.zip và NativeServerChanges.zip để lấy 289 map, script Unity và source server/data.
UnityOriginalActors-Starter.zip là gói 8 binding actor cho Đại Lý/Vô Lượng Sơn, không gồm scenery.
Để lấy toàn bộ art đã chuyển, tải tất cả 23 UnityOriginalArt-XX.zip và giải nén chung vào project Unity.
Các ZIP độc lập; không cần ghép byte. Xem ART-COMBAT.md để import prefab và bật combat.

- 7.738 mesh, 875 mesh có animation gốc, 7.584 binding scenery và 159 binding actor.
- Combat PvE vật lý cơ bản do server quản lý HP, cooldown, di chuyển/nav, chết/hồi sinh.
- Thiếu all.obj: 755 model chưa tự ghép/gán chính xác, giữ capsule. Material/shader gần đúng.
- Chưa port toàn bộ skill, inventory, nhiệm vụ, tài khoản hoặc persistence.
- Đã kiểm Linux/native và render Blender; chưa compile/chạy Unity Editor hoặc macOS ARM64.
- Combat không khả dụng ở scene 40/95/104 do nav nguồn không được reader chấp nhận.
- Source server là delta áp dụng lên commit 436a12317f0408f303692078790f48537a33fd20, không phải full repository/binary Mac.

Dữ liệu art có điều kiện sử dụng riêng: đọc DATA-NOTICE.txt. Kiểm SHA256SUMS.txt sau khi tải.
Đã kiểm CRC/SHA-256 từng member nguồn; chưa kiểm hash toàn bộ archive nguồn 12 GB.
