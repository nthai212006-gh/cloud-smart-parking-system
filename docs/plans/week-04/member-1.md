# KẾ HOẠCH CHI TIẾT TUẦN 4 - SINH VIÊN 1 (MEMBER 1)
### VAI TRÒ: PHỤ TRÁCH BÁO CÁO TỔNG KẾT, KIẾN TRÚC SERVERLESS, KIỂM TOÁN CHI PHÍ & TỰ ĐỘNG HÓA DỌN DẸP
* **Thành viên:** Lê Cao Việt Tín
* **Mã số sinh viên (MSSV):** 24110354
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm đề tài:** Domain Apps
* **Thời gian thực hiện Tuần 4:** **28/10/2026 – 02/11/2026**
* **Tổng thời gian phân bổ:** **8.5 giờ** (Quy định môn học: $\ge$ 8.0 giờ)

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN 4
1. **Tinh chỉnh hoàn thiện giao diện Desktop POS:**
   - Chuẩn hóa layout 5 tầng đối xứng giữa Làn 1 (Vào) và Làn 2 (Ra) trên `frontend/index.html` và `style.css`.
   - Khóa cứng kích thước tầng hiển thị thông tin và điều khiển barie để triệt tiêu hiện tượng giật cục layout (Cumulative Layout Shift - CLS).
   - Loại bỏ các khung nét đứt giữ chỗ thừa, đảm bảo giao diện POS sạch sẽ, trực quan cho buổi quay demo.
2. **Xây dựng Báo cáo tổng kết đồ án toàn trình (Word & PDF):**
   - Soạn thảo tài liệu báo cáo tổng kết hoàn chỉnh 5 chương theo chuẩn học thuật.
   - Hoàn thiện sơ đồ kiến trúc Serverless Decoupled độ nét cao, thể hiện rõ luồng dữ liệu hai chiều giữa POS, API Gateway, Lambda, Rekognition, S3, DynamoDB, CloudWatch và Athena.
   - Thuyết minh chi tiết các giải pháp kỹ thuật nâng cao: Xử lý Race Condition với DynamoDB Atomic Conditional Write, Giới hạn tần suất gọi API Gateway Throttling.
3. **Lập Báo cáo kiểm toán chi phí thực tế (AWS Billing & Cost Management):**
   - Phân tích chi phí thực tế phát sinh trên tài khoản AWS Learner Lab: **`$0.03`** (CloudWatch $0.02, Rekognition $0.01 do kiểm thử tải và demo nhiều lượt).
   - Chứng minh kiến trúc Serverless giúp tiết kiệm chi phí tối đa, bảo toàn 99.97% hạn mức $100 của tài khoản Lab.
4. **Xây dựng kịch bản dọn dẹp tài nguyên (Resource Cleanup Guide):**
   - Rà soát file CloudFormation `iac/cloudformation_template.yaml`.
   - Soạn thảo quy trình dọn dẹp tài nguyên 1-chạm (`aws cloudformation delete-stack`) để thực hiện ngay sau khi bảo vệ đồ án, đáp ứng đúng yêu cầu bắt buộc thứ 3 của GVHD.

---

## II. ĐỐI CHIẾU KẾT QUẢ KẾ THỪA TỪ TUẦN 3
* **Điểm kế thừa từ Tuần 3:**
  - Nhóm đã được GVHD ThS. Huỳnh Xuân Phụng phê duyệt với kết quả **"ĐÃ DUYỆT"**.
  - Đã có đầy đủ mã nguồn Lambda, DynamoDB Atomic Write, CloudFormation IaC, CloudWatch Alarms và Athena queries từ Tuần 3.
  - Giao diện POS đã kết nối thông suốt với API Gateway.
* **Nhiệm vụ trọng tâm cần hoàn thành trong Tuần 4:**
  - Tập trung 100% nguồn lực hoàn thiện bản Báo cáo tổng kết đồ án chuyên nghiệp, chỉn chu để nộp cùng Video Demo.
  - Cập nhật số liệu chi phí thực tế `$0.03` và các minh chứng hệ thống mới nhất vào tài liệu báo cáo.

---

## III. LỊCH TRÌNH THỰC HIỆN CHI TIẾT (4 BUỔI - TỔNG 8.5 GIỜ)

### Buổi 1 (Thứ 4: 28/10/2026 | 19:30 - 21:30 | 2.0 giờ): Tinh chỉnh giao diện POS Desktop
* **Mục tiêu:** Tối ưu hóa giao diện POS phục vụ trực tiếp cho việc quay video demo của Thành viên 2.
* **Nhiệm vụ cụ thể:**
  - Cập nhật `frontend/index.html` và `frontend/style.css`:
    + Cố định kích thước Tầng 3 (48px) và Tầng 4 (44px) đối xứng giữa 2 làn xe.
    + Loại bỏ các khung nét đứt standby rườm rà.
    + Kiểm tra tính toàn vẹn của 45 DOM element IDs được điều khiển bởi `frontend/app.js`.
  - Thực hiện commit lên Git: Commit `f90a317` và `986cf0c`.
* **Sản phẩm:** Giao diện POS phẳng, hiện đại, không bị xô lệch layout khi nhận diện biển số.

---

### Buổi 2 (Thứ 5: 29/10/2026 | 19:30 - 21:45 | 2.25 giờ): Xây dựng khung Báo cáo & Sơ đồ kiến trúc
* **Mục tiêu:** Khởi tạo tài liệu báo cáo và hoàn thiện sơ đồ kiến trúc hệ thống.
* **Nhiệm vụ cụ thể:**
  - Tạo cấu trúc file Báo cáo đồ án tổng kết: Bìa, Mục lục, Lời mở đầu, Danh mục hình ảnh/bảng biểu.
  - Thiết kế sơ đồ kiến trúc AWS Serverless Decoupled độ phân giải cao:
    + Thể hiện rõ các thành phần: POS Frontend $\rightarrow$ REST API Gateway $\rightarrow$ AWS Lambda $\rightarrow$ Amazon Rekognition / Amazon S3 / Amazon DynamoDB $\rightarrow$ CloudWatch Logs Insights / Amazon Athena.
  - Soạn thảo Chương 1 (Tổng quan đề tài & Yêu cầu bài toán), Chương 2 (Cơ sở lý thuyết dịch vụ AWS) và Chương 3 (Thiết kế kiến trúc & Luồng xử lý dữ liệu).
* **Sản phẩm:** Bản thảo Báo cáo chương 1, 2, 3 và file sơ đồ kiến trúc chuẩn SVG/PNG.

---

### Buổi 3 (Thứ 6: 30/10/2026 | 14:00 - 16:15 | 2.25 giờ): Soạn thảo chương Kỹ thuật chuyên sâu & Báo cáo Chi phí
* **Mục tiêu:** Trình bày chi tiết các cơ chế kỹ thuật xuất sắc và báo cáo tài chính AWS.
* **Nhiệm vụ cụ thể:**
  - Soạn thảo Chương 4: *"Kiểm thử an toàn, Xử lý Race Condition & Giới hạn tải"*:
    + Giải thích cơ chế DynamoDB Atomic Conditional Write (`ConditionExpression="#st = :parked OR #st = :active"`).
    + Phân tích cơ chế chống DDoS/Spam qua API Gateway Throttling (Rate: 10 req/s, Burst: 20 req).
  - Soạn thảo Chương 5: *"Kiểm toán chi phí & Đánh giá hiệu năng"*:
    + Trích xuất dữ liệu từ AWS Billing & Cost Management: Month-to-date cost = **`$0.03`** (CloudWatch $0.02, Rekognition $0.01).
    + Phân tích hiệu quả kinh tế so với mô hình máy chủ truyền thống (EC2).
* **Sản phẩm:** Nội dung Chương 4, 5 hoàn chỉnh kèm biểu đồ phân tích chi phí.

---

### Buổi 4 (Thứ 7: 31/10/2026 | 19:30 - 21:30 | 2.0 giờ): Hướng dẫn dọn dẹp IaC & Xuất bản Báo cáo
* **Mục tiêu:** Hoàn thiện bản báo cáo cuối cùng và quy trình dọn dẹp tài nguyên.
* **Nhiệm vụ cụ thể:**
  - Soạn thảo phần phụ lục: *"Quy trình dọn dẹp và hủy tài nguyên 1-chạm qua AWS CloudFormation"*:
    + Lệnh xóa stack: `aws cloudformation delete-stack --stack-name SmartParkingStack`.
    + Lệnh làm rỗng bucket S3: `aws s3 rm s3://smart-parking-images-24110207 --recursive`.
  - Soát lỗi chính tả, căn chỉnh định dạng tài liệu theo chuẩn đồ án (Font Times New Roman, dãn dòng 1.3, lề chuẩn).
  - Xuất bản file Báo cáo định dạng Word (.docx) và PDF (.pdf).
  - Cập nhật nhật ký tuần `docs/worklogs/week-04/member-1.md`.
* **Sản phẩm:** File Báo cáo tổng kết đồ án hoàn chỉnh sẵn sàng nộp bài.

---

## IV. BẢNG TỔNG HỢP KẾ HOẠCH BÀN GIAO CỦA SINH VIÊN 1

| Hạng mục công việc | Khung thời gian | Thời lượng | Sản phẩm bàn giao cụ thể | Trạng thái |
| :--- | :---: | :---: | :--- | :---: |
| Tinh chỉnh POS đối xứng & clean layout | 28/10/2026 | 2.0h | Commit `f90a317`, `986cf0c` trên Git | Đã hoàn thành |
| Soạn thảo Báo cáo chương 1, 2, 3 & Kiến trúc | 29/10/2026 | 2.25h | Bản thảo Báo cáo và Sơ đồ kiến trúc | Đã hoàn thành |
| Soạn thảo Báo cáo chương 4, 5 & Chi phí $0.03 | 30/10/2026 | 2.25h | Chương kỹ thuật và Báo cáo chi phí $0.03 | Đã hoàn thành |
| Hoàn thiện Báo cáo Word/PDF & Hướng dẫn IaC | 31/10/2026 | 2.0h | File Báo cáo đồ án chính thức (.pdf) | Đang thực hiện |
| **TỔNG CỘNG** | | **8.5h** | **Đạt và vượt chuẩn quy định môn học ($\ge$ 8.0h)** | **Sẵn sàng nghiệm thu** |
