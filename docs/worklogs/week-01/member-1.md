# NHẬT KÝ CHI TIẾT TUẦN 1 - SINH VIÊN 1 (MEMBER 1)
### VAI TRÒ: TRƯỞNG NHÓM / KIẾN TRÚC SERVERLESS, AI REKOGNITION & BACKEND CORE
* **Thành viên:** Sinh viên 1 (Lê Cao Việt Tín - 24110354)
* **Học phần:** Điện toán đám mây (Cloud Computing) · 2026 - 2027
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Tổng thời gian thực tế:** **8.5 giờ** (Chỉ tiêu: ≥ 8.0 giờ)
* **GitHub Repository:** [nthai212006-gh/cloud-smart-parking-system](https://github.com/nthai212006-gh/cloud-smart-parking-system) (Nhánh: `main`)

---

## BẢNG NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **06/10/2026**<br>(Thứ 2) | 19:30 - 21:30 | 2.0h | - Đọc tài liệu AWS Rekognition `DetectText` API.<br>- Viết giải thuật Regex chuẩn hóa biển số xe Việt Nam (ghép dòng, bỏ ký tự lạ). | Script [`scripts/test_plate_regex.py`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/scripts/test_plate_regex.py)<br>Commit: [`cb85da8`](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) |
| **08/10/2026**<br>(Thứ 4) | 19:00 - 21:30 | 2.5h | - Thiết kế sơ đồ kiến trúc Serverless bằng Mermaid.<br>- Thiết kế lược đồ luồng dữ liệu (Data Flow).<br>- Định nghĩa bảng dữ liệu DynamoDB `ParkingTickets`. | Tài liệu [`docs/THIET_KE_KIEN_TRUC_HE_THONG.md`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/docs/THIET_KE_KIEN_TRUC_HE_THONG.md)<br>Commit: [`cb85da8`](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) |
| **10/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Rà soát và hoàn thiện mã nguồn `backend/checkin.py` và `backend/checkout.py`.<br>- Tinh chỉnh thuật toán tính tiền theo block giờ.<br>- Kiểm tra CORS headers và xử lý ngoại lệ biển số không đọc được. | Mã nguồn [`backend/checkin.py`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/backend/checkin.py) & [`backend/checkout.py`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/backend/checkout.py)<br>Commit: [`cb85da8`](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) |
| **11/10/2026**<br>(Thứ 7) | 14:00 - 16:00 | 2.0h | - Khởi tạo GitHub repository cho nhóm.<br>- Soạn thảo file `README.md` và tổ chức cấu trúc thư mục dự án chuẩn mực.<br>- Cấu hình Git Flow và tích hợp các module của thành viên. | [GitHub Repository](https://github.com/nthai212006-gh/cloud-smart-parking-system)<br>Commit: [`cb85da8`](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) |

---

## ĐÁNH GIÁ KẾT QUẢ VÀ TỰ NHẬN XÉT
- **Tiến độ:** Hoàn thành 100% mục tiêu đề ra cho tuần 1 (Đạt 8.5h làm việc).
- **Khó khăn đã giải quyết:** Rekognition trả về từng `LINE` rời rạc cho biển số 2 dòng xe máy; đã giải quyết triệt để bằng thuật toán duyệt mảng bounding box, ghép 2 dòng liên tiếp và lọc bỏ ký tự nhiễu bằng Regex.
- **Kế hoạch tuần tiếp theo (Tuần 2):** Đóng gói Lambda function, tích hợp API Gateway và viết test script mô phỏng gọi API.
