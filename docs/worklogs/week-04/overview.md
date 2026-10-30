# TỔNG HỢP NHẬT KÝ TIẾN ĐỘ TUẦN 4 - NHÓM DOMAIN APPS
### HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING) - HỌC KỲ 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm sinh viên thực hiện:**
  1. Lê Cao Việt Tín (MSSV: 24110354) – Thành viên 1
  2. Nguyễn Trung Hải (MSSV: 24110207) – Thành viên 2
* **Đề tài:** Hệ thống Quản lý Bãi giữ xe Thông minh (Smart Parking System)
* **Giai đoạn:** Tuần 4 – Kiểm thử tổng thể, Tối ưu chi phí, Viết báo cáo & Hoàn tất video demo nghiệm thu

---

## 1. BẢNG TỔNG HỢP SỐ GIỜ LÀM VIỆC TUẦN 4

| Thành viên | Trách nhiệm chính Tuần 4 | Số giờ thực hiện | Tỷ lệ đóng góp | Trạng thái hoàn thành |
| :--- | :--- | :---: | :---: | :---: |
| **Lê Cao Việt Tín** (`lcvt438`) | - Xây dựng Báo cáo tổng kết đồ án toàn trình 4 tuần.<br>- Chuẩn hóa sơ đồ kiến trúc Serverless Decoupled.<br>- Báo cáo tối ưu chi phí AWS Billing ($0.00).<br>- Rà soát kịch bản dọn dẹp tài nguyên CloudFormation (IaC). | **8.5 giờ** | 50% | **Đã hoàn thành 100%** |
| **Nguyễn Trung Hải** (`nthai212006-gh`) | - Xây dựng bản Kịch bản Demo đồng bộ thao tác & lời thoại.<br>- Kiểm thử toàn diện luồng vận hành POS Desktop.<br>- Thực hiện quay và biên tập video demo toàn trình ($\le$ 10 phút).<br>- Tải video lên Drive/YouTube, kiểm tra phân quyền truy cập. | **8.5 giờ** | 50% | **Đã hoàn thành 100%** |
| **TỔNG CỘNG CẢ NHÓM** | **2 thành viên phối hợp chặt chẽ** | **17.0 giờ** | **100%** | **Đạt và vượt chuẩn môn học** |

---

## 2. BẢNG ĐỐI CHIẾU 3 TIÊU CHÍ BẮT BUỘC TUẦN 4 CỦA GVHD

| STT | Yêu cầu bắt buộc của Thầy Phụng | Kết quả thực hiện của nhóm | Trạng thái nghiệm thu |
|:---:|---|---|:---:|
| 1 | **Video demo toàn trình không quá 10 phút** | Video demo hoàn chỉnh ~8 phút (gồm đầy đủ 8 phân cảnh: Ô tô, Xe máy, Rekognition, Chống Double-Checkout, Test tải Throttling, AWS Console). | **ĐẠT (100%)** |
| 2 | **Báo cáo chi phí AWS ($0.00)** | Toàn bộ hệ thống chạy trên nền tảng Serverless và Free Tier, xác nhận trên AWS Billing Month-to-date duy trì an toàn `$0.00`. | **ĐẠT (100%)** |
| 3 | **Dọn sạch tài nguyên sau khi demo** | Hạ tầng được định nghĩa 100% bằng CloudFormation `iac/cloudformation_template.yaml`, sẵn sàng lệnh `aws cloudformation delete-stack` xóa sạch tài nguyên sau khi chấm điểm. | **ĐẠT (100%)** |

---

## 3. BỘ HỒ SƠ BÀN GIAO NGHIỆM THU ĐỒ ÁN
1. **Mã nguồn đầy đủ trên GitHub:** Bao gồm Backend (Lambda Python), Frontend (Desktop POS), IaC (CloudFormation), Scripts (Test Throttling, Athena SQL).
2. **Video demo toàn trình ($\le$ 10 phút):** Kèm link Drive / YouTube không công khai.
3. **Báo cáo tổng kết đồ án:** Định dạng Word/PDF kèm ảnh minh chứng thực tế trên AWS Console.
4. **Nhật ký làm việc (Worklogs):** Đầy đủ 4 tuần cho cả 2 thành viên, mỗi tuần $\ge$ 17.0 giờ/nhóm.
