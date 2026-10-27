# BÁO CÁO TIẾN ĐỘ TUẦN 3 - NHÓM DOMAIN APPS
### DỰ ÁN: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING SYSTEM)
* **Học phần:** Điện toán đám mây (Cloud Computing) – Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Thời gian thực hiện Tuần 3:** 20/10/2026 – 26/10/2026
* **Môi trường triển khai:** AWS Learner Lab (`us-east-1`)
* **Tổng thời gian tích lũy nhóm:** **17.0 giờ** (SV1: 8.5h, SV2: 8.5h – Vượt chỉ tiêu $\ge 16.0$ giờ)

---

## 1. THÀNH VIÊN VÀ PHÂN CÔNG TRÁCH NHIỆM

| Thành viên | MSSV | Vai trò chính trong dự án | Thời gian cam kết | Trạng thái Tuần 3 |
| :--- | :---: | :--- | :---: | :---: |
| **Lê Cao Việt Tín** | 24110354 | **Thành viên 1 (Trưởng nhóm):** Backend Core, IaC (CloudFormation) & Frontend Web UI | **8.5 giờ** | **ĐÃ HOÀN THÀNH 100%** |
| **Nguyễn Trung Hải** | 24110207 | **Thành viên 2:** Infrastructure, Data Analytics (Athena), Monitoring (CloudWatch) & Security | **8.5 giờ** | **ĐÃ HOÀN THÀNH 100%** |

---

## 2. TỔNG HỢP KẾT QUẢ TRIỂN KHAI TUẦN 3 CỦA CẢ 2 THÀNH VIÊN

### 2.1. Phân hệ Tự động hóa Hạ tầng (IaC) & Bảo mật API (Thành viên 1 phụ trách)
* **AWS CloudFormation Template (`iac/cloudformation_template.yaml`)**:
  - Tự động hóa 100% quy trình khởi tạo toàn bộ hạ tầng Serverless chỉ với một lệnh duy nhất.
  - Định nghĩa đầy đủ S3 Bucket, DynamoDB Table `ParkingTickets`, 2 hàm Lambda (`SmartParking-Checkin`, `SmartParking-Checkout`), API Gateway REST API (`SmartParking-API`), CloudWatch Alarms kèm 3 thẻ Tag chuẩn môn học.
* **Tăng cường Bảo mật, Xác thực Dữ liệu & Chống Race Condition**:
  - Bổ sung bộ kiểm soát kích thước payload Base64 $\le 5\text{MB}$ trong Lambda (trả về HTTP 413 Payload Too Large khi vượt quá) và xác thực loại xe hợp lệ.
  - Áp dụng cơ chế **DynamoDB Atomic Conditional Write** trong `backend/checkout.py` (`ConditionExpression="#st = :parked OR #st = :active"`), ngăn ngừa hoàn toàn nguy cơ Race Condition thu cước 2 lần khi client gọi đồng thời.
  - Viết kịch bản kiểm thử bảo mật `scripts/test_api_throttling.py` bắn 30 requests đồng thời trong 1 giây để xác thực cơ chế chặn spam HTTP 429 Too Many Requests từ API Gateway.
* **Giao diện Web Enterprise POS chuyên dụng (`frontend/`)**:
  - Tái thiết kế giao diện theo phong cách POS chuyên nghiệp: Viewport Camera 16:9 sắc nét cho Làn Vào / Làn Ra, bảng quản lý xe đang trong bãi theo thời gian thực kèm nút 1-click `[ ➔ Cho Xe Ra ]`.
  - Khắc phục triệt để lỗi phông chữ tiếng Việt với `Be Vietnam Pro`, lọc sạch chuỗi rác camera (`extractCleanPlate`), nhận diện biển số thông minh (`resolveTicketId`) và cơ chế reset form tự động liên tục không bị đơ ảnh.
  - Tích hợp gọi trực tiếp REST API trên API Gateway, định dạng tiền tệ VNĐ và gắn nhãn cảnh báo trực quan khi biển số mờ (`UNKNOWN`).

### 2.2. Phân hệ Giám sát & Cảnh báo Tập trung (Thành viên 2 phụ trách)
* **CloudWatch Dashboard (`SmartParking-Dashboard`)**:
  - Tích hợp 4 widgets theo dõi toàn diện: Lambda Invocations & Errors, Lambda Execution Duration, API Gateway Network Traffic (4XX/5XX) và DynamoDB Consumed Read/Write Capacity.
* **CloudWatch Alarms**:
  - Thiết lập 02 cảnh báo tự động: `SmartParking-Lambda-Errors` (Errors $\ge 1$) và `SmartParking-Lambda-Duration` (Duration $> 5000\text{ ms}$). Cả 2 đều chuyển trạng thái `OK` xanh lá.
* **CloudWatch Log Analytics (Logs Insights)**:
  - Bóc tách thành công 10 dòng log `REPORT` thực tế phục vụ kiểm toán hiệu năng và tài nguyên bộ nhớ.

### 2.3. Phân hệ Phân tích Dữ liệu Kinh doanh (Amazon Athena Data Lake - Thành viên 2 phụ trách)
* Xây dựng Data Lake Serverless với Amazon Athena đọc trực tiếp từ S3 (`analytics-data/`).
* Nạp tập dữ liệu 50 vé xe thực tế và chạy 5 câu truy vấn SQL phân tích nghiệp vụ:
  - **Xe ô tô (CAR)**: 18 lượt, doanh thu **940.000 VNĐ** (chiếm 83.6%), cước trung bình **52.222 VNĐ/lượt**.
  - **Xe máy (MOTORBIKE)**: 32 lượt, doanh thu **184.000 VNĐ** (chiếm 16.4%), cước trung bình **5.750 VNĐ/lượt**.
  - **Tổng doanh thu**: **1.124.000 VNĐ** / 50 lượt xe.
  - Phân tích giờ cao điểm (Peak Hours) và tỷ lệ nhận diện thành công vs ngoại lệ UNKNOWN.
  - Hiệu năng truy vấn Athena: Thời gian quét chỉ **462 ms**, dữ liệu quét **11.60 KB**.

### 2.4. An toàn Lưu trữ & Quản trị Chi phí (Thành viên 2 phụ trách)
* **API Gateway Throttling**: Kích hoạt trên Stage `dev` với Rate Limit `10 req/s`, Burst Limit `20 req`.
* **S3 Server-side Encryption**: Kích hoạt mã hóa lưu trữ `SSE-S3 (AES-256)` và Block Public Access.
* **Quản trị chi phí**: Xác nhận trên AWS Billing & Cost Management duy trì an toàn ở mức **`$0.00`**, bảo toàn 100% ngân sách Lab.

---

## 3. DANH MỤC HỒ SƠ MINH CHỨNG TUẦN 3 (`evidence/week3/`)

| STT | Tên file minh chứng | Nội dung minh chứng |
| :---: | :--- | :--- |
| 1 | [`01_cloudwatch_dashboard.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/01_cloudwatch_dashboard.png) | Màn hình CloudWatch Dashboard tổng hợp 4 widgets |
| 2 | [`02_cloudwatch_alarms.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/02_cloudwatch_alarms.png) | Danh sách 2 Alarms ở trạng thái OK |
| 3 | [`03_cloudwatch_logs_insights.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/03_cloudwatch_logs_insights.png) | Truy vấn Log Analytics bóc tách log Lambda |
| 4 | [`04_athena_database_tables.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/04_athena_database_tables.png) | Giao diện Athena database và bảng `parking_tickets_analytics` |
| 5 | [`05_athena_sql_queries.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/05_athena_sql_queries.png) | Kết quả chạy SQL thống kê doanh thu và lượt xe |
| 6 | [`06_api_security_throttling.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/06_api_security_throttling.png) | Cấu hình Throttling Rate: 10, Burst: 20 trên API Gateway Stage `dev` |
| 7 | [`07_s3_encryption_security.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/07_s3_encryption_security.png) | Cấu hình Default Encryption SSE-S3 AES-256 trên S3 Bucket |
| 8 | [`08_cost_and_billing.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/08_cost_and_billing.png) | Kiểm toán chi phí AWS Billing xác nhận $0.00 |

---

## 4. TÀI LIỆU VÀ NHẬT KÝ CHI TIẾT
* Kế hoạch Tuần 3: [`PLAN_TUAN_3.md`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/PLAN_TUAN_3.md)
* Nhật ký chi tiết Thành viên 1: [`docs/worklogs/week-03/member-1.md`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/docs/worklogs/week-03/member-1.md) (8.5 giờ)
* Nhật ký chi tiết Thành viên 2: [`docs/worklogs/week-03/member-2.md`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/docs/worklogs/week-03/member-2.md) (8.5 giờ)
