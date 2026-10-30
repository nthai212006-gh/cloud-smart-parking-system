# BÁO CÁO NHẬT KÝ CÔNG VIỆC TUẦN 4 - THÀNH VIÊN 1
### HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Sinh viên 1:** Lê Cao Việt Tín (MSSV: 24110354)
* **Nhóm:** Domain Apps
* **Đề tài:** Hệ thống Quản lý Bãi giữ xe Thông minh (Smart Parking System)
* **Giai đoạn:** Tuần 4 – Kiểm thử tổng thể, Tối ưu chi phí, Viết báo cáo tổng kết & Nghiệm thu đồ án

---

## 1. BẢNG THEO DÕI TIẾN ĐỘ & SỐ GIỜ LÀM VIỆC (8.5 GIỜ)

| Ngày thực hiện | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng bàn giao |
| :---: | :---: | :---: | :--- | :--- |
| **28/10/2026**<br>(Thứ 4) | 19:30 - 21:30 | 2.0h | - Tinh chỉnh giao diện Enterprise Desktop POS 5 tầng đối xứng (`frontend/index.html` và `frontend/style.css`).<br>- Khóa chiều cao Tầng 3 (48px) và Tầng 4 (44px) cân bằng tuyệt đối giữa Cổng Vào và Cổng Ra.<br>- Loại bỏ các khung chờ nét đứt để tối ưu diện tích hiển thị POS.<br>- Kiểm tra tương thích với API Gateway và DynamoDB. | Commit `f90a317`, `986cf0c`<br>Giao diện POS đối xứng hoàn hảo |
| **29/10/2026**<br>(Thứ 5) | 19:30 - 21:45 | 2.25h | - Xây dựng tài liệu Báo cáo tổng kết đồ án toàn trình 4 tuần.<br>- Chuẩn hóa sơ đồ kiến trúc hệ thống Serverless Decoupled (API Gateway, Lambda, Rekognition, S3, DynamoDB, CloudWatch, Athena).<br>- Tổng hợp báo cáo kiểm thử an toàn dữ liệu: DynamoDB Atomic Conditional Write chống Race Condition. | Bản thảo Báo cáo tổng kết đồ án<br>Sơ đồ kiến trúc hệ thống |
| **30/10/2026**<br>(Thứ 6) | 14:00 - 16:15 | 2.25h | - Tổng hợp báo cáo kiểm toán chi phí AWS Billing cuối kỳ: Xác nhận duy trì an toàn `$0.00` Month-to-date cost.<br>- Phối hợp với Thành viên 2 (Hải) chạy thử nghiệm kịch bản quay video demo toàn trình.<br>- Kiểm tra kịch bản chạy thử tải Throttling với script đa luồng `scripts/test_api_throttling.py` (30 req/s $\rightarrow$ HTTP 429). | Số liệu chi phí Billing `$0.00`<br>Kết quả kiểm thử tải API Gateway |
| **31/10/2026**<br>(Thứ 7) | 19:30 - 21:30 | 2.0h | - Rà soát file Infrastructure as Code `iac/cloudformation_template.yaml`.<br>- Chuẩn bị kịch bản lệnh dọn dẹp tài nguyên sau khi nghiệm thu (`aws cloudformation delete-stack`).<br>- Hoàn thiện file Báo cáo tổng kết cuối kỳ (Word/PDF) và đồng bộ tài liệu nộp bài. | File Báo cáo tổng kết cuối kỳ<br>Quy trình dọn dẹp tài nguyên IaC |
| **TỔNG CỘNG** | | **8.5h** | **Đạt và vượt định mức quy định môn học ($\ge$ 8.0 giờ/tuần)** | **Đầy đủ sản phẩm nghiệm thu** |

---

## 2. KẾT QUẢ ĐẠT ĐƯỢC
1. Hoàn tất 100% bộ tài liệu Báo cáo tổng kết đồ án theo quy chuẩn môn học.
2. Xác nhận chi phí đám mây duy trì tối ưu ở mức **$0.00** nhờ kiến trúc Serverless.
3. Toàn bộ hạ tầng đám mây sẵn sàng cho quy trình dọn dẹp 1-chạm bằng CloudFormation.
