# KẾ HOẠCH CHI TIẾT TUẦN 2 - SINH VIÊN 2 (MEMBER 2)
### VAI TRÒ: KỸ SƯ HẠ TẦNG CLOUD, QUẢN TRỊ DỮ LIỆU & ĐẢM BẢO CHẤT LƯỢNG (INFRASTRUCTURE / DATA / QA)
* **Thành viên:** Nguyễn Trung Hải
* **Mã số sinh viên (MSSV):** 24110207
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Thời gian thực hiện Tuần 2:** 13/10/2026 – 19/10/2026
* **Tổng thời gian phân bổ:** **8.5 giờ** (Quy định: ≥ 8.0 giờ)

---

## I. MỤC TIÊU CÔNG VIỆC TRONG TUẦN 2
1. **Kiểm tra và cấu hình tương thích hạ tầng AWS:**
   - Cấu hình S3 CORS trên bucket `smart-parking-images-24110207` để hỗ trợ frontend gọi trực tiếp hoặc xem ảnh vé.
   - Xác thực quyền của `LabRole` đối với các thao tác `rekognition:DetectText`, `dynamodb:PutItem/GetItem/UpdateItem`, `s3:PutObject`.
   - Kiểm tra trạng thái hoạt động của bảng DynamoDB `ParkingTickets` (Billing mode On-demand).
2. **Kiểm thử độc lập khả năng nhận diện của Amazon Rekognition:**
   - Viết script thực thi kiểm thử hàng loạt trên 120 ảnh mẫu (thuộc 5 nhóm đã chuẩn hóa ở Tuần 1: ô tô rõ, xe máy rõ, ô tô khó, xe máy khó, ảnh ngoại lệ).
   - Đánh giá tỷ lệ trích xuất thành công và độ chính xác của biểu thức Regex đối với biển số 2 dòng xe máy.
   - Lập bảng ma trận kết quả kiểm thử chất lượng nhận diện (Confusion Matrix / Accuracy Report).
3. **Phối hợp kiểm thử tích hợp (Integration Testing):**
   - Hỗ trợ Sinh viên 1 kiểm thử luồng Check-in và Check-out thông qua API Gateway.
   - Trực tiếp kiểm tra và xác nhận trên AWS Console:
     - Dữ liệu trong bảng DynamoDB: Các trường `ticketId`, `plateNumber`, `vehicleType`, `checkinTime`, `checkoutTime`, `fee`, `status` được cập nhật chính xác.
     - Dữ liệu trong S3: Ảnh được lưu đúng định dạng tại `in/{ticketId}.jpg` và `out/{ticketId}.jpg`.
4. **Thu thập bộ minh chứng hoàn chỉnh Tuần 2 (`evidence/week2/`):**
   - Chụp toàn màn hình có hiển thị rõ Account ID, Region `us-east-1` và đồng hồ máy tính theo đúng yêu cầu kiểm định của GVHD.
   - Kiểm toán chi phí AWS Billing (đảm bảo phát sinh = $0.00 hoặc dưới $0.50).
5. **Hoàn thiện tài liệu Worklog Tuần 2 và đồng bộ Git.**

---

## II. ĐỐI CHIẾU VỚI KẾT QUẢ GIT TUẦN 1
* **Điểm kế thừa từ Tuần 1:**
  - Bucket S3 `smart-parking-images-24110207` và bảng DynamoDB `ParkingTickets` đã tạo sẵn từ script `scripts/setup_aws_resources.py` (Commit `41ec17b`).
  - 120 ảnh thử nghiệm đã che thông tin cá nhân trong `test-images/` (Commit `a2d46cd`).
  - Quy chuẩn Tagging bắt buộc trong `docs/guidelines/tagging-standards.md` (Commit `a3ad771`).
* **Nhiệm vụ cần giải quyết triệt để trong Tuần 2:**
  - Đưa 120 ảnh vào kiểm thử thực tế trên AWS Rekognition thật để ghi nhận số liệu định lượng (thay vì chỉ test regex chuỗi cục bộ).
  - Xác nhận dữ liệu thực tế được ghi vào DynamoDB và S3 qua console AWS.
  - Kiểm soát chi phí gọi Rekognition API (120 calls ~ $0.12, hoàn toàn nằm trong Free Tier / Hạn mức Learner Lab $100).

---

## III. LỊCH TRÌNH THỰC HIỆN CHI TIẾT (4 BUỔI - TỔNG 8.5 GIỜ)

### Buổi 1 (Thứ 3: 14/10/2026 | 19:00 - 21:30 | 2.5 giờ): Cấu hình S3 CORS & Xác thực Quyền LabRole
* **Mục tiêu:** Đảm bảo toàn bộ hạ tầng lưu trữ và phân quyền sẵn sàng cho Lambda kết nối.
* **Nhiệm vụ cụ thể:**
  - Khởi động AWS Learner Lab, chọn Region `us-east-1`.
  - Truy cập S3 Console, kiểm tra bucket `smart-parking-images-24110207`:
    - Cấu hình S3 CORS Policy (cho phép phương thức GET, PUT, POST từ mọi nguồn để hiển thị ảnh trên Web):
      ```json
      [
        {
          "AllowedHeaders": ["*"],
          "AllowedMethods": ["GET", "PUT", "POST", "HEAD"],
          "AllowedOrigins": ["*"],
          "ExposeHeaders": []
        }
      ]
      ```
  - Kiểm tra bảng DynamoDB `ParkingTickets`: Xác nhận Partition Key `ticketId` (String), Table status `Active`, On-demand mode.
  - Viết script kiểm tra quyền thực thi của `LabRole`: Gửi thử nghiệm một lệnh `rekognition:DetectText`, `s3:PutObject` và `dynamodb:PutItem` qua AWS CLI / boto3 để đảm bảo không bị chặn bởi IAM Permission Boundary.
* **Sản phẩm:** Cấu hình S3 CORS hoàn tất, biên bản kiểm tra quyền `LabRole` thông suốt.

---

### Buổi 2 (Thứ 5: 16/10/2026 | 19:30 - 21:30 | 2.0 giờ): Kiểm thử Độc lập Rekognition trên 120 ảnh mẫu
* **Mục tiêu:** Đánh giá định lượng hiệu quả nhận diện của Rekognition kết hợp giải thuật Regex.
* **Nhiệm vụ cụ thể:**
  - Xây dựng script kiểm thử hàng loạt `scripts/evaluate_rekognition_accuracy.py`:
    - Duyệt qua từng ảnh trong 5 thư mục `test-images/`.
    - Gửi ảnh trực tiếp lên AWS Rekognition API `DetectText`.
    - Áp dụng hàm Regex bóc tách biển số.
    - So sánh với nhãn biển số thực tế (Ground Truth).
  - Phân tích và thống kê số liệu:
    - Nhóm 1 (`01_car_clear` - 40 ảnh): Tỷ lệ nhận diện biển ô tô tiêu chuẩn.
    - Nhóm 2 (`02_motor_clear` - 40 ảnh): Tỷ lệ nhận diện biển xe máy 2 dòng và ghép chuỗi.
    - Nhóm 3 (`03_car_hard` - 10 ảnh): Đánh giá khi ảnh thiếu sáng/góc nghiêng.
    - Nhóm 4 (`04_motor_hard` - 10 ảnh): Đánh giá biển số xe máy bị mờ/nghiêng.
    - Nhóm 5 (`05_error_cases` - 20 ảnh): Xác nhận hệ thống phát hiện chính xác trường hợp không đọc được biển số và gán nhãn `UNKNOWN`.
  - Tổng hợp bảng báo cáo độ chính xác để chuẩn bị đưa vào báo cáo tuần.
* **Sản phẩm:** Script đánh giá và bảng kết quả đo lường độ chính xác nhận diện biển số thực tế.

---

### Buổi 3 (Thứ 6: 17/10/2026 | 19:30 - 21:30 | 2.0 giờ): Phối hợp Kiểm thử Tích hợp & Kiểm tra Dữ liệu
* **Mục tiêu:** Cùng Sinh viên 1 kiểm thử toàn diện luồng nghiệp vụ trên AWS và kiểm tra tính toàn vẹn dữ liệu.
* **Nhiệm vụ cụ thể:**
  - Nhận API Gateway URL từ Sinh viên 1.
  - Thực hiện gửi request test các luồng:
    - Check-in xe máy biển số `59X1-12345`.
    - Check-in ô tô biển số `51A-99999`.
    - Check-in xe có ảnh mờ không đọc được biển.
  - Truy cập AWS Console để xác minh:
    - DynamoDB: Mở giao diện **Explore items** của bảng `ParkingTickets`, kiểm tra các trường dữ liệu và định dạng thời gian ISO 8601 (`checkinTime`).
    - S3: Mở folder `in/`, kiểm tra xem ảnh đã được lưu trữ với tên file `{ticketId}.jpg` chưa, dung lượng và định dạng có chuẩn không.
  - Tiến hành gọi API Check-out:
    - Kiểm tra công thức tính phí đỗ xe đối với từng loại xe.
    - Xác nhận bản ghi DynamoDB được cập nhật trường `checkoutTime`, `fee`, `status = COMPLETED`.
    - Xác nhận ảnh xe ra được lưu vào folder `out/{ticketId}.jpg` trên S3.
* **Sản phẩm:** Biên bản kiểm thử tích hợp ghi nhận các giao dịch thành công trên AWS Console.

---

### Buổi 4 (Chủ nhật: 19/10/2026 | 14:00 - 16:00 | 2.0 giờ): Thu thập Minh chứng, Kiểm toán Chi phí & Báo cáo
* **Mục tiêu:** Hoàn thiện toàn bộ hồ sơ minh chứng Tuần 2 theo quy chuẩn của GVHD.
* **Nhiệm vụ cụ thể:**
  - Chụp ảnh màn hình minh chứng đầy đủ theo tiêu chuẩn (Hiển thị rõ Account ID, Region `us-east-1` và đồng hồ hệ thống):
    - `evidence/week2/01_lambda_functions.png`: Danh sách 2 hàm Lambda kèm cấu hình runtime, memory, timeout, tag.
    - `evidence/week2/02_apigateway_routes.png`: Cấu hình API Gateway REST API với 2 endpoint và stage `dev`.
    - `evidence/week2/03_rekognition_cloudwatch.png`: Log thực thi nhận diện biển số trên CloudWatch Logs.
    - `evidence/week2/04_dynamodb_items.png`: Bảng dữ liệu `ParkingTickets` chứa các bản ghi vé xe thực tế.
    - `evidence/week2/05_s3_stored_images.png`: Các tệp ảnh đã upload thành công trong folder `in/` và `out/`.
    - `evidence/week2/06_api_test_terminal_1.png`: Kiểm thử Check-in thành công qua API Gateway trên PowerShell.
    - `evidence/week2/07_api_test_terminal_2.png`: Kiểm thử Check-out và các ca ngoại lệ trên PowerShell.
    - `evidence/week2/08_cost_and_billing.png`: Màn hình Billing xác nhận mức chi phí an toàn ($0.00).
  - Soạn thảo nhật ký thực hiện chi tiết vào `docs/worklogs/week-02/member-2.md` và `docs/worklogs/week-02/overview.md`.
  - Thực hiện lệnh **End Lab** trên AWS Learner Lab để tắt phiên làm việc, chống phát sinh chi phí ngoài ý muốn.
  - Commit toàn bộ minh chứng và tài liệu lên nhánh `main`.
* **Sản phẩm:** Bộ ảnh minh chứng trong `evidence/week2/`, nhật ký hoàn chỉnh và mã nguồn đồng bộ trên Git.

---

## IV. BẢNG TỔNG HỢP GIỜ LÀM VIỆC DỰ KIẾN - SINH VIÊN 2
| Buổi làm việc | Ngày thực hiện | Khung giờ | Nội dung chính | Số giờ |
| :---: | :---: | :---: | :--- | :---: |
| Buổi 1 | 14/10/2026 (Thứ 3) | 19:00 - 21:30 | Cấu hình S3 CORS, kiểm tra trạng thái DynamoDB, xác thực quyền LabRole | 2.5h |
| Buổi 2 | 16/10/2026 (Thứ 5) | 19:30 - 21:30 | Kiểm thử Rekognition độc lập trên 120 ảnh dataset, thống kê độ chính xác | 2.0h |
| Buổi 3 | 17/10/2026 (Thứ 6) | 19:30 - 21:30 | Phối hợp test tích hợp, kiểm tra dữ liệu trên DynamoDB Console và S3 Objects | 2.0h |
| Buổi 4 | 19/10/2026 (Chủ nhật) | 14:00 - 16:00 | Thu thập 6 ảnh minh chứng console, kiểm toán chi phí $0.00 & hoàn thiện Worklog | 2.0h |
| **Tổng cộng** | | | **Tổng thời gian thực tế cam kết** | **8.5 giờ** |
*(Đạt chỉ tiêu môn học quy định: ≥ 8.0 giờ/tuần)*
