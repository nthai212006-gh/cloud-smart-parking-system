# NHẬT KÝ CHI TIẾT TUẦN 1 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, QUẢN TRỊ DỮ LIỆU & ĐẢM BẢO CHẤT LƯỢNG (DEVOPS / QA)
* **Thành viên:** Sinh viên 2 (Nguyễn Trung Hải - 24110207)
* **Học phần:** Điện toán đám mây (Cloud Computing) · 2026 - 2027
* **Tổng thời gian thực tế:** **8.5 giờ** (Chỉ tiêu: ≥ 8.0 giờ)

---

## BẢNG NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **07/10/2026**<br>(Thứ 3) | 19:00 - 21:30 | 2.5h | - Khảo sát môi trường AWS Learner Lab: Kiểm tra role `LabRole`, quota Region `us-east-1`.<br>- Thiết lập quy chuẩn Tagging bắt buộc (`Project`, `Owner`, `Environment`). | Biên bản cấu hình hạ tầng<br>File `docs/guidelines/tagging-standards.md` |
| **09/10/2026**<br>(Thứ 5) | 19:30 - 21:30 | 2.0h | - Chụp 20 ảnh biển số xe máy & ô tô thực tế.<br>- **Che mờ mặt người và các thông tin nhạy cảm** bằng công cụ đồ họa.<br>- Phân loại và tối ưu kích thước ảnh mẫu (200KB - 800KB). | Thư mục `test-images/`<br>20 file ảnh đã ẩn danh hóa |
| **10/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Khởi tạo S3 Bucket `smart-parking-images-24110207`, tạo 3 thư mục ảo `in/`, `out/`, `athena-logs/`.<br>- Khởi tạo DynamoDB table `ParkingTickets` (PK: `ticketId`, On-demand).<br>- Gắn đầy đủ Tagging chuẩn. | Ảnh chụp màn hình Console S3 & DynamoDB có Account ID, Region, Timestamp trong `evidence/week1/` |
| **12/10/2026**<br>(Chủ nhật) | 14:00 - 16:00 | 2.0h | - Tổng hợp minh chứng Tuần 1 vào thư mục `evidence/week1/`.<br>- Soạn thảo file Worklog Tuần 1, đối chiếu thời lượng.<br>- Kiểm tra và tắt phiên AWS Learner Lab, xác nhận chi phí phát sinh = $0.00. | File `docs/worklogs/week-01/overview.md`<br>Ảnh chụp Billing / Cost |

---

## ĐÁNH GIÁ KẾT QUẢ VÀ TỰ NHẬN XÉT
- **Tiến độ:** Hoàn thành 100% mục tiêu hạ tầng và chuẩn bị dữ liệu thử nghiệm.
- **Tuân thủ quy định:** Đảm bảo 100% ảnh test che kín mặt người (bảo mật PII), toàn bộ tài nguyên AWS gán đủ 3 tag theo quy định.
- **Kế hoạch tuần tiếp theo (Tuần 2):** Hỗ trợ Sinh viên 1 test tải dữ liệu qua S3, thiết lập cấu hình CORS trên S3/API Gateway, chuẩn bị dữ liệu test cho quy trình xe vào/xe ra.
