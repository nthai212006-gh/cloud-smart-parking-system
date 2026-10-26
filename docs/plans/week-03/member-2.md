# KẾ HOẠCH CHI TIẾT TUẦN 3 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, PHÂN TÍCH DỮ LIỆU, GIÁM SÁT & ĐẢM BẢO CHẤT LƯỢNG (DEVOPS / QA / ANALYTICS)
* **Thành viên:** Nguyễn Trung Hải
* **Mã số sinh viên (MSSV):** 24110207
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Thời gian thực hiện Tuần 3:** 20/10/2026 – 26/10/2026
* **Tổng thời gian phân bổ:** **8.5 giờ** (Quy định: ≥ 8.0 giờ)

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN 3
1. **Thiết lập hệ thống Giám sát & Cảnh báo tập trung (Amazon CloudWatch):**
   - Xây dựng CloudWatch Dashboard `SmartParking-Dashboard` với 4 widgets theo dõi toàn diện hiệu năng và lưu lượng (Invocations, Errors, Duration, 4xx/5xx).
   - Thiết lập 02 CloudWatch Alarms: Cảnh báo lỗi thực thi (`Errors >= 1`) và cảnh báo độ trễ xử lý AI (`Duration > 5000ms`).
   - Xây dựng các câu truy vấn lọc nhật ký chuyên sâu trên CloudWatch Logs Insights.
2. **Thiết lập Phân tích dữ liệu kinh doanh với Amazon Athena:**
   - Cấu hình Athena Workgroup `smartparking`, thiết lập Output location tại `s3://smart-parking-images-24110207/athena-logs/`.
   - Tạo Database `smart_parking_db` và External Table `parking_tickets_analytics`.
   - Viết và chạy 5 câu truy vấn SQL nghiệp vụ: Thống kê tổng doanh thu; Doanh thu theo loại xe; Giờ cao điểm (Peak Hours); Thời gian đỗ trung bình; Báo cáo tỷ lệ nhận diện biển số vs lỗi `UNKNOWN`.
3. **Tối ưu hóa Bảo mật lưu trữ đám mây (S3 Storage Security):**
   - Kích hoạt mã hóa phía máy chủ SSE-S3 (khóa `AES-256`) trên bucket `smart-parking-images-24110207`.
   - Cấu hình Block Public Access bảo vệ an toàn các tệp ảnh biển số xe (PII).
   - Cấu hình S3 Static Website Hosting cho thư mục frontend, thiết lập bucket policy an toàn.
4. **Thu thập bộ hồ sơ minh chứng Tuần 3 (`evidence/week3/`):**
   - Chụp toàn màn hình trọn bộ 8 ảnh minh chứng console có Account ID, Region `us-east-1` và đồng hồ hệ thống theo đúng quy định của GVHD.
   - Kiểm toán chi phí AWS Billing xác nhận phát sinh an toàn **$0.00**, thực hiện End Lab bảo toàn ngân sách.
5. **Hoàn thiện tài liệu và đồng bộ Git:**
   - Soạn thảo Worklog cá nhân `docs/worklogs/week-03/member-2.md` và tổng hợp nhóm `docs/worklogs/week-03/overview.md`.
   - Commit toàn bộ sản phẩm của Người 2 lên nhánh `main`.

---

## II. ĐỐI CHIẾU VỚI KẾT QUẢ GIT TUẦN 2
* **Điểm kế thừa từ Tuần 2:**
  - Bucket S3 `smart-parking-images-24110207` và bảng DynamoDB `ParkingTickets` đã có dữ liệu vé thật và ảnh thật (Commit `619b547`).
  - Đã có báo cáo kiểm thử 120 ảnh Rekognition đạt 96.7% trong `docs/worklogs/week-02/rekognition_evaluation_report.md`.
  - Bộ 8 ảnh minh chứng Tuần 2 đã được lưu trữ hoàn chỉnh tại `evidence/week2/`.
* **Nhiệm vụ cần giải quyết triệt để trong Tuần 3:**
  - Khai thác thư mục `athena-logs/` đã chuẩn bị từ Tuần 1 để đưa vào hoạt động thực tế với Amazon Athena.
  - Chuyển đổi từ việc xem log thủ công trên từng Lambda sang Dashboard tập trung và hệ thống Alarms tự động.
  - Tối ưu hóa cấu hình bảo mật dữ liệu lưu trữ theo chuẩn AWS Well-Architected Framework.

---

## III. LỊCH TRÌNH THỰC HIỆN CHI TIẾT (4 BUỔI - TỔNG 8.5 GIỜ)

### Buổi 1 (Thứ 4: 21/10/2026 | 19:00 - 21:30 | 2.5 giờ): Thiết lập CloudWatch Dashboard & Alarms
* **Mục tiêu:** Xây dựng trung tâm giám sát sức khỏe hệ sinh thái Serverless.
* **Nhiệm vụ cụ thể:**
  - Đăng nhập AWS Console (`us-east-1`), mở dịch vụ Amazon CloudWatch.
  - Tạo Dashboard mới: `SmartParking-Dashboard`:
    - Widget 1: Line chart theo dõi `Invocations` và `Errors` của 2 hàm Lambda.
    - Widget 2: Line chart theo dõi `Duration` (Average và Maximum).
    - Widget 3: Line chart theo dõi `Count`, `4XXError`, `5XXError` của API Gateway.
    - Widget 4: Số lượng bản ghi trong DynamoDB.
  - Khởi tạo 02 CloudWatch Alarms:
    - Alarm 1 (`SmartParking-Lambda-Errors`): Metric `Errors >= 1` trong chu kỳ 5 phút.
    - Alarm 2 (`SmartParking-Lambda-Duration`): Metric `Duration > 5000ms` trong chu kỳ 5 phút.
  - Mở CloudWatch Logs Insights, soạn thảo và lưu 2 câu query tra cứu log bóc tách biển số và thời gian gọi Rekognition.
* **Sản phẩm:** Dashboard hoạt động trực quan, 2 Alarms ở trạng thái `OK`, 2 query Logs Insights sẵn sàng.

---

### Buổi 2 (Thứ 6: 23/10/2026 | 19:30 - 21:30 | 2.0 giờ): Thiết lập Amazon Athena & Chạy 5 Câu Truy vấn SQL
* **Mục tiêu:** Cung cấp tính năng phân tích dữ liệu lưu lượng và doanh thu theo giờ theo đúng đề cương.
* **Nhiệm vụ cụ thể:**
  - Mở dịch vụ Amazon Athena, cấu hình Workgroup `smartparking`:
    - Output location: `s3://smart-parking-images-24110207/athena-logs/`.
  - Thực thi lệnh DDL tạo cơ sở dữ liệu:
    ```sql
    CREATE DATABASE IF NOT EXISTS smart_parking_db;
    ```
  - Tạo External Table `parking_tickets_analytics` đọc dữ liệu JSON từ S3 `analytics-data/`.
  - Nạp dữ liệu kiểm thử (mẫu 50 bản ghi vé xe đỗ qua các khung giờ khác nhau).
  - Chạy và ghi nhận kết quả của bộ 5 câu truy vấn SQL:
    1. Tổng doanh thu bãi xe (`SUM(fee)`).
    2. Doanh thu và số lượng theo loại xe (Xe máy vs Ô tô).
    3. Thống kê lưu lượng xe vào theo từng khung giờ (Peak Hours).
    4. Thời gian đỗ xe trung bình của từng loại xe.
    5. Tỷ lệ biển số nhận diện thành công vs cờ `UNKNOWN`.
* **Sản phẩm:** Database, bảng dữ liệu và kết quả 5 câu truy vấn SQL phân tích kinh doanh hiển thị trên Athena Console.

---

### Buổi 3 (Thứ 7: 24/10/2026 | 19:30 - 21:30 | 2.0 giờ): Bảo mật S3, Hosting Web & Test Kích hoạt Alarm
* **Mục tiêu:** Tăng cường an ninh hạ tầng lưu trữ và kiểm thử cơ chế cảnh báo tự động.
* **Nhiệm vụ cụ thể:**
  - Truy cập S3 Console, kiểm tra bucket `smart-parking-images-24110207`:
    - Bật mã hóa mặc định: **Server-Side Encryption with Amazon S3 managed keys (SSE-S3, AES-256)**.
    - Kích hoạt **Block Public Access** cho các thư mục nhạy cảm chứa ảnh xe (`in/`, `out/`).
  - Thiết lập S3 Static Website Hosting cho thư mục frontend, phối hợp cùng SV1 kiểm thử giao diện web gọi API.
  - Tiến hành kịch bản kiểm thử kích hoạt CloudWatch Alarm:
    - Gửi request chứa payload Base64 hỏng để gây lỗi Lambda $\rightarrow$ Quan sát trên CloudWatch Alarm Console trạng thái chuyển từ `OK` sang `In ALARM`.
    - Chụp lại màn hình minh chứng sự cố được phát hiện tự động.
* **Sản phẩm:** S3 bucket được mã hóa an toàn, website tĩnh hoạt động, minh chứng Alarm chuyển trạng thái.

---

### Buổi 4 (Chủ nhật: 26/10/2026 | 14:00 - 16:00 | 2.0 giờ): Thu thập Minh chứng, Kiểm toán Chi phí & Báo cáo
* **Mục tiêu:** Hoàn thiện trọn bộ hồ sơ nghiệm thu Tuần 3 theo quy chuẩn kiểm định của GVHD.
* **Nhiệm vụ cụ thể:**
  - Chụp ảnh màn hình minh chứng đầy đủ theo tiêu chuẩn (Hiển thị rõ Account ID, Region `us-east-1` và đồng hồ hệ thống):
    - `evidence/week3/01_cloudwatch_dashboard.png`: CloudWatch Dashboard tổng hợp 4 widgets.
    - `evidence/week3/02_cloudwatch_alarms.png`: Danh sách 2 CloudWatch Alarms kèm cấu hình ngưỡng.
    - `evidence/week3/03_cloudwatch_logs_insights.png`: Màn hình truy vấn Logs Insights bóc tách log biển số.
    - `evidence/week3/04_athena_database_tables.png`: Giao diện Athena Query Editor hiển thị database và schema bảng.
    - `evidence/week3/05_athena_sql_queries.png`: Bảng kết quả chạy các câu truy vấn SQL thống kê doanh thu và lưu lượng.
    - `evidence/week3/06_api_security_throttling.png`: Cấu hình Throttling Rate 10 req/s và phản hồi HTTP 429.
    - `evidence/week3/07_s3_encryption_security.png`: Cấu hình S3 Default Encryption SSE-S3 và Block Public Access.
    - `evidence/week3/08_frontend_web_dashboard.png`: Màn hình giao diện Web UI chạy trên trình duyệt gọi API thành công.
  - Kiểm toán AWS Billing Dashboard xác nhận mức chi phí phát sinh an toàn (**$0.00**).
  - Soạn thảo Worklog cá nhân `docs/worklogs/week-03/member-2.md` và tổng hợp nhóm `docs/worklogs/week-03/overview.md`.
  - Thực hiện lệnh **End Lab** an toàn trên AWS Academy để bảo toàn ngân sách.
  - Commit toàn bộ minh chứng và tài liệu của Người 2 lên nhánh `main`.
* **Sản phẩm:** Bộ 8 ảnh minh chứng Tuần 3, nhật ký đầy đủ 8.5 giờ và mã nguồn đồng bộ trên Git.

---

## IV. BẢNG TỔNG HỢP GIỜ LÀM VIỆC DỰ KIẾN - SINH VIÊN 2
| Buổi làm việc | Ngày thực hiện | Khung giờ | Nội dung chính | Số giờ |
| :---: | :---: | :---: | :--- | :---: |
| Buổi 1 | 21/10/2026 (Thứ 4) | 19:00 - 21:30 | Thiết lập CloudWatch Dashboard 4 widgets, tạo 2 Alarms lỗi & độ trễ | 2.5h |
| Buổi 2 | 23/10/2026 (Thứ 6) | 19:30 - 21:30 | Cấu hình Amazon Athena, tạo database, bảng và chạy 5 câu SQL phân tích | 2.0h |
| Buổi 3 | 24/10/2026 (Thứ 7) | 19:30 - 21:30 | Kích hoạt mã hóa S3 SSE-S3, Block Public Access, test kích hoạt Alarm | 2.0h |
| Buổi 4 | 26/10/2026 (Chủ nhật) | 14:00 - 16:00 | Thu thập bộ 8 ảnh minh chứng console, kiểm toán Billing $0.00 & Git | 2.0h |
| **Tổng cộng** | | | **Tổng thời gian thực tế cam kết** | **8.5 giờ** |
*(Đạt chỉ tiêu môn học quy định: ≥ 8.0 giờ/tuần)*
