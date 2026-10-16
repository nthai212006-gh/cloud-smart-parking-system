# NHẬT KÝ TỔNG HỢP CÔNG VIỆC TUẦN 2 (WEEK 2 WORKLOG - OVERVIEW)
### HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD) · ĐỢT 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm đề tài:** Domain Apps — Hệ thống quản lý bãi giữ xe thông minh (Smart Parking)
* **Thời gian thực hiện Tuần 2:** Từ ngày 13/10/2026 đến ngày 19/10/2026
* **Môi trường thực hành:** AWS Learner Lab | Region: `us-east-1` (N. Virginia)
* **GitHub Repository:** [nthai212006-gh/cloud-smart-parking-system](https://github.com/nthai212006-gh/cloud-smart-parking-system) (Nhánh chính: `main`)

---

## 1. THÔNG TIN THÀNH VIÊN NHÓM
1. **Sinh viên 1 (Trưởng nhóm):**
   - Họ và tên: Lê Cao Việt Tín
   - Mã số sinh viên (MSSV): 24110354
   - Vai trò: Triển khai Lambda Functions, Rekognition OCR, API Gateway & Test Scripts tự động
   - Chi tiết nhật ký: [worklogs/week-02/member-1.md](member-1.md)
2. **Sinh viên 2:**
   - Họ và tên: Nguyễn Trung Hải
   - Mã số sinh viên (MSSV): 24110207
   - Vai trò: Cấu hình hạ tầng S3 CORS, Kiểm thử Dataset 120 ảnh trên Rekognition, QA & Thu thập minh chứng
   - Chi tiết nhật ký: [worklogs/week-02/member-2.md](member-2.md)

---

## 2. BẢNG TỔNG HỢP GIỜ LÀM VIỆC TUẦN 2
*(Yêu cầu môn học: Mỗi sinh viên ≥ 8.0 giờ/tuần)*

| Sinh viên | Tổng số giờ quy định | Tổng số giờ thực tế | Trạng thái đạt/không đạt |
| :--- | :---: | :---: | :---: |
| **Lê Cao Việt Tín** (`24110354`) | ≥ 8.0 giờ | **8.5 giờ** | **ĐẠT (Vượt chỉ tiêu)** |
| **Nguyễn Trung Hải** (`24110207`) | ≥ 8.0 giờ | **8.5 giờ** | **ĐẠT (Vượt chỉ tiêu)** |
| **Tổng cả nhóm** | ≥ 16.0 giờ | **17.0 giờ** | **HOÀN THÀNH XUẤT SẮC** |

---

## 3. TỔNG KẾT KẾT QUẢ KỸ THUẬT TUẦN 2

1. **Hạ tầng & Dịch vụ Serverless:**
   - Hoàn thành cấu hình S3 CORS trên bucket `smart-parking-images-24110207`.
   - Triển khai 2 hàm AWS Lambda lõi (`SmartParking-Checkin`, `SmartParking-Checkout`) với Python 3.11, Timeout 15s, Memory 256MB và `LabRole`.
   - Triển khai Amazon API Gateway REST API `SmartParking-API` (ID: `fdbsdxyto1`) tại Stage `dev`:
     * Endpoint Check-in: `POST https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev/checkin`
     * Endpoint Check-out: `POST https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev/checkout`
2. **Kiểm thử thành phần & Toàn trình:**
   - Nhận diện biển số thật bằng Amazon Rekognition: Đọc đúng biển số `29B155555`, tạo vé `eeca78ee...` và `99ec3ca4...`.
   - Lưu trữ tự động 2 file ảnh xe vào thư mục S3 `in/`.
   - Tính phí gửi xe chính xác theo block thời gian (5.000 VNĐ cho xe máy).
   - Kiểm thử ngoại lệ thành công: Chặn thanh toán trùng lặp (400) và vé không tồn tại (404).
   - Đánh giá trên bộ dữ liệu 120 ảnh: Đạt tỷ lệ thành công 96.7% (chi tiết tại [`rekognition_evaluation_report.md`](rekognition_evaluation_report.md)).
3. **Quản trị chi phí:**
   - Chi phí phiên làm việc: **`$0.00`** (bảo toàn ngân sách $100).
4. **Hồ sơ minh chứng:**
   - Đã thu thập đủ 8 ảnh màn hình console trong thư mục [`evidence/week2/`](../../evidence/week2).

---

## 4. KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI TRANSPARENCY)
*(Thực hiện đúng yêu cầu quy định: Được dùng AI để tham khảo, sinh mã, gỡ lỗi; nhưng mọi tài nguyên phải được triển khai và chạy thật trên AWS Learner Lab. Ghi rõ phần nào có AI hỗ trợ và sinh viên phải giải thích được khi vấn đáp)*

* **Các công cụ AI đã tham khảo:** Google Gemini, Anthropic Claude, Amazon Q Developer.
* **Các nội dung có sự hỗ trợ của AI:**
  1. Tham khảo cú pháp SDK `boto3` khi gọi Amazon Rekognition `detect_text` và xử lý stream ảnh bytes từ Base64.
  2. Gợi ý cấu trúc chuyển đổi kiểu số sang `Decimal` khi cập nhật trường `fee` trong DynamoDB.
  3. Gợi ý mẫu cấu hình CORS `OPTIONS` preflight trong Amazon API Gateway REST API.
* **Cam kết và mức độ làm chủ của Sinh viên:**
  - 100% tài nguyên Lambda, API Gateway, S3, DynamoDB đã được nhóm sinh viên trực tiếp thiết lập, cấu hình và chạy thử nghiệm thực tế trên môi trường AWS Learner Lab cá nhân.
  - Cả 2 sinh viên đã nghiên cứu sâu, hiểu rõ từng thông số cấu hình và chịu trách nhiệm giải thích tường tận mọi thắc mắc trong buổi vấn đáp của GVHD.

---

## 5. XÁC NHẬN CỦA CÁC THÀNH VIÊN
*(Ký và ghi rõ họ tên)*

| Chữ ký Sinh viên 1 (Trưởng nhóm) | Chữ ký Sinh viên 2 |
| :---: | :---: |
| *(Đã ký xác nhận)* | *(Đã ký xác nhận)* |
| **Lê Cao Việt Tín** | **Nguyễn Trung Hải** |
