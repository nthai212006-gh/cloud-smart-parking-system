# KẾ HOẠCH TRIỂN KHAI CHI TIẾT TUẦN 3 (WEEK 3 IMPLEMENTATION PLAN)
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING SYSTEM)

* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm đề tài:** Domain Apps (Nhóm 2 sinh viên)
* **Môi trường triển khai:** AWS Learner Lab | Region bắt buộc: `us-east-1` (N. Virginia)
* **Thời gian thực hiện Tuần 3:** **20/10/2026 – 26/10/2026**
* **Kho lưu trữ Git:** [nthai212006-gh/cloud-smart-parking-system](https://github.com/nthai212006-gh/cloud-smart-parking-system) (Nhánh chính: `main`)

---

## 📌 PHẦN 1: ĐỐI CHIẾU VÀ ĐÁNH GIÁ HIỆN TRẠNG TỪ GIT TUẦN 1 & TUẦN 2

Để xây dựng kế hoạch Tuần 3 liền mạch, khoa học và giải quyết đúng trọng tâm yêu cầu môn học, nhóm thực hiện kiểm toán (baseline audit) toàn bộ các sản phẩm đã commit trên Git trong Tuần 1 và Tuần 2:

### 1.1. Lược sử các mốc Commit quan trọng (Tuần 1 & Tuần 2)
- **Tuần 1 Baseline:**
  - `cb85da8` (*feat: Week 1 - Core Backend Logic, Architect Docs and Setup*): Khởi tạo tài liệu kiến trúc hệ thống, regex bóc tách biển số cục bộ, mã nguồn mock của 2 hàm Lambda.
  - `41ec17b` (*feat(scripts): add automated AWS setup and dataset compressor scripts for Member 2*): Tạo S3 Bucket `smart-parking-images-24110207` và bảng DynamoDB `ParkingTickets`.
  - `a2d46cd` (*feat(dataset): add complete 120 curated test images across 5 evaluation groups*): Chuẩn hóa 120 ảnh biển số xe đã làm mờ mặt (PII) thuộc 5 nhóm kiểm thử.
  - `6c5728a` (*docs & feat: add API Gateway OpenAPI spec and generate Week 1 submission docx report*): Bản đặc tả OpenAPI 3.0 (`backend/api_gateway_openapi.json`).
- **Tuần 2 Baseline:**
  - `d95bb33` (*docs & feat(member-2): complete S3 CORS setup, Rekognition QA evaluation report, and Member 2 worklogs*): Cấu hình S3 CORS, script kiểm định quyền `LabRole`, chạy batch evaluation 120 ảnh Rekognition đạt 96.7% độ chính xác, lập báo cáo QA `rekognition_evaluation_report.md`.
  - `4ced72a` (*feat(week2): implement production boto3 lambda handlers, automated test script and update member 1 worklog*): Sinh viên 1 commit mã nguồn Boto3 chính thức cho `backend/checkin.py`, `backend/checkout.py` và script test tự động `scripts/test_api_endpoints.py`.
  - `619b547` (*docs(evidence): add week 2 AWS console screenshots and integration test verification*): Đẩy trọn bộ 8 ảnh màn hình console minh chứng thực tế (Lambda, API Gateway, CloudWatch logs 914ms, DynamoDB 2 vé thật, S3 folder `in/`, Terminal tests, Billing $0.00).

---

### 1.2. Bảng ma trận đối chiếu hiện trạng và khoảng cách kỹ thuật cần thực hiện trong Tuần 3

| Thành phần hệ thống | Hiện trạng trên Git (Hết Tuần 2) | Khoảng trống kỹ thuật (Gaps) | Nhiệm vụ bắt buộc trong Tuần 3 |
| :--- | :--- | :--- | :--- |
| **Giám sát (CloudWatch Monitoring)** | Chỉ có log stream cơ bản tự sinh khi chạy Lambda (`evidence/week2/03_rekognition_cloudwatch.png`). | Chưa có Dashboard tập trung; chưa có Alarms cảnh báo lỗi hoặc cảnh báo độ trễ; chưa cấu hình thông báo SNS. | **Thiết lập CloudWatch toàn diện:** Tạo Dashboard `SmartParking-Dashboard` gom các widgets (Lambda Invocations, Errors, Duration, API Gateway 4xx/5xx/Latency); tạo 02 CloudWatch Alarms cảnh báo lỗi & timeout; viết truy vấn CloudWatch Logs Insights. |
| **Phân tích dữ liệu (Amazon Athena)** | S3 mới chỉ có folder `athena-logs/` rỗng từ Tuần 1, chưa từng tạo database hay bảng trên Athena. | Chưa có bảng dữ liệu để truy vấn; chưa có dashboard/SQL thống kê lưu lượng và doanh thu theo giờ như yêu cầu đề tài. | **Thiết lập Amazon Athena:** Tạo Database `smart_parking_db`, tạo External Table ánh xạ dữ liệu vé xe từ S3; viết 5 câu truy vấn SQL phân tích nghiệp vụ (doanh thu theo ngày/loại xe, khung giờ cao điểm, thời gian đỗ xe trung bình, tỷ lệ lỗi OCR). |
| **Bảo mật (Cloud Security)** | API Gateway mở công khai không giới hạn; S3 bật CORS `*`; chưa áp dụng cơ chế giới hạn tần suất (Rate Limiting). | Dễ bị spam request làm cạn ngân sách Lab; nguy cơ rò rỉ dữ liệu hoặc vượt hạn mức Free Tier; chưa mã hóa dữ liệu nghỉ (Encryption at Rest). | **Bảo mật nhiều lớp:** Cấu hình API Throttling & Quota (10 req/s, burst 20 req) trên API Gateway; bật mã hóa SSE-S3 (AES-256) trên S3 bucket; cấu hình S3 Block Public Access; kiểm soát payload đầu vào (input sanitization chống injection). |
| **Giao diện tích hợp (Frontend Web UI)** | Kiểm thử API hoàn toàn qua PowerShell Terminal (`scripts/test_api_endpoints.py`) và Postman. | Chưa có giao diện trực quan cho người vận hành/khách gửi xe; khó quan sát kết quả demo trực tiếp. | **Xây dựng Web Dashboard tĩnh:** Thiết kế Single Page Web App (`frontend/index.html`, `app.js`, `style.css`) cho phép tải ảnh xe vào/ra, hiển thị biển số nhận diện, thời gian và tiền cước; host tĩnh trên **S3 Static Website Hosting**. |
| **Tự động hóa & IaC (Infrastructure as Code)** | Tài nguyên AWS được tạo bán tự động qua script Python và AWS Console. | Nếu Lab bị reset hoặc sang tài khoản mới, phải thao tác thủ công lại từ đầu, mất nhiều thời gian và dễ nhầm lẫn thông số. | **Xây dựng kịch bản IaC / Automation:** Viết mẫu AWS CloudFormation Template (`iac/cloudformation_template.yaml`) hoặc Python Deployer Script tự động hóa khởi tạo toàn bộ hạ tầng (S3, DynamoDB, Lambda, API Gateway, Alarms) kèm đầy đủ 3 tag chuẩn. |
| **Quản trị chi phí & Minh chứng** | Đã thu thập 8 ảnh Tuần 2, Billing duy trì mức an toàn $0.00. | Chưa có minh chứng cho CloudWatch Alarms, Dashboard, Athena Queries, Web Hosting và Billing Tuần 3. | **Thu thập trọn bộ 8 ảnh minh chứng Tuần 3 (`evidence/week3/`)** có Account ID, Region `us-east-1` và đồng hồ hệ thống. |

---

## 🎯 PHẦN 2: MỤC TIÊU VÀ YÊU CẦU TRỌNG TÂM TUẦN 3

Căn cứ đề cương môn học của GVHD ThS. Huỳnh Xuân Phụng:  
**"Tuần 3: tích hợp, bảo mật, giám sát (CloudWatch), tự động hóa/IaC nếu có."**  
Và yêu cầu đặc thù của đề tài Smart Parking: **"dashboard thống kê theo giờ (Athena)."**

Nhóm xác định 4 mục tiêu trọng tâm trong Tuần 3:

1. **Giám sát hệ thống (CloudWatch Monitoring & Alerting):**
   - Xây dựng CloudWatch Dashboard hợp nhất theo dõi sức khỏe toàn bộ hệ sinh thái Serverless (API Gateway $\rightarrow$ Lambda $\rightarrow$ Rekognition $\rightarrow$ DynamoDB $\rightarrow$ S3).
   - Thiết lập tối thiểu 02 CloudWatch Alarms:
     * `SmartParking-Lambda-Errors`: Kích hoạt khi có lỗi thực thi (`Errors >= 1` trong 5 phút).
     * `SmartParking-Lambda-Duration`: Kích hoạt khi thời gian thực thi vượt ngưỡng an toàn (`Duration > 5000ms`).
   - Xây dựng các mẫu truy vấn chuyên sâu với CloudWatch Logs Insights để tra cứu nhanh biển số và phát hiện bất thường.
2. **Phân tích dữ liệu kinh doanh bãi xe (Amazon Athena Analytics):**
   - Thiết lập Amazon Athena kết nối với S3 log/data location.
   - Định nghĩa DDL tạo bảng `parking_tickets_analytics` cấu trúc phân vùng theo ngày/tháng.
   - Xây dựng bộ 5 câu truy vấn SQL nghiệp vụ: Thống kê doanh thu theo ngày; Thống kê lưu lượng theo khung giờ (Peak Hours); Tỷ lệ xe máy vs ô tô; Thời gian đỗ trung bình; Báo cáo các ca biển số `UNKNOWN`.
3. **Bảo mật toàn diện hệ thống (Multi-layer Security):**
   - **API Security:** Kích hoạt Throttling và Quota Limits trên Stage `dev` của API Gateway (Rate: 10 req/s, Burst: 20 req) để ngăn ngừa DoS và bảo vệ chi phí Lab.
   - **Storage Security:** Bật mã hóa SSE-S3 (Server-Side Encryption với khóa AES-256) trên S3 bucket; kích hoạt Block Public Access cho các folder dữ liệu nhạy cảm (`in/`, `out/`).
   - **Payload Security:** Kiểm tra kích thước và định dạng ảnh Base64 hợp lệ tại tầng Lambda, chặn đứng dữ liệu rác trước khi gọi Rekognition.
4. **Tích hợp Frontend Web & Tự động hóa IaC:**
   - Triển khai giao diện Web tĩnh (Single Page Application) trên S3 Static Website Hosting, tích hợp gọi trực tiếp API Gateway.
   - Viết template Infrastructure as Code (AWS CloudFormation) chuẩn hóa toàn bộ hạ tầng, đảm bảo tính tái lập (reproducibility) cao.

---

## 👥 PHẦN 3: PHÂN CÔNG NHIỆM VỤ & LỊCH TRÌNH THỰC HIỆN CHI TIẾT

### 3.1. Bảng phân công tổng quan 2 thành viên

| STT | Thành viên | MSSV | Vai trò chính trong Tuần 3 | Số giờ dự kiến | File kế hoạch chi tiết |
| :---: | :--- | :---: | :--- | :---: | :---: |
| 1 | **Lê Cao Việt Tín** | 24110354 | **Trưởng nhóm / Backend & Tích hợp:** Xây dựng CloudFormation IaC, cấu hình bảo mật API Gateway Throttling, phát triển giao diện Web tĩnh S3 | **8.5 giờ** | [docs/plans/week-03/member-1.md](docs/plans/week-03/member-1.md) |
| 2 | **Nguyễn Trung Hải** | 24110207 | **Thành viên / Hạ tầng & QA:** Thiết lập CloudWatch Dashboard & Alarms, cấu hình Amazon Athena & 5 câu SQL phân tích, bảo mật S3, thu thập minh chứng console | **8.5 giờ** | [docs/plans/week-03/member-2.md](docs/plans/week-03/member-2.md) |
| **Tổng** | **Cả nhóm** | — | **Toàn bộ khối lượng công việc Tuần 3** | **17.0 giờ** | *(Đạt chuẩn quy định môn học)* |

---

### 3.2. Lịch trình chi tiết của Sinh viên 1: Lê Cao Việt Tín (8.5 giờ)

```text
Buổi 1 (Thứ 3: 20/10/2026, 19:30 - 21:30 | 2.0h):
├── Nghiên cứu và viết template AWS CloudFormation (iac/cloudformation_template.yaml)
└── Định nghĩa tài nguyên Serverless chuẩn: S3 Bucket, DynamoDB Table, 2 Lambdas, API Gateway REST API

Buổi 2 (Thứ 5: 22/10/2026, 19:00 - 21:30 | 2.5h):
├── Cấu hình bảo mật tầng API: Thiết lập Throttling (Rate: 10 req/s, Burst: 20 req) trên API Gateway Stage dev
├── Bổ sung kiểm tra dữ liệu đầu vào (Input Validation) trong Lambda: Kiểm tra kích thước ảnh Base64 <= 5MB
└── Viết script kiểm thử bảo mật scripts/test_api_throttling.py kiểm tra phản hồi HTTP 429 Too Many Requests

Buổi 3 (Thứ 7: 24/10/2026, 14:00 - 16:00 | 2.0h):
├── Thiết kế giao diện Web tĩnh Single Page (frontend/index.html, frontend/app.js, frontend/style.css)
├── Tích hợp JavaScript Fetch API gọi trực tiếp Endpoint POST /checkin và POST /checkout
└── Thử nghiệm tải ảnh từ máy tính / camera, hiển thị kết quả vé, biển số và tính tiền trực quan

Buổi 4 (Chủ nhật: 25/10/2026, 19:30 - 21:30 | 2.0h):
├── Hỗ trợ SV2 triển khai Web UI lên S3 Static Website Hosting và kiểm thử tích hợp toàn trình
├── Rà soát mã nguồn, kiểm tra chuẩn hóa code IaC và Frontend
└── Commit và push các sản phẩm của Người 1 lên nhánh main của GitHub
```

---

### 3.3. Lịch trình chi tiết của Sinh viên 2: Nguyễn Trung Hải (8.5 giờ)

```text
Buổi 1 (Thứ 4: 21/10/2026, 19:00 - 21:30 | 2.5h):
├── Đăng nhập AWS Console us-east-1, truy cập dịch vụ Amazon CloudWatch
├── Tạo CloudWatch Dashboard "SmartParking-Dashboard" tổng hợp 4 widgets (Invocations, Errors, Duration, 4xx/5xx)
├── Tạo 02 CloudWatch Alarms: SmartParking-Lambda-Errors và SmartParking-Lambda-Duration
└── Thiết lập truy vấn CloudWatch Logs Insights trích xuất thời gian xử lý Rekognition và thống kê biển số

Buổi 2 (Thứ 6: 23/10/2026, 19:30 - 21:30 | 2.0h):
├── Cấu hình dịch vụ Amazon Athena: Tạo Workgroup "smartparking" trỏ kết quả vào S3 athena-logs/
├── Viết DDL tạo Database "smart_parking_db" và External Table "parking_tickets_analytics"
├── Đồng bộ dữ liệu lịch sử vé xe từ DynamoDB/S3 vào thư mục phân tích
└── Viết và chạy thử nghiệm bộ 5 câu truy vấn SQL phân tích nghiệp vụ (doanh thu, lưu lượng, tỷ lệ UNKNOWN)

Buổi 3 (Thứ 7: 24/10/2026, 19:30 - 21:30 | 2.0h):
├── Tối ưu hóa bảo mật hạ tầng S3: Kích hoạt mã hóa phía máy chủ SSE-S3 (AES-256)
├── Cấu hình S3 Static Website Hosting cho bucket frontend, cấp quyền bucket policy an toàn
├── Phối hợp cùng SV1 kiểm thử luồng Checkin/Checkout từ Web UI đến API Gateway và cơ sở dữ liệu
└── Kích hoạt thử nghiệm CloudWatch Alarm bằng cách gửi payload lỗi, chụp lại trạng thái ALARM

Buổi 4 (Chủ nhật: 26/10/2026, 14:00 - 16:00 | 2.0h):
├── Thu thập trọn bộ 8 ảnh màn hình console minh chứng Tuần 3 (Account ID, Region us-east-1, đồng hồ hệ thống)
├── Kiểm toán chi phí AWS Billing Dashboard đảm bảo $0.00, thực hiện End Lab an toàn
├── Hoàn thiện tài liệu kế hoạch và nhật ký công việc Tuần 3 (member-2.md, overview.md)
└── Commit và đồng bộ toàn bộ tài liệu, minh chứng Tuần 3 lên nhánh main của GitHub
```

---

## 🛠️ PHẦN 4: ĐẶC TẢ KỸ THUẬT TRIỂN KHAI TRÊN AWS (TECHNICAL SPECIFICATIONS)

### 4.1. Giám sát hệ thống với Amazon CloudWatch

#### 1. Cấu hình CloudWatch Dashboard (`SmartParking-Dashboard`):
- **Widget 1 (Lambda Health):** Biểu đồ đường (Line chart) theo dõi metric `Invocations` và `Errors` của 2 hàm `SmartParking-Checkin` và `SmartParking-Checkout` (Statistic: Sum, Period: 1 minute).
- **Widget 2 (Latency & Performance):** Biểu đồ theo dõi metric `Duration` (Statistic: Average, Maximum, Period: 1 minute).
- **Widget 3 (API Gateway Traffic):** Biểu đồ theo dõi metric `Count`, `4XXError`, `5XXError` của API `SmartParking-API` (Statistic: Sum, Period: 1 minute).
- **Widget 4 (Storage Volume):** Số lượng Items trong bảng DynamoDB `ParkingTickets` và dung lượng S3 bucket.

#### 2. Cấu hình 02 CloudWatch Alarms:
| Tên Alarm | Metric giám sát | Ngưỡng kích hoạt (Threshold) | Chu kỳ đánh giá | Hành động (Action) |
| :--- | :--- | :--- | :--- | :--- |
| `SmartParking-Lambda-Errors` | `Errors` (Namespace: `AWS/Lambda`) | $\ge 1$ lỗi | 1 chu kỳ 5 phút (1 evaluation period) | Đổi trạng thái sang `ALARM`, ghi log cảnh báo |
| `SmartParking-Lambda-Duration` | `Duration` (Namespace: `AWS/Lambda`) | $> 5.000\text{ ms}$ ($5.0$ giây) | 1 chu kỳ 5 phút | Đổi trạng thái sang `ALARM` (phát hiện nghẽn OCR) |

#### 3. Các câu truy vấn mẫu trên CloudWatch Logs Insights:
```sql
-- Truy vấn 1: Thống kê 20 lượt nhận diện biển số gần nhất và thời gian xử lý
fields @timestamp, @message
| filter @message like /plateNumber/ or @message like /REPORT/
| sort @timestamp desc
| limit 20

-- Truy vấn 2: Thống kê các trường hợp ảnh mờ bị gán nhãn UNKNOWN
fields @timestamp, @message
| filter @message like /UNKNOWN/
| stats count(*) as unknown_count by bin(1h)
```

---

### 4.2. Phân tích kinh doanh bãi xe với Amazon Athena

- **Athena Database:** `smart_parking_db`
- **Output Location:** `s3://smart-parking-images-24110207/athena-logs/`
- **DDL khởi tạo External Table:**
```sql
CREATE EXTERNAL TABLE IF NOT EXISTS smart_parking_db.parking_tickets_analytics (
    ticketId string,
    plateNumber string,
    vehicleType string,
    checkinTime string,
    checkoutTime string,
    fee int,
    totalHours int,
    status string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
    'ignore.malformed.json' = 'TRUE'
)
LOCATION 's3://smart-parking-images-24110207/analytics-data/';
```

#### 5 Câu truy vấn SQL nghiệp vụ trọng tâm:
1. **Câu 1 - Tổng doanh thu bãi xe:**
   ```sql
   SELECT SUM(fee) AS total_revenue, COUNT(*) AS total_completed_tickets 
   FROM smart_parking_db.parking_tickets_analytics 
   WHERE status = 'COMPLETED';
   ```
2. **Câu 2 - Phân bổ doanh thu theo loại phương tiện (Xe máy vs Ô tô):**
   ```sql
   SELECT vehicleType, COUNT(*) AS vehicle_count, SUM(fee) AS total_revenue, AVG(fee) AS avg_fee 
   FROM smart_parking_db.parking_tickets_analytics 
   WHERE status = 'COMPLETED' 
   GROUP BY vehicleType;
   ```
3. **Câu 3 - Thống kê lưu lượng xe vào theo từng khung giờ (Peak Hours Analysis):**
   ```sql
   SELECT SUBSTR(checkinTime, 12, 2) AS hour_of_day, COUNT(*) AS checkin_count 
   FROM smart_parking_db.parking_tickets_analytics 
   GROUP BY SUBSTR(checkinTime, 12, 2) 
   ORDER BY checkin_count DESC;
   ```
4. **Câu 4 - Thời gian đỗ xe trung bình của từng loại xe:**
   ```sql
   SELECT vehicleType, AVG(totalHours) AS avg_parked_hours, MAX(totalHours) AS max_parked_hours 
   FROM smart_parking_db.parking_tickets_analytics 
   WHERE status = 'COMPLETED' 
   GROUP BY vehicleType;
   ```
5. **Câu 5 - Báo cáo tỷ lệ nhận diện biển số thành công vs lỗi UNKNOWN:**
   ```sql
   SELECT 
       CASE WHEN plateNumber = 'UNKNOWN' THEN 'UNRECOGNIZED_UNKNOWN' ELSE 'RECOGNIZED_SUCCESS' END AS recognition_status,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM smart_parking_db.parking_tickets_analytics), 2) AS percentage
   FROM smart_parking_db.parking_tickets_analytics
   GROUP BY CASE WHEN plateNumber = 'UNKNOWN' THEN 'UNRECOGNIZED_UNKNOWN' ELSE 'RECOGNIZED_SUCCESS' END;
   ```

---

### 4.3. Bảo mật toàn diện hệ thống (Multi-layer Security)

1. **Bảo mật API Gateway (Rate Limiting & Throttling):**
   - Áp dụng trên Stage `dev`:
     * **Rate:** 10 requests / second (Tốc độ ổn định).
     * **Burst:** 20 requests (Cho phép đột biến tối đa).
   - Mục đích: Chống tấn công brute-force / DoS, bảo vệ ngân sách AWS Learner Lab không bị cạn kiệt.
2. **Bảo mật S3 Storage (Data at Rest):**
   - Kích hoạt mã hóa **Server-Side Encryption (SSE-S3)** sử dụng thuật toán chuẩn `AES-256`.
   - Cấu hình **Block Public Access (BPA)** cho toàn bộ bucket chứa ảnh vé xe để bảo vệ thông tin nhận diện biển số (PII) của khách hàng.
3. **Kiểm tra và làm sạch dữ liệu đầu vào (Input Sanitization):**
   - Lambda từ chối ngay lập tức payload nếu kích thước ảnh Base64 vượt quá $5\text{ MB}$.
   - Chuẩn hóa chuỗi ký tự bằng Regex nghiêm ngặt, ngăn chặn các ký tự điều khiển gây lỗi SQL/NoSQL injection.

---

### 4.4. Tự động hóa hạ tầng (Infrastructure as Code - IaC)

- Định nghĩa file `iac/cloudformation_template.yaml` (hoặc `iac/deploy_all.py`):
  * Khởi tạo đồng bộ: S3 Bucket (CORS + Encryption), DynamoDB Table (On-demand), 2 Lambda functions (Python 3.11, Memory 256MB, Timeout 15s, `LabRole`), API Gateway REST API kèm Throttling, CloudWatch Alarms.
  * Tự động áp dụng 3 tag quy định:
    - `Project`: `SmartParking`
    - `Owner`: `24110354_24110207`
    - `Environment`: `Development`

---

## 🧪 PHẦN 5: KẾ HOẠCH KIỂM THỬ TỪNG THÀNH PHẦN (COMPONENT TESTING PLAN)

1. **Kịch bản 1: Kiểm thử CloudWatch Alarms:**
   - Gửi payload lỗi (ví dụ chuỗi Base64 hỏng) để kích hoạt Lambda Error $\rightarrow$ Quan sát trên CloudWatch Console trạng thái chuyển từ `OK` sang `ALARM`.
2. **Kịch bản 2: Kiểm thử API Throttling (Rate Limiting):**
   - Sử dụng script `scripts/test_api_throttling.py` gửi liên tục 30 requests/giây $\rightarrow$ Kiểm tra API Gateway từ chối các request vượt ngưỡng với mã lỗi `HTTP 429 Too Many Requests`.
3. **Kịch bản 3: Kiểm thử Truy vấn Athena:**
   - Nạp dữ liệu giả lập 50 lượt xe vào S3 `analytics-data/` $\rightarrow$ Chạy lần lượt 5 câu truy vấn SQL trên Athena Console $\rightarrow$ Xác nhận kết quả trả về chính xác trong thời gian $< 3$ giây.
4. **Kịch bản 4: Kiểm thử End-to-End từ Web UI:**
   - Mở giao diện Web trên trình duyệt $\rightarrow$ Chọn ảnh xe máy $\rightarrow$ Nhấn Check-in $\rightarrow$ Hiển thị mã vé và biển số $\rightarrow$ Nhấn Check-out $\rightarrow$ Hiển thị cước phí 5.000 VNĐ chính xác.

---

## 📸 PHẦN 6: DANH MỤC HỒ SƠ MINH CHỨNG TUẦN 3 (`evidence/week3/`)

Theo quy định bắt buộc của GVHD ThS. Huỳnh Xuân Phụng, toàn bộ ảnh chụp màn hình minh chứng phải chụp **toàn màn hình máy tính (Full Screen)**, hiển thị rõ ràng:
1. **AWS Account ID** (Góc trên bên phải Console).
2. **AWS Region:** Bắt buộc là `us-east-1` (N. Virginia).
3. **Đồng hồ hệ thống máy tính:** Ngày giờ thực tế tương ứng với thời gian trong bảng Worklog.

| Tên tệp ảnh minh chứng | Nội dung minh chứng chi tiết | Tiêu chuẩn nghiệm thu |
| :--- | :--- | :--- |
| `evidence/week3/01_cloudwatch_dashboard.png` | Màn hình CloudWatch Dashboard `SmartParking-Dashboard`. | Hiển thị đầy đủ 4 widgets theo dõi Invocations, Errors, Duration và API Gateway Traffic. |
| `evidence/week3/02_cloudwatch_alarms.png` | Màn hình CloudWatch Alarms liệt kê 2 Alarms. | Thấy rõ alarm `SmartParking-Lambda-Errors` và `SmartParking-Lambda-Duration` ở trạng thái `OK` hoặc `In ALARM` khi test. |
| `evidence/week3/03_cloudwatch_logs_insights.png` | Màn hình CloudWatch Logs Insights đang chạy truy vấn tra cứu. | Thấy kết quả lọc log bóc tách biển số xe và phân tích thời gian thực thi của Rekognition. |
| `evidence/week3/04_athena_database_tables.png` | Màn hình Amazon Athena Query Editor hiển thị database và bảng. | Thấy rõ Database `smart_parking_db`, bảng `parking_tickets_analytics` và cấu trúc schema các cột. |
| `evidence/week3/05_athena_sql_queries.png` | Màn hình kết quả thực thi các câu truy vấn SQL trên Athena. | Thấy bảng kết quả thống kê doanh thu bãi xe và phân tích lưu lượng xe theo khung giờ (Peak Hours). |
| `evidence/week3/06_api_security_throttling.png` | Màn hình cấu hình Throttling trên API Gateway hoặc Terminal test 429. | Thấy cấu hình Rate Limit 10 req/s, Burst 20 req và mã lỗi HTTP 429 Too Many Requests khi bị spam. |
| `evidence/week3/07_s3_encryption_security.png` | Màn hình S3 Bucket Properties và Permissions. | Thấy rõ cấu hình Default Encryption `SSE-S3 (AES-256)` và Block Public Access bật an toàn. |
| `evidence/week3/08_frontend_web_dashboard.png` | Màn hình giao diện Web UI chạy trực tiếp trên trình duyệt. | Thấy giao diện trực quan cho phép Checkin, Checkout, hiển thị biển số nhận diện và cước phí thành công. |

---

## 💰 PHẦN 7: QUẢN LÝ NGÂN SÁCH & AN TOÀN TRÊN AWS LEARNER LAB

Để bảo toàn ngân sách cấp sẵn $100.00 của AWS Learner Lab xuyên suốt 4 tuần học:
1. **Kiểm soát dịch vụ tính phí trong Tuần 3:**
   - **Amazon CloudWatch:** Miễn phí 3 dashboards (tối đa 50 metrics), 10 alarms và 5GB dữ liệu log mỗi tháng. Sử dụng hoàn toàn trong hạn mức Free Tier.
   - **Amazon Athena:** Tính phí $5.00 cho mỗi 1TB dữ liệu quét. Tập dữ liệu kiểm thử bãi xe chỉ khoảng $\approx 100\text{ KB}$, chi phí truy vấn $\approx \$0.0000005$ (hoàn toàn $= \$0.00$).
   - **S3 Storage & Hosting:** Dung lượng web tĩnh $< 1\text{ MB}$, chi phí $= \$0.00$.
2. **Quy tắc an toàn vận hành:**
   - Tuyệt đối không bật tài nguyên ngầm tính theo giờ như EC2 lớn hoặc RDS.
   - Sau mỗi buổi làm việc, thành viên phụ trách buổi đó phải nhấn **End Lab** để đóng phiên kết nối.
   - Kiểm tra Billing Dashboard vào cuối mỗi buổi để duy trì mức chi phí phát sinh $= \mathbf{\$0.00}$.

---

## ✅ PHẦN 8: BẢNG CHECKLIST NGHIỆM THU TUẦN 3 (WEEK 3 CHECKLIST)

- [x] **1. Giám sát hệ thống (CloudWatch Monitoring):**
  - [x] Khởi tạo CloudWatch Dashboard `SmartParking-Dashboard` với đủ 4 widgets theo dõi.
  - [x] Tạo CloudWatch Alarm `SmartParking-Lambda-Errors` giám sát lỗi thực thi.
  - [x] Tạo CloudWatch Alarm `SmartParking-Lambda-Duration` giám sát độ trễ vượt ngưỡng 5s.
  - [x] Viết và lưu trữ các câu truy vấn CloudWatch Logs Insights mẫu.
- [x] **2. Phân tích dữ liệu kinh doanh (Amazon Athena):**
  - [x] Thiết lập Athena Workgroup và cấu hình S3 output location `athena-logs/`.
  - [x] Tạo Database `smart_parking_db` và External Table `parking_tickets_analytics`.
  - [x] Thực thi thành công 5 câu truy vấn SQL phân tích nghiệp vụ (doanh thu, giờ cao điểm, loại xe, lỗi OCR).
- [x] **3. Bảo mật toàn diện (Security):**
  - [x] Kích hoạt Throttling (Rate: 10 req/s, Burst: 20 req) trên API Gateway Stage `dev`.
  - [x] Kiểm tra phản hồi mã lỗi HTTP 429 khi vượt ngưỡng request.
  - [x] Bật mã hóa SSE-S3 (AES-256) trên S3 bucket.
  - [x] Cấu hình Block Public Access an toàn cho dữ liệu ảnh và vé xe.
- [x] **4. Tích hợp Web & Tự động hóa (Integration & IaC):**
  - [x] Hoàn thiện mã nguồn giao diện Web tĩnh (`frontend/index.html`, `app.js`, `style.css`).
  - [x] Triển khai giao diện web lên S3 Static Website Hosting kết nối thành công tới API Gateway.
  - [x] Soạn thảo template CloudFormation / script IaC tự động hóa khởi tạo tài nguyên.
- [x] **5. Hồ sơ & Báo cáo:**
  - [x] Chụp đầy đủ 8 ảnh minh chứng theo tiêu chuẩn trong `evidence/week3/`.
  - [x] Nhật ký cá nhân SV1 (`docs/worklogs/week-03/member-1.md`) ghi nhận đủ 8.5 giờ.
  - [x] Nhật ký cá nhân SV2 (`docs/worklogs/week-03/member-2.md`) ghi nhận đủ 8.5 giờ.
  - [x] Nhật ký tổng hợp nhóm (`docs/worklogs/week-03/overview.md`) ghi nhận đủ 17.0 giờ.
  - [x] Toàn bộ mã nguồn, tài liệu và minh chứng được commit và push lên nhánh `main`.
