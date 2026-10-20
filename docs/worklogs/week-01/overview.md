# NHẬT KÝ TỔNG HỢP CÔNG VIỆC TUẦN 1 (WEEK 1 WORKLOG - OVERVIEW)
### HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD) · ĐỢT 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm đề tài:** Domain Apps — Hệ thống quản lý bãi giữ xe thông minh (Smart Parking)
* **Thời gian thực hiện Tuần 1:** Từ ngày 06/10/2026 đến ngày 12/10/2026
* **Môi trường thực hành:** AWS Learner Lab | Region: `us-east-1` (N. Virginia)
* **GitHub Repository:** [nthai212006-gh/cloud-smart-parking-system](https://github.com/nthai212006-gh/cloud-smart-parking-system) (Nhánh chính: `main`)

---

## 1. THÔNG TIN THÀNH VIÊN NHÓM
1. **Sinh viên 1 (Trưởng nhóm):**
   - Họ và tên: Lê Cao Việt Tín
   - Mã số sinh viên (MSSV): 24110354
   - Vai trò: Thiết kế kiến trúc Serverless, AI Rekognition & Backend Core Lambda
   - Chi tiết nhật ký: [worklogs/week-01/member-1.md](member-1.md)
2. **Sinh viên 2:**
   - Họ và tên: Nguyễn Trung Hải
   - Mã số sinh viên (MSSV): 24110207
   - Vai trò: Thiết lập hạ tầng AWS (S3, DynamoDB), Thu thập & Xử lý bộ ảnh test, Kiểm thử & QA
   - Chi tiết nhật ký: [worklogs/week-01/member-2.md](member-2.md)

---

## 2. BẢNG TỔNG HỢP GIỜ LÀM VIỆC TUẦN 1
*(Yêu cầu môn học: Mỗi sinh viên ≥ 8.0 giờ/tuần)*

| Sinh viên | Tổng số giờ quy định | Tổng số giờ thực tế | Trạng thái đạt/không đạt |
| :--- | :---: | :---: | :---: |
| **Lê Cao Việt Tín** (`24110354`) | ≥ 8.0 giờ | **8.5 giờ** | **ĐẠT (Vượt chỉ tiêu)** |
| **Nguyễn Trung Hải** (`24110207`) | ≥ 8.0 giờ | **8.5 giờ** | **ĐẠT (Vượt chỉ tiêu)** |
| **Tổng cả nhóm** | ≥ 16.0 giờ | **17.0 giờ** | **HOÀN THÀNH XUẤT SẮC** |

---

## 3. BẢNG TỔNG HỢP MINH CHỨNG GITHUB TRỰC TIẾP (DIRECT BLOB & COMMIT LINKS)

| STT | Hạng mục / Chức năng kỹ thuật | Thành viên phụ trách | Minh chứng Commit cụ thể | Minh chứng File mã nguồn trực tiếp (blob) |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Lambda Check-in Core**<br>(Nhận diện biển số, tạo vé vào) | Lê Cao Việt Tín<br>(`24110354`) | [Commit cb85da8](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) | [`backend/checkin.py`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/backend/checkin.py) |
| 2 | **Lambda Check-out Core**<br>(Xử lý xe ra, tính phí theo block) | Lê Cao Việt Tín<br>(`24110354`) | [Commit cb85da8](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) | [`backend/checkout.py`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/backend/checkout.py) |
| 3 | **Thiết kế Kiến trúc Serverless**<br>(Tài liệu kiến trúc hệ thống) | Lê Cao Việt Tín<br>(`24110354`) | [Commit cb85da8](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) | [`docs/THIET_KE_KIEN_TRUC_HE_THONG.md`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/docs/THIET_KE_KIEN_TRUC_HE_THONG.md) |
| 4 | **Kiểm thử Regex Biển số VN**<br>(Bộ regex OCR biển số xe) | Lê Cao Việt Tín<br>(`24110354`) | [Commit cb85da8](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/cb85da8) | [`scripts/test_plate_regex.py`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/scripts/test_plate_regex.py) |
| 5 | **Khởi tạo Hạ tầng S3 & DynamoDB**<br>(Script cấu hình tự động) | Nguyễn Trung Hải<br>(`24110207`) | [Commit 41ec17b](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/41ec17b) | [`scripts/setup_aws_resources.py`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/scripts/setup_aws_resources.py) |
| 6 | **Bộ dữ liệu 120 ảnh test che mờ PII**<br>(Thu thập, tiền xử lý & bảo mật) | Nguyễn Trung Hải<br>(`24110207`) | [Commit a2d46cd](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/a2d46cd) | [`test-images/`](https://github.com/nthai212006-gh/cloud-smart-parking-system/tree/main/test-images) |
| 7 | **Đặc tả REST API Gateway**<br>(OpenAPI 3.0 / Swagger spec) | Nguyễn Trung Hải<br>(`24110207`) | [Commit 6c5728a](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/6c5728a) | [`backend/api_gateway_openapi.json`](https://github.com/nthai212006-gh/cloud-smart-parking-system/blob/main/backend/api_gateway_openapi.json) |
| 8 | **Minh chứng AWS Console & Billing**<br>(Ảnh chụp S3, DynamoDB, Billing $0) | Nguyễn Trung Hải<br>(`24110207`) | [Commit b43ca19](https://github.com/nthai212006-gh/cloud-smart-parking-system/commit/b43ca19) | [`evidence/week1/`](https://github.com/nthai212006-gh/cloud-smart-parking-system/tree/main/evidence/week1) |

---

## 4. TỔNG KẾT KẾT QUẢ KỸ THUẬT TUẦN 1
1. **Thiết kế kiến trúc hệ thống:**
   - Xây dựng sơ đồ kiến trúc Serverless (Client -> API Gateway -> Lambda -> Rekognition -> DynamoDB -> S3).
   - Thiết kế Data Flow và lược đồ cơ sở dữ liệu `ParkingTickets` (PK: `ticketId`).
2. **Backend Core & Xử lý AI OCR:**
   - Triển khai thuật toán xử lý chuỗi OCR từ Amazon Rekognition `DetectText`: giải quyết triệt để vấn đề biển số xe máy 2 dòng bị tách block rời rạc bằng cơ chế ghép dòng và Regex chuẩn hóa biển số Việt Nam.
   - Viết khung logic hàm `checkin.py` và `checkout.py` tính toán phí theo block thời gian và trạng thái vé.
3. **Thiết lập Hạ tầng AWS Learner Lab:**
   - Khởi tạo S3 Bucket `smart-parking-images-24110207` với 3 prefix `in/`, `out/`, `athena-logs/`.
   - Khởi tạo bảng DynamoDB `ParkingTickets` (Chế độ On-demand) và gán đủ 3 tag theo quy định (`Project`, `Owner`, `Environment`).
   - Xử lý bộ ảnh test 120 ảnh che kín mặt người (bảo mật PII).
4. **Quản trị chi phí & Minh chứng:**
   - Chi phí phiên làm việc: **`$0.00`** (bảo toàn ngân sách $100).
   - Đã thu thập đủ 4 ảnh minh chứng console trong [`evidence/week1/`](https://github.com/nthai212006-gh/cloud-smart-parking-system/tree/main/evidence/week1).

---

## 5. KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI TRANSPARENCY)
*(Thực hiện đúng yêu cầu quy định: Được dùng AI để tham khảo cú pháp, gợi ý regex; sinh viên trực tiếp thiết lập hạ tầng, code logic và làm chủ 100% khi vấn đáp)*

* **Các công cụ AI đã tham khảo:** Google Gemini, ChatGPT (GPT-4o), Anthropic Claude.
* **Các nội dung có sự hỗ trợ của AI:**
  1. Hỗ trợ sinh cấu trúc cú pháp sơ đồ Mermaid trong tài liệu thiết kế kiến trúc.
  2. Gợi ý biểu thức chính quy (Regex) cơ bản kiểm tra định dạng chuỗi ký tự biển số xe.
  3. Gợi ý script cấu hình tài nguyên tự động kèm gắn thẻ Tag theo chuẩn Learner Lab.
* **Cam kết và mức độ làm chủ của Sinh viên:**
  - 100% tài nguyên đã được nhóm sinh viên trực tiếp thiết lập, cấu hình và chạy thử nghiệm thực tế trên môi trường AWS Learner Lab cá nhân.
  - Nhóm sinh viên đã tự sửa đổi giải thuật ghép dòng biển số 2 dòng thực tế (kết quả Rekognition trả về rời rạc mà AI ban đầu chỉ gợi ý regex 1 dòng), tự viết thuật toán tính phí bãi xe và làm chủ 100% nội dung giải trình khi GVHD vấn đáp.

---

## 6. XÁC NHẬN CỦA CÁC THÀNH VIÊN
*(Ký và ghi rõ họ tên)*

| Chữ ký Sinh viên 1 (Trưởng nhóm) | Chữ ký Sinh viên 2 |
| :---: | :---: |
| *(Đã ký xác nhận)* | *(Đã ký xác nhận)* |
| **Lê Cao Việt Tín** | **Nguyễn Trung Hải** |
