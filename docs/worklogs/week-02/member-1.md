# BÁO CÁO CÔNG VIỆC VÀ NHẬT KÝ CHI TIẾT TUẦN 2 - SINH VIÊN 1 (MEMBER 1)
## HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING SYSTEM)

* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Thành viên thực hiện:** **Lê Cao Việt Tín**
* **Mã số sinh viên (MSSV):** **24110354**
* **Vai trò trong nhóm:** **Trưởng nhóm / Kiến trúc Serverless, AI Rekognition & Backend Core**
* **Thời gian thực hiện:** 13/10/2026 – 19/10/2026
* **Tổng số giờ làm việc thực tế:** **8.5 giờ** (Quy định: ≥ 8.0 giờ/tuần — **ĐẠT**)
* **Môi trường triển khai:** AWS Learner Lab | Region: `us-east-1` (N. Virginia)

---

## 📌 I. TỔNG QUAN PHẦN VIỆC ĐẢM NHẬN TRONG TUẦN 2

Căn cứ theo đề cương môn học và Kế hoạch phân công Tuần 2 (`PLAN_TUAN_2.md`), Sinh viên 1 chịu trách nhiệm chính về toàn bộ logic backend lõi, dịch vụ AI thị giác máy tính và giao tiếp API:

1. **Nâng cấp mã nguồn Backend chính thức (`backend/checkin.py` và `backend/checkout.py`):**
   - Loại bỏ hoàn toàn mã giả lập (Mock) của Tuần 1.
   - Ứng dụng AWS SDK `boto3` để kết nối trực tiếp với 3 dịch vụ AWS: **Amazon Rekognition**, **Amazon S3** và **Amazon DynamoDB**.
   - Thiết lập cấu trúc CORS Headers chuẩn mực (`Access-Control-Allow-Origin: *`) cho mọi response.
2. **Triển khai và Cấu hình 02 AWS Lambda Functions trên AWS Console:**
   - Hàm `SmartParking-Checkin`: Xử lý xe vào, nhận diện biển số, upload ảnh S3, lưu vé vào DynamoDB.
   - Hàm `SmartParking-Checkout`: Xử lý xe ra, tra cứu vé, kiểm tra trạng thái, tính tiền theo block giờ và cập nhật vé `COMPLETED`.
   - Cấu hình Runtime Python 3.11, Timeout 15s, Memory 256MB, Execution Role `LabRole`, thiết lập biến môi trường và gắn đủ 3 thẻ Tag chuẩn.
3. **Triển khai và Cấu hình Amazon API Gateway REST API:**
   - Khởi tạo REST API `SmartParking-API`.
   - Thiết lập các endpoint `/checkin` và `/checkout` với phương thức `POST` sử dụng **Lambda Proxy Integration**.
   - Kích hoạt CORS Preflight (`OPTIONS` method) và deploy lên Stage `dev`.
4. **Xây dựng kịch bản kiểm thử tích hợp tự động (`scripts/test_api_endpoints.py`):**
   - Viết script Python hoàn chỉnh gửi ảnh Base64 lên API Gateway.
   - Tự động kiểm tra các trường hợp chuẩn và các ca biên ngoại lệ (vé không tồn tại 404, thanh toán lặp 400, ảnh mờ gán `UNKNOWN`).

---

## ⏱️ II. BẢNG NHẬT KÝ LÀM VIỆC CHI TIẾT (WORKLOG - 8.5 GIỜ)

| Buổi làm việc | Ngày & Giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm & Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **Buổi 1** | **13/10/2026**<br>19:30 - 21:30 | **2.0h** | - Nâng cấp mã nguồn `backend/checkin.py`: Xử lý decode Base64, tích hợp Amazon Rekognition `DetectText`, bóc tách Regex biển số xe Việt Nam, upload ảnh vào S3 folder `in/{ticketId}.jpg`, ghi vé trạng thái `PARKED` vào DynamoDB.<br>- Nâng cấp `backend/checkout.py`: Đọc vé DynamoDB, tính tiền theo block giờ (xe máy 5k/4h đầu, ô tô 20k/2h đầu), cập nhật vé `COMPLETED` với kiểu `Decimal`. | - File `backend/checkin.py`<br>- File `backend/checkout.py`<br>- Commit: `feat: implement production boto3 lambda handlers` |
| **Buổi 2** | **15/10/2026**<br>19:00 - 21:30 | **2.5h** | - Đăng nhập AWS Console (`us-east-1`), truy cập dịch vụ AWS Lambda.<br>- Khởi tạo 2 hàm: `SmartParking-Checkin` và `SmartParking-Checkout` (Python 3.11, x86_64).<br>- Cấu hình Memory 256MB, Timeout 15 giây.<br>- Gán Execution Role `LabRole` (sử dụng role có sẵn của Learner Lab).<br>- Cấu hình 3 biến môi trường: `BUCKET_NAME`, `TABLE_NAME`, `REGION_NAME`.<br>- Gắn 3 thẻ Tag chuẩn: `Project=SmartParking`, `Owner=24110354_24110207`, `Environment=Development`.<br>- Dán code, Deploy và kiểm tra chạy thử Test Event trên Console. | - 02 Lambda Functions hoạt động tốt trên AWS Console.<br>- Ảnh minh chứng: `evidence/week2/01_lambda_functions.png` |
| **Buổi 3** | **17/10/2026**<br>19:30 - 21:30 | **2.0h** | - Truy cập Amazon API Gateway Console, khởi tạo REST API `SmartParking-API` (Regional).<br>- Tạo Resource `/checkin`, tạo Method `POST` gắn Lambda Proxy Integration trỏ tới `SmartParking-Checkin`.<br>- Tạo Resource `/checkout`, tạo Method `POST` gắn Lambda Proxy Integration trỏ tới `SmartParking-Checkout`.<br>- Kích hoạt **Enable CORS** cho cả 2 resources (tạo method `OPTIONS` và cấu hình CORS headers).<br>- Deploy API lên Stage `dev`, trích xuất Invoke URL và chia sẻ cho SV2 phối hợp kiểm thử. | - REST API `SmartParking-API` hoạt động trên Stage `dev`.<br>- Ảnh minh chứng: `evidence/week2/02_apigateway_routes.png` |
| **Buổi 4** | **18/10/2026**<br>14:00 - 16:00 | **2.0h** | - Xây dựng file script kiểm thử tự động `scripts/test_api_endpoints.py` sử dụng thư viện chuẩn `urllib.request`.<br>- Thực hiện kiểm thử toàn trình 4 ca: Check-in xe máy hợp lệ, Check-out tính phí, chặn thanh toán lần 2 (HTTP 400), phát hiện vé không tồn tại (HTTP 404).<br>- Rà soát mã nguồn, ghi chép tài liệu worklog và chuẩn bị commit lên GitHub repository. | - Script `scripts/test_api_endpoints.py`<br>- Ảnh minh chứng terminal: `evidence/week2/06_api_test_terminal_1.png` và `evidence/week2/07_api_test_terminal_2.png` |
| **Tổng cộng** | | **8.5h** | **Hoàn thành 100% khối lượng công việc được phân công** | **ĐẠT TIÊU CHUẨN MÔN HỌC (≥ 8.0h)** |

---

## 🛠️ III. CHI TIẾT KỸ THUẬT CÁC SẢN PHẨM MÃ NGUỒN

### 1. Hàm Lambda Check-in (`backend/checkin.py`)
* **Mục tiêu:** Tiếp nhận ảnh từ camera cổng vào, nhận diện biển số xe bằng AI, cấp vé và lưu trữ dữ liệu.
* **Quy trình xử lý:**
  1. Kiểm tra CORS Preflight: Nếu `httpMethod == "OPTIONS"`, trả về HTTP 200 kèm đầy đủ header.
  2. Parse body và kiểm tra tính hợp lệ của chuỗi `image` (Base64) và `vehicleType` (`MOTORBIKE` hoặc `CAR`).
  3. Tách bỏ tiền tố Data URI (nếu có) và decode Base64 thành binary bytes.
  4. Gọi Amazon Rekognition SDK: `rekognition_client.detect_text(Image={"Bytes": image_bytes})`.
  5. Lọc các khối văn bản dạng `LINE` có `Confidence >= 70%`, dùng Regex loại bỏ ký tự nhiễu, ghép thành chuỗi biển số xe chuẩn hóa.
  6. **Cơ chế an toàn (Fail-safe):** Nếu ảnh không rõ hoặc không nhận diện được biển số, tự động gán biển số là `"UNKNOWN"` để vé vẫn được sinh ra, nhân viên bảo vệ có thể nhập tay, hệ thống không bị crash 500.
  7. Sinh mã vé ngẫu nhiên UUIDv4 `ticketId`, lấy mốc thời gian UTC ISO 8601 `checkinTime`.
  8. Upload ảnh gốc lên S3 bucket: `Key=f"in/{ticketId}.jpg"`.
  9. Ghi bản ghi vào DynamoDB bảng `ParkingTickets` với trạng thái ban đầu `"PARKED"`.
  10. Trả về mã vé, biển số và thời gian cho client với mã HTTP 200.

### 2. Hàm Lambda Check-out (`backend/checkout.py`)
* **Mục tiêu:** Tra cứu vé xe, kiểm soát tính hợp lệ, tính tiền phí gửi xe theo block giờ và cập nhật hoàn tất vé.
* **Quy trình xử lý:**
  1. Parse request lấy `ticketId` và `image` (nếu có).
  2. Tra cứu DynamoDB theo Partition Key `ticketId`. Nếu không tìm thấy $\rightarrow$ trả về **HTTP 404 Not Found**.
  3. Kiểm tra trạng thái vé: Nếu vé đã có `status == "COMPLETED"` $\rightarrow$ trả về **HTTP 400 Bad Request** kèm thông báo vé đã thanh toán trước đó, ngăn chặn gian lận hoặc gọi nhầm.
  4. Tính toán thời gian đỗ xe thực tế: `delta = checkout - checkin`, quy đổi ra số giờ làm tròn lên (`math.ceil`, tối thiểu 1 giờ).
  5. Áp dụng công thức tính phí:
     - **Xe máy (`MOTORBIKE`):** $\le 4\text{ giờ} = 5.000\text{ VNĐ}$; mỗi giờ tiếp theo $+2.000\text{ VNĐ}$.
     - **Ô tô (`CAR`):** $\le 2\text{ giờ} = 20.000\text{ VNĐ}$; mỗi giờ tiếp theo $+10.000\text{ VNĐ}$.
  6. Nếu client có gửi ảnh xe ra, lưu vào S3 tại `out/{ticketId}.jpg`.
  7. Cập nhật bản ghi trong DynamoDB: đổi `status = 'COMPLETED'`, gán `checkoutTime`, `fee`, `totalHours` (ép kiểu `Decimal` tương thích DynamoDB).
  8. Trả về thông tin biên lai thanh toán hoàn tất cho client với mã HTTP 200.

### 3. Script Kiểm thử API Tự động (`scripts/test_api_endpoints.py`)
* **Mục tiêu:** Tự động hóa kiểm thử liên thông (E2E) từ bên ngoài internet vào API Gateway.
* **Điểm nổi bật:**
  - Hoàn toàn dùng thư viện chuẩn `urllib.request` của Python, không phụ thuộc thư viện bên ngoài.
  - Hỗ trợ tham số `--endpoint` để truyền URL API Gateway thật, và `--mock` khi cần test cục bộ.
  - Tự động nạp ảnh từ thư mục dữ liệu mẫu `test-images/02_motor_clear/motor_clear_01.jpg`.
  - Kiểm thử đầy đủ 4 trường hợp:
    1. `POST /checkin`: Tạo vé xe máy thành công, trả về ticketId và biển số.
    2. `POST /checkout`: Tính phí gửi xe chính xác theo block giờ và hoàn tất vé.
    3. Ngoại lệ thanh toán lần 2: Đảm bảo server chặn với mã 400 Bad Request.
    4. Ngoại lệ vé không tồn tại: Đảm bảo server bắt lỗi với mã 404 Not Found.

---

## 📋 IV. CẤU HÌNH THỰC TẾ TRÊN AWS LEARNER LAB

* **Region:** `us-east-1` (N. Virginia)
* **IAM Execution Role:** `arn:aws:iam::<AccountID>:role/LabRole` (Chỉ dùng role cấp sẵn, không tạo mới).
* **AWS Lambda:**
  - Runtime: Python 3.11, Architecture: x86_64.
  - General Configuration: Memory 256MB, Timeout 15s.
  - Environment Variables:
    - `BUCKET_NAME`: `smart-parking-images-24110207`
    - `TABLE_NAME`: `ParkingTickets`
    - `REGION_NAME`: `us-east-1`
* **Amazon API Gateway:**
  - REST API: `SmartParking-API` (Regional)
  - Resources & Methods:
    - `POST /checkin` $\rightarrow$ Lambda Proxy $\rightarrow$ `SmartParking-Checkin`
    - `OPTIONS /checkin` $\rightarrow$ CORS Preflight (200 OK)
    - `POST /checkout` $\rightarrow$ Lambda Proxy $\rightarrow$ `SmartParking-Checkout`
    - `OPTIONS /checkout` $\rightarrow$ CORS Preflight (200 OK)
  - Stage: `dev`
* **Quy chuẩn Tagging 3 thẻ bắt buộc:**
  - `Project`: `SmartParking`
  - `Owner`: `24110354_24110207`
  - `Environment`: `Development`

---

## 📷 V. DANH MỤC HỒ SƠ MINH CHỨNG NGƯỜI 1 (`evidence/week2/`)

Toàn bộ ảnh chụp màn hình minh chứng của Sinh viên 1 tuân thủ nghiêm ngặt quy định: chụp toàn màn hình máy tính (Full Screen), hiển thị rõ AWS Account ID, Region `us-east-1` và đồng hồ hệ thống:

1. `evidence/week2/01_lambda_functions.png`: Danh sách và cấu hình 2 hàm Lambda `SmartParking-Checkin` và `SmartParking-Checkout`.
2. `evidence/week2/02_apigateway_routes.png`: Cây tài nguyên API Gateway (`/checkin`, `/checkout`), cấu hình CORS và Stage `dev`.
3. `evidence/week2/06_api_test_terminal_1.png`: Màn hình Terminal chạy test case Check-in thành công qua API Gateway.
4. `evidence/week2/07_api_test_terminal_2.png`: Màn hình Terminal chạy test case Check-out và các ca ngoại lệ (400, 404).

---

## 🤖 VI. MINH BẠCH SỬ DỤNG AI (AI TRANSPARENCY)
* **Công cụ hỗ trợ:** Google Gemini, Anthropic Claude.
* **Phần có sự hỗ trợ của AI:**
  - Gợi ý cấu trúc cú pháp `boto3` khi gọi Rekognition `detect_text` dạng Bytes.
  - Xử lý chuyển đổi kiểu số sang `Decimal` cho các thuộc tính số trong DynamoDB.
* **Mức độ làm chủ của Sinh viên:**
  - Toàn bộ mã nguồn đã được sinh viên đọc, hiểu cặn kẽ và kiểm thử kỹ lưỡng.
  - Sinh viên trực tiếp cấu hình trên AWS Console cá nhân và tự tin giải thích từng thông số khi vấn đáp với GVHD.

---

**Xác nhận của Sinh viên 1 (Trưởng nhóm):**  
*(Đã ký xác nhận)*  
**Lê Cao Việt Tín** (MSSV: 24110354)
