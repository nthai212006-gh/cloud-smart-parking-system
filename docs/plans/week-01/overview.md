# KẾ HOẠCH TỔNG QUAN TUẦN 1 (WEEK 1 PLAN - OVERVIEW)
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING)
* **Học phần:** Điện toán đám mây (Cloud Computing) - Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** Huỳnh Xuân Phụng
* **Nhóm sinh viên thực hiện:** 2 Sinh viên
* **Môi trường triển khai:** AWS Learner Lab (`us-east-1`)
* **Thời gian thực hiện:** 06/10/2026 - 12/10/2026

---

## I. MỤC TIÊU CHUNG TUẦN 1
1. **Nghiên cứu công nghệ & dịch vụ:** Nắm vững Amazon Rekognition (DetectText), AWS Lambda (Python 3.11), Amazon S3, Amazon DynamoDB, Amazon API Gateway, Amazon Athena.
2. **Thiết kế kiến trúc hệ thống:** Xây dựng sơ đồ kiến trúc Serverless tổng thể, lược đồ luồng dữ liệu (Data Flow) và thiết kế Schema cơ sở dữ liệu.
3. **Dựng nền tảng hạ tầng AWS (Foundations):**
   - Khởi tạo S3 Bucket lưu trữ ảnh và logs, cấu hình thư mục ảo (`in/`, `out/`, `athena-logs/`).
   - Khởi tạo DynamoDB Table `ParkingTickets` với Partition Key `ticketId` (On-demand mode).
   - Thiết lập chuẩn Tagging: `Project=SmartParking`, `Owner=[MSSV]`, `Environment=Development`.
   - Nắm rõ giới hạn và quy định sử dụng `LabRole` trong AWS Learner Lab.
4. **Chuẩn bị dữ liệu thử nghiệm:** Thu thập 15–20 ảnh biển số thực tế, che mờ khuôn mặt người và thông tin cá nhân theo đúng yêu cầu đề tài.
5. **Khởi tạo mã nguồn & Quy trình làm việc:** Thiết lập GitHub repository, phân chia module, quản lý Git branch `dev` và `main`.

---

## II. BẢNG PHÂN CÔNG NHIỆM VỤ TỔNG THỂ

> **Quy định môn học:** Mỗi sinh viên phải dành **≥ 8.0 giờ/tuần** cho dự án.

| Thành viên | Vai trò chính | Thời lượng | Kế hoạch chi tiết | Nhật ký thực hiện |
| :--- | :--- | :---: | :---: | :---: |
| **Member 1 (Sinh viên 1)** | Kiến trúc Serverless, AI Rekognition & Backend Core | **8.5 giờ** | [plans/week-01/member-1.md](member-1.md) | [worklogs/week-01/member-1.md](../../worklogs/week-01/member-1.md) |
| **Member 2 (Sinh viên 2)** | Hạ tầng AWS (S3, DynamoDB), Dataset & QA/Audit | **8.5 giờ** | [plans/week-01/member-2.md](member-2.md) | [worklogs/week-01/member-2.md](../../worklogs/week-01/member-2.md) |
| **Cả nhóm** | Họp tiến độ, rà soát hồ sơ & Git workflow | **17.0 giờ** | [plans/week-01/overview.md](overview.md) | [worklogs/week-01/overview.md](../../worklogs/week-01/overview.md) |

---

## III. CHECKLIST NGHIỆM THU TUẦN 1 (ACCEPTANCE CHECKLIST)

- [ ] **Tài liệu & Kiến trúc:**
  - [ ] Sơ đồ kiến trúc Serverless Mermaid & Data Flow.
  - [ ] Schema DynamoDB được định nghĩa chi tiết.
  - [ ] Quy chuẩn Tagging & Naming convention ([guidelines/tagging-standards.md](../../guidelines/tagging-standards.md)).
- [ ] **Hạ tầng AWS Learner Lab:**
  - [ ] S3 Bucket `smart-parking-images-[mssv]` đã tạo thành công và gắn tag chuẩn.
  - [ ] 3 folder `in/`, `out/`, `athena-logs/` đã có trong bucket.
  - [ ] Bảng DynamoDB `ParkingTickets` đã tạo (PK `ticketId`, On-Demand, Active).
  - [ ] Đã xác thực quyền thực thi của `LabRole`.
- [ ] **Dữ liệu & Mã nguồn:**
  - [ ] Đã có ít nhất 15 ảnh biển số được che mờ mặt người trong `test-images/`.
  - [ ] Mã nguồn Lambda trong thư mục `backend/` đã kiểm thử regex cục bộ.
  - [ ] Git repository làm việc trên nhánh `dev`, đẩy đủ commit.
- [ ] **Hồ sơ minh chứng:**
  - [ ] Ảnh chụp màn hình S3 Console (có Account ID, Region `us-east-1`, Timestamp đồng hồ).
  - [ ] Ảnh chụp màn hình DynamoDB Console (có Account ID, Region, Timestamp).
  - [ ] Nhật ký công việc đầy đủ chữ ký/xác nhận giờ của 2 thành viên.
