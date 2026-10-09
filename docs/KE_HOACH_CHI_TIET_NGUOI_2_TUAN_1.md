# KẾ HOẠCH CHI TIẾT & HƯỚNG DẪN THỰC HIỆN TUẦN 1 (DÀNH CHO NGƯỜI 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, QUẢN TRỊ DỮ LIỆU & ĐẢM BẢO CHẤT LƯỢNG (DEVOPS / QA)
* **Học phần:** Điện toán đám mây (Cloud Computing) - Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** Thầy Huỳnh Xuân Phụng
* **Nhánh Git thực hiện:** `dev`
* **Mục tiêu thời gian:** Tối thiểu 8.0 giờ (Dự kiến: **8.5 giờ**)

---

## 🎯 MỤC TIÊU NGHIỆM THU TUẦN 1 CỦA NGƯỜI 2
1. **Hạ tầng AWS sẵn sàng:** Có 1 S3 Bucket (3 folders `in/`, `out/`, `athena-logs/`) và 1 DynamoDB Table `ParkingTickets` (PK `ticketId`, On-Demand mode), gắn đúng 3 thẻ Tag chuẩn.
2. **Bộ Dataset chuẩn bị xong:** 15–20 ảnh biển số thực tế trong thư mục `test-images/`, **100% ảnh đã che mờ khuôn mặt người và thông tin nhạy cảm**.
3. **Bộ ảnh minh chứng hoàn chỉnh:** 4 ảnh chụp màn hình trong `evidence/week1/` đạt tiêu chuẩn (rõ Account ID, Region `us-east-1`, đồng hồ máy tính).
4. **Hồ sơ minh bạch:** Điền đầy đủ thông tin cá nhân vào `NHAT_KY_CONG_VIEC_TUAN_1.md` và push toàn bộ lên nhánh `dev`.

---

## 📋 CHI TIẾT TỪNG NHIỆM VỤ CỤ THỂ

### TASK 1: Khảo sát AWS Learner Lab & Kiểm tra quyền IAM (Thời lượng: 2.5 giờ)
* **Mục đích:** Đảm bảo hiểu rõ môi trường AWS của trường, tránh vi phạm chính sách dẫn đến bị khóa tài khoản hoặc lỗi phân quyền.
* **Các bước thực hiện:**
  1. Đăng nhập hệ thống Canvas / AWS Academy $\rightarrow$ Vào lớp học $\rightarrow$ Chọn **AWS Learner Lab**.
  2. Bấm nút **Start Lab** $\rightarrow$ Đợi biểu tượng AWS chuyển từ màu đỏ sang màu xanh lá cây.
  3. Bấm vào chữ **AWS** kế bên nút Start Lab để mở AWS Management Console trong tab mới.
  4. **Kiểm tra Region:** Nhìn lên góc trên cùng bên phải, bấm vào tên Region và chọn đúng **`US East (N. Virginia) us-east-1`**. Tuyệt đối không chọn Region khác (như `ap-southeast-1` hay `us-west-2`) vì Learner Lab giới hạn dịch vụ ở `us-east-1`.
  5. **Kiểm tra IAM Role bắt buộc:**
     - Tìm kiếm dịch vụ `IAM` trên thanh tìm kiếm.
     - Vào menu **Roles** bên trái $\rightarrow$ Gõ tìm kiếm `LabRole`.
     - Nhấp vào `LabRole`, copy lại chuỗi ARN: `arn:aws:iam::<ACCOUNT_ID>:role/LabRole`.
     - *Lưu ý sống còn:* AWS Learner Lab không cho phép học viên tự tạo IAM Role/Policy mới (`iam:CreateRole` bị cấm). Tất cả các dịch vụ (Lambda, API Gateway, EventBridge...) sau này đều phải gán chung role `LabRole` này.
  6. **Đọc tài liệu quy chuẩn:**
     - Xem file [docs/QUY_CHUAN_TAGGING.md](QUY_CHUAN_TAGGING.md) để nắm rõ cách đặt tên và 3 tag bắt buộc:
       - `Project`: `SmartParking`
       - `Owner`: `<MSSV_SV1>_<MSSV_SV2>`
       - `Environment`: `Development`

---

### TASK 2: Thu thập và Xử lý Dataset ảnh mẫu (Thời lượng: 2.0 giờ)
* **Mục đích:** Cung cấp dữ liệu đầu vào cho AI Rekognition và hàm Check-in/Check-out của Sinh viên 1 kiểm thử.
* **Yêu cầu kỹ thuật:**
  - Số lượng: **15 – 20 ảnh**.
  - Đa dạng loại phương tiện:
    - 10 ảnh xe máy: Biển 2 dòng (ví dụ: `59-X1` dòng trên, `123.45` dòng dưới).
    - 5 - 10 ảnh ô tô: Biển 1 dòng dài (`51A-123.45`) hoặc biển vuông.
  - Đa dạng điều kiện chụp: Đủ sáng, hơi tối/ngược sáng, chụp thẳng vuông góc, chụp góc nghiêng $15^\circ - 30^\circ$.
  - Định dạng: `.jpg` hoặc `.png`. Kích thước: **200KB – 800KB** (không để ảnh gốc 5MB–10MB vì upload qua API Gateway sẽ dễ bị lỗi payload limit 10MB).
* **Yêu cầu bắt buộc về bảo mật (Privacy/PII - Thầy Huỳnh Xuân Phụng yêu cầu):**
  - Mở ảnh bằng công cụ chỉnh sửa (Paint, Photoshop, Canva hoặc app điện thoại).
  - Dùng công cụ Blur/Che đen (Pixelate / Solid Box) **che toàn bộ khuôn mặt người chụp, người đi đường hoặc khuôn mặt xuất hiện trong gương chiếu hậu**.
* **Tổ chức thư mục:**
  - Đổi tên file chuẩn hóa:
    - `test_motor_01.jpg` đến `test_motor_10.jpg`
    - `test_car_01.jpg` đến `test_car_10.jpg`
  - Đưa toàn bộ file ảnh vào thư mục: `test-images/`.

---

### TASK 3: Khởi tạo S3 Bucket & DynamoDB trên AWS (Thời lượng: 2.0 giờ)

#### Bước 3.1: Tạo Amazon S3 Bucket
1. Trên AWS Console, tìm dịch vụ **S3** $\rightarrow$ Bấm nút cam **Create bucket**.
2. **General configuration:**
   - **Bucket name:** `smart-parking-images-<mssv-cua-ban>` (Ví dụ: `smart-parking-images-21110123`). Tên bucket phải viết chữ thường, không dấu cách, không trùng với ai trên toàn thế giới.
   - **AWS Region:** Chọn `US East (N. Virginia) us-east-1`.
3. **Object Ownership:** Giữ mặc định `ACLs disabled (recommended)`.
4. **Block Public Access settings for this bucket:** Đảm bảo vẫn tích chọn **Block all public access** (Bảo mật theo chuẩn Cloud).
5. **Tags:** Bấm **Add tag** và thêm đúng 3 tag:
   - `Project` : `SmartParking`
   - `Owner` : `<MSSV_SV1>_<MSSV_SV2>`
   - `Environment` : `Development`
6. Bấm nút cam **Create bucket** ở cuối trang.
7. **Tạo 3 thư mục ảo:**
   - Nhấp vào tên bucket vừa tạo.
   - Bấm nút **Create folder** $\rightarrow$ Nhập tên thư mục `in` $\rightarrow$ Bấm Create folder.
   - Bấm nút **Create folder** $\rightarrow$ Nhập tên thư mục `out` $\rightarrow$ Bấm Create folder.
   - Bấm nút **Create folder** $\rightarrow$ Nhập tên thư mục `athena-logs` $\rightarrow$ Bấm Create folder.

#### Bước 3.2: Tạo Amazon DynamoDB Table
1. Trên AWS Console, tìm dịch vụ **DynamoDB** $\rightarrow$ Bấm nút cam **Create table**.
2. **Table details:**
   - **Table name:** Nhập chính xác `ParkingTickets` (chú ý chữ hoa/thường).
   - **Partition key:** Nhập `ticketId` | Chọn kiểu dữ liệu là **String**.
   - **Sort key:** Để trống (không cần thiết ở tuần 1).
3. **Table settings:**
   - Chọn mục **Customize settings**.
   - Kéo xuống phần **Read/write capacity settings** $\rightarrow$ Tích chọn **On-demand** *(Cực kỳ quan trọng: On-demand chỉ tính phí khi có truy vấn đọc/ghi, không ngốn tiền $100 credits cố định hàng tháng như Provisioned)*.
4. **Tags:** Bấm **Add new tag** và thêm 3 tag:
   - `Project` : `SmartParking`
   - `Owner` : `<MSSV_SV1>_<MSSV_SV2>`
   - `Environment` : `Development`
5. Bấm nút cam **Create table** ở cuối trang và đợi cột Status chuyển sang màu xanh **Active**.

---

### TASK 4: Chụp ảnh minh chứng chuẩn quy định (Thời lượng: 1.0 giờ)
* **Tiêu chuẩn chụp ảnh minh chứng hợp lệ:**
  - Chụp **toàn màn hình (Full Screen Desktop)**.
  - Phải hiển thị rõ 3 yếu tố:
    1. **AWS Account ID** (ở góc trên bên phải thanh điều hướng AWS Console).
    2. **Region:** `us-east-1` (N. Virginia).
    3. **Đồng hồ hệ thống máy tính** (Taskbar góc dưới cùng bên phải, hiển thị rõ Ngày và Giờ).
* **Danh sách 4 ảnh cần chụp và lưu vào thư mục `evidence/week1/`:**
  1. `evidence/week1/s3_console.png`: Trang chi tiết S3 Bucket hiển thị tên bucket `smart-parking-images-<mssv>` và thẻ Tags.
  2. `evidence/week1/s3_folders.png`: Màn hình bên trong bucket thấy 3 folder `in/`, `out/`, `athena-logs/`.
  3. `evidence/week1/dynamodb_console.png`: Trang DynamoDB Table `ParkingTickets` thấy rõ Partition Key `ticketId`, On-demand mode, Status Active.
  4. `evidence/week1/billing_cost.png`: Vào menu **Billing and Cost Management** $\rightarrow$ Chụp màn hình mục chi tiêu (hiển thị $0.00 hoặc số dư credits còn lại).

---

### TASK 5: Hoàn thiện hồ sơ & Đẩy lên GitHub (Thời lượng: 1.0 giờ)
1. Mở file [NHAT_KY_CONG_VIEC_TUAN_1.md](../NHAT_KY_CONG_VIEC_TUAN_1.md):
   - Cập nhật Họ và tên, MSSV của bạn và bạn SV1 vào các vị trí `[Điền ...]`.
   - Kiểm tra bảng thống kê giờ làm việc (đảm bảo đủ $\ge 8.0$ giờ).
2. Kiểm tra lại toàn bộ file trên nhánh `dev`:
   ```bash
   git status
   ```
3. Thêm file và commit:
   ```bash
   git add .
   git commit -m "feat(infra): complete week 1 resources, sample dataset, and evidence"
   git push origin dev
   ```
4. Đăng nhập vào trang AWS Learner Lab, bấm nút **End Lab** khi không còn làm việc để tiết kiệm thời gian phiên và credits.

---

## 💡 CÁC CÂU HỎI VẤN ĐÁP THẦY PHỤNG CÓ THỂ HỎI NGƯỜI 2

| Câu hỏi | Câu trả lời trọng tâm cần nắm |
| :--- | :--- |
| **1. Tại sao dùng thư mục ảo `in/`, `out/` trên S3?** | S3 là dạng lưu trữ Object Storage dựa trên Flat namespace (không có thư mục thực sự, chỉ là chuỗi tiền tố Prefix). Việc đặt prefix `in/` và `out/` giúp phân chia vòng đời lưu trữ (Lifecycle rules) và dễ dàng kích hoạt S3 Event Notifications riêng biệt cho từng luồng xe vào / xe ra. |
| **2. Tại sao chọn DynamoDB On-Demand thay vì Provisioned?** | Bãi đỗ xe có lưu lượng truy cập không đều (giờ cao điểm sáng/chiều xe vào nhiều, ban đêm ít). On-demand tự động scale theo lượt request và chỉ tính tiền khi có đọc/ghi thực tế, tối ưu hóa $100 credits của Learner Lab, không lo bị vượt giới hạn WCU/RCU. |
| **3. Tại sao không tạo IAM Role riêng cho Lambda?** | Môi trường AWS Learner Lab áp dụng SCP (Service Control Policy) chặn quyền `iam:CreateRole` để bảo mật. Toàn bộ sinh viên bắt buộc sử dụng `LabRole` đã được AWS cấp sẵn đủ quyền cho Lambda, S3, DynamoDB, Rekognition. |
| **4. Tại sao phải che mờ khuôn mặt người trong ảnh mẫu?** | Tuân thủ tiêu chuẩn an toàn thông tin và quyền riêng tư (Data Privacy/GDPR/PII). Hệ thống nhận diện biển số xe chỉ cần vùng dữ liệu biển số xe, không được phép thu thập hoặc xử lý dữ liệu sinh trắc học/hình ảnh khuôn mặt khi chưa được sự đồng ý. |
