"""
Script tự động hóa khởi tạo tài nguyên AWS cho Người 2 (Nguyễn Trung Hải - 24110207)
Dành cho: Học phần Điện toán đám mây - AWS Learner Lab (us-east-1)

Tài nguyên khởi tạo:
1. S3 Bucket: smart-parking-images-24110207 (Block Public Access = True)
   - Thư mục ảo: in/, out/, athena-logs/
2. DynamoDB Table: ParkingTickets (PK: ticketId [String], Capacity: On-Demand)
3. Gắn chuẩn 3 Tag: Project=SmartParking, Owner=24110207, Environment=Development

Cách dùng:
- Yêu cầu cài đặt: pip install boto3
- Cấu hình AWS CLI với AWS Learner Lab credentials hoặc chạy trực tiếp trong AWS CloudShell.
"""

import boto3
import sys

REGION = "us-east-1"
MSSV = "24110207"
BUCKET_NAME = f"smart-parking-images-{MSSV}"
TABLE_NAME = "ParkingTickets"

TAGS = [
    {"Key": "Project", "Value": "SmartParking"},
    {"Key": "Owner", "Value": MSSV},
    {"Key": "Environment", "Value": "Development"}
]

TAGS_DICT = {tag["Key"]: tag["Value"] for tag in TAGS}

def create_s3_bucket(s3_client):
    print(f"\n[1/2] Đang tạo S3 Bucket: {BUCKET_NAME}...")
    try:
        # Với us-east-1, không truyền CreateBucketConfiguration
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f" -> Tạo bucket {BUCKET_NAME} thành công!")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f" -> Bucket {BUCKET_NAME} đã tồn tại trong tài khoản của bạn.")
    except Exception as e:
        print(f" [!] Lỗi tạo bucket: {e}")
        return False

    # Block public access
    try:
        s3_client.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        print(" -> Đã kích hoạt Block All Public Access.")
    except Exception as e:
        print(f" [!] Lỗi Block Public Access: {e}")

    # Gắn Tag cho S3
    try:
        s3_client.put_bucket_tagging(
            Bucket=BUCKET_NAME,
            Tagging={'TagSet': TAGS}
        )
        print(f" -> Đã gắn 3 thẻ Tag chuẩn: {TAGS_DICT}")
    except Exception as e:
        print(f" [!] Lỗi gắn Tag S3: {e}")

    # Tạo 3 folder ảo: in/, out/, athena-logs/
    for folder in ["in/", "out/", "athena-logs/"]:
        try:
            s3_client.put_object(Bucket=BUCKET_NAME, Key=folder)
            print(f" -> Đã tạo folder ảo: {folder}")
        except Exception as e:
            print(f" [!] Lỗi tạo folder {folder}: {e}")

    return True

def create_dynamodb_table(dynamodb_client):
    print(f"\n[2/2] Đang tạo DynamoDB Table: {TABLE_NAME}...")
    try:
        response = dynamodb_client.create_table(
            TableName=TABLE_NAME,
            KeySchema=[
                {'AttributeName': 'ticketId', 'KeyType': 'HASH'} # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'ticketId', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST', # On-Demand mode
            Tags=TAGS
        )
        print(f" -> Gửi yêu cầu tạo bảng {TABLE_NAME} thành công!")
        print(" -> Đang đợi bảng chuyển sang trạng thái ACTIVE...")
        waiter = dynamodb_client.get_waiter('table_exists')
        waiter.wait(TableName=TABLE_NAME)
        print(f" -> [THÀNH CÔNG] Bảng {TABLE_NAME} đã ACTIVE!")
        return True
    except dynamodb_client.exceptions.ResourceInUseException:
        print(f" -> Bảng {TABLE_NAME} đã tồn tại.")
        return True
    except Exception as e:
        print(f" [!] Lỗi tạo DynamoDB table: {e}")
        return False

def main():
    print("=" * 60)
    print(" KHỞI TẠO TÀI NGUYÊN AWS CHO SMART PARKING SYSTEM")
    print(f" Sinh viên: Nguyễn Trung Hải | MSSV: {MSSV} | Region: {REGION}")
    print("=" * 60)

    try:
        s3 = boto3.client('s3', region_name=REGION)
        dynamodb = boto3.client('dynamodb', region_name=REGION)
    except Exception as e:
        print(f"[!] Lỗi kết nối AWS SDK: {e}")
        print("[!] Hãy chắc chắn bạn đã cấu hình AWS credentials hợp lệ.")
        sys.exit(1)

    s3_ok = create_s3_bucket(s3)
    ddb_ok = create_dynamodb_table(dynamodb)

    if s3_ok and ddb_ok:
        print("\n" + "=" * 60)
        print(" [HOÀN TẤT] Mọi tài nguyên S3 và DynamoDB đã sẵn sàng!")
        print(f" 1. S3 Bucket: {BUCKET_NAME} (có in/, out/, athena-logs/)")
        print(f" 2. DynamoDB: {TABLE_NAME} (PK: ticketId, On-Demand)")
        print(" Đừng quên chụp ảnh màn hình lưu vào evidence/week1/ nhé!")
        print("=" * 60)

if __name__ == "__main__":
    main()
