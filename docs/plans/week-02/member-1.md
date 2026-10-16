# KẾ HOẠCH CHI TIẾT TUẦN 2 - SINH VIÊN 1 (MEMBER 1)
### VAI TRÒ: TRƯỞNG NHÓM / KIẾN TRÚC SERVERLESS, AI REKOGNITION & BACKEND CORE
* **Thành viên:** Lê Cao Việt Tín
* **Mã số sinh viên (MSSV):** 24110354
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Thời gian thực hiện Tuần 2:** 13/10/2026 – 19/10/2026
* **Tổng thời gian phân bổ:** **8.5 giờ** (Quy định: ≥ 8.0 giờ)

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN 2
1. **Nâng cấp mã nguồn Backend (Production Code):** Chuyển đổi mã nguồn `backend/checkin.py` và `backend/checkout.py` từ dạng Mock ở Tuần 1 sang mã nguồn chính thức sử dụng thư viện `boto3` để tương tác trực tiếp với Amazon Rekognition, Amazon DynamoDB và Amazon S3.
2. **Triển khai Lambda Functions lên AWS:**
   - Tạo và cấu hình 2 hàm: `SmartParking-Checkin` và `SmartParking-Checkout`.
   - Thiết lập Runtime Python 3.11, gán quyền `LabRole` (tuyệt đối không tạo role mới).
   - Cấu hình Timeout 15s (đủ độ trễ xử lý AI OCR), Memory 256MB.
   - Cấu hình các biến môi trường: `BUCKET_NAME`, `TABLE_NAME`, `REGION_NAME`.
3. **Triển khai Amazon API Gateway REST API:**
   - Tạo REST API `SmartParking-API` dựa trên file đặc tả OpenAPI `backend/api_gateway_openapi.json` đã viết ở Tuần 1.
   - Cấu hình Lambda Proxy Integration cho 2 endpoints: `POST /checkin` và `POST /checkout`.
   - Cấu hình CORS Preflight (`OPTIONS` method) và headers cho phép gọi từ web client.
   - Triển khai (Deploy) API lên Stage `dev` và cung cấp URL cho nhóm.
4. **Viết kịch bản kiểm thử API tự động:**
   - Xây dựng file Python script `scripts/test_api_endpoints.py` tự động đọc ảnh từ bộ dữ liệu `test-images/`, chuyển đổi Base64, gửi HTTP POST lên API Gateway và in kết quả kiểm tra.
5. **Quản lý Git:** Rà soát pull request, giải quyết xung đột mã nguồn và đồng bộ nhánh `dev`.

---

## II. ĐỐI CHIẾU VỚI KẾT QUẢ GIT TUẦN 1
* **Điểm kế thừa từ Tuần 1:**
  - Logic trích xuất biển số regex trong `scripts/test_plate_regex.py` (Commit `cb85da8`).
  - Cấu trúc hàm và xử lý ngoại lệ trong `backend/checkin.py`, `backend/checkout.py` (Commit `cb85da8`).
  - Bản đặc tả API OpenAPI 3.0 trong `backend/api_gateway_openapi.json` (Commit `6c5728a`).
* **Nhiệm vụ cần giải quyết triệt để trong Tuần 2:**
  - Thay thế các đoạn code mock/placeholder bằng lệnh gọi SDK `boto3` thực thụ.
  - Xử lý chuyển đổi dữ liệu Base64 string từ HTTP payload thành binary bytes để Rekognition và S3 tiếp nhận chuẩn xác.
  - Xử lý chuyển đổi kiểu dữ liệu số (`float`/`int`) sang `Decimal` khi làm việc với DynamoDB SDK.

---

## III. LỊCH TRÌNH THỰC HIỆN CHI TIẾT (4 BUỔI - TỔNG 8.5 GIỜ)

### Buổi 1 (Thứ 2: 13/10/2026 | 19:30 - 21:30 | 2.0 giờ): Nâng cấp Backend Core Logic sang Boto3
* **Mục tiêu:** Hoàn thiện 100% mã nguồn thực tế cho 2 hàm Lambda `checkin.py` và `checkout.py`.
* **Nhiệm vụ cụ thể:**
  - Cập nhật `backend/checkin.py`:
    - Giải mã chuỗi ảnh Base64 từ request body thành dạng bytes (`base64.b64decode`).
    - Gọi API Rekognition `detect_text(Image={'Bytes': image_bytes})`.
    - Bóc tách danh sách nhãn văn bản, áp dụng regex chuẩn hóa biển số xe Việt Nam.
    - Lưu file ảnh gốc vào S3 bucket với key `in/{ticketId}.jpg` (`s3.put_object`).
    - Lưu bản ghi vé vào DynamoDB bảng `ParkingTickets` (`dynamodb.put_item`).
    - Trả về mã vé `ticketId`, biển số `plateNumber`, thời gian `checkinTime`, trạng thái `PARKED`.
  - Cập nhật `backend/checkout.py`:
    - Tiếp nhận request chứa `ticketId` (hoặc ảnh xe ra Base64 để nhận diện biển số).
    - Tra cứu vé tương ứng trong DynamoDB (`dynamodb.get_item`).
    - Kiểm tra tính hợp lệ: Vé phải tồn tại và đang ở trạng thái `PARKED` (nếu đã `COMPLETED` thì trả về lỗi 400).
    - Tính toán số giờ gửi xe (`checkoutTime - checkinTime`, làm tròn lên) và áp dụng công thức tính phí:
      - Xe máy: 5.000 VNĐ cho 4 giờ đầu, mỗi giờ tiếp theo +2.000 VNĐ.
      - Ô tô: 20.000 VNĐ cho 2 giờ đầu, mỗi giờ tiếp theo +10.000 VNĐ.
    - Upload ảnh xe ra vào S3 key `out/{ticketId}.jpg`.
    - Cập nhật DynamoDB: `status = 'COMPLETED'`, `checkoutTime`, `fee`, `outImageKey` (`dynamodb.update_item`).
* **Sản phẩm:** File mã nguồn `backend/checkin.py` và `backend/checkout.py` hoàn chỉnh, tương thích môi trường AWS Lambda.

---

### Buổi 2 (Thứ 4: 15/10/2026 | 19:00 - 21:30 | 2.5 giờ): Triển khai Lambda Functions trên AWS Console
* **Mục tiêu:** Đưa 2 hàm Lambda lên AWS Learner Lab và cấu hình đúng tiêu chuẩn.
* **Nhiệm vụ cụ thể:**
  - Đăng nhập AWS Console (Region `us-east-1`).
  - Khởi tạo hàm `SmartParking-Checkin`:
    - Runtime: Python 3.11, Architecture: x86_64.
    - Execution Role: Chọn **Use an existing role** -> chọn **`LabRole`**.
    - Cấu hình General Configuration: Timeout = 15 giây, Memory = 256 MB.
    - Cấu hình Environment Variables:
      - `BUCKET_NAME`: `smart-parking-images-24110207`
      - `TABLE_NAME`: `ParkingTickets`
      - `REGION_NAME`: `us-east-1`
    - Dán mã nguồn `backend/checkin.py` và nhấn **Deploy**.
  - Khởi tạo hàm `SmartParking-Checkout` với cấu hình tương tự.
  - Gắn đầy đủ 3 tag theo chuẩn: `Project=SmartParking`, `Owner=24110354_24110207`, `Environment=Development`.
  - Tạo Test Event trực tiếp trên AWS Console để kiểm tra việc thực thi của hàm (kiểm tra CloudWatch logs xem có lỗi IAM permission hay timeout không).
* **Sản phẩm:** 2 hàm Lambda hoạt động tốt trên AWS Console, có log CloudWatch xác nhận không phát sinh lỗi.

---

### Buổi 3 (Thứ 6: 17/10/2026 | 19:30 - 21:30 | 2.0 giờ): Triển khai và Cấu hình Amazon API Gateway
* **Mục tiêu:** Cung cấp cổng RESTful API công khai để tiếp nhận request từ client.
* **Nhiệm vụ cụ thể:**
  - Truy cập dịch vụ Amazon API Gateway trên Console (Region `us-east-1`).
  - Tạo REST API mới: `SmartParking-API` (hoặc Import từ file `backend/api_gateway_openapi.json`).
  - Cấu hình Resource & Method:
    - Tạo resource `/checkin` với method `POST`.
    - Tạo resource `/checkout` với method `POST`.
    - Chọn Integration Type: **Lambda Function** kèm tùy chọn **Lambda Proxy integration**.
    - Trỏ tương ứng tới `SmartParking-Checkin` và `SmartParking-Checkout`.
  - Kích hoạt CORS (Enable CORS):
    - Thêm method `OPTIONS` cho cả 2 resources.
    - Cấu hình response header `Access-Control-Allow-Origin: *`, `Access-Control-Allow-Methods: POST, OPTIONS`.
  - Gắn tag cho API Gateway.
  - Deploy API lên Stage `dev`.
  - Ghi nhận và chia sẻ Invoke URL cho Sinh viên 2 (Ví dụ: `https://xxxxxx.execute-api.us-east-1.amazonaws.com/dev`).
* **Sản phẩm:** API Gateway REST API đã deploy thành công, có đầy đủ 2 endpoint sẵn sàng nhận dữ liệu.

---

### Buổi 4 (Thứ 7: 18/10/2026 | 14:00 - 16:00 | 2.0 giờ): Viết Test Script tự động & Kiểm thử tích hợp
* **Mục tiêu:** Tự động hóa quá trình kiểm thử API và rà soát mã nguồn.
* **Nhiệm vụ cụ thể:**
  - Viết file script `scripts/test_api_endpoints.py`:
    - Đọc file ảnh từ thư mục `test-images/`.
    - Mã hóa sang chuỗi Base64.
    - Gửi request `POST /checkin`, nhận về `ticketId` và biển số xe.
    - Sau đó giả lập thời gian trôi qua, gửi request `POST /checkout` với `ticketId` đó.
    - Kiểm tra HTTP status code (200 OK) và giá trị tiền phí trả về.
  - Kiểm thử các trường hợp biên (Edge Cases):
    - Gửi ảnh không có biển số (`test-images/05_error_cases/`): Hệ thống phải trả về `plateNumber: "UNKNOWN"` kèm mã vé và không bị crash.
    - Gửi request checkout với `ticketId` không tồn tại: Trả về lỗi 404 Not Found.
    - Gửi checkout lần thứ 2 cho cùng 1 vé: Trả về lỗi 400 Bad Request thông báo vé đã thanh toán.
  - Rà soát code, commit toàn bộ mã nguồn lên nhánh `dev` của Git repository.
* **Sản phẩm:** File `scripts/test_api_endpoints.py` chạy thành công, mã nguồn backend được đẩy lên Git.

---

## IV. BẢNG TỔNG HỢP GIỜ LÀM VIỆC DỰ KIẾN - SINH VIÊN 1
| Buổi làm việc | Ngày thực hiện | Khung giờ | Nội dung chính | Số giờ |
| :---: | :---: | :---: | :--- | :---: |
| Buổi 1 | 13/10/2026 (Thứ 2) | 19:30 - 21:30 | Nâng cấp backend `checkin.py` và `checkout.py` sang Boto3 thật | 2.0h |
| Buổi 2 | 15/10/2026 (Thứ 4) | 19:00 - 21:30 | Triển khai 2 hàm Lambda lên AWS Console, cấu hình LabRole, biến môi trường | 2.5h |
| Buổi 3 | 17/10/2026 (Thứ 6) | 19:30 - 21:30 | Triển khai API Gateway REST API, cấu hình CORS, deploy stage `dev` | 2.0h |
| Buổi 4 | 18/10/2026 (Thứ 7) | 14:00 - 16:00 | Xây dựng test script tự động `test_api_endpoints.py`, test ngoại lệ & Git | 2.0h |
| **Tổng cộng** | | | **Tổng thời gian thực tế cam kết** | **8.5 giờ** |
*(Đạt chỉ tiêu môn học quy định: ≥ 8.0 giờ/tuần)*

