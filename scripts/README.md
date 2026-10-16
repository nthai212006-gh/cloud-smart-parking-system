# Scripts Thử Nghiệm & Tự Động Hóa (Automation & Test Scripts)

Thư mục chứa các kịch bản kiểm thử, đánh giá và tự động hóa hạ tầng hệ thống:

1. **`test_plate_regex.py`**:
   - Kiểm thử thuật toán biểu thức chính quy (Regex) bóc tách biển số xe máy (2 dòng) và ô tô Việt Nam từ văn bản OCR.
2. **`setup_aws_resources.py`**:
   - Script tự động khởi tạo S3 Bucket (`smart-parking-images-24110207`) và DynamoDB Table (`ParkingTickets`).
3. **`build_curated_dataset.py`**:
   - Tiền xử lý, lọc chọn và làm mờ khuôn mặt/thông tin cá nhân (PII) cho 120 ảnh mẫu thuộc 5 nhóm kiểm thử.
4. **`verify_aws_infrastructure.py`**:
   - Kiểm tra kết nối hạ tầng AWS, xác thực quyền `LabRole`, kiểm tra trạng thái bảng DynamoDB và tự động áp dụng CORS Policy cho S3 Bucket.
5. **`evaluate_rekognition_accuracy.py`**:
   - Chạy đánh giá độ chính xác thực tế của Amazon Rekognition `DetectText` trên toàn bộ 120 ảnh dataset, xuất báo cáo Markdown tại `docs/worklogs/week-02/rekognition_evaluation_report.md`.
6. **`test_api_endpoints.py`**:
   - Kịch bản kiểm thử tự động toàn trình (Integration E2E) gọi Amazon API Gateway (`POST /checkin` và `POST /checkout`), kiểm tra tính cước phí và các ca ngoại lệ (400, 404, UNKNOWN).

