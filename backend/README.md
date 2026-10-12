# Backend: AWS Lambda & API Gateway

Thư mục chứa toàn bộ mã nguồn xử lý và cấu hình giao tiếp tầng điện toán Serverless (Serverless Compute & API Layer):

## 1. Amazon API Gateway
- `api_gateway_openapi.json`: File định nghĩa và đặc tả REST API theo chuẩn **OpenAPI 3.0 / Swagger**, cấu hình tích hợp `aws_proxy` tới các hàm AWS Lambda, hỗ trợ CORS đầy đủ cho các endpoint:
  - `POST /checkin`: Tiếp nhận ảnh xe vào, kích hoạt Lambda `SmartParking-Checkin`.
  - `POST /checkout`: Tiếp nhận mã vé/ảnh xe ra, kích hoạt Lambda `SmartParking-Checkout`.

## 2. AWS Lambda Functions (Python 3.11)
- `checkin.py`: Lambda xử lý xe vào bãi:
  - Tiếp nhận request từ API Gateway.
  - Gọi AWS Rekognition (`DetectText`) để nhận diện biển số xe máy và ô tô.
  - Phân loại và gán cờ `UNKNOWN` nếu ảnh mờ/không đọc được để hỗ trợ nhập thủ công.
  - Lưu ảnh phương tiện vào S3 bucket (`in/{ticket_id}.jpg`).
  - Ghi bản ghi vé gửi xe vào DynamoDB table `ParkingTickets` (Trạng thái: `PARKED`).
  - Trả về mã vé `ticketId`, biển số và thời gian vào chuẩn ISO 8601 kèm CORS header.

- `checkout.py`: Lambda xử lý xe ra bãi & tính tiền:
  - Tiếp nhận `ticketId` từ API Gateway.
  - Truy xuất bản ghi từ DynamoDB table `ParkingTickets`.
  - Áp dụng thuật toán tính phí gửi xe theo block giờ:
    - **Xe máy:** 5.000đ cho 4 giờ đầu, mỗi giờ tiếp theo +2.000đ/giờ.
    - **Ô tô:** 20.000đ cho 2 giờ đầu, mỗi giờ tiếp theo +10.000đ/giờ.
  - Cập nhật trạng thái `COMPLETED`, lưu thời gian ra `checkoutTime` và số tiền `fee` vào DynamoDB.
  - Trả về tổng thời gian đỗ xe và chi phí cần thanh toán.
