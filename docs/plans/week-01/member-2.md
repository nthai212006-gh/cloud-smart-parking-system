# KẾ HOẠCH CHI TIẾT TUẦN 1 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, QUẢN TRỊ DỮ LIỆU & ĐẢM BẢO CHẤT LƯỢNG (INFRASTRUCTURE / DATA / QA)
* **Thành viên:** Sinh viên 2 (Nguyễn Trung Hải - 24110207)
* **Tổng thời gian phân bổ:** **8.5 giờ**

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN
1. Khảo sát môi trường AWS Learner Lab, xác nhận IAM Role `LabRole` và quy chuẩn Tagging.
2. Thu thập và xử lý bộ ảnh biển số xe mẫu, che mờ toàn bộ khuôn mặt người và thông tin nhạy cảm.
3. Khởi tạo S3 Bucket `smart-parking-images-24110207` với 3 thư mục `in/`, `out/`, `athena-logs/`.
4. Khởi tạo DynamoDB Table `ParkingTickets` (PK `ticketId`, On-Demand mode).
5. Thu thập bộ 4 ảnh chụp màn hình minh chứng console (đáp ứng tiêu chuẩn kiểm tra của GVHD).
6. Soạn thảo tài liệu nhật ký làm việc và theo dõi chi phí phiên làm việc ($0.00).

---

## II. LỊCH TRÌNH THỰC HIỆN CHI TIẾT (4 BUỔI)

### Buổi 1 (Thứ 3: 19:00 - 21:30 | 2.5 giờ): Khảo sát AWS Learner Lab & Quy chuẩn Tagging
* **Mục tiêu:** Nắm vững ràng buộc AWS Learner Lab, soạn thảo quy chuẩn cấu hình.
* **Nhiệm vụ cụ thể:**
  - Đăng nhập Learner Lab, Start Lab và mở AWS Console.
  - Chọn Region bắt buộc: `us-east-1` (N. Virginia).
  - Tra cứu IAM: Tìm `LabRole`, sao chép ARN (`arn:aws:iam::<AccountID>:role/LabRole`). Tuyệt đối không tạo IAM Role/User mới.
  - Soạn thảo quy chuẩn Tagging tài nguyên trong file [docs/guidelines/tagging-standards.md](../../guidelines/tagging-standards.md):
    - `Project=SmartParking`
    - `Owner=[MSSV_SV1]_[MSSV_SV2]`
    - `Environment=Development`
* **Sản phẩm:** File `docs/guidelines/tagging-standards.md` và ghi nhận thông tin tài khoản lab.

### Buổi 2 (Thứ 5: 19:30 - 21:30 | 2.0 giờ): Chuẩn bị Dataset ảnh biển số thực tế
* **Mục tiêu:** Tạo bộ dữ liệu ảnh mẫu đáp ứng tiêu chuẩn riêng tư.
* **Nhiệm vụ cụ thể:**
  - Thu thập và phân loại ảnh xe máy (biển 2 dòng) và ô tô (biển 1 dòng/biển vuông), góc thẳng và nghiêng.
  - Sử dụng công cụ đồ họa **che mờ/bôi đen toàn bộ khuôn mặt người** và thông tin cá nhân.
  - Nén ảnh về khoảng 200KB - 800KB để upload nhanh qua API.
  - Chuẩn hóa tên file và cấu trúc phân loại theo các kịch bản kiểm thử.
* **Sản phẩm:** Thư mục `test-images/` chứa bộ ảnh mẫu đã xử lý và che thông tin nhạy cảm.

### Buổi 3 (Thứ 6: 19:30 - 21:30 | 2.0 giờ): Khởi tạo S3 Bucket & Bảng DynamoDB
* **Mục tiêu:** Dựng xong tài nguyên lưu trữ nền tảng trên AWS Console.
* **Nhiệm vụ cụ thể:**
  - Tạo S3 Bucket: `smart-parking-images-24110207` (Region `us-east-1`), Block all public access, gắn 3 tag chuẩn.
  - Tạo 3 folder ảo trong S3: `in/`, `out/`, `athena-logs/`.
  - Tạo DynamoDB Table: `ParkingTickets` (Partition Key: `ticketId` kiểu String, Capacity: `On-Demand`, gắn 3 tag chuẩn).
  - Chụp ảnh màn hình minh chứng console (full screen, rõ Account ID, Region, đồng hồ máy tính).
* **Sản phẩm:** S3 Bucket, DynamoDB Table Active, ảnh minh chứng trong `evidence/week1/`.

### Buổi 4 (Chủ nhật: 14:00 - 16:00 | 2.0 giờ): Báo cáo tiến độ & Hoàn thiện Worklog
* **Mục tiêu:** Hoàn tất bộ hồ sơ minh chứng Tuần 1.
* **Nhiệm vụ cụ thể:**
  - Chụp ảnh màn hình Billing/Cost Management xác nhận chi phí $0.00.
  - Điền đầy đủ thông tin vào `docs/worklogs/week-01/member-2.md` và `docs/worklogs/week-01/overview.md`.
  - Commit toàn bộ dữ liệu lên nhánh `dev` của GitHub repo.
  - Bấm **End Lab** để kết thúc phiên làm việc.
* **Sản phẩm:** File worklog hoàn chỉnh, commit đầy đủ trên GitHub.
