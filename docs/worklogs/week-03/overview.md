# BÁO CÁO TIẾN ĐỘ TUẦN 3 - NHÓM DOMAIN APPS
### DỰ ÁN: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING)
* **Học phần:** Điện toán đám mây (Cloud Computing) – Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Thời gian thực hiện Tuần 3:** 20/10/2026 – 26/10/2026
* **Môi trường triển khai:** AWS Learner Lab (`us-east-1`)

---

## 1. THÀNH VIÊN VÀ PHÂN CÔNG TRÁCH NHIỆM

| Thành viên | MSSV | Vai trò chính trong dự án | Thời gian cam kết | Trạng thái Tuần 3 |
| :--- | :---: | :--- | :---: | :---: |
| **Lê Cao Việt Tín** | 24110354 | **Thành viên 1 (Trưởng nhóm):** Backend Core, IaC (CloudFormation) & Frontend Web UI | 8.5 giờ | Đang phối hợp tích hợp |
| **Nguyễn Trung Hải** | 24110207 | **Thành viên 2:** Infrastructure, Data Analytics (Athena), Monitoring (CloudWatch) & Security | 8.5 giờ | **Đã hoàn thành 100%** |

---

## 2. TỔNG HỢP KẾT QUẢ TRIỂN KHAI TUẦN 3

### 2.1. Phân hệ Giám sát & Cảnh báo (CloudWatch Monitoring & Alarms)
* Đã thiết lập thành công **CloudWatch Dashboard** (`SmartParking-Dashboard`) gồm 4 biểu đồ theo dõi hiệu năng hệ thống:
  1. *Lambda Invocations & Errors*: Theo dõi số lượt gọi hàm Checkin/Checkout và tỷ lệ lỗi.
  2. *Lambda Execution Duration*: Theo dõi thời gian thực thi (trung bình và tối đa).
  3. *API Gateway Network Traffic*: Theo dõi lưu lượng mạng và các mã phản hồi HTTP 4XX/5XX.
  4. *DynamoDB Consumed Capacity*: Theo dõi lưu lượng đọc/ghi trên bảng `ParkingTickets`.
* Đã tạo và cấu hình 02 **CloudWatch Alarms**:
  - `SmartParking-Lambda-Errors`: Cảnh báo khi có $\ge 1$ lỗi phát sinh trong 1 phút.
  - `SmartParking-Lambda-Duration`: Cảnh báo độ trễ vượt ngưỡng $5000\text{ ms}$.
  - Cả 2 Alarms đều ở trạng thái `OK` xanh lá, đã qua kiểm thử kích hoạt bằng kịch bản test.
* Đã ứng dụng **CloudWatch Log Analytics (Logs Insights)** truy vấn và bóc tách các dòng log `REPORT` thực tế của Lambda.

### 2.2. Phân hệ Phân tích Dữ liệu Kinh doanh (Amazon Athena Data Lake)
* Thiết lập Data Lake Serverless với Amazon Athena và Amazon S3:
  - Database: `smart_parking_db`
  - External Table: `parking_tickets_analytics` (đọc dữ liệu NDJSON từ `s3://smart-parking-images-24110207/analytics-data/`).
* Đã nạp tập dữ liệu thực tế 50 lượt xe và chạy 5 câu truy vấn phân tích nghiệp vụ:
  - **Doanh thu theo loại xe**:
    * Xe ô tô (CAR): 18 lượt, tổng thu **940.000 VNĐ**, cước trung bình **52.222 VNĐ/lượt**.
    * Xe máy (MOTORBIKE): 32 lượt, tổng thu **184.000 VNĐ**, cước trung bình **5.750 VNĐ/lượt**.
  - **Lưu lượng theo khung giờ (Peak Hours)**: Bóc tách giờ cao điểm sáng và chiều phục vụ điều tiết bãi đỗ.
  - Hiệu năng truy vấn Athena: Thời gian quét chỉ **462 ms**, dữ liệu quét **11.60 KB**.

### 2.3. Phân hệ An toàn & Bảo mật (Cloud Security)
* **API Gateway Throttling**: Kích hoạt trên Stage `dev` với Rate Limit `10 req/s` và Burst Limit `20 req`, ngăn chặn triệt để tấn công DoS và spam request.
* **S3 Server-side Encryption**: Kích hoạt chuẩn mã hóa `SSE-S3 (AES-256)` cho toàn bộ bucket chứa ảnh biển số xe.
* **Block Public Access**: Bật bảo vệ 100% ngăn chặn truy cập trái phép từ Internet.

### 2.4. Quản trị Chi phí & Ngân sách Lab
* Chi phí tháng xác nhận trên AWS Billing & Cost Management duy trì ở mức **`$0.00`**.
* Đảm bảo an toàn tuyệt đối cho ngân sách $100 của nhà trường cấp.

---

## 3. DANH MỤC HỒ SƠ MINH CHỨNG TUẦN 3 (`evidence/week3/`)

1. [`01_cloudwatch_dashboard.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/01_cloudwatch_dashboard.png) - Màn hình Dashboard 4 widgets.
2. [`02_cloudwatch_alarms.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/02_cloudwatch_alarms.png) - Danh sách 2 Alarms ở trạng thái OK.
3. [`03_cloudwatch_logs_insights.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/03_cloudwatch_logs_insights.png) - Kết quả truy vấn bóc tách log Lambda.
4. [`04_athena_database_tables.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/04_athena_database_tables.png) - Giao diện Athena database và bảng `parking_tickets_analytics`.
5. [`05_athena_sql_queries.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/05_athena_sql_queries.png) - Kết quả chạy câu truy vấn SQL thống kê doanh thu bãi xe.
6. [`06_api_security_throttling.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/06_api_security_throttling.png) - Cấu hình Throttling Rate: 10, Burst: 20 trên API Gateway Stage `dev`.
7. [`07_s3_encryption_security.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/07_s3_encryption_security.png) - Cấu hình Default Encryption SSE-S3 AES-256 trên S3 Bucket.
8. [`08_cost_and_billing.png`](file:///c:/Users/T14%20GEN2/Documents/cloud-smart-parking-system/evidence/week3/08_cost_and_billing.png) - Kiểm toán chi phí AWS Billing xác nhận $0.00.
