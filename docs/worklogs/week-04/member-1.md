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
| **30/10/2026**<br>(Thứ 6) | 14:00 - 16:15 | 2.25h | - Soạn thảo Chương 4 (Triển khai các dịch vụ AWS) và Chương 6 (Đánh giá chi phí AWS Billing & Tối ưu hóa).<br>- Phân tích thực tế chi phí **`$0.03`** Month-to-date cost (CloudWatch $0.02, Rekognition $0.01 do quá trình chạy stress test và demo nhiều lượt), khẳng định mức tối ưu vượt trội, bảo toàn 99.97% ngân sách $100.<br>- Phối hợp với Thành viên 2 (Hải) chạy thử nghiệm kịch bản quay video demo với 2 ảnh `car_clear_05.jpg` và `motor_clear_06.jpg`. | Số liệu chi phí Billing `$0.03`<br>Bản thảo Chương 4 & Chương 6 |
| **31/10/2026**<br>(Thứ 7) | 19:30 - 21:30 | 2.0h | - Tiếp nhận file Chương 5 (`BaoCao_Chuong_5_KiemThu_Va_GiamSat.docx`) từ Thành viên 2 (Hải) để hợp nhất vào Báo cáo Master tổng thể toàn trình (Chương 1 đến Chương 8).<br>- Rà soát file Infrastructure as Code `iac/cloudformation_template.yaml`, hoàn thiện Chương 8: hướng dẫn quy trình dọn dẹp tài nguyên 1-chạm sau khi nghiệm thu (`aws cloudformation delete-stack`).<br>- Định dạng chuẩn hóa toàn bộ file Báo cáo tổng kết đồ án Master (Word và xuất bản PDF).<br>- Cập nhật nhật ký tuần `docs/worklogs/week-04/member-1.md`. | File Báo cáo Master hoàn chỉnh<br>Quy trình dọn dẹp tài nguyên IaC |
| **TỔNG CỘNG** | | **8.5h** | **Đạt và vượt định mức quy định môn học ($\ge$ 8.0 giờ/tuần)** | **Hoàn thành Master Report** |

---

## 2. KẾT QUẢ ĐẠT ĐƯỢC
1. Soạn thảo các Chương 1, 2, 3, 4, 6, 7, 8 và hợp nhất Chương 5 từ Thành viên 2 để hoàn tất 100% bộ tài liệu Báo cáo tổng kết đồ án Master theo quy chuẩn môn học.
2. Xác nhận chi phí đám mây thực tế duy trì tối ưu ở mức **$0.03** nhờ kiến trúc Serverless, bảo toàn 99.97% ngân sách Lab.
3. Toàn bộ hạ tầng đám mây sẵn sàng cho quy trình dọn dẹp 1-chạm bằng CloudFormation.
