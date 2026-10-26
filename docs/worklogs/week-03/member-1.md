# BÁO CÁO CÔNG VIỆC VÀ NHẬT KÝ CHI TIẾT TUẦN 3 - SINH VIÊN 1 (MEMBER 1)
## HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING SYSTEM)

* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Thành viên thực hiện:** **Lê Cao Việt Tín**
* **Mã số sinh viên (MSSV):** **24110354**
* **Vai trò trong nhóm:** **Trưởng nhóm / Kiến trúc Serverless, Tự động hóa IaC & Tích hợp hệ thống**
* **Thời gian thực hiện:** 20/10/2026 – 26/10/2026
* **Tổng số giờ làm việc thực tế:** **8.5 giờ** (Quy định: ≥ 8.0 giờ/tuần — **ĐẠT**)
* **Môi trường triển khai:** AWS Learner Lab | Region: `us-east-1` (N. Virginia)

---

## 📌 I. TỔNG QUAN PHẦN VIỆC ĐẢM NHẬN TRONG TUẦN 3

Căn cứ theo đề cương môn học và Kế hoạch phân công Tuần 3 (`PLAN_TUAN_3.md` và `docs/plans/week-03/member-1.md`), Sinh viên 1 chịu trách nhiệm chính về tự động hóa hạ tầng (IaC), bảo mật tầng API và phát triển giao diện Web Dashboard:

1. **Xây dựng template Tự động hóa hạ tầng AWS CloudFormation (`iac/cloudformation_template.yaml`):**
   - Định nghĩa toàn bộ kiến trúc Serverless dạng Infrastructure as Code (IaC): S3 Bucket, DynamoDB Table `ParkingTickets`, 2 Lambda Functions (`SmartParking-Checkin`, `SmartParking-Checkout`), API Gateway REST API (`SmartParking-API`), CloudWatch Alarms.
   - Thiết lập cấu hình CORS, mã hóa SSE-S3 AES-256, API Gateway Method Throttling (Rate: 10 req/s, Burst: 20 req) và gán đủ 3 thẻ Tag chuẩn môn học.
2. **Tăng cường bảo mật và kiểm soát dữ liệu đầu vào (Input Validation & Throttling):**
   - Cập nhật 2 hàm Lambda `backend/checkin.py` và `backend/checkout.py`: Bổ sung kiểm tra kích thước payload Base64 $\le 5\text{MB}$ (trả về HTTP 413 Payload Too Large khi vượt quá) và xác thực loại phương tiện (`MOTORBIKE`, `CAR`).
   - Xây dựng script kiểm thử bảo mật `scripts/test_api_throttling.py` dùng đa luồng gửi 30 requests liên tục trong 1 giây để xác thực cơ chế chặn spam HTTP 429 Too Many Requests từ API Gateway.
3. **Phát triển giao diện Web Dashboard tĩnh (`frontend/`):**
   - Xây dựng ứng dụng Web Single Page Dashboard gồm `index.html`, `style.css`, `app.js` có thể chạy trên trình duyệt hoặc host qua S3 Static Website.
   - Giao diện chia 2 phân hệ rõ ràng: Check-in (chụp/chọn ảnh, chọn loại xe, tạo vé xe thông minh) và Check-out (nhập mã vé, tra cứu cước phí, chụp ảnh ra và hoàn tất thanh toán).
   - Tích hợp trực tiếp với API Gateway REST API, hiển thị thông báo trực quan, cước phí chuẩn tiền tệ Việt Nam (`VNĐ`) và gắn nhãn cảnh báo khi biển số không rõ (`UNKNOWN`).
4. **Kiểm thử tích hợp và đồng bộ mã nguồn Git:**
   - Phối hợp cùng Sinh viên 2 kiểm thử toàn trình từ Web UI qua API Gateway đến Lambda, DynamoDB và S3.
   - Rà soát mã nguồn, hoàn thiện hồ sơ báo cáo và đồng bộ lên GitHub repository.

---

## ⏱️ II. BẢNG NHẬT KÝ LÀM VIỆC CHI TIẾT (WORKLOG - 8.5 GIỜ)

| Buổi làm việc | Ngày & Giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm & Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **Buổi 1** | **20/10/2026**<br>19:30 - 21:30 | **2.0h** | - Soạn thảo file CloudFormation template `iac/cloudformation_template.yaml`.<br>- Khai báo Parameters (`EnvironmentName`, `BucketName`, `TableName`).<br>- Định nghĩa tài nguyên S3 (CORS, mã hóa SSE-S3), DynamoDB `ParkingTickets` (PK `ticketId`, On-Demand).<br>- Định nghĩa 2 Lambda Functions sử dụng `LabRole`, gán biến môi trường.<br>- Định nghĩa API Gateway REST API, các resources `/checkin`, `/checkout`, method `POST` (Lambda Proxy) và `OPTIONS` (CORS).<br>- Cấu hình CloudWatch Alarms giám sát lỗi Lambda và thời gian thực thi.<br>- Gán đủ 3 thẻ Tag chuẩn: `Project=SmartParking`, `Owner=24110354_24110207`, `Environment=Development`. | - File `iac/cloudformation_template.yaml`<br>- Template validate chuẩn cú pháp AWS CloudFormation |
| **Buổi 2** | **22/10/2026**<br>19:00 - 21:30 | **2.5h** | - Cấu hình bảo mật Rate Limiting & Throttling trên API Gateway Stage `dev` (RateLimit: 10 req/s, BurstLimit: 20 req).<br>- Cập nhật mã nguồn `backend/checkin.py`: Thêm kiểm tra độ dài Base64 (trả về HTTP 413 nếu $> 7.000.000$ ký tự tương đương $> 5\text{MB}$), xác thực `vehicleType` trong danh mục cho phép.<br>- Cập nhật `backend/checkout.py`: Bổ sung kiểm tra kích thước ảnh đầu ra và xác thực `ticketId`.<br>- Viết script Python `scripts/test_api_throttling.py` dùng `ThreadPoolExecutor` bắn 30 requests/giây để kiểm thử cơ chế Throttling (HTTP 429). | - Mã nguồn `backend/checkin.py` và `backend/checkout.py` được bổ sung validation.<br>- File `scripts/test_api_throttling.py`<br>- Kết quả terminal ghi nhận HTTP 429 Too Many Requests |
| **Buổi 3** | **24/10/2026**<br>14:00 - 16:00 | **2.0h** | - Thiết kế cấu trúc thư mục `frontend/` gồm: `index.html`, `style.css`, `app.js`.<br>- Xây dựng giao diện Dashboard chia 2 cột: Cổng vào (Check-in) và Cổng ra (Check-out).<br>- Thiết kế CSS Responsive, màu sắc hiện đại (Dark theme cards, Accent blue & emerald), hỗ trợ xem trước ảnh (image preview), trạng thái tải (spinner) và toast notifications.<br>- Viết logic JavaScript: Đọc file ảnh chuyển sang Base64, gọi REST API `/checkin` và `/checkout`, định dạng thời gian và tiền tệ VNĐ (`5.000 VNĐ`, `20.000 VNĐ`). | - Thư mục `frontend/` hoàn chỉnh (`index.html`, `style.css`, `app.js`).<br>- Giao diện web chạy thử cục bộ mượt mà, phản hồi tốt trên trình duyệt |
| **Buổi 4** | **25/10/2026**<br>19:30 - 21:30 | **2.0h** | - Kiểm thử liên thông toàn trình (End-to-End): Kết nối Web Dashboard với Invoke URL API Gateway thật trên AWS (`fdbsdxyto1`).<br>- Thử nghiệm ca Check-in xe máy với ảnh mẫu $\rightarrow$ Nhận diện biển số và sinh mã vé thành công $\rightarrow$ Thử nghiệm Check-out tính cước phí chính xác theo block thời gian.<br>- Kiểm tra tính năng sao chép nhanh mã vé từ kết quả Check-in sang ô Check-out.<br>- Rà soát toàn bộ mã nguồn, dọn dẹp các ghi chú thừa, hoàn thiện tài liệu nhật ký làm việc cá nhân Tuần 3 và đồng bộ mã nguồn lên Git repository. | - Web UI tích hợp hoàn tất với API Gateway thật.<br>- File `docs/worklogs/week-03/member-1.md`<br>- Commit và push lên GitHub nhánh `main` |
| **Tổng cộng** | | **8.5h** | **Hoàn thành 100% khối lượng công việc được phân công** | **ĐẠT TIÊU CHUẨN MÔN HỌC (≥ 8.0h)** |

---

## 🛠️ III. CHI TIẾT KỸ THUẬT CÁC SẢN PHẨM MÃ NGUỒN

### 1. Template AWS CloudFormation (`iac/cloudformation_template.yaml`)
* **Mục tiêu:** Tự động hóa việc khởi tạo toàn bộ hệ sinh thái Serverless chuẩn mực, có thể tái lập (reproducible) tại bất kỳ tài khoản AWS nào.
* **Các thành phần được khai báo:**
  - `Parameters`: Cho phép tùy biến `EnvironmentName`, `BucketName`, `TableName`.
  - `AWS::S3::Bucket`: Bucket lưu trữ ảnh xe vào/ra, kích hoạt mã hóa `AES256` (SSE-S3) và cấu hình CORS đầy đủ.
  - `AWS::DynamoDB::Table`: Bảng `ParkingTickets` với Partition Key `ticketId` (String), thanh toán theo yêu cầu `PAY_PER_REQUEST`.
  - `AWS::Lambda::Function`: 2 hàm `SmartParking-Checkin` và `SmartParking-Checkout` (Runtime Python 3.11, Memory 256MB, Timeout 15s, gắn `LabRole` và biến môi trường).
  - `AWS::ApiGateway::RestApi`: API Gateway `SmartParking-API` với các resource `/checkin`, `/checkout`, tích hợp Lambda Proxy và phương thức `OPTIONS` cho CORS.
  - `AWS::ApiGateway::Stage`: Stage `dev` có cấu hình `MethodSettings` giới hạn tần suất: `ThrottlingRateLimit: 10`, `ThrottlingBurstLimit: 20`.
  - `AWS::CloudWatch::Alarm`: Cảnh báo tự động khi hàm Lambda phát sinh lỗi hoặc thời gian thực thi vượt ngưỡng quy định.
  - `Tags`: Tự động áp dụng 3 thẻ Tag chuẩn: `Project=SmartParking`, `Owner=24110354_24110207`, `Environment=Development`.

### 2. Tăng cường Bảo mật & Input Validation (`backend/checkin.py`, `backend/checkout.py`)
* **Kiểm tra độ dài Base64 (HTTP 413 Payload Too Large):**
  - Tránh nguy cơ cạn kiệt bộ nhớ Lambda hoặc chi phí phát sinh bất thường do ảnh quá lớn, hệ thống kiểm tra độ dài chuỗi Base64:
    ```python
    if len(image_base64) > 7_000_000:  # Tương đương > 5MB
        return {
            'statusCode': 413,
            'headers': CORS_HEADERS,
            'body': json.dumps({'error': 'Kích thước ảnh vượt quá giới hạn cho phép (tối đa 5MB)'}, ensure_ascii=False)
        }
    ```
* **Xác thực danh mục đầu vào (HTTP 400 Bad Request):**
  - Giới hạn loại phương tiện chỉ chấp nhận `MOTORBIKE` hoặc `CAR`.
  - Bắt buộc phải có `ticketId` hợp lệ khi gửi yêu cầu trả phòng (checkout).

### 3. Script Kiểm thử Bảo mật API Gateway Throttling (`scripts/test_api_throttling.py`)
* **Mục tiêu:** Chứng minh cơ chế bảo vệ Rate Limiting của API Gateway hoạt động hiệu quả, ngăn chặn các đợt bùng nổ traffic hoặc tấn công DoS.
* **Cơ chế kiểm thử:**
  - Sử dụng thư viện `concurrent.futures.ThreadPoolExecutor` để kích hoạt đồng thời 30 luồng HTTP POST trong vòng chưa đầy 1 giây.
  - Kết quả kiểm thử: Các request đầu tiên được API tiếp nhận và xử lý (HTTP 200/400), các request thứ 21 trở đi lập tức nhận mã phản hồi **HTTP 429 Too Many Requests** từ API Gateway.

### 4. Giao diện Web Dashboard (`frontend/`)
* **Cấu trúc sản phẩm:**
  - `index.html`: Cấu trúc Dashboard trực quan, bố cục chia 2 phân hệ Check-in và Check-out rõ ràng. Có phần cấu hình URL API động để linh hoạt kiểm thử ở mọi môi trường.
  - `style.css`: Thiết kế giao diện hiện đại, tinh gọn, tương thích màn hình máy tính và thiết bị di động.
  - `app.js`: Tự động hóa chuyển đổi ảnh sang Base64, gửi dữ liệu qua API Gateway bằng `fetch`, hiển thị kết quả trực tiếp và hỗ trợ nút bấm 1 chạm sao chép mã vé sang phân hệ Check-out.

---

## 📋 IV. CẤU HÌNH THỰC TẾ TRÊN AWS LEARNER LAB

* **Region:** `us-east-1` (N. Virginia)
* **IAM Execution Role:** `arn:aws:iam::<AccountID>:role/LabRole`
* **API Gateway Throttling Configuration:**
  - Rate Limit: `10 requests/second`
  - Burst Limit: `20 requests`
* **Hạ tầng IaC:**
  - Template: `iac/cloudformation_template.yaml`
  - Đảm bảo tính nhất quán giữa template CloudFormation và các tài nguyên thực tế đã triển khai trên AWS Console.
* **Quy chuẩn Tagging 3 thẻ bắt buộc:**
  - `Project`: `SmartParking`
  - `Owner`: `24110354_24110207`
  - `Environment`: `Development`

---

## 🤖 V. MINH BẠCH SỬ DỤNG AI (AI TRANSPARENCY)
* **Công cụ hỗ trợ:** Google Gemini, Claude.
* **Nội dung tham khảo:**
  - Tra cứu cú pháp định nghĩa tài nguyên `AWS::ApiGateway::Stage` và `MethodSettings` trong CloudFormation.
  - Tham khảo cách viết kiểm thử đa luồng với `concurrent.futures` trong Python.
* **Mức độ làm chủ của Sinh viên:**
  - Sinh viên trực tiếp thiết kế kiến trúc, tổ chức mã nguồn và kiểm thử toàn diện trên tài khoản AWS cá nhân.
  - Nắm vững toàn bộ cơ chế bảo mật và luồng vận hành của hệ thống.

---

**Xác nhận của Sinh viên 1 (Trưởng nhóm):**  
*(Đã ký xác nhận)*  
**Lê Cao Việt Tín** (MSSV: 24110354)
