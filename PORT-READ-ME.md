# Lấy toàn bộ code không cần ZIP

- `PORT-ALL-SOURCE.md`: toàn bộ nội dung của 92 file trong ZIP source, theo từng đường dẫn.
- `PORT-SOURCE.json`: cùng 92 file và SHA-256 từng file, để chép tự động bằng Python.
- Dữ liệu map/art nhiều GB không nằm trong hai file này; chúng không thể thay thế các gói dữ liệu.
- Nhánh này chứa code áp dụng lên base commit ghi trong manifest. `main` không được đổi.
- Unity scripts: Tools/unity/Package/Assets/DragonPort.
- Hướng dẫn và giới hạn: Tools/unity/Package/ART-COMBAT.md.

Python chỉ ghi file, không chạy các script tải được. Để tránh ghi đè project hiện tại, nên trích vào thư mục mới rồi tự chép/merge vào repository gốc.
