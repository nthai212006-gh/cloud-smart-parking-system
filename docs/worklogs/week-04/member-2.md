# BÁO CÁO NHẬT KÝ CÔNG VIỆC TUẦN 4 - THÀNH VIÊN 2
### HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Sinh viên 2:** Nguyễn Trung Hải (MSSV: 24110207)
* **Nhóm:** Domain Apps
* **Đề tài:** Hệ thống Quản lý Bãi giữ xe Thông minh (Smart Parking System)
* **Giai đoạn:** Tuần 4 – Xây dựng kịch bản, Kiểm thử vận hành, Quay video demo toàn trình & Nghiệm thu đồ án

---

## 1. BẢNG THEO DÕI TIẾN ĐỘ & SỐ GIỜ LÀM VIỆC (8.5 GIỜ)

| Ngày thực hiện | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng bàn giao |
| :---: | :---: | :---: | :--- | :--- |
| **28/10/2026**<br>(Thứ 4) | 19:30 - 21:30 | 2.0h | - Rà soát toàn bộ quy trình kiểm thử hệ thống POS trên môi trường thực tế.<br>- Thử nghiệm kiểm tra độ trễ nhận diện biển số của Amazon Rekognition trên tập ảnh Ô tô và Xe máy.<br>- Lựa chọn 2 ảnh mẫu kiểm thử chính thức: Ô tô (`car_clear_05.jpg`) và Xe máy (`motor_clear_06.jpg`).<br>- Xác thực luồng đối soát hình ảnh CAM 02 đẩy ảnh vào thư mục `out/` trên Amazon S3. | Báo cáo kiểm thử luồng POS<br>Ảnh xe ra lưu vết trên S3 `out/`<br>2 ảnh test `car_05` & `motor_06` |
| **29/10/2026**<br>(Thứ 5) | 19:30 - 21:45 | 2.25h | - Xây dựng bản Kịch bản Demo toàn trình chi tiết (`docs/plans/week-04/KICH_BAN_DEMO_VIDEO.md`) sử dụng 2 ảnh `car_clear_05.jpg` và `motor_clear_06.jpg`.<br>- Soạn thảo lời thoại thuyết minh đồng bộ theo từng giây thao tác ("Tay làm đâu - Miệng nói đó").<br>- Phân bổ khung thời lượng chuẩn: 8 phân cảnh chính, khống chế tổng thời gian $\le$ 10 phút. | File `docs/plans/week-04/KICH_BAN_DEMO_VIDEO.md`<br>Kịch bản phân cảnh chi tiết |
| **30/10/2026**<br>(Thứ 6) | 14:00 - 16:15 | 2.25h | - Thiết lập môi trường ghi hình chuẩn: OBS Studio 1080p 60fps, micro lọc ồn.<br>- Vận hành toàn bộ 8 phân cảnh: Ô tô `car_clear_05.jpg`, Xe máy `motor_clear_06.jpg`, Chống Double-Checkout (HTTP 400), Test tải Throttling (HTTP 429), Show AWS Console (DynamoDB items, S3 folders, Athena SQL 1.124.000đ, CloudWatch Alarms `OK`, Billing `$0.03`).<br>- Hoàn tất quay video demo toàn trình chính thức `DEMO.mp4` với thời lượng đạt chuẩn $\le$ 10 phút. | File video `DEMO.mp4`<br>Minh chứng Billing `$0.03` |
| **31/10/2026**<br>(Thứ 7) | 19:30 - 21:30 | 2.0h | - Tải video `DEMO.mp4` lên Google Drive tại thư mục: [Google Drive - DEMO.mp4](https://drive.google.com/drive/folders/1iYy8aeg6JkXlWysBVxFYQMlPEZcbFLb6?usp=drive_link).<br>- Thiết lập mở quyền truy cập công khai (Anyone with link can view).<br>- Phối hợp với Thành viên 1 hoàn tất bộ hồ sơ nộp bài nghiệm thu cuối kỳ. | Link Google Drive video demo<br>Worklog Tuần 4 hoàn tất |
| **TỔNG CỘNG** | | **8.5h** | **Đạt và vượt định mức quy định môn học ($\ge$ 8.0 giờ/tuần)** | **Hoàn tất 100% video demo** |

---

## 2. KẾT QUẢ ĐẠT ĐƯỢC
1. Hoàn thành 100% video demo toàn trình `DEMO.mp4` chất lượng cao, thời lượng chuẩn $\le$ 10 phút, đã tải lên Google Drive.
2. Thể hiện trọn vẹn các điểm sáng kỹ thuật Thầy yêu cầu: Rekognition AI (với `car_clear_05.jpg` & `motor_clear_06.jpg`), S3, DynamoDB Atomic Write, Athena, CloudWatch Alarms OK, Billing $0.03 tối ưu, IaC CloudFormation.
3. Đáp ứng đầy đủ quy định môn học về khối lượng công việc và báo cáo tiến độ.
