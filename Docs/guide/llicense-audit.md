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
