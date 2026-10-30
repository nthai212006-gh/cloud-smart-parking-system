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
| **28/10/2026**<br>(Thứ 4) | 19:30 - 21:30 | 2.0h | - Rà soát toàn bộ quy trình kiểm thử hệ thống POS trên môi trường thực tế.<br>- Thử nghiệm kiểm tra độ trễ nhận diện biển số của Amazon Rekognition trên tập ảnh Ô tô và Xe máy.<br>- Xác thực luồng đối soát hình ảnh CAM 02 đẩy ảnh vào thư mục `out/` trên Amazon S3. | Báo cáo kiểm thử luồng POS<br>Ảnh xe ra lưu vết trên S3 `out/` |
| **29/10/2026**<br>(Thứ 5) | 19:30 - 21:45 | 2.25h | - Xây dựng bản Kịch bản Demo toàn trình chi tiết (`docs/plans/week-04/KICH_BAN_DEMO_VIDEO.md`).<br>- Soạn thảo lời thoại thuyết minh đồng bộ theo từng giây thao tác ("Tay làm đâu - Miệng nói đó").<br>- Phân bổ khung thời lượng chuẩn: 8 phân cảnh chính, khống chế tổng thời gian $\le$ 10 phút. | File `docs/plans/week-04/KICH_BAN_DEMO_VIDEO.md`<br>Kịch bản phân cảnh chi tiết |
| **30/10/2026**<br>(Thứ 6) | 14:00 - 16:15 | 2.25h | - Thiết lập môi trường ghi hình chuẩn: OBS Studio 1080p 60fps, micro lọc ồn.<br>- Chạy thử nghiệm toàn bộ 8 phân cảnh: Ô tô vào/ra, Xe máy vào/ra, Chống Double-Checkout (HTTP 400), Test tải Throttling (HTTP 429), Show AWS Console (DynamoDB, S3, Athena, CloudWatch Alarms, Billing $0.00).<br>- Tinh chỉnh thời lượng video dừng chuẩn xác ở mốc ~8 phút. | Bản ghi thử nghiệm video demo<br>Thời lượng đạt chuẩn 8 phút |
| **31/10/2026**<br>(Thứ 7) | 19:30 - 21:30 | 2.0h | - Thực hiện quay video demo toàn trình chính thức với âm thanh rõ ràng, thao tác dứt khoát.<br>- Biên tập video, xuất file định dạng MP4 chất lượng cao (1080p).<br>- Tải video lên Google Drive/YouTube chế độ Unlisted và kiểm tra phân quyền truy cập.<br>- Phối hợp với Thành viên 1 hoàn tất bộ hồ sơ nộp bài nghiệm thu cuối kỳ. | File Video Demo hoàn chỉnh ($\le$ 10 phút)<br>Link Google Drive / YouTube |
| **TỔNG CỘNG** | | **8.5h** | **Đạt và vượt định mức quy định môn học ($\ge$ 8.0 giờ/tuần)** | **Hoàn tất 100% video demo** |

---

## 2. KẾT QUẢ ĐẠT ĐƯỢC
1. Hoàn thành 100% video demo toàn trình chất lượng cao, thời lượng chuẩn $\le$ 10 phút.
2. Thể hiện trọn vẹn các điểm sáng kỹ thuật Thầy yêu cầu: Rekognition AI, S3, DynamoDB Atomic Write, Athena, CloudWatch Alarms OK, Billing $0.00, IaC CloudFormation.
3. Đáp ứng đầy đủ quy định môn học về khối lượng công việc và báo cáo tiến độ.
