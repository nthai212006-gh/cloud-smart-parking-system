# THƯ MỤC MINH CHỨNG TUẦN 2 (WEEK 2 EVIDENCE)
### ĐỀ TÀI: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING)

Thư mục này lưu trữ toàn bộ ảnh chụp màn hình minh chứng thực tế trên môi trường AWS Learner Lab cho Tuần 2 theo quy định của GVHD ThS. Huỳnh Xuân Phụng.

> **QUY CHUẨN BẮT BUỘC KHI CHỤP ẢNH MINH CHỨNG:**
> 1. Chụp **Toàn màn hình máy tính** (Full screen).
> 2. Nhìn rõ **AWS Account ID** ở góc phải trên.
> 3. Nhìn rõ **Region `us-east-1`** (N. Virginia).
> 4. Nhìn rõ **Đồng hồ hệ thống máy tính** (Ngày giờ phải khớp với khung giờ trong bảng Worklog).

### Danh mục ảnh minh chứng cần lưu:
1. `01_lambda_functions.png`: Màn hình AWS Lambda Console hiển thị 2 hàm `SmartParking-Checkin` và `SmartParking-Checkout` (Python 3.11, LabRole, Memory 256MB, Timeout 15s).
2. `02_apigateway_routes.png`: Màn hình API Gateway Console hiển thị REST API `SmartParking-API` với các routes `/checkin`, `/checkout` và Stage `dev`.
3. `03_rekognition_cloudwatch.png`: Log thực thi nhận diện biển số của Amazon Rekognition trên CloudWatch Logs.
4. `04_dynamodb_items.png`: Màn hình DynamoDB Console mục Explore Items hiển thị các bản ghi vé xe thật.
5. `05_s3_stored_images.png`: Màn hình S3 Bucket hiển thị ảnh xe vào trong folder `in/` và xe ra trong `out/`.
6. `06_api_test_terminal.png`: Màn hình Terminal / Postman chạy kiểm thử API thành công (Status 200 OK, JSON response).
7. `07_cost_and_billing.png`: Màn hình AWS Billing Dashboard xác nhận chi phí phát sinh an toàn ($0.00).
