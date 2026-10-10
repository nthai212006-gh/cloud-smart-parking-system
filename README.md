# Smart Parking System - Cloud Computing Project

Hệ thống quản lý bãi giữ xe thông minh ứng dụng Điện toán đám mây (AWS).  
**Dự án Môn học:** Điện toán đám mây - Đợt 1 (2026-2027)

## Kiến trúc (Serverless Architecture)
Hệ thống sử dụng các dịch vụ của AWS Learner Lab:
- **AWS API Gateway:** Nhận request RESTful từ client.
- **AWS Lambda:** Chứa logic xử lý Check-in và Check-out (Python 3.11).
- **Amazon Rekognition:** Bóc tách biển số xe từ ảnh (DetectText OCR).
- **Amazon DynamoDB:** Lưu trữ thông tin vé gửi xe (On-Demand).
- **Amazon S3:** Lưu trữ ảnh xe ra/vào.

## Cấu trúc thư mục
- `/backend/`: Chứa mã nguồn AWS Lambda functions (`checkin.py`, `checkout.py`).
- `/docs/`: Chứa tài liệu thiết kế hệ thống và sơ đồ cấu trúc.
- `/scripts/`: Các script kiểm thử nhận diện biển số ở môi trường local.
- `/test-images/`: Dữ liệu ảnh test (Biển số xe đã được che mờ mặt người chụp và thông tin cá nhân).

## Nhóm thực hiện (Tuần 1)
- **Sinh viên 1:** Trưởng nhóm / Backend & AI
- **Sinh viên 2:** Hạ tầng, Data & QA
