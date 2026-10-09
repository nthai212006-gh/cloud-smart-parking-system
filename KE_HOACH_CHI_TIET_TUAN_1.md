# KẾ HOẠCH CHI TIẾT TUẦN 1 (WEEK 1 PLAN)
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING)
* **Học phần:** Điện toán đám mây (Cloud) - Đợt 1 - 2026-2027
* **Giảng viên hướng dẫn (GVHD):** Huỳnh Xuân Phụng
* **Nhóm sinh viên thực hiện:** 2 Sinh viên
* **Môi trường triển khai:** AWS Learner Lab (Region mặc định: `us-east-1`)

---

## I. MỤC TIÊU TUẦN 1
1. **Nghiên cứu công nghệ & dịch vụ:** Nắm vững cách thức vận hành và tích hợp của Amazon Rekognition (DetectText), AWS Lambda (Python 3.11), Amazon S3, Amazon DynamoDB, Amazon API Gateway, Amazon Athena.
2. **Thiết kế kiến trúc hệ thống:** Xây dựng sơ đồ kiến trúc Serverless tổng thể, lược đồ luồng dữ liệu (Data Flow) và thiết kế Schema cơ sở dữ liệu.
3. **Dựng nền tảng hạ tầng AWS (Foundations):**
   - Khởi tạo S3 Bucket lưu trữ ảnh và logs, cấu hình thư mục (`in/`, `out/`, `athena-logs/`).
   - Khởi tạo DynamoDB Table `ParkingTickets` với Partition Key `ticketId`.
   - Thiết lập chuẩn Tagging: `Project=SmartParking`, `Owner=[MSSV]`, `Environment=Development`.
   - Nắm rõ giới hạn và quy định sử dụng `LabRole` trong AWS Learner Lab.
4. **Chuẩn bị dữ liệu thử nghiệm:** Thu thập 15–20 ảnh biển số thực tế, thực hiện che mờ khuôn mặt người và thông tin cá nhân theo đúng yêu cầu đề tài.
5. **Khởi tạo mã nguồn & Quy trình làm việc:** Thiết lập GitHub repository, phân chia module, lập file Nhật ký công việc (Worklog).

---

## II. PHÂN CHIA NHIỆM VỤ CHI TIẾT (2 THÀNH VIÊN)

> **Quy định môn học:** Mỗi sinh viên phải dành **≥ 8 giờ/tuần** cho dự án.

```
+-----------------------------------------------------------------------------------------+
|                                    PHÂN CÔNG TUẦN 1                                     |
+----------------------------------------------------+------------------------------------+
| SINH VIÊN 1 (Trưởng nhóm / Backend & AI)          | SINH VIÊN 2 (Hạ tầng, Data & QA)   |
| Tổng thời gian: 8.5 giờ                            | Tổng thời gian: 8.5 giờ            |
+----------------------------------------------------+------------------------------------+
| 1. Nghiên cứu Rekognition OCR & Lambda (2.0h)      | 1. Khảo sát AWS Learner Lab (2.5h) |
| 2. Thiết kế kiến trúc & Data Flow (2.5h)           | 2. Thu thập & che ảnh mẫu (2.0h)   |
| 3. Hoàn thiện Core Logic bóc tách biển số (2.0h)   | 3. Khởi tạo S3 & DynamoDB (2.0h)   |
| 4. Khởi tạo Git Repo & cấu trúc dự án (2.0h)       | 4. Thiết lập Worklog & Audit (2.0h)|
+----------------------------------------------------+------------------------------------+
```

### 1. Kế hoạch chi tiết của Sinh viên 1 (Kiến trúc & Backend Core)

#### Buổi 1 (Thứ 2: 19:30 - 21:30 | 2.0 giờ): Nghiên cứu Rekognition & Logic bóc tách biển số
* **Mục tiêu:** Hiểu đầu ra của Rekognition `DetectText` API và xây dựng thuật toán lọc chuỗi.
* **Nhiệm vụ cụ thể:**
  - Đọc tài liệu AWS Rekognition API: Phân biệt `LINE` vs `WORD`, chỉ số độ tin cậy `Confidence`.
  - Nghiên cứu quy chuẩn biển số xe cơ giới Việt Nam:
    - Xe máy: Dòng trên (Mã tỉnh + Seri, ví dụ: `59-X1`), dòng dưới (Số thứ tự, ví dụ: `123.45`).
    - Ô tô: Biển vuông hoặc biển dài (`51A-123.45`, `30H-999.88`).
  - Xây dựng regex lọc nhiễu loại bỏ dấu chấm, dấu gạch ngang và ghép 2 dòng thành 1 chuỗi chuẩn (ví dụ: `59X112345`).
* **Sản phẩm:** Script Python test local regex `scripts/test_plate_regex.py`.

#### Buổi 2 (Thứ 4: 19:00 - 21:30 | 2.5 giờ): Thiết kế Kiến trúc & Thiết kế Dữ liệu
* **Mục tiêu:** Hoàn thiện bản vẽ kiến trúc Serverless và thiết kế Database Schema.
* **Nhiệm vụ cụ thể:**
  - Vẽ sơ đồ kiến trúc hệ thống (Architecture Diagram) bằng Mermaid / Draw.io.
  - Thiết kế luồng dữ liệu (Data Flow Diagram) từ Client -> API Gateway -> Lambda -> Rekognition -> DynamoDB -> S3.
  - Thiết kế cấu trúc bảng DynamoDB `ParkingTickets`:
    - `ticketId` (PK, String - UUID): Mã vé gửi.
    - `plateNumber` (String): Biển số xe đã chuẩn hóa.
    - `vehicleType` (String): `MOTORBIKE` hoặc `CAR`.
    - `checkinTime` (String - ISO8601): Thời điểm xe vào.
    - `checkoutTime` (String - ISO8601): Thời điểm xe ra.
    - `status` (String): `PARKED` hoặc `COMPLETED`.
    - `fee` (Number): Phí gửi xe tính toán (VNĐ).
    - `inImageKey` / `outImageKey` (String): Đường dẫn file trên S3.
* **Sản phẩm:** File tài liệu `docs/THIET_KE_KIEN_TRUC_HE_THONG.md`.

#### Buổi 3 (Thứ 6: 19:30 - 21:30 | 2.0 giờ): Rà soát Backend Logic & Mock Test
* **Mục tiêu:** Kiểm tra và hoàn thiện 2 hàm Lambda `SmartParking-Checkin` và `SmartParking-Checkout`.
* **Nhiệm vụ cụ thể:**
  - Đọc và tinh chỉnh file `backend/checkin.py`: Xử lý ngoại lệ khi ảnh mờ không đọc được biển số (gán cờ `UNKNOWN` để cho phép bảo vệ nhập tay).
  - Tinh chỉnh file `backend/checkout.py`: Thuật toán tính tiền theo block giờ (ví dụ: Xe máy 5.000đ/4h đầu, mỗi giờ tiếp theo +2.000đ; Ô tô 20.000đ/2h đầu...).
  - Đảm bảo cơ chế CORS headers đầy đủ trong Lambda response.
* **Sản phẩm:** Mã nguồn sẵn sàng triển khai trong thư mục `backend/`.

#### Buổi 4 (Thứ 7: 14:00 - 16:00 | 2.0 giờ): Thiết lập GitHub Repository & Tài liệu hóa
* **Mục tiêu:** Đưa toàn bộ cấu trúc mã nguồn lên GitHub, tạo README chuyên nghiệp.
* **Nhiệm vụ cụ thể:**
  - Khởi tạo git repo, cấu hình `.gitignore` (chặn `.env`, file ảnh nặng không cần thiết, virtual environment).
  - Viết hướng dẫn tổng quan `README.md` mô tả đề tài, thành viên, kiến trúc và cách chạy.
  - Tạo Pull Request / Commit chuẩn hóa cho Tuần 1.
* **Sản phẩm:** Repository Git công khai/nội bộ có đầy đủ commit history.

---

### 2. Kế hoạch chi tiết của Sinh viên 2 (Hạ tầng AWS, Dataset & Audit)

#### Buổi 1 (Thứ 3: 19:00 - 21:30 | 2.5 giờ): Khảo sát môi trường Learner Lab & Quy chuẩn Tagging
* **Mục tiêu:** Làm chủ các ràng buộc của AWS Learner Lab, tránh bị trừ điểm hoặc khóa bài thực hành.
* **Nhiệm vụ cụ thể:**
  - Đăng nhập Learner Lab, xác định Region (`us-east-1`).
  - Kiểm tra IAM Role: Xác nhận sự tồn tại của role **`LabRole`** (ARN: `arn:aws:iam::[AccountID]:role/LabRole`). Ghi nhớ **tuyệt đối không tạo custom IAM Role/User**.
  - Kiểm tra hạn mức session Learner Lab (thường là 4 tiếng/lần bật Start Lab).
  - Soạn thảo quy chuẩn Tagging:
    - Key: `Project` | Value: `SmartParking`
    - Key: `Owner` | Value: `[MSSV_SV1]_[MSSV_SV2]`
    - Key: `Environment` | Value: `Development`
* **Sản phẩm:** Biên bản kiểm tra môi trường và cấu hình tag.

#### Buổi 2 (Thứ 5: 19:30 - 21:30 | 2.0 giờ): Chuẩn bị Dataset ảnh biển số thực tế
* **Mục tiêu:** Tạo bộ dữ liệu thử nghiệm 15–20 ảnh đúng quy định của GVHD.
* **Nhiệm vụ cụ thể:**
  - Chụp ảnh biển số xe máy và ô tô tại bãi đỗ xe thực tế (đa dạng góc chụp: chính diện, hơi nghiêng, đủ sáng, ngược sáng).
  - Sử dụng công cụ đồ họa (Photoshop/Paint/Canva) **che mờ mặt người chụp/người đi đường và thông tin nhạy cảm** (chỉ để lộ khung biển số và loại phương tiện).
  - Phân loại và nén ảnh (dung lượng mỗi ảnh 200KB - 800KB để upload nhanh qua API).
  - Đặt tên file có cấu trúc rõ ràng: `test_motor_01.jpg`, `test_car_01.jpg`...
* **Sản phẩm:** Thư mục `test-images/` chứa ảnh test đã được che thông tin cá nhân.

#### Buổi 3 (Thứ 6: 19:30 - 21:30 | 2.0 giờ): Khởi tạo S3 Bucket & Bảng DynamoDB
* **Mục tiêu:** Dựng xong 2 tài nguyên lưu trữ nền tảng trên AWS Console.
* **Nhiệm vụ cụ thể:**
  - Tạo S3 Bucket: `smart-parking-images-[mssv]` (Region `us-east-1`).
    - Bật "Block all public access" (đảm bảo bảo mật).
    - Tạo các folder ảo: `in/`, `out/`, `athena-logs/`.
    - Gắn Tag: `Project=SmartParking`, `Owner=[MSSV]`.
  - Tạo DynamoDB Table: `ParkingTickets`.
    - Partition Key: `ticketId` (kiểu `String`).
    - Capacity mode: Chọn `On-Demand` (tiết kiệm chi phí, phù hợp với Learner Lab).
    - Gắn Tag: `Project=SmartParking`, `Owner=[MSSV]`.
  - Chụp ảnh màn hình minh chứng console (đáp ứng tiêu chuẩn: Thấy rõ Account ID, Region, Đồng hồ máy tính).
* **Sản phẩm:** Tài nguyên S3 + DynamoDB sẵn sàng; file ảnh minh chứng trong `evidence/week1/`.

#### Buổi 4 (Chủ nhật: 14:00 - 16:00 | 2.0 giờ): Soạn thảo Worklog Tuần 1 & Báo cáo tiến độ
* **Mục tiêu:** Hoàn thiện hồ sơ minh chứng và nhật ký công việc nộp cho GVHD.
* **Nhiệm vụ cụ thể:**
  - Đối chiếu số giờ làm việc thực tế của 2 sinh viên (đạt tối thiểu 8h/người).
  - Điền đầy đủ file `docs/NHAT_KY_CONG_VIEC_TUAN_1.md`.
  - Viết phần "Khai báo sử dụng AI" trung thực và chi tiết.
  - Rà soát toàn bộ tài nguyên trên AWS, tắt/dọn dẹp phiên làm việc để không lãng phí credits.
* **Sản phẩm:** File nhật ký công việc hoàn chỉnh và bộ ảnh minh chứng.

---

## III. CHECK-LIST NGHIỆM THU TUẦN 1

- [ ] **Tài liệu & Kiến trúc:**
  - [ ] Sơ đồ kiến trúc Mermaid/Hình ảnh được lưu tại `docs/THIET_KE_KIEN_TRUC_HE_THONG.md`.
  - [ ] Schema DynamoDB được định nghĩa chi tiết.
- [ ] **Hạ tầng AWS Learner Lab:**
  - [ ] S3 Bucket đã tạo thành công và được gắn Tag chuẩn.
  - [ ] Bảng DynamoDB `ParkingTickets` đã tạo và ở trạng thái Active.
  - [ ] Đã xác thực quyền thực thi của `LabRole`.
- [ ] **Dữ liệu & Mã nguồn:**
  - [ ] Đã có ít nhất 15 ảnh biển số được che mờ mặt người trong `test-images/`.
  - [ ] Mã nguồn Lambda trong thư mục `backend/` đã được kiểm thử regex cục bộ.
  - [ ] Git repository đã commit đầy đủ toàn bộ tài liệu Tuần 1.
- [ ] **Hồ sơ minh chứng:**
  - [ ] Ảnh chụp màn hình S3 Console (có Account ID, Region `us-east-1`, Timestamp).
  - [ ] Ảnh chụp màn hình DynamoDB Console (có Account ID, Region, Timestamp).
  - [ ] File `docs/NHAT_KY_CONG_VIEC_TUAN_1.md` có đầy đủ chữ ký/xác nhận giờ của 2 thành viên.
