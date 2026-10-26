# KẾ HOẠCH CHI TIẾT TUẦN 3 - SINH VIÊN 1 (MEMBER 1)
### VAI TRÒ: TRƯỞNG NHÓM / KIẾN TRÚC SERVERLESS, TỰ ĐỘNG HÓA IAC & TÍCH HỢP HỆ THỐNG
* **Thành viên:** Lê Cao Việt Tín
* **Mã số sinh viên (MSSV):** 24110354
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Thời gian thực hiện Tuần 3:** 20/10/2026 – 26/10/2026
* **Tổng thời gian phân bổ:** **8.5 giờ** (Quy định: ≥ 8.0 giờ)

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN 3
1. **Xây dựng kịch bản Tự động hóa hạ tầng (Infrastructure as Code - IaC):**
   - Viết template AWS CloudFormation (`iac/cloudformation_template.yaml`) định nghĩa toàn bộ tài nguyên Serverless (S3 Bucket, DynamoDB Table, 2 Lambda Functions, API Gateway REST API, CloudWatch Alarms) kèm đầy đủ 3 tag quy chuẩn.
   - Giúp hệ thống có thể được triển khai lại hoàn chỉnh chỉ với 1 câu lệnh trên bất kỳ tài khoản AWS nào.
2. **Cấu hình bảo mật tầng API Gateway:**
   - Thiết lập Rate Limiting & Throttling trên API Gateway Stage `dev` (Rate: 10 requests/second, Burst: 20 requests) để chống tấn công DoS và bảo vệ ngân sách Lab.
   - Thêm lớp xác thực payload đầu vào trong Lambda: Kiểm tra giới hạn kích thước ảnh Base64 $\le 5\text{MB}$ và định dạng hợp lệ.
   - Viết script kiểm thử bảo mật `scripts/test_api_throttling.py` xác thực phản hồi lỗi HTTP 429 Too Many Requests khi bị spam.
3. **Phát triển Giao diện Web tĩnh tích hợp (Frontend Web UI):**
   - Xây dựng giao diện Web Single Page Application (`frontend/index.html`, `app.js`, `style.css`) trực quan, hiện đại.
   - Cho phép người dùng:
     * Tải ảnh xe vào $\rightarrow$ Nhấn Check-in $\rightarrow$ Hiển thị mã vé, biển số nhận diện và ảnh xe.
     * Nhập mã vé hoặc tải ảnh xe ra $\rightarrow$ Nhấn Check-out $\rightarrow$ Hiển thị thời gian gửi, cước phí tính toán và trạng thái thanh toán.
   - Tích hợp gọi trực tiếp các API Gateway endpoints `/checkin` và `/checkout`.
4. **Phối hợp tích hợp và quản lý Git:**
   - Phối hợp cùng Sinh viên 2 kiểm thử toàn trình từ Web UI qua API Gateway đến DynamoDB và S3.
   - Rà soát mã nguồn, commit các sản phẩm của Người 1 lên nhánh `main` bằng tài khoản `lcvt438`.

---

## II. ĐỐI CHIẾU VỚI KẾT QUẢ GIT TUẦN 2
* **Điểm kế thừa từ Tuần 2:**
  - 2 hàm Lambda Boto3 chính thức `backend/checkin.py` và `backend/checkout.py` đã hoạt động tốt (Commit `4ced72a`).
  - REST API `SmartParking-API` với 2 route `/checkin` và `/checkout` đã deploy trên Stage `dev` (Commit `4ced72a`).
  - Script test API cơ bản `scripts/test_api_endpoints.py` đã xác nhận luồng nghiệp vụ thông suốt.
* **Nhiệm vụ cần giải quyết triệt để trong Tuần 3:**
  - Chuyển đổi việc cấu hình hạ tầng từ thao tác thủ công/scripts phân mảnh sang mẫu IaC CloudFormation hoàn chỉnh.
  - Khắc phục nguy cơ API bị spam không kiểm soát bằng cách áp dụng Throttling.
  - Thay thế việc test trên terminal bằng giao diện Web thân thiện với người dùng thực tế.

---

## III. LỊCH TRÌNH THỰC HIỆN CHI TIẾT (4 BUỔI - TỔNG 8.5 GIỜ)

### Buổi 1 (Thứ 3: 20/10/2026 | 19:30 - 21:30 | 2.0 giờ): Xây dựng AWS CloudFormation Template (IaC)
* **Mục tiêu:** Hoàn thiện mã nguồn IaC chuẩn hóa toàn bộ hạ tầng Serverless của đề tài.
* **Nhiệm vụ cụ thể:**
  - Tạo file `iac/cloudformation_template.yaml`:
    - Khai báo Parameters: `EnvironmentName` (mặc định `dev`), `BucketName`, `TableName`.
    - Khai báo Resource S3: Bucket với cấu hình CORS và SSE-S3 AES-256.
    - Khai báo Resource DynamoDB: Table `ParkingTickets` (PK `ticketId`, BillingMode: PAY_PER_REQUEST).
    - Khai báo Resource Lambda: 2 Functions `SmartParking-Checkin` và `SmartParking-Checkout` (Python 3.11, Memory 256MB, Timeout 15s, IAM Role `LabRole`).
    - Khai báo Resource API Gateway: REST API, Resources `/checkin` & `/checkout`, Methods `POST` & `OPTIONS`, Deployment và Stage `dev` có cấu hình Throttling.
    - Khai báo 3 thẻ Tag chuẩn: `Project=SmartParking`, `Owner=24110354_24110207`, `Environment=Development`.
  - Kiểm tra tính hợp lệ của template qua lệnh `aws cloudformation validate-template`.
* **Sản phẩm:** File `iac/cloudformation_template.yaml` hợp lệ, sẵn sàng triển khai.

---

### Buổi 2 (Thứ 5: 22/10/2026 | 19:00 - 21:30 | 2.5 giờ): Cấu hình Bảo mật API Gateway & Input Validation
* **Mục tiêu:** Bảo vệ hệ thống khỏi tấn công từ chối dịch vụ (DoS) và dữ liệu độc hại.
* **Nhiệm vụ cụ thể:**
  - Truy cập API Gateway Console (Stage `dev`), mở mục **Default Method Throttling**:
    - Thiết lập Rate: `10` requests/second.
    - Thiết lập Burst: `20` requests.
  - Cập nhật mã nguồn `backend/checkin.py` và `backend/checkout.py`:
    - Bổ sung đoạn mã kiểm tra kích thước Base64: Nếu `len(image_base64) > 7_000_000` (tương đương $> 5\text{MB}$ ảnh gốc) $\rightarrow$ trả về HTTP 413 Payload Too Large.
    - Kiểm tra loại xe hợp lệ trong danh mục cho phép (`MOTORBIKE`, `CAR`).
  - Viết script `scripts/test_api_throttling.py`:
    - Gửi đồng thời 30 requests trong 1 giây đến API Gateway.
    - Kiểm tra phản hồi: Ghi nhận các request đầu trả về 200/400, các request vượt ngưỡng trả về đúng mã lỗi `HTTP 429 Too Many Requests`.
* **Sản phẩm:** Cấu hình Throttling kích hoạt trên API Gateway, script test bảo mật chạy thành công.

---

### Buổi 3 (Thứ 7: 24/10/2026 | 14:00 - 16:00 | 2.0 giờ): Xây dựng Giao diện Web Tĩnh (Frontend Web UI)
* **Mục tiêu:** Xây dựng giao diện ứng dụng web trực quan phục vụ demo và vận hành bãi giữ xe.
* **Nhiệm vụ cụ thể:**
  - Tạo cấu trúc thư mục `frontend/`:
    - `frontend/index.html`: Giao diện chia 2 cột: Cột bên trái xử lý Check-in (chọn ảnh/chụp ảnh xe vào, chọn loại xe, nút Tạo vé); Cột bên phải xử lý Check-out (nhập mã vé/chọn ảnh xe ra, nút Thanh toán & Tính cước).
    - `frontend/style.css`: Giao diện phong cách Dashboard hiện đại, hỗ trợ Responsive trên điện thoại và máy tính.
    - `frontend/app.js`: Tích hợp logic xử lý JavaScript:
      * Chuyển đổi file ảnh do người dùng chọn sang chuỗi Base64.
      * Gọi HTTP POST tới Invoke URL của API Gateway (`/checkin` và `/checkout`).
      * Xử lý hiển thị kết quả: Mã vé, Biển số xe bóc tách được (có badge cảnh báo màu vàng nếu `UNKNOWN`), Thời gian vào/ra, Số tiền cước phải trả.
  - Chạy thử nghiệm giao diện cục bộ trên trình duyệt để kiểm tra tương tác mượt mà.
* **Sản phẩm:** Bộ mã nguồn Frontend hoàn chỉnh trong thư mục `frontend/`.

---

### Buổi 4 (Chủ nhật: 25/10/2026 | 19:30 - 21:30 | 2.0 giờ): Tích hợp Hệ thống, Kiểm thử Toàn trình & Commit Git
* **Mục tiêu:** Kiểm thử tích hợp toàn bộ các thành phần và đồng bộ mã nguồn của Người 1 lên Git.
* **Nhiệm vụ cụ thể:**
  - Phối hợp cùng Sinh viên 2: Tải bộ mã nguồn `frontend/` lên S3 Static Website Hosting.
  - Mở URL website tĩnh trên trình duyệt, thực hiện luồng end-to-end:
    - Chọn 1 ảnh xe máy trong dataset `test-images/02_motor_clear/` $\rightarrow$ Nhấn Check-in $\rightarrow$ Nhận diện biển số và sinh vé thành công.
    - Nhập mã vé vừa sinh $\rightarrow$ Nhấn Check-out $\rightarrow$ Tính phí 5.000 VNĐ chính xác.
  - Rà soát toàn bộ code, cập nhật nhật ký làm việc cá nhân vào `docs/worklogs/week-03/member-1.md`.
  - Thực hiện commit và push các file thuộc phần việc Người 1 lên nhánh `main` bằng tài khoản `lcvt438`.
* **Sản phẩm:** Hệ thống tích hợp thông suốt từ Web UI đến Backend Cloud, commit Người 1 trên Git.

---

## IV. BẢNG TỔNG HỢP GIỜ LÀM VIỆC DỰ KIẾN - SINH VIÊN 1
| Buổi làm việc | Ngày thực hiện | Khung giờ | Nội dung chính | Số giờ |
| :---: | :---: | :---: | :--- | :---: |
| Buổi 1 | 20/10/2026 (Thứ 3) | 19:30 - 21:30 | Soạn thảo AWS CloudFormation template (IaC) chuẩn hóa hạ tầng | 2.0h |
| Buổi 2 | 22/10/2026 (Thứ 5) | 19:00 - 21:30 | Cấu hình Throttling API Gateway, Input Validation và script test 429 | 2.5h |
| Buổi 3 | 24/10/2026 (Thứ 7) | 14:00 - 16:00 | Xây dựng giao diện Web Dashboard tĩnh (HTML, CSS, JavaScript) | 2.0h |
| Buổi 4 | 25/10/2026 (Chủ nhật) | 19:30 - 21:30 | Kiểm thử toàn trình qua Web UI, rà soát mã nguồn & Git commit | 2.0h |
| **Tổng cộng** | | | **Tổng thời gian thực tế cam kết** | **8.5 giờ** |
*(Đạt chỉ tiêu môn học quy định: ≥ 8.0 giờ/tuần)*
