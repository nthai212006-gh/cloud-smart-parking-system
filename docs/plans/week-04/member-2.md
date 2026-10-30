# KẾ HOẠCH CHI TIẾT TUẦN 4 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: PHỤ TRÁCH VẬN HÀNH KIỂM THỬ POS, QUAY DỰNG VIDEO DEMO TOÀN TRÌNH & NGHIỆM THU ĐỒ ÁN
* **Thành viên:** Nguyễn Trung Hải
* **Mã số sinh viên (MSSV):** 24110207
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm đề tài:** Domain Apps
* **Thời gian thực hiện Tuần 4:** **28/10/2026 – 02/11/2026**
* **Tổng thời gian phân bổ:** **8.5 giờ** (Quy định môn học: $\ge$ 8.0 giờ)

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN 4
1. **Kiểm thử vận hành thực tế hệ thống POS Desktop:**
   - Khởi chạy máy chủ web cục bộ (`python -m http.server 8000 --directory frontend`) để kiểm tra toàn bộ tính năng giao diện POS 5 tầng mới.
   - Thử nghiệm nhận diện biển số thực tế qua Amazon Rekognition trên tập ảnh mẫu; lựa chọn 2 ảnh đại diện chính thức: **Ô tô (`car_clear_05.jpg`)** và **Xe máy (`motor_clear_06.jpg`)**.
   - Xác thực luồng đối soát CAM 02: Ảnh xe ra khi thanh toán được tải lên và lưu trữ chính xác tại thư mục `out/` trên Amazon S3.
2. **Chuẩn bị và phân bổ thời lượng kịch bản Demo:**
   - Xây dựng trình tự các phân cảnh demo logic, mượt mà ("Tay làm đâu - Thuyết minh đó").
   - Khống chế nghiêm ngặt tổng thời lượng demo không vượt quá **10 phút** theo đúng yêu cầu bắt buộc của GVHD ThS. Huỳnh Xuân Phụng.
   - Chuẩn bị sẵn dữ liệu kiểm thử, các tab điều khiển AWS Console và tài nguyên liên quan.
3. **Thực hiện quay và biên tập Video Demo toàn trình (`DEMO.mp4`):**
   - Thiết lập phần mềm ghi hình chất lượng Full HD 1080p, âm thanh rõ ràng.
   - Thực hiện ghi hình toàn bộ luồng nghiệp vụ thực tế:
     * Check-in ô tô Làn 1 (`car_clear_05.jpg` - `52Z-9755`).
     * Check-in xe máy Làn 1 (`motor_clear_06.jpg` - `54N6-4172`).
     * Check-out xe máy Làn 2: Đối soát hình ảnh vào/ra, thu cước 5.000 VNĐ, barie mở.
     * Cơ chế chống Double-Checkout & Test tải API Gateway Throttling (HTTP 429).
     * Minh chứng trực tiếp trên AWS Console: DynamoDB (`ParkingTickets`), Athena SQL, S3 folders, CloudWatch Alarms (trạng thái `OK` xanh lá), AWS Billing (`$0.03`).
     * Mở file CloudFormation `cloudformation_template.yaml` chứng minh giải pháp tự động hóa dọn dẹp.
4. **Lưu trữ đám mây & Đồng bộ hồ sơ nộp bài:**
   - Tải video `DEMO.mp4` lên Google Drive tại thư mục chia sẻ công khai.
   - Cập nhật nhật ký tuần `docs/worklogs/week-04/member-2.md` và phối hợp với Thành viên 1 hoàn tất bộ tài liệu nghiệm thu.

---

## II. ĐỐI CHIẾU KẾT QUẢ KẾ THỪA TỪ TUẦN 3
* **Điểm kế thừa từ Tuần 3:**
  - Hệ thống hạ tầng AWS đã vận hành ổn định trên tài khoản Lab (`us-east-1`).
  - Đã có dữ liệu 50 vé xe thật và 5 câu truy vấn SQL phân tích doanh thu trên Amazon Athena.
  - 2 CloudWatch Alarms đã cấu hình và chuyển trạng thái `OK` xanh lá.
* **Nhiệm vụ trọng tâm cần hoàn thành trong Tuần 4:**
  - Chuyển giao toàn bộ kết quả kỹ thuật của nhóm thành sản phẩm Video Demo trực quan, chuyên nghiệp.
  - Đảm bảo video không vượt quá 10 phút, thể hiện đầy đủ các minh chứng số liệu thực tế theo đúng yêu cầu nghiệm thu của Thầy.

---

## III. LỊCH TRÌNH THỰC HIỆN CHI TIẾT (4 BUỔI - TỔNG 8.5 GIỜ)

### Buổi 1 (Thứ 4: 28/10/2026 | 19:30 - 21:30 | 2.0 giờ): Kiểm thử vận hành POS & Lựa chọn ảnh mẫu
* **Mục tiêu:** Kiểm tra độ ổn định của POS Desktop và chọn bộ ảnh test chính thức.
* **Nhiệm vụ cụ thể:**
  - Khởi chạy frontend cục bộ tại cổng 8000.
  - Thực hiện kiểm thử nhận diện biển số với nhiều góc chụp trong thư mục `test-images/`.
  - Chọn 2 ảnh thử nghiệm chính thức có độ rõ nét cao, thể hiện rõ 2 phân khúc xe:
    + Ô tô: `test-images/01_car_clear/car_clear_05.jpg` (Biển số: `52Z-9755`).
    + Xe máy: `test-images/02_motor_clear/motor_clear_06.jpg` (Biển số: `54N6-4172`).
  - Kiểm tra API `/checkout` xác thực luồng tải ảnh xe ra lên S3 thư mục `out/`.
* **Sản phẩm:** Môi trường POS hoàn chỉnh, 2 ảnh test sẵn sàng cho buổi ghi hình.

---

### Buổi 2 (Thứ 5: 29/10/2026 | 19:30 - 21:45 | 2.25 giờ): Thiết kế phân cảnh Demo & Chuẩn bị môi trường
* **Mục tiêu:** Xây dựng trình tự các phân cảnh demo, khống chế thời lượng $\le$ 10 phút.
* **Nhiệm vụ cụ thể:**
  - Thiết kế cấu trúc các phân cảnh demo:
    + Phân cảnh 1: Giới thiệu kiến trúc hệ thống và giao diện POS 5 tầng (khoảng 1 phút).
    + Phân cảnh 2: Check-in xe ô tô tại Làn 1 với `car_clear_05.jpg` (khoảng 1 phút).
    + Phân cảnh 3: Check-in xe máy tại Làn 1 với `motor_clear_06.jpg` (khoảng 1 phút).
    + Phân cảnh 4: Check-out và đối soát xe máy tại Làn 2 (khoảng 1.5 phút).
    + Phân cảnh 5: Kiểm thử an toàn (Chống Double-Checkout & API Throttling) (khoảng 1.5 phút).
    + Phân cảnh 6: Trình bày minh chứng AWS Console (DynamoDB, Athena, S3, CloudWatch Alarms, Billing $0.03) (khoảng 2.5 phút).
    + Phân cảnh 7: Giới thiệu mã nguồn CloudFormation IaC và kết thúc (khoảng 30 giây).
  - Mở sẵn các tab trên trình duyệt theo thứ tự kịch bản để tránh thao tác thừa khi quay.
* **Sản phẩm:** Bảng phân cảnh và thời lượng chuẩn bị cho buổi ghi hình.

---

### Buổi 3 (Thứ 6: 30/10/2026 | 14:00 - 16:15 | 2.25 giờ): Quay và hoàn thiện Video Demo toàn trình
* **Mục tiêu:** Sản xuất video demo `DEMO.mp4` đạt chuẩn chất lượng Full HD, thời lượng $\le$ 10 phút.
* **Nhiệm vụ cụ thể:**
  - Cài đặt phần mềm quay màn hình ở độ phân giải 1920x1080 (30 FPS).
  - Tiến hành ghi hình xuyên suốt toàn bộ các phân cảnh đã thiết kế.
  - Thao tác mượt mà giữa giao diện POS và các màn hình console dịch vụ AWS.
  - Xác nhận thời lượng video đạt chuẩn: **9 phút 16 giây** ($\le 10$ phút).
  - Kiểm tra chất lượng âm thanh, hình ảnh sau khi xuất file `DEMO.mp4`.
* **Sản phẩm:** File video `DEMO.mp4` hoàn chỉnh, đạt 100% tiêu chí môn học.

---

### Buổi 4 (Thứ 7: 31/10/2026 | 19:30 - 21:30 | 2.0 giờ): Upload Google Drive & Nghiệm thu
* **Mục tiêu:** Lưu trữ video lên đám mây và hoàn thiện nhật ký công việc.
* **Nhiệm vụ cụ thể:**
  - Tải file `DEMO.mp4` lên thư mục Google Drive: [Google Drive - DEMO.mp4](https://drive.google.com/drive/folders/1iYy8aeg6JkXlWysBVxFYQMlPEZcbFLb6?usp=drive_link).
  - Bật tính năng chia sẻ quyền xem công khai (*Anyone with the link can view*).
  - Cập nhật nhật ký tuần `docs/worklogs/week-04/member-2.md`.
  - Phối hợp cùng Thành viên 1 rà soát toàn bộ hồ sơ nghiệm thu trước khi nộp bài.
* **Sản phẩm:** Link Google Drive video demo công khai, nhật ký tuần 4 hoàn tất.

---

## IV. BẢNG TỔNG HỢP KẾ HOẠCH BÀN GIAO CỦA SINH VIÊN 2

| Hạng mục công việc | Khung thời gian | Thời lượng | Sản phẩm bàn giao cụ thể | Trạng thái |
| :--- | :---: | :---: | :--- | :---: |
| Kiểm thử luồng POS với car_05 & motor_06 | 28/10/2026 | 2.0h | Bộ ảnh test & luồng S3 `out/` sẵn sàng | Đã hoàn thành |
| Chuẩn bị dữ liệu demo & phân cảnh | 29/10/2026 | 2.25h | Bảng phân cảnh và các tab AWS Console | Đã hoàn thành |
| Quay video DEMO.mp4 & verify Billing $0.03 | 30/10/2026 | 2.25h | Video `DEMO.mp4` (9 phút 16 giây) | Đã hoàn thành |
| Upload Google Drive & hoàn tất nghiệm thu | 31/10/2026 | 2.0h | Link Google Drive công khai & Worklog | Đang thực hiện |
| **TỔNG CỘNG** | | **8.5h** | **Đạt và vượt chuẩn quy định môn học ($\ge$ 8.0h)** | **Sẵn sàng nghiệm thu** |
