# NHẬT KÝ CHI TIẾT TUẦN 2 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, QUẢN TRỊ DỮ LIỆU & ĐẢM BẢO CHẤT LƯỢNG (INFRASTRUCTURE / DATA / QA)
* **Thành viên:** Nguyễn Trung Hải (MSSV: 24110207)
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Tổng thời gian thực tế:** **8.5 giờ** (Chỉ tiêu môn học: ≥ 8.0 giờ)

---

## BẢNG NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **14/10/2026**<br>(Thứ 3) | 19:00 - 21:30 | 2.5h | - Đăng nhập AWS Learner Lab (`us-east-1`), cấu hình S3 CORS trên bucket `smart-parking-images-24110207`.<br>- Xác thực quyền của `LabRole` đối với Rekognition, DynamoDB và S3 qua AWS CLI.<br>- Kiểm tra bảng DynamoDB `ParkingTickets` trạng thái Active. | File cấu hình S3 CORS<br>Biên bản kiểm tra quyền LabRole |
| **16/10/2026**<br>(Thứ 5) | 19:30 - 21:30 | 2.0h | - Viết script `scripts/evaluate_rekognition_accuracy.py`.<br>- Chạy kiểm thử Rekognition `DetectText` trên 120 ảnh dataset mẫu (5 nhóm).<br>- Thống kê tỷ lệ bóc tách biển số đúng trên 90% đối với ảnh rõ nét; xác nhận nhóm ảnh lỗi gán đúng cờ `UNKNOWN`. | Script `evaluate_rekognition_accuracy.py`<br>Bảng thống kê ma trận nhận diện OCR |
| **17/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Phối hợp cùng SV1 kiểm thử tích hợp qua API Gateway Invoke URL.<br>- Kiểm tra DynamoDB Console: Các items được ghi nhận đúng chuẩn, có timestamp ISO 8601 và trạng thái `PARKED`/`COMPLETED`.<br>- Kiểm tra S3 Console: Ảnh xe vào/ra đã xuất hiện trong `in/` và `out/`. | Ảnh chụp DynamoDB Items & S3 Bucket trong `evidence/week2/` |
| **19/10/2026**<br>(Chủ nhật) | 14:00 - 16:00 | 2.0h | - Thu thập trọn bộ 7 ảnh minh chứng console (Account ID, Region `us-east-1`, đồng hồ máy tính).<br>- Kiểm toán chi phí Billing Dashboard (xác nhận $0.00).<br>- Thực hiện **End Lab** an toàn và hoàn thiện hồ sơ Worklog.<br>- Commit toàn bộ dữ liệu lên nhánh `dev`. | Thư mục `evidence/week2/`<br>Ảnh Billing xác nhận chi phí an toàn |

---

## ĐÁNH GIÁ KẾT QUẢ VÀ TỰ NHẬN XÉT
- **Tiến độ:** Hoàn thành 100% mục tiêu kiểm thử từng thành phần và đảm bảo an toàn hạ tầng.
- **Tuân thủ quy định:** Đảm bảo 100% tài nguyên dùng `LabRole`, gắn đủ 3 tag chuẩn, không phát sinh chi phí ngoài định mức ($0.00).
- **Kế hoạch tuần tiếp theo (Tuần 3):** Phối hợp với SV1 cấu hình CloudWatch Alarms giám sát lỗi Lambda (Error Rate, Duration), thiết lập database và phân vùng logs cho Amazon Athena để thống kê lưu lượng bãi xe.
