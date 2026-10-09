# QUY CHUẨN ĐẶT TÊN VÀ GẮN TAG TÀI NGUYÊN AWS (TAGGING STANDARD)
### ĐỀ TÀI: SMART PARKING SYSTEM · HỌC PHẦN ĐIỆN TOÁN ĐÁM MÂY

---

## 1. MỤC TIÊU
- Tuân thủ nghiêm ngặt quy định quản lý tài nguyên trong môi trường **AWS Learner Lab**.
- Phân biệt rõ tài nguyên của nhóm với các bài lab khác, phục vụ việc giám sát chi phí (Cost Allocation) và kiểm tra tiến độ của Giảng viên.

---

## 2. QUY CHUẨN TAGGING BẮT BUỘC
Mọi tài nguyên được khởi tạo trên AWS (S3 Bucket, DynamoDB Table, Lambda Function, API Gateway, CloudWatch Log Group...) đều phải được gắn tối thiểu 3 Tags sau:

| Tag Key | Giá trị mẫu (Tag Value) | Mô tả |
| :--- | :--- | :--- |
| **`Project`** | `SmartParking` | Tên dự án |
| **`Owner`** | `[MSSV_SV1]_[MSSV_SV2]` | Mã số sinh viên của 2 thành viên phụ trách |
| **`Environment`** | `Development` | Môi trường phát triển và thử nghiệm |

> **Ví dụ:** Nếu MSSV của 2 bạn là `21110001` và `21110002`:  
> `Owner` = `21110001_21110002`

---

## 3. QUY CHUẨN ĐẶT TÊN TÀI NGUYÊN (NAMING CONVENTION)
| Dịch vụ AWS | Quy tắc đặt tên | Ví dụ |
| :--- | :--- | :--- |
| **Amazon S3** | `smart-parking-images-[mssv]` | `smart-parking-images-24110207` |
| **Amazon DynamoDB** | `ParkingTickets` | `ParkingTickets` (Partition Key: `ticketId`) |
| **AWS Lambda (Checkin)** | `SmartParking-Checkin` | `SmartParking-Checkin` (Runtime: Python 3.11) |
| **AWS Lambda (Checkout)**| `SmartParking-Checkout` | `SmartParking-Checkout` (Runtime: Python 3.11) |
| **API Gateway** | `SmartParking-API` | `SmartParking-API` (HTTP API hoặc REST API) |

---

## 4. QUY ĐỊNH VỀ QUYỀN (IAM ROLE) TRONG AWS LEARNER LAB
- **Quy tắc tuyệt đối:** Không được tạo IAM Role hoặc IAM User mới (tài khoản Learner Lab không có quyền `iam:CreateRole`).
- **Role bắt buộc sử dụng:** `LabRole` (ARN: `arn:aws:iam::<AccountID>:role/LabRole`).
- Tất cả hàm AWS Lambda khi khởi tạo phải chọn: **Use an existing role** $\rightarrow$ chọn **`LabRole`**.
