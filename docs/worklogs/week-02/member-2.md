# NHẬT KÝ CHI TIẾT TUẦN 2 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, QUẢN TRỊ DỮ LIỆU & ĐẢM BẢO CHẤT LƯỢNG (INFRASTRUCTURE / DATA / QA)
* **Thành viên:** Nguyễn Trung Hải (MSSV: 24110207)
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Môi trường triển khai:** AWS Learner Lab (`us-east-1`)
* **Tổng thời gian thực tế hoàn thành:** **8.5 giờ** (Chỉ tiêu môn học: ≥ 8.0 giờ)

---

## 1. BẢNG NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng thực tế |
| :---: | :---: | :---: | :--- | :--- |
| **14/10/2026**<br>(Thứ 3) | 19:00 - 21:30 | 2.5h | - Đăng nhập AWS Learner Lab (`us-east-1`), cấu hình S3 CORS trên bucket `smart-parking-images-24110207` cho phép GET, PUT, POST.<br>- Xác thực quyền của `LabRole` đối với Rekognition, DynamoDB và S3 qua AWS SDK/CLI.<br>- Kiểm tra bảng DynamoDB `ParkingTickets` (PK: `ticketId`, On-demand mode, Active). | S3 Bucket CORS policy cấu hình thành công.<br>Bảng DynamoDB Active sẵn sàng lưu vé. |
| **16/10/2026**<br>(Thứ 5) | 19:30 - 21:30 | 2.0h | - Viết và chạy script `scripts/evaluate_rekognition_accuracy.py`.<br>- Chạy kiểm thử Rekognition `DetectText` trên toàn bộ 120 ảnh dataset mẫu (5 nhóm).<br>- Thống kê tỷ lệ nhận diện: Ô tô rõ (100%), Xe máy rõ 2 dòng (100%), Ảnh góc nghiêng/thiếu sáng (80%), Bắt ngoại lệ UNKNOWN (100%). | File báo cáo đánh giá chi tiết:<br>`docs/worklogs/week-02/rekognition_evaluation_report.md` |
| **17/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Triển khai 2 hàm Lambda `SmartParking-Checkin` và `SmartParking-Checkout` (Python 3.11, Timeout 15s, Memory 256MB, gắn `LabRole` và 3 tag chuẩn).<br>- Triển khai Amazon API Gateway `SmartParking-API` (Stage `dev`), mở 2 endpoints `/checkin` và `/checkout`.<br>- Chạy kiểm thử toàn trình bằng script `scripts/test_api_endpoints.py`.<br>- Xác minh trên DynamoDB: Đã lưu thành công 2 vé xe thật (`eeca78ee...` và `99ec3ca4...`), biển số `29B155555`, cước phí 5.000 VNĐ, trạng thái `COMPLETED`.<br>- Xác minh trên S3: Đã lưu 2 file ảnh xe vào trong thư mục `in/`. | API Gateway Endpoint:<br>`https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev`<br>Dữ liệu vé thật trong DynamoDB & ảnh trong S3. |
| **19/10/2026**<br>(Chủ nhật) | 14:00 - 16:00 | 2.0h | - Thu thập trọn bộ 8 ảnh màn hình minh chứng console (Account ID `0287-8854-3565`, Region `us-east-1`, đồng hồ máy tính của sinh viên).<br>- Kiểm toán chi phí AWS Billing xác nhận `$0.00` an toàn.<br>- Thực hiện **End Lab** an toàn trên AWS Academy.<br>- Đồng bộ và commit toàn bộ dữ liệu, mã nguồn và minh chứng lên nhánh `main`. | Trọn bộ 8 ảnh trong thư mục `evidence/week2/`<br>Ảnh `08_cost_and_billing.png` ($0.00) |

---

## 2. KẾT QUẢ ĐẠT ĐƯỢC & SỐ LIỆU ĐỊNH LƯỢNG

1. **Hiệu năng hệ thống (System Performance):**
   - Thời gian xử lý hàm Check-in Lambda + Rekognition: **`914.78 ms`** (Dưới 1 giây).
   - Bộ nhớ RAM tiêu thụ: **`88 MB / 256 MB`** (Tối ưu tài nguyên).
2. **Độ chính xác AI (Rekognition & Regex):**
   - Tổng số ảnh kiểm thử: **120 ảnh**.
   - Số trường hợp xử lý chuẩn xác: **116 / 120 trường hợp** (Đạt tỷ lệ **96.7%**).
   - Biển số xe máy 2 dòng được gộp và làm sạch chuẩn xác thành `29B155555`.
   - 100% các trường hợp ảnh mờ / hỏng được phân loại an toàn vào cờ `UNKNOWN`, không gây crash server.
3. **Quản trị chi phí (Cost Management):**
   - Chi phí phát sinh thực tế: **`$0.00`** (Tận dụng 100% Free Tier, bảo toàn ngân sách $100 của nhà trường).

---

## 3. DANH MỤC ẢNH MINH CHỨNG ĐÃ THU THẬP (`evidence/week2/`)

Toàn bộ 8 ảnh minh chứng đã được chụp toàn màn hình (Full Screen), hiển thị rõ Account ID `0287-8854-3565`, Region `us-east-1` và đồng hồ hệ thống:

| Tên file | Mô tả minh chứng | Trạng thái |
| :--- | :--- | :---: |
| `01_lambda_functions.png` | Danh sách 2 hàm Lambda `SmartParking-Checkin` và `SmartParking-Checkout` (Active, Python 3.11, LabRole). | **ĐÃ HOÀN TẤT** |
| `02_apigateway_routes.png` | Cấu hình API Gateway `SmartParking-API` (fdbsdxyto1) Stage `dev` và Invoke URL. | **ĐÃ HOÀN TẤT** |
| `03_rekognition_cloudwatch.png` | Chi tiết Log stream CloudWatch hiển thị thời gian thực thi 914ms, Memory 256MB. | **ĐÃ HOÀN TẤT** |
| `04_dynamodb_items.png` | Bảng `ParkingTickets` chứa 2 bản ghi vé xe thật với đầy đủ mã vé, biển số `29B155555`, cước phí 5.000đ. | **ĐÃ HOÀN TẤT** |
| `05_s3_stored_images.png` | Bucket `smart-parking-images-24110207` folder `in/` chứa 2 file ảnh xe thật (.jpg). | **ĐÃ HOÀN TẤT** |
| `06_api_test_terminal_1.png` | Cửa sổ PowerShell chạy kiểm thử check-in nhận vé thành công (HTTP 200). | **ĐÃ HOÀN TẤT** |
| `07_api_test_terminal_2.png` | Cửa sổ PowerShell chạy kiểm thử checkout tính tiền 5.000đ và bắt ngoại lệ 400, 404 thành công. | **ĐÃ HOÀN TẤT** |
| `08_cost_and_billing.png` | AWS Billing Dashboard xác nhận chi phí an toàn `$0.00`. | **ĐÃ HOÀN TẤT** |

---

## 4. TỰ ĐÁNH GIÁ & KẾ HOẠCH TUẦN TIẾP THEO

- **Tự nhận xét:** Hoàn thành 100% khối lượng công việc được giao của Người 2, chủ động phối hợp cùng Người 1 dựng xong cả Lambda và API Gateway, hệ thống hoạt động ổn định và có dữ liệu thật.
- **Kế hoạch Tuần 3:** 
  1. Cấu hình CloudWatch Alarms giám sát lỗi Lambda (Error Rate) và thời gian thực thi (Duration).
  2. Khởi tạo Amazon Athena truy vấn phân tích logs và thống kê doanh thu bãi xe.
  3. Xây dựng giao diện Web tĩnh (Single HTML) lưu trữ trên S3 Static Website Hosting để chuẩn bị cho buổi quay video demo.
