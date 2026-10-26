# NHẬT KÝ CHI TIẾT TUẦN 3 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, PHÂN TÍCH DỮ LIỆU, GIÁM SÁT & ĐẢM BẢO CHẤT LƯỢNG (DEVOPS / QA / ANALYTICS)
* **Thành viên:** Nguyễn Trung Hải (MSSV: 24110207)
* **Học phần:** Điện toán đám mây (Cloud Computing) – Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Môi trường triển khai:** AWS Learner Lab (`us-east-1`)
* **Tổng thời gian thực tế hoàn thành:** **8.5 giờ** (Chỉ tiêu môn học: $\ge$ 8.0 giờ)

---

## 1. BẢNG NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng thực tế |
| :---: | :---: | :---: | :--- | :--- |
| **21/10/2026**<br>(Thứ 3) | 19:30 - 21:30 | 2.0h | - Đăng nhập AWS Console (`us-east-1`), mở dịch vụ Amazon CloudWatch.<br>- Xây dựng CloudWatch Dashboard `SmartParking-Dashboard` tổng hợp 4 biểu đồ giám sát hiệu năng theo thời gian thực:<br>  + Biểu đồ 1: Invocations & Errors của hàm Lambda Checkin/Checkout.<br>  + Biểu đồ 2: Duration trung bình & tối đa (ms) của Rekognition/DynamoDB.<br>  + Biểu đồ 3: API Gateway Traffic & mã lỗi (Count, 4XX, 5XX).<br>  + Biểu đồ 4: DynamoDB Consumed Read/Write Capacity.<br>- Xuất file đặc tả JSON `monitoring/cloudwatch_dashboard.json`. | File cấu hình `monitoring/cloudwatch_dashboard.json`<br>Ảnh minh chứng `evidence/week3/01_cloudwatch_dashboard.png` |
| **23/10/2026**<br>(Thứ 5) | 19:30 - 21:30 | 2.0h | - Thiết lập 02 CloudWatch Alarms giám sát độ ổn định hệ thống:<br>  + `SmartParking-Lambda-Errors`: Cảnh báo lỗi thực thi khi Errors $\ge 1$ trong 1 phút.<br>  + `SmartParking-Lambda-Duration`: Cảnh báo độ trễ vượt ngưỡng khi Duration $> 5000\text{ ms}$.<br>- Viết script `scripts/trigger_alarm_test.py` gửi request sai định dạng và xử lý logic để kiểm tra phản hồi Alarm.<br>- Xác thực cả 2 Alarm chuyển trạng thái `OK` xanh lá khi hệ thống ổn định.<br>- Chạy truy vấn lọc log chuyên sâu trên **CloudWatch Log Analytics (Logs Insights)** bóc tách 10 dòng log `REPORT` có thông số Duration, Billed Duration, Memory Used. | 2 CloudWatch Alarms sẵn sàng.<br>File truy vấn `monitoring/logs_insights_queries.txt`<br>Ảnh `evidence/week3/02_cloudwatch_alarms.png`<br>Ảnh `evidence/week3/03_cloudwatch_logs_insights.png` |
| **25/10/2026**<br>(Thứ 7) | 14:00 - 16:30 | 2.5h | - Chuẩn bị bộ 50 bản ghi mẫu vé xe thực tế định dạng NDJSON trong `data/athena_sample_tickets.json` (đầy đủ các trường: `ticketId`, `plateNumber`, `vehicleType`, `checkinTime`, `checkoutTime`, `fee`, `totalHours`, `status`).<br>- Mở S3 Console, tạo folder `analytics-data/` và `athena-logs/` trong bucket `smart-parking-images-24110207`. Upload file JSON mẫu lên S3.<br>- Cấu hình Amazon Athena Query result location trỏ về `s3://smart-parking-images-24110207/athena-logs/`.<br>- Khởi tạo Database `smart_parking_db` và External Table `parking_tickets_analytics` sử dụng SerDe `org.openx.data.jsonserde.JsonSerDe`.<br>- Soạn thảo và thực thi bộ 5 câu truy vấn SQL phân tích kinh doanh trong `scripts/athena_queries.sql`:<br>  + Thống kê doanh thu theo loại phương tiện: CAR (18 lượt, 940.000 VNĐ, trung bình 52.222 VNĐ); MOTORBIKE (32 lượt, 184.000 VNĐ, trung bình 5.750 VNĐ).<br>  + Phân tích lưu lượng xe theo từng khung giờ trong ngày (Peak Hours).<br>  + Phân tích thời gian đỗ trung bình theo loại xe.<br>  + Báo cáo tỷ lệ nhận diện biển số thành công so với ngoại lệ UNKNOWN. | File `data/athena_sample_tickets.json`<br>File `scripts/athena_queries.sql`<br>Ảnh `evidence/week3/04_athena_database_tables.png`<br>Ảnh `evidence/week3/05_athena_sql_queries.png` |
| **26/10/2026**<br>(Chủ nhật) | 19:30 - 21:30 | 2.0h | - Thiết lập bảo mật API Gateway: Truy cập Stage `dev` của `SmartParking-API`, cấu hình Throttling với Rate Limit `10 requests/sec` và Burst Limit `20 requests` nhằm chống spam request và tấn công DDoS.<br>- Cấu hình bảo mật lưu trữ S3: Xác thực Default Encryption Server-side `SSE-S3 (AES-256)` và Block Public Access bật an toàn trên bucket `smart-parking-images-24110207`.<br>- Kiểm toán chi phí AWS Billing & Cost Management: Xác nhận chi phí phát sinh duy trì an toàn ở mức `$0.00` Month-to-date cost.<br>- Thực hiện **End Lab** an toàn trên AWS Academy để bảo toàn ngân sách học tập.<br>- Rà soát, chuẩn hóa trọn bộ 8 ảnh minh chứng có đầy đủ Account ID `0287-8854-3565`, Region `us-east-1` và đồng hồ hệ thống. Đồng bộ tài liệu và commit lên Git nhánh `main`. | Ảnh `evidence/week3/06_api_security_throttling.png`<br>Ảnh `evidence/week3/07_s3_encryption_security.png`<br>Ảnh `evidence/week3/08_cost_and_billing.png`<br>Báo cáo tuần hoàn tất. |

---

## 2. KẾT QUẢ ĐẠT ĐƯỢC & SỐ LIỆU ĐỊNH LƯỢNG

1. **Giám sát & Cảnh báo tập trung (CloudWatch Monitoring & Alarms):**
   - Đã xây dựng 1 Dashboard duy nhất theo dõi trực quan 4 chỉ số cốt lõi của toàn bộ hệ thống Serverless.
   - 02 CloudWatch Alarms sẵn sàng bảo vệ: phát hiện sự cố mã nguồn trong $\le 60\text{s}$ và cảnh báo độ trễ xử lý hình ảnh Rekognition vượt quá $5000\text{ms}$.
   - Khả năng tra cứu và phân tích log chuyên sâu trên CloudWatch Log Analytics đạt thời gian phản hồi dưới $500\text{ms}$ cho tập dữ liệu log kiểm thử.
2. **Phân tích dữ liệu & Dashboard báo cáo doanh thu (Amazon Athena):**
   - Khởi tạo thành công Data Lake Serverless đọc trực tiếp từ S3 không cần máy chủ ETL.
   - Tập dữ liệu 50 lượt xe gửi được bóc tách và tổng hợp chính xác:
     * Tổng số lượt xe hoàn tất: **50 lượt**.
     * Tổng doanh thu bãi xe: **1.124.000 VNĐ**.
     * Doanh thu Ô tô (CAR): **940.000 VNĐ** (18 lượt, chiếm 83.6% tổng doanh thu).
     * Doanh thu Xe máy (MOTORBIKE): **184.000 VNĐ** (32 lượt, chiếm 16.4% tổng doanh thu).
     * Thời gian quét truy vấn Athena cực nhanh: **462 ms**, lượng dữ liệu quét chỉ **11.60 KB** (tiết kiệm 100% chi phí truy vấn).
3. **Bảo mật & Quản trị rủi ro (Security & Compliance):**
   - Rate limiting trên API Gateway chặn đứng nguy cơ bùng nổ chi phí hoặc treo Lambda khi bị tấn công tần suất cao.
   - Toàn bộ ảnh biển số xe (dữ liệu nhạy cảm PII) được mã hóa tự động bằng chuẩn AES-256 của S3.
   - Chi phí tháng duy trì ở mức **`$0.00`** (bảo toàn 100% ngân sách $100 AWS Learner Lab).

---

## 3. DANH MỤC ẢNH MINH CHỨNG TUẦN 3 (`evidence/week3/`)

Toàn bộ 8 ảnh minh chứng đã được thu thập và lưu trữ đầy đủ trong thư mục `evidence/week3/` theo đúng tiêu chuẩn môn học:

| STT | Tên file minh chứng | Nội dung minh chứng | Trạng thái xác thực |
| :---: | :--- | :--- | :---: |
| 1 | [`01_cloudwatch_dashboard.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/01_cloudwatch_dashboard.png) | CloudWatch Dashboard `SmartParking-Dashboard` với 4 widgets theo dõi Invocations, Duration, API Gateway Traffic, DynamoDB Capacity | **Đã hoàn thành (100%)** |
| 2 | [`02_cloudwatch_alarms.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/02_cloudwatch_alarms.png) | Danh sách 2 CloudWatch Alarms (`SmartParking-Lambda-Errors` & `SmartParking-Lambda-Duration`) ở trạng thái `OK` xanh lá | **Đã hoàn thành (100%)** |
| 3 | [`03_cloudwatch_logs_insights.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/03_cloudwatch_logs_insights.png) | Truy vấn CloudWatch Log Analytics bóc tách 10 dòng log `REPORT` thực tế của Lambda | **Đã hoàn thành (100%)** |
| 4 | [`04_athena_database_tables.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/04_athena_database_tables.png) | Amazon Athena Query Editor hiển thị Database `smart_parking_db`, bảng `parking_tickets_analytics` và danh mục cột | **Đã hoàn thành (100%)** |
| 5 | [`05_athena_sql_queries.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/05_athena_sql_queries.png) | Kết quả thực thi câu truy vấn SQL thống kê doanh thu và lượt xe theo loại phương tiện (CAR & MOTORBIKE) | **Đã hoàn thành (100%)** |
| 6 | [`06_api_security_throttling.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/06_api_security_throttling.png) | Cấu hình Throttling trên API Gateway Stage `dev`: Rate Limit `10 req/s`, Burst Limit `20 req` | **Đã hoàn thành (100%)** |
| 7 | [`07_s3_encryption_security.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/07_s3_encryption_security.png) | Thuộc tính S3 Bucket `smart-parking-images-24110207` kích hoạt Default Encryption `SSE-S3 (AES-256)` | **Đã hoàn thành (100%)** |
| 8 | [`08_cost_and_billing.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/08_cost_and_billing.png) | AWS Billing & Cost Management xác nhận tổng chi phí tháng duy trì an toàn `$0.00` | **Đã hoàn thành (100%)** |
