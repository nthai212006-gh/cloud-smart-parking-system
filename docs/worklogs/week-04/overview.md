# TỔNG HỢP NHẬT KÝ TIẾN ĐỘ TUẦN 4 - NHÓM DOMAIN APPS
### HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING) - HỌC KỲ 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm sinh viên thực hiện:**
  1. Lê Cao Việt Tín (MSSV: 24110354) – Thành viên 1
  2. Nguyễn Trung Hải (MSSV: 24110207) – Thành viên 2
* **Đề tài:** Hệ thống Quản lý Bãi giữ xe Thông minh (Smart Parking System)
* **Giai đoạn:** Tuần 4 – Kiểm thử tổng thể, Tối ưu chi phí, Viết báo cáo & Hoàn tất video demo nghiệm thu
* **Thư mục Video Demo (Google Drive):** [Google Drive - DEMO.mp4](https://drive.google.com/drive/folders/1iYy8aeg6JkXlWysBVxFYQMlPEZcbFLb6?usp=drive_link)

---

## 1. BẢNG TỔNG HỢP SỐ GIỜ LÀM VIỆC TUẦN 4

| Thành viên | Trách nhiệm chính Tuần 4 | Số giờ thực hiện | Tỷ lệ đóng góp | Trạng thái hoàn thành |
| :--- | :--- | :---: | :---: | :---: |
| **Lê Cao Việt Tín** (`lcvt438`) | - Xây dựng Báo cáo tổng kết đồ án toàn trình 4 tuần.<br>- Chuẩn hóa sơ đồ kiến trúc Serverless Decoupled.<br>- Báo cáo phân tích chi phí thực tế AWS Billing ($0.03).<br>- Rà soát kịch bản dọn dẹp tài nguyên CloudFormation (IaC). | **8.5 giờ** | 50% | **Đã hoàn thành 100%** |
| **Nguyễn Trung Hải** (`nthai212006-gh`) | - Xây dựng Kịch bản Demo đồng bộ 2 ảnh `car_clear_05.jpg` & `motor_clear_06.jpg`.<br>- Vận hành & kiểm thử toàn diện POS Desktop.<br>- Thực hiện quay và biên tập video demo toàn trình `DEMO.mp4` ($\le$ 10 phút).<br>- Tải video lên Google Drive, kiểm tra phân quyền truy cập. | **8.5 giờ** | 50% | **Đã hoàn thành 100%** |
| **TỔNG CỘNG CẢ NHÓM** | **2 thành viên phối hợp chặt chẽ** | **17.0 giờ** | **100%** | **Đạt và vượt chuẩn môn học** |

---

## 2. BẢNG ĐỐI CHIẾU 3 TIÊU CHÍ BẮT BUỘC TUẦN 4 CỦA GVHD

| STT | Yêu cầu bắt buộc của Thầy Phụng | Kết quả thực hiện của nhóm | Trạng thái nghiệm thu |
|:---:|---|---|:---:|
| 1 | **Video demo toàn trình không quá 10 phút** | Video demo `DEMO.mp4` thời lượng đạt chuẩn $\le$ 10 phút (gồm đầy đủ 8 phân cảnh: Ô tô `car_05`, Xe máy `motor_06`, Rekognition, Chống Double-Checkout, Test tải Throttling, AWS Console). Đã upload lên Google Drive. | **ĐẠT (100%)** |
| 2 | **Báo cáo chi phí AWS** | Toàn bộ hệ thống chạy trên nền tảng Serverless và Free Tier, tổng chi phí phát sinh thực tế xuyên suốt quá trình kiểm thử tải và demo chỉ vỏn vẹn **`$0.03`** (bảo toàn 99.97% hạn mức $100 Lab). | **ĐẠT (100%)** |
| 3 | **Dọn sạch tài nguyên sau khi demo** | Hạ tầng được định nghĩa 100% bằng CloudFormation `iac/cloudformation_template.yaml`, sẵn sàng lệnh `aws cloudformation delete-stack` xóa sạch tài nguyên sau khi chấm điểm. | **ĐẠT (100%)** |

---

## 3. BỘ HỒ SƠ BÀN GIAO NGHIỆM THU ĐỒ ÁN
1. **Kho mã nguồn GitHub:** Đầy đủ commit từ Tuần 1 đến Tuần 4, không có lỗi xung đột, kèm tài liệu hướng dẫn triển khai.
2. **Video Demo toàn trình:** File `DEMO.mp4` ($\le$ 10 phút) lưu trữ tại [Google Drive Folder](https://drive.google.com/drive/folders/1iYy8aeg6JkXlWysBVxFYQMlPEZcbFLb6?usp=drive_link).
3. **Báo cáo tổng kết đồ án:** File Word và PDF trình bày đẹp mắt, đầy đủ sơ đồ kiến trúc, minh chứng chi phí thực tế `$0.03`, bảng kết quả kiểm thử tải và phân tích dữ liệu Athena.
4. **Nhật ký công việc (Worklogs):** Đầy đủ 4 tuần cho cả 2 thành viên trong thư mục `docs/worklogs/`, mỗi tuần đạt tối thiểu 17.0 giờ/nhóm.
