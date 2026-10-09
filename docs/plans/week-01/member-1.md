# KẾ HOẠCH CHI TIẾT TUẦN 1 - SINH VIÊN 1 (MEMBER 1)
### VAI TRÒ: TRƯỞNG NHÓM / KIẾN TRÚC SERVERLESS, AI REKOGNITION & BACKEND CORE
* **Thành viên:** Sinh viên 1 (`[Họ và tên SV 1]` - `[MSSV 1]`)
* **Tổng thời gian phân bổ:** **8.5 giờ**

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN
1. Nghiên cứu cơ chế trích xuất văn bản từ hình ảnh của AWS Rekognition API (`DetectText`).
2. Xây dựng giải thuật Regex bóc tách và chuẩn hóa biển số xe máy & ô tô Việt Nam.
3. Thiết kế kiến trúc Serverless, luồng dữ liệu (Data Flow) và lược đồ cơ sở dữ liệu DynamoDB.
4. Xây dựng logic nền tảng cho 2 hàm AWS Lambda: `SmartParking-Checkin` và `SmartParking-Checkout`.
5. Quản trị Git repository, phân nhánh `dev` và rà soát mã nguồn.

---

## II. LỊCH TRÌNH THỰC HIỆN CHI TIẾT

### Buổi 1 (Thứ 2: 19:30 - 21:30 | 2.0 giờ): Nghiên cứu Rekognition & Logic bóc tách biển số
* **Mục tiêu:** Hiểu cấu trúc JSON trả về của Rekognition và viết giải thuật Regex.
* **Nhiệm vụ cụ thể:**
  - Đọc tài liệu AWS Rekognition `DetectText`: Phân biệt `LINE` vs `WORD`, chỉ số `Confidence`.
  - Nghiên cứu quy chuẩn biển số xe cơ giới Việt Nam:
    - Xe máy: Dòng trên (Mã tỉnh + Seri: `59-X1`), dòng dưới (Số thứ tự: `123.45`).
    - Ô tô: Biển vuông hoặc biển dài (`51A-123.45`, `30H-999.88`).
  - Xây dựng regex lọc nhiễu loại bỏ dấu chấm, gạch ngang, ghép 2 dòng thành 1 chuỗi chuẩn (ví dụ: `59X112345`).
* **Sản phẩm:** Script Python test local regex `scripts/test_plate_regex.py`.

### Buổi 2 (Thứ 4: 19:00 - 21:30 | 2.5 giờ): Thiết kế Kiến trúc & Thiết kế Schema Dữ liệu
* **Mục tiêu:** Hoàn thiện sơ đồ kiến trúc Serverless và schema database.
* **Nhiệm vụ cụ thể:**
  - Vẽ sơ đồ kiến trúc hệ thống (Architecture Diagram) bằng Mermaid / Draw.io.
  - Thiết kế luồng dữ liệu (Data Flow Diagram) từ Client -> API Gateway -> Lambda -> Rekognition -> DynamoDB -> S3.
  - Thiết kế cấu trúc bảng DynamoDB `ParkingTickets`:
    - `ticketId` (PK, String - UUID)
    - `plateNumber` (String)
    - `vehicleType` (String: `MOTORBIKE` / `CAR`)
    - `checkinTime` (String - ISO8601)
    - `checkoutTime` (String - ISO8601)
    - `status` (String: `PARKED` / `COMPLETED`)
    - `fee` (Number)
    - `inImageKey` / `outImageKey` (String)
* **Sản phẩm:** File tài liệu kiến trúc.

### Buổi 3 (Thứ 6: 19:30 - 21:30 | 2.0 giờ): Rà soát Backend Logic & Mock Test
* **Mục tiêu:** Kiểm tra và hoàn thiện 2 hàm Lambda `SmartParking-Checkin` và `SmartParking-Checkout`.
* **Nhiệm vụ cụ thể:**
  - Viết logic `backend/checkin.py`: Xử lý ngoại lệ khi ảnh mờ không đọc được biển số (gán cờ `UNKNOWN` để cho phép bảo vệ can thiệp).
  - Viết logic `backend/checkout.py`: Thuật toán tính tiền theo block giờ (Xe máy 5.000đ/4h đầu, +2.000đ/giờ tiếp; Ô tô 20.000đ/2h đầu...).
  - Thiết lập chuẩn CORS headers đầy đủ trong Lambda response.
* **Sản phẩm:** Mã nguồn sẵn sàng trong thư mục `backend/`.

### Buổi 4 (Thứ 7: 14:00 - 16:00 | 2.0 giờ): Thiết lập GitHub Repository & Tài liệu hóa
* **Mục tiêu:** Hoàn thiện tài liệu dự án, cấu hình Git Flow.
* **Nhiệm vụ cụ thể:**
  - Khởi tạo git repo, cấu hình `.gitignore`, tạo nhánh `dev`.
  - Viết hướng dẫn tổng quan `README.md` mô tả đề tài, thành viên, kiến trúc và cách chạy.
  - Tạo Pull Request / Commit chuẩn hóa cho Tuần 1.
* **Sản phẩm:** Repository Git có đầy đủ commit history trên nhánh `dev`.
