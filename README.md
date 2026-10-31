# Hệ Thống Quản Lý Bãi Giữ Xe Thông Minh (Smart Parking System)

Dự án môn học **Điện toán đám mây (Cloud Computing)** - Đợt 1 (2026 - 2027)  
**Giảng viên hướng dẫn:** Huỳnh Xuân Phụng  
**Môi trường triển khai:** AWS Learner Lab (`us-east-1`)  
**Git Branch:** `main` (Nhánh chính thức)

---

## 📌 1. Giới thiệu đề tài
Hệ thống quản lý bãi giữ xe thông minh ứng dụng kiến trúc Serverless trên nền tảng Amazon Web Services (AWS). Hệ thống tự động nhận diện biển số xe qua hình ảnh bằng trí tuệ nhân tạo (Amazon Rekognition), quản lý lượt xe ra/vào và tự động tính toán phí gửi xe theo thời gian thực.

## 👥 2. Thành viên nhóm
| STT | Họ và tên | MSSV | Vai trò chính |
| :---: | :--- | :---: | :--- |
| 1 | Lê Cao Việt Tín | 24110354 | Trưởng nhóm: Kiến trúc Serverless, AI Rekognition, Master Report |
| 2 | Nguyễn Trung Hải | 24110207 | Thành viên: Hạ tầng AWS (S3, DynamoDB), Báo cáo Chương 5 (Kiểm thử & Giám sát), Video Demo |

---

## 🏗️ 3. Kiến trúc hệ thống (Serverless Architecture)
- **Frontend / Client:** Web Dashboard hoặc thiết bị camera cổng gửi ảnh qua API.
- **Amazon API Gateway:** Tiếp nhận request RESTful (`/checkin`, `/checkout`), kiểm soát CORS và định tuyến tới các hàm Lambda xử lý (Đặc tả: `backend/api_gateway_openapi.json`).
- **AWS Lambda:**
  - `SmartParking-Checkin`: Xử lý xe vào, gọi Rekognition bóc tách biển số, ghi vé vào DynamoDB, lưu ảnh vào S3 (`in/`).
  - `SmartParking-Checkout`: Xử lý xe ra, nhận diện biển số, đối soát vé, tính phí gửi xe và cập nhật trạng thái.
- **Amazon Rekognition:** API `DetectText` nhận diện văn bản / biển số từ hình ảnh.
- **Amazon DynamoDB:** Bảng `ParkingTickets` lưu trữ thông tin vé gửi xe (Partition Key: `ticketId`, On-Demand).
- **Amazon S3:** Bucket `smart-parking-images-24110207` lưu trữ hình ảnh xe vào/ra (`in/`, `out/`) và logs.
- **Amazon Athena:** Truy vấn và phân tích báo cáo doanh thu bãi xe.

Chi tiết xem tại tài liệu [docs/THIET_KE_KIEN_TRUC_HE_THONG.md](docs/THIET_KE_KIEN_TRUC_HE_THONG.md).

---

## 📁 4. Cấu trúc thư mục dự án (Project Structure)
```text
cloud-smart-parking-system/
├── PLAN_TUAN_2.md                        # Kế hoạch chi tiết Tuần 2 (Đối chiếu sát Git Tuần 1)
├── PLAN_TUAN_3.md                        # Kế hoạch chi tiết Tuần 3 (Giám sát CloudWatch, Athena, Bảo mật, IaC, Web UI)
├── backend/                              # Mã nguồn Lambda & Cấu hình API Gateway
│   ├── api_gateway_openapi.json          # Đặc tả REST API Gateway (OpenAPI 3.0 / Swagger)
│   ├── checkin.py                        # Lambda xử lý xe vào (Check-in)
│   └── checkout.py                       # Lambda xử lý xe ra & tính phí (Check-out)
├── frontend/                             # Giao diện Web Dashboard tĩnh (S3 Static Hosting)
├── iac/                                  # Kịch bản Tự động hóa hạ tầng (AWS CloudFormation IaC)
├── docs/                                 # Tài liệu dự án
│   ├── THIET_KE_KIEN_TRUC_HE_THONG.md    # Tài liệu thiết kế kiến trúc chi tiết
│   ├── architecture/                     # Thiết kế kiến trúc & cơ sở dữ liệu
│   │   └── architecture-design.md
│   ├── guidelines/                       # Quy chuẩn đặt tên & gắn tag tài nguyên AWS
│   │   └── tagging-standards.md
│   ├── plans/                            # Kế hoạch công việc theo từng tuần & thành viên
│   │   ├── week-01/
│   │   ├── week-02/
│   │   └── week-03/                      # Kế hoạch chi tiết Tuần 3 (Overview, SV1, SV2)
│   └── worklogs/                         # Nhật ký công việc theo từng tuần & thành viên
│       ├── week-01/
│       ├── week-02/                      # Nhật ký thực hiện Tuần 2 & Báo cáo Rekognition
│       └── week-03/                      # Nhật ký thực hiện Tuần 3
├── evidence/                             # Ảnh chụp màn hình minh chứng console
│   ├── week1/                            # Minh chứng Tuần 1 (S3, DynamoDB, Billing)
│   ├── week2/                            # Minh chứng Tuần 2 (Lambda, API Gateway, CloudWatch, Items, S3, Tests, Billing)
│   └── week3/                            # Minh chứng Tuần 3 (CloudWatch Dashboard/Alarms, Athena SQL, Throttling, Web UI)
├── scripts/                              # Các script kiểm thử, tự động hóa & QA
│   ├── test_plate_regex.py               # Kiểm thử giải thuật Regex OCR biển số
│   ├── setup_aws_resources.py            # Tự động khởi tạo S3 & DynamoDB
│   ├── build_curated_dataset.py          # Trích xuất và chuẩn hóa dataset 120 ảnh
│   ├── verify_aws_infrastructure.py      # Xác thực quyền LabRole & cấu hình S3 CORS
│   ├── evaluate_rekognition_accuracy.py  # Đánh giá độ chính xác Rekognition trên 120 ảnh
│   └── test_api_endpoints.py             # Kiểm thử tự động API Gateway E2E
├── test-images/                          # Bộ ảnh biển số xe mẫu đã che thông tin cá nhân
├── .gitignore
└── README.md
```

---

## 🚀 5. Quy chuẩn Tagging bắt buộc (AWS Learner Lab)
- `Project`: `SmartParking`
- `Owner`: `24110354_24110207`
- `Environment`: `Development`
Chi tiết xem tại [docs/guidelines/tagging-standards.md](docs/guidelines/tagging-standards.md).
