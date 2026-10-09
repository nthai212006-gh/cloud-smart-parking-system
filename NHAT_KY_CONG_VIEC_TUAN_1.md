# NHẬT KÝ CÔNG VIỆC TUẦN 1 (WORKLOG - WEEK 1)
### HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD) · ĐỢT 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** Huỳnh Xuân Phụng
* **Nhóm đề tài:** Domain Apps — Hệ thống quản lý bãi giữ xe thông minh (Smart Parking)
* **Thời gian thực hiện Tuần 1:** Từ ngày 06/10/2026 đến ngày 12/10/2026
* **Môi trường thực hành:** AWS Learner Lab | Region: `us-east-1` (N. Virginia)

---

## 1. THÔNG TIN THÀNH VIÊN NHÓM
1. **Sinh viên 1 (Trưởng nhóm):**
   - Họ và tên: `[Điền Họ và Tên SV 1]`
   - Mã số sinh viên (MSSV): `[Điền MSSV 1]`
   - Vai trò: Phụ trách Thiết kế kiến trúc hệ thống, Logic AI & Backend Core
2. **Sinh viên 2:**
   - Họ và tên: `[Điền Họ và Tên SV 2]`
   - Mã số sinh viên (MSSV): `[Điền MSSV 2]`
   - Vai trò: Phụ trách Thiết lập hạ tầng AWS, Thu thập & Xử lý dữ liệu mẫu, Kiểm thử & QA

---

## 2. BẢNG TỔNG HỢP GIỜ LÀM VIỆC TUẦN 1
*(Yêu cầu môn học: Mỗi sinh viên ≥ 8 giờ/tuần)*

| Sinh viên | Tổng số giờ quy định | Tổng số giờ thực tế | Trạng thái đạt/không đạt |
| :--- | :---: | :---: | :---: |
| **Sinh viên 1** (`[MSSV 1]`) | ≥ 8.0 giờ | **8.5 giờ** | **ĐẠT (Vượt chỉ tiêu)** |
| **Sinh viên 2** (`[MSSV 2]`) | ≥ 8.0 giờ | **8.5 giờ** | **ĐẠT (Vượt chỉ tiêu)** |
| **Tổng cả nhóm** | ≥ 16.0 giờ | **17.0 giờ** | **HOÀN THÀNH TỐT** |

---

## 3. NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

### A. Sinh viên 1: `[Họ và tên SV 1]` (Tổng: 8.5 giờ)
| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **06/10/2026**<br>(Thứ 2) | 19:30 - 21:30 | 2.0h | - Đọc tài liệu AWS Rekognition `DetectText` API.<br>- Viết giải thuật Regex chuẩn hóa biển số xe Việt Nam (ghép dòng, bỏ ký tự lạ). | Script `scripts/test_plate_regex.py`<br>Commit Git: `feat: add plate regex parser` |
| **08/10/2026**<br>(Thứ 4) | 19:00 - 21:30 | 2.5h | - Thiết kế sơ đồ kiến trúc Serverless bằng Mermaid.<br>- Thiết kế lược đồ luồng dữ liệu (Data Flow).<br>- Định nghĩa bảng dữ liệu DynamoDB `ParkingTickets`. | Tài liệu `docs/THIET_KE_KIEN_TRUC_HE_THONG.md` |
| **10/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Rà soát logic `backend/checkin.py` và `backend/checkout.py`.<br>- Tinh chỉnh thuật toán tính tiền theo block giờ.<br>- Kiểm tra CORS headers và xử lý ngoại lệ biển số không đọc được. | Mã nguồn hoàn thiện trong thư mục `backend/` |
| **11/10/2026**<br>(Thứ 7) | 14:00 - 16:00 | 2.0h | - Khởi tạo GitHub repository cho nhóm.<br>- Soạn thảo file `README.md` và tổ chức cấu trúc thư mục dự án chuẩn mực. | [GitHub Repository](https://github.com/nthai212006-gh/cloud-smart-parking-system) |

---

### B. Sinh viên 2: `[Họ và tên SV 2]` (Tổng: 8.5 giờ)
| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **07/10/2026**<br>(Thứ 3) | 19:00 - 21:30 | 2.5h | - Khảo sát môi trường AWS Learner Lab: Kiểm tra role `LabRole`, quota Region `us-east-1`.<br>- Thiết lập quy chuẩn Tagging bắt buộc (`Project`, `Owner`, `Environment`). | Biên bản cấu hình hạ tầng<br>File `docs/QUY_CHUAN_TAGGING.md` |
| **09/10/2026**<br>(Thứ 5) | 19:30 - 21:30 | 2.0h | - Chụp 20 ảnh biển số xe máy & ô tô thực tế.<br>- **Che mờ mặt người và các thông tin nhạy cảm** bằng công cụ đồ họa.<br>- Phân loại và tối ưu kích thước ảnh mẫu. | Thư mục `test-images/`<br>20 file ảnh đã ẩn danh hóa |
| **10/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Khởi tạo S3 Bucket `smart-parking-images-[mssv]`, tạo các thư mục `in/`, `out/`, `athena-logs/`.<br>- Khởi tạo DynamoDB table `ParkingTickets` (PK: `ticketId`).<br>- Gắn đầy đủ Tagging chuẩn. | Ảnh chụp màn hình Console S3 & DynamoDB có Account ID, Region, Timestamp |
| **12/10/2026**<br>(Chủ nhật) | 14:00 - 16:00 | 2.0h | - Tổng hợp minh chứng Tuần 1 vào thư mục `evidence/week1/`.<br>- Soạn thảo file Worklog Tuần 1, đối chiếu thời lượng.<br>- Kiểm tra và tắt phiên AWS Learner Lab, xác nhận chi phí phát sinh = $0.00. | File `docs/NHAT_KY_CONG_VIEC_TUAN_1.md`<br>Ảnh chụp Billing / Cost |

---

## 4. KHAI BÁO SỬ DỤNG CÔNG CỤ TRÍ TUỆ NHÂN TẠO (AI TRANSPARENCY)
*(Thực hiện đúng yêu cầu quy định: Được dùng AI nhưng phải ghi rõ phần nào có AI hỗ trợ và sinh viên phải giải thích được khi vấn đáp)*

* **Các công cụ AI đã tham khảo:** Google Gemini, Anthropic Claude, ChatGPT.
* **Các nội dung có sự hỗ trợ của AI:**
  1. Hỗ trợ sinh cấu trúc cú pháp sơ đồ Mermaid trong tài liệu thiết kế kiến trúc.
  2. Gợi ý biểu thức chính quy (Regex) bóc tách chuỗi biển số từ kết quả OCR thô của Rekognition.
  3. Gợi ý script Python Boto3 để tạo tài nguyên tự động kèm gắn thẻ Tag theo chuẩn Learner Lab.
* **Cam kết và mức độ làm chủ của Sinh viên:**
  - 100% tài nguyên đã được nhóm sinh viên trực tiếp thiết lập, cấu hình và chạy thử nghiệm thực tế trên môi trường AWS Learner Lab cá nhân.
  - Cả 2 sinh viên đã nghiên cứu sâu, hiểu rõ từng dòng lệnh, từng thông số cấu hình và chịu trách nhiệm giải thích tường tận mọi thắc mắc trong buổi vấn đáp của GVHD.

---

## 5. XÁC NHẬN CỦA CÁC THÀNH VIÊN
*(Ký và ghi rõ họ tên)*

| Chữ ký Sinh viên 1 | Chữ ký Sinh viên 2 |
| :---: | :---: |
| *(Đã ký xác nhận)* | *(Đã ký xác nhận)* |
| **[Họ và tên SV 1]** | **[Họ và tên SV 2]** |
