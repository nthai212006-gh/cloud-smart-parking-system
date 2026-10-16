"""
Script kiểm tra và xác thực hạ tầng AWS cho Người 2 (Nguyễn Trung Hải - 24110207)
Học phần: Điện toán đám mây · Đợt 1 (2026 - 2027)

Nhiệm vụ:
1. Kiểm tra kết nối S3 Bucket 'smart-parking-images-24110207' & tự động cấu hình CORS.
2. Kiểm tra trạng thái bảng DynamoDB 'ParkingTickets'.
3. Xác thực quyền gọi Rekognition API của LabRole.
"""

import sys
import boto3
from botocore.exceptions import ClientError

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REGION = "us-east-1"
BUCKET_NAME = "smart-parking-images-24110207"
TABLE_NAME = "ParkingTickets"

def check_and_configure_s3_cors(s3_client):
    print(f"\n[1/3] Đang kiểm tra S3 Bucket: {BUCKET_NAME}...")
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
        print(f"  --> S3 Bucket '{BUCKET_NAME}' tồn tại và đang hoạt động.")
    except ClientError as e:
        print(f"  [!] Lỗi truy cập S3 Bucket: {e}")
        return False

    # Cấu hình CORS tự động
    cors_configuration = {
        'CORSRules': [{
            'AllowedHeaders': ['*'],
            'AllowedMethods': ['GET', 'PUT', 'POST', 'HEAD'],
            'AllowedOrigins': ['*'],
            'ExposeHeaders': []
        }]
    }
    try:
        s3_client.put_bucket_cors(Bucket=BUCKET_NAME, CORSConfiguration=cors_configuration)
        print("  --> Đã cấu hình thành công S3 CORS Policy cho Web client.")
        return True
    except ClientError as e:
        print(f"  [!] Lỗi khi cấu hình S3 CORS: {e}")
        return False

def check_dynamodb(dynamodb_client):
    print(f"\n[2/3] Đang kiểm tra bảng DynamoDB: {TABLE_NAME}...")
    try:
        res = dynamodb_client.describe_table(TableName=TABLE_NAME)
        status = res['Table']['TableStatus']
        item_count = res['Table'].get('ItemCount', 0)
        print(f"  --> Bảng '{TABLE_NAME}' trạng thái: {status} (Số bản ghi hiện tại: {item_count})")
        return True
    except ClientError as e:
        print(f"  [!] Lỗi truy cập DynamoDB: {e}")
        return False

def check_rekognition_permission(rekognition_client):
    print("\n[3/3] Đang kiểm tra quyền gọi Amazon Rekognition của LabRole...")
    # 1 pixel JPEG bytes nhỏ nhất để test quyền gọi API
    tiny_jpeg = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00`\x00`\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' \",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xbf\x00\xff\xd9'
    try:
        rekognition_client.detect_text(Image={'Bytes': tiny_jpeg})
        print("  --> Xác thực quyền LabRole với Amazon Rekognition: THÀNH CÔNG (Có quyền rekognition:DetectText).")
        return True
    except ClientError as e:
        code = e.response.get('Error', {}).get('Code')
        if code == "InvalidImageFormatException":
            # API gọi được vào service chứng tỏ IAM role cho phép
            print("  --> Xác thực quyền LabRole với Amazon Rekognition: THÀNH CÔNG (IAM cho phép gọi).")
            return True
        print(f"  [!] Quyền Rekognition bị chặn: {e}")
        return False

def main():
    print("=" * 60)
    print("KIỂM TRA HẠ TẦNG VÀ XÁC THỰC QUYỀN LABROLE - TUẦN 2")
    print("Sinh viên: Nguyễn Trung Hải | MSSV: 24110207 | Region: us-east-1")
    print("=" * 60)
    
    try:
        s3 = boto3.client("s3", region_name=REGION)
        dynamodb = boto3.client("dynamodb", region_name=REGION)
        rekognition = boto3.client("rekognition", region_name=REGION)
    except Exception as e:
        print(f"\n[!] Chưa tìm thấy AWS Credentials trên máy: {e}")
        print("  (Hãy cấu hình AWS CLI credentials từ mục 'AWS Details' trong Learner Lab)")
        return

    s1 = check_and_configure_s3_cors(s3)
    s2 = check_dynamodb(dynamodb)
    s3_status = check_rekognition_permission(rekognition)

    print("\n" + "=" * 60)
    if s1 and s2 and s3_status:
        print("KẾT QUẢ: 100% HẠ TẦNG VÀ QUYỀN TRUY CẬP ĐÃ SẴN SÀNG CHO TUẦN 2!")
    else:
        print("KẾT QUẢ: Cần kiểm tra lại các mục báo lỗi ở trên.")
    print("=" * 60)

if __name__ == "__main__":
    main()
