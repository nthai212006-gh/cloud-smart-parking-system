# Hệ Thống Quản Lý Bãi Giữ Xe Thông Minh (Smart Parking System)

Dự án môn học **Điện toán đám mây (Cloud Computing)** - Đợt 1 (2026 - 2027)  
**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng  
**Môi trường triển khai:** AWS Learner Lab (`us-east-1`)  
**Git Branch:** `dev` (phát triển) / `main` (nghiệm thu)

---

## 📌 1. Giới thiệu đề tài
Hệ thống quản lý bãi giữ xe thông minh ứng dụng kiến trúc Serverless trên nền tảng Amazon Web Services (AWS). Hệ thống tự động nhận diện biển số xe qua hình ảnh bằng trí tuệ nhân tạo (Amazon Rekognition), quản lý lượt xe ra/vào và tự động tính toán phí gửi xe theo thời gian thực.

## 👥 2. Thành viên nhóm
| STT | Họ và tên | MSSV | Vai trò chính |
| :---: | :--- | :---: | :--- |
| 1 | `[Họ và tên SV 1]` | `[MSSV 1]` | Trưởng nhóm: Kiến trúc Serverless, AI Rekognition & Backend Core |
| 2 | Nguyễn Trung Hải | 24110207 | Thành viên: Hạ tầng AWS (S3, DynamoDB), Dataset & QA/Audit |

---

## 🏗️ 3. Kiến trúc hệ thống (Serverless Architecture)
- **Frontend / Client:** Web Dashboard hoặc thiết bị camera cổng gửi ảnh qua API.
- **API Gateway:** Nhận request và định tuyến tới các hàm Lambda xử lý.
- **AWS Lambda:**
  - `SmartParking-Checkin`: Xử lý xe vào, gọi Rekognition bóc tách biển số, ghi vé vào DynamoDB, lưu ảnh vào S3 (`in/`).
  - `SmartParking-Checkout`: Xử lý xe ra, nhận diện biển số, đối soát vé, tính phí gửi xe và cập nhật trạng thái.
- **Amazon Rekognition:** API `DetectText` nhận diện văn bản / biển số từ hình ảnh.
- **Amazon DynamoDB:** Bảng `ParkingTickets` lưu trữ thông tin vé gửi xe (Partition Key: `ticketId`).
- **Amazon S3:** Bucket `smart-parking-images-[mssv]` lưu trữ hình ảnh xe vào/ra (`in/`, `out/`) và logs.
- **Amazon Athena:** Truy vấn và phân tích báo cáo doanh thu bãi xe.

---

## 📁 4. Cấu trúc thư mục dự án (Project Structure)
```text
cloud-smart-parking-system/
├── backend/                              # Mã nguồn các hàm AWS Lambda (Python 3.11)
├── docs/                                 # Tài liệu dự án
│   ├── architecture/                     # Thiết kế kiến trúc & cơ sở dữ liệu
│   │   └── architecture-design.md
│   ├── guidelines/                       # Quy chuẩn đặt tên & gắn tag tài nguyên AWS
│   │   └── tagging-standards.md
│   ├── plans/                            # Kế hoạch công việc theo từng tuần & thành viên
│   │   └── week-01/
│   │       ├── overview.md               # Kế hoạch tổng quan Tuần 1
│   │       ├── member-1.md               # Kế hoạch chi tiết Người 1
│   │       └── member-2.md               # Kế hoạch chi tiết Người 2
│   └── worklogs/                         # Nhật ký công việc theo từng tuần & thành viên
│       └── week-01/
│           ├── overview.md               # Tổng hợp giờ & minh chứng chung Tuần 1
│           ├── member-1.md               # Nhật ký chi tiết Người 1
│           └── member-2.md               # Nhật ký chi tiết Người 2
├── evidence/                             # Ảnh chụp màn hình minh chứng console
│   └── week1/
├── scripts/                              # Các script kiểm thử, tự động hóa cục bộ
├── test-images/                          # Bộ 15-20 ảnh biển số xe mẫu đã che thông tin cá nhân
├── .gitignore
└── README.md
```

---

## 🚀 5. Quy chuẩn Tagging bắt buộc (AWS Learner Lab)
- `Project`: `SmartParking`
- `Owner`: `[MSSV_SV1]_[MSSV_SV2]`
- `Environment`: `Development`
Chi tiết xem tại [docs/guidelines/tagging-standards.md](docs/guidelines/tagging-standards.md).
