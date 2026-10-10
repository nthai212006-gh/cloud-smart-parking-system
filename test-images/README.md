# BỘ DỮ LIỆU THỬ NGHIỆM BIỂN SỐ XE (TEST DATASET)
### ĐỀ TÀI: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING)
* **Phụ trách:** Sinh viên 2 (Nguyễn Trung Hải - 24110207)
* **Quy chuẩn:** Bảo mật thông tin cá nhân (PII Privacy - 100% không để lộ khuôn mặt người)
* **Tổng số lượng:** **120 ảnh**

---

## 1. BẢNG PHÂN LOẠI CHI TIẾT SỐ LƯỢNG ẢNH

| STT | Nhóm ảnh | Thư mục lưu trữ | Số lượng | Mục đích thử nghiệm |
| :---: | :--- | :--- | :---: | :--- |
| 1 | **Ô tô — biển số rõ** | `01_car_clear/` | **40 ảnh** | Kiểm tra nhận diện cơ bản (Amazon Rekognition OCR) cho phương tiện ô tô. |
| 2 | **Xe máy — biển số rõ** | `02_motor_clear/` | **40 ảnh** | Kiểm tra nhận diện biển số 2 dòng xe máy và thuật toán Regex ghép chuỗi. |
| 3 | **Ô tô — điều kiện khó** | `03_car_hard/` | **10 ảnh** | Góc nghiêng, khoảng cách xa, điều kiện thiếu sáng ban đêm. |
| 4 | **Xe máy — điều kiện khó** | `04_motor_hard/` | **10 ảnh** | Biển số nhỏ, góc nghiêng $45^\circ$, thiếu sáng, bóng râm. |
| 5 | **Không biển số / Khó đọc** | `05_error_cases/` | **20 ảnh** | Kiểm tra hệ thống xử lý trường hợp ngoại lệ (gán cờ `UNKNOWN` để bảo vệ nhập tay). |
| **Tổng** | **Toàn bộ Dataset** | | **120 ảnh** | **Đầy đủ 100% các kịch bản kiểm thử** |

---

## 2. NGUỒN DỮ LIỆU (DATA SOURCES)
1. **Ảnh chụp thực tế của nhóm (HCMUTE & đường phố):**
   - Đã được làm mờ/che mặt người và thông tin nhạy cảm.
   - Được phân bổ vào các nhóm `01_car_clear/`, `02_motor_clear/`, và `04_motor_hard/`.
2. **Bộ dữ liệu chuẩn biển số Việt Nam (Vietnamese License Plate Dataset):**
   - Được lọc và tuyển chọn từ bộ ảnh biển số xe cơ giới thực tế tại Việt Nam.
   - Đã tối ưu hóa kích thước (dung lượng trung bình 30KB - 80KB/ảnh), tương thích hoàn toàn với AWS Lambda và API Gateway payload limit.

---

## 3. CẤU TRÚC THƯ MỤC
```text
test-images/
├── 01_car_clear/          # 40 ảnh: car_clear_01.jpg -> car_clear_40.jpg
├── 02_motor_clear/        # 40 ảnh: motor_clear_01.jpg -> motor_clear_40.jpg
├── 03_car_hard/           # 10 ảnh: car_hard_01.jpg -> car_hard_10.jpg
├── 04_motor_hard/         # 10 ảnh: motor_hard_01.jpg -> motor_hard_10.jpg
├── 05_error_cases/        # 20 ảnh: error_case_01.jpg -> error_case_20.jpg
└── README.md
```
