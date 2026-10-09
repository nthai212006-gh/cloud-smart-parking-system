# Backend Lambda Functions
Chứa mã nguồn các hàm AWS Lambda (Python 3.11):
- `checkin.py`: Lambda xử lý xe vào (nhận diện biển số Rekognition, ghi DynamoDB, lưu ảnh S3 in/)
- `checkout.py`: Lambda xử lý xe ra (nhận diện biển số, tính phí gửi xe, cập nhật trạng thái DynamoDB, lưu ảnh S3 out/)
