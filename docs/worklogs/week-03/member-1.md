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
2. **Tăng cường bảo mật, Input Validation & Chống Race Condition (`backend/checkin.py`, `backend/checkout.py`):**
   - Cập nhật 2 hàm Lambda `backend/checkin.py` và `backend/checkout.py`: Bổ sung kiểm tra kích thước payload Base64 $\le 5\text{MB}$ (trả về HTTP 413 Payload Too Large khi vượt quá) và xác thực loại phương tiện (`MOTORBIKE`, `CAR`).
   - Ứng dụng cơ chế **DynamoDB Atomic Conditional Write** trong `backend/checkout.py` (`ConditionExpression="#st = :parked OR #st = :active"`): Ngăn chặn triệt để hiện tượng Race Condition thu phí 2 lần khi bị gọi đồng thời trên cùng một mã vé.
   - Xây dựng script kiểm thử bảo mật `scripts/test_api_throttling.py` dùng đa luồng gửi 30 requests liên tục trong 1 giây để xác thực cơ chế chặn spam HTTP 429 Too Many Requests từ API Gateway.
3. **Phát triển & Tái thiết kế Giao diện Web Enterprise POS (`frontend/`):**
   - Xây dựng giao diện Web Single Page phong cách POS công nghiệp hiện đại (`index.html`, `style.css`, `app.js`).
   - Thiết kế 2 Làn Vào / Ra với viewport Camera chuẩn tỉ lệ 16:9 sắc nét, nút bấm to bản tương phản cao, phông chữ `Be Vietnam Pro` chuẩn ngữ pháp và dấu tiếng Việt (không lỗi font).
   - Tích hợp bộ lọc biển số sạch (`extractCleanPlate`), tìm kiếm thông minh theo Biển số hoặc UUID (`resolveTicketId`), quản lý danh sách xe đang trong bãi (`activeVehicles` lưu `localStorage`) kèm nút bấm 1-click `[ ➔ Cho Xe Ra ]`.
   - Cơ chế reset form tự động và nút "Làm mới", loại bỏ hoàn toàn tình trạng đơ ảnh sau một lần chụp.
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
| **Buổi 4** | **25/10/2026**<br>19:30 - 21:30 | **2.0h** | - Kiểm thử liên thông toàn trình (End-to-End) với API Gateway thật trên AWS (`fdbsdxyto1`).<br>- Tái thiết kế toàn diện giao diện Web theo chuẩn Enterprise POS: Chia 2 làn Vào/Ra với camera 16:9, bảng quản lý xe đang trong bãi với nút bấm 1-click `[ ➔ Cho Xe Ra ]`.<br>- Tích hợp bộ lọc biển số sạch (`extractCleanPlate`), nhận diện biển số thông minh (`resolveTicketId`) và khắc phục triệt để lỗi phông chữ tiếng Việt với `Be Vietnam Pro`.<br>- Cập nhật cơ chế DynamoDB Atomic Conditional Write trong `backend/checkout.py` chống Race Condition thu cước 2 lần.<br>- Hoàn thiện tài liệu nhật ký làm việc cá nhân Tuần 3 và đồng bộ mã nguồn lên Git repository. | - Web POS UI và Lambda hoàn tất nâng cấp.<br>- File `docs/worklogs/week-03/member-1.md`<br>- Commit và push lên GitHub nhánh `main` |
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

### 2. Tăng cường Bảo mật, Input Validation & Chống Race Condition (`backend/checkin.py`, `backend/checkout.py`)
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
* **Cơ chế Ghi có điều kiện nguyên tử (DynamoDB Atomic Conditional Write):**
  - Trong `backend/checkout.py`, áp dụng `ConditionExpression="#st = :parked OR #st = :active"` khi thực hiện `table.update_item`.
  - Bắt ngoại lệ `botocore.exceptions.ClientError` với mã `ConditionalCheckFailedException` và trả về HTTP 400.
  - Ngăn chặn triệt để hiện tượng Race Condition khi 2 client cùng gọi thanh toán đồng thời cho một vé xe.

### 3. Script Kiểm thử Bảo mật API Gateway Throttling (`scripts/test_api_throttling.py`)
* **Mục tiêu:** Chứng minh cơ chế bảo vệ Rate Limiting của API Gateway hoạt động hiệu quả, ngăn chặn các đợt bùng nổ traffic hoặc tấn công DoS.
* **Cơ chế kiểm thử:**
  - Sử dụng thư viện `concurrent.futures.ThreadPoolExecutor` để kích hoạt đồng thời 30 luồng HTTP POST trong vòng chưa đầy 1 giây.
  - Kết quả kiểm thử: Các request đầu tiên được API tiếp nhận và xử lý (HTTP 200/400), các request thứ 21 trở đi lập tức nhận mã phản hồi **HTTP 429 Too Many Requests** từ API Gateway.

### 4. Giao diện Web Enterprise POS (`frontend/`)
* **Cấu trúc sản phẩm:**
  - `index.html`: Giao diện POS công nghiệp chuyên dụng, chia 2 phân hệ Làn Vào (Check-in) và Làn Ra (Check-out) với khung camera 16:9 sắc nét. Nửa dưới là bảng danh sách xe đang trong bãi theo thời gian thực kèm nút `[ ➔ Cho Xe Ra ]` 1-click.
  - `style.css`: Sử dụng phông chữ chuẩn tiếng Việt `Be Vietnam Pro` (khắc phục hoàn toàn lỗi lệch phông chữ hoa có dấu tiếng Việt), nút bấm to bản tương phản cao, loại bỏ emoji trẻ con và ẩn thanh cấu hình API phô trương.
  - `app.js`: Tích hợp hàm làm sạch chuỗi rác camera `extractCleanPlate()`, tìm kiếm thông minh `resolveTicketId()`, quản lý trạng thái bãi xe `activeVehicles` trong `localStorage`, cơ chế reset form tự động liên tục không bị đơ ảnh và đồng hồ số thời gian thực.

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
