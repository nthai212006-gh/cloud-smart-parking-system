# NHẬT KÝ CHI TIẾT TUẦN 1 - SINH VIÊN 1 (MEMBER 1)
### VAI TRÒ: TRƯỞNG NHÓM / KIẾN TRÚC SERVERLESS, AI REKOGNITION & BACKEND CORE
* **Thành viên:** Sinh viên 1 (`[Họ và tên SV 1]` - `[MSSV 1]`)
* **Học phần:** Điện toán đám mây (Cloud Computing) · 2026 - 2027
* **Tổng thời gian thực tế:** **8.5 giờ** (Chỉ tiêu: ≥ 8.0 giờ)

---

## BẢNG NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **06/10/2026**<br>(Thứ 2) | 19:30 - 21:30 | 2.0h | - Đọc tài liệu AWS Rekognition `DetectText` API.<br>- Viết giải thuật Regex chuẩn hóa biển số xe Việt Nam (ghép dòng, bỏ ký tự lạ). | Script `scripts/test_plate_regex.py`<br>Commit: `feat: add plate regex parser` |
| **08/10/2026**<br>(Thứ 4) | 19:00 - 21:30 | 2.5h | - Thiết kế sơ đồ kiến trúc Serverless bằng Mermaid.<br>- Thiết kế lược đồ luồng dữ liệu (Data Flow).<br>- Định nghĩa bảng dữ liệu DynamoDB `ParkingTickets`. | Tài liệu `docs/architecture/architecture-design.md` |
| **10/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Rà soát logic `backend/checkin.py` và `backend/checkout.py`.<br>- Tinh chỉnh thuật toán tính tiền theo block giờ.<br>- Kiểm tra CORS headers và xử lý ngoại lệ biển số không đọc được. | Mã nguồn hoàn thiện trong thư mục `backend/` |
| **11/10/2026**<br>(Thứ 7) | 14:00 - 16:00 | 2.0h | - Khởi tạo GitHub repository cho nhóm.<br>- Soạn thảo file `README.md` và tổ chức cấu trúc thư mục dự án chuẩn mực.<br>- Cấu hình nhánh `dev` và Git Flow. | [GitHub Repository](https://github.com/nthai212006-gh/cloud-smart-parking-system) |

---

## ĐÁNH GIÁ KẾT QUẢ VÀ TỰ NHẬN XÉT
- **Tiến độ:** Hoàn thành 100% mục tiêu đề ra cho tuần 1.
- **Khó khăn đã giải quyết:** Rekognition trả về từng `LINE` rời rạc cho biển số 2 dòng xe máy; đã giải quyết bằng regex ghép dòng và lọc bỏ ký tự nhiễu.
- **Kế hoạch tuần tiếp theo (Tuần 2):** Đóng gói Lambda function, tích hợp API Gateway và viết test script mô phỏng gọi API.
