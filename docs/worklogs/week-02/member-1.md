# NHẬT KÝ CHI TIẾT TUẦN 2 - SINH VIÊN 1 (MEMBER 1)
### VAI TRÒ: TRƯỞNG NHÓM / KIẾN TRÚC SERVERLESS, AI REKOGNITION & BACKEND CORE
* **Thành viên:** Lê Cao Việt Tín (MSSV: 25110159)
* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn:** ThS. Huỳnh Xuân Phụng
* **Tổng thời gian thực tế:** **8.5 giờ** (Chỉ tiêu môn học: ≥ 8.0 giờ)

---

## BẢNG NHẬT KÝ CHI TIẾT TỪNG BUỔI LÀM VIỆC

| Ngày | Khung giờ | Số giờ | Nội dung công việc chi tiết | Sản phẩm / Minh chứng |
| :---: | :---: | :---: | :--- | :--- |
| **13/10/2026**<br>(Thứ 2) | 19:30 - 21:30 | 2.0h | - Nâng cấp mã nguồn `backend/checkin.py`: Tích hợp Boto3 gọi Rekognition `DetectText`, bóc tách Regex biển số Việt Nam, upload ảnh S3 `in/`, ghi DynamoDB.<br>- Nâng cấp `backend/checkout.py`: Đọc vé DynamoDB, tính tiền theo block, cập nhật `COMPLETED`. | Mã nguồn Boto3 hoàn thiện trong `backend/`<br>Commit: `feat: implement real boto3 logic for lambda handlers` |
| **15/10/2026**<br>(Thứ 4) | 19:00 - 21:30 | 2.5h | - Đăng nhập AWS Console (`us-east-1`), tạo 2 Lambda function `SmartParking-Checkin` và `SmartParking-Checkout`.<br>- Cấu hình Python 3.11, Timeout 15s, Memory 256MB, gán role `LabRole`.<br>- Thiết lập biến môi trường và gắn đủ 3 tag chuẩn (`Project`, `Owner`, `Environment`). | Ảnh chụp Lambda Console & CloudWatch logs trong `evidence/week2/01_lambda_functions.png` |
| **17/10/2026**<br>(Thứ 6) | 19:30 - 21:30 | 2.0h | - Khởi tạo REST API `SmartParking-API` trên API Gateway Console.<br>- Tạo routes `/checkin` và `/checkout`, tích hợp Lambda Proxy.<br>- Kích hoạt CORS (OPTIONS preflight) và deploy lên Stage `dev`.<br>- Cung cấp Invoke URL cho SV2 để phối hợp kiểm thử. | Ảnh chụp API Gateway Console trong `evidence/week2/02_apigateway_routes.png` |
| **18/10/2026**<br>(Thứ 7) | 14:00 - 16:00 | 2.0h | - Viết script tự động `scripts/test_api_endpoints.py` gửi request Base64 lên API Gateway.<br>- Kiểm thử các ca biên: ảnh mờ trả về UNKNOWN, vé không tồn tại 404, checkout vé 2 lần 400.<br>- Rà soát mã nguồn và đẩy code lên nhánh `dev`. | Script `scripts/test_api_endpoints.py`<br>Commit: `feat(test): add automated API integration test script` |

---

## ĐÁNH GIÁ KẾT QUẢ VÀ TỰ NHẬN XÉT
- **Tiến độ:** Hoàn thành 100% mục tiêu triển khai chức năng lõi trên AWS.
- **Khó khăn đã giải quyết:** Ban đầu khi gọi Rekognition từ ảnh Base64 gặp lỗi payload format, đã giải quyết bằng cách sử dụng `base64.b64decode` chuyển đổi sang binary bytes trước khi truyền vào param `Bytes` của Rekognition.
- **Kế hoạch tuần tiếp theo (Tuần 3):** Tích hợp giám sát CloudWatch Metrics/Alarms, thiết lập phân tích doanh thu qua Amazon Athena, và viết kịch bản tự động hóa Infrastructure as Code (IaC) hoặc CI/CD nếu có.
