# THIẾT KẾ KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE DESIGN)
### ĐỀ TÀI: QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING)

---

## 1. SƠ ĐỒ KIẾN TRÚC SERVERLESS TỔNG THỂ

```mermaid
graph TD
    Client["Client / Web UI / Camera Cổng"] -->|1. Upload Ảnh Xe| APIGW["Amazon API Gateway"]
    
    APIGW -->|Check-in Route| LambdaIn["AWS Lambda: SmartParking-Checkin"]
    APIGW -->|Check-out Route| LambdaOut["AWS Lambda: SmartParking-Checkout"]
    
    LambdaIn -->|2. Nhận diện biển số| Rekog["Amazon Rekognition (DetectText)"]
    LambdaOut -->|2. Nhận diện biển số| Rekog
    
    LambdaIn -->|3. Lưu ảnh vào s3://.../in/| S3["Amazon S3 Bucket"]
    LambdaOut -->|3. Lưu ảnh ra s3://.../out/| S3
    
    LambdaIn -->|4. Tạo vé mới (PARKED)| DDB[("Amazon DynamoDB (ParkingTickets)")]
    LambdaOut -->|4. Cập nhật vé, tính phí (COMPLETED)| DDB
    
    S3 -.->|Truy vấn dữ liệu báo cáo| Athena["Amazon Athena"]
```

---

## 2. THIẾT KẾ BẢNG DỮ LIỆU DYNAMODB (`ParkingTickets`)

* **Tên bảng:** `ParkingTickets`
* **Partition Key (PK):** `ticketId` (kiểu String - UUIDv4)
* **Chế độ Capacity:** On-Demand

### Chi tiết các trường dữ liệu (Attributes):
| Tên trường | Kiểu dữ liệu | Mô tả |
| :--- | :--- | :--- |
| `ticketId` | String (PK) | Mã vé định danh duy nhất (UUID) |
| `plateNumber` | String | Biển số xe đã lọc và chuẩn hóa qua Regex |
| `vehicleType` | String | Phân loại phương tiện (`MOTORBIKE` / `CAR`) |
| `checkinTime` | String | Thời gian xe vào (ISO 8601: `YYYY-MM-DDTHH:mm:ssZ`) |
| `checkoutTime` | String | Thời gian xe ra (ISO 8601) |
| `status` | String | Trạng thái vé: `PARKED` (Đang đỗ) hoặc `COMPLETED` (Đã lấy xe) |
| `fee` | Number | Tiền gửi xe tính theo quy chuẩn block giờ (VNĐ) |
| `inImageKey` | String | Đường dẫn ảnh xe vào trên S3 (`in/uuid.jpg`) |
| `outImageKey` | String | Đường dẫn ảnh xe ra trên S3 (`out/uuid.jpg`) |
