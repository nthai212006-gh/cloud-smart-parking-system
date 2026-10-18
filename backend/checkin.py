import json
import uuid
import datetime
import base64
import os
import re
import boto3

# Lấy cấu hình từ biến môi trường (mặc định nếu chưa set)
BUCKET_NAME = os.environ.get("BUCKET_NAME", "smart-parking-images-24110207")
TABLE_NAME = os.environ.get("TABLE_NAME", "ParkingTickets")
REGION_NAME = os.environ.get("REGION_NAME", "us-east-1")

# Khởi tạo các AWS SDK clients
s3_client = boto3.client("s3", region_name=REGION_NAME)
dynamodb_resource = boto3.resource("dynamodb", region_name=REGION_NAME)
rekognition_client = boto3.client("rekognition", region_name=REGION_NAME)
table = dynamodb_resource.Table(TABLE_NAME)

def clean_license_plate(text_lines):
    """
    Chuẩn hóa và ghép các dòng văn bản thành biển số chuẩn.
    Loại bỏ khoảng trắng, dấu chấm, gạch ngang, chỉ giữ chữ và số.
    """
    raw_text = "".join(text_lines)
    cleaned_plate = re.sub(r'[^A-Z0-9]', '', raw_text.upper())
    return cleaned_plate

def extract_plate_from_bytes(image_bytes):
    """
    Gọi Amazon Rekognition DetectText để nhận diện biển số từ bytes ảnh.
    """
    try:
        response = rekognition_client.detect_text(Image={"Bytes": image_bytes})
        text_lines = []
        for item in response.get("TextDetections", []):
            if item.get("Type") == "LINE" and item.get("Confidence", 0) >= 70.0:
                text_lines.append(item.get("DetectedText", ""))
        
        plate = clean_license_plate(text_lines)
        return plate if len(plate) >= 4 else None
    except Exception as e:
        print(f"Lỗi khi gọi Rekognition: {str(e)}")
        return None

def lambda_handler(event, context):
    """
    AWS Lambda Handler xử lý sự kiện Check-in (Xe vào).
    Hỗ trợ cả gọi trực tiếp từ API Gateway (Lambda Proxy Integration) hoặc test console.
    """
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization"
    }
    
    # Xử lý CORS Preflight request nếu có
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": cors_headers, "body": json.dumps({"message": "OK"})}
        
    try:
        # 1. Parse body từ API Gateway
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body) if body else {}
            
        image_base64 = body.get("image", "")
        vehicle_type = body.get("vehicleType", "MOTORBIKE").upper()
        if vehicle_type not in ["MOTORBIKE", "CAR"]:
            vehicle_type = "MOTORBIKE"
            
        if not image_base64:
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"error": "Thiếu dữ liệu ảnh (image base64 is required)"})
            }
            
        # 2. Giải mã Base64 thành binary bytes
        # Loại bỏ header data:image/jpeg;base64, nếu client gửi kèm
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]
        image_bytes = base64.b64decode(image_base64)
        
        # 3. Nhận diện biển số bằng Amazon Rekognition
        plate_number = extract_plate_from_bytes(image_bytes)
        is_unknown = False
        if not plate_number:
            plate_number = "UNKNOWN"
            is_unknown = True
            
        # 4. Khởi tạo mã vé và thời gian check-in theo chuẩn ISO 8601
        ticket_id = str(uuid.uuid4())
        checkin_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        image_key = f"in/{ticket_id}.jpg"
        
        # 5. Lưu ảnh xe vào lên Amazon S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=image_key,
            Body=image_bytes,
            ContentType="image/jpeg"
        )
        
        # 6. Ghi thông tin vé xe vào Amazon DynamoDB
        table.put_item(
            Item={
                "ticketId": ticket_id,
                "plateNumber": plate_number,
                "vehicleType": vehicle_type,
                "checkinTime": checkin_time,
                "status": "PARKED",
                "inImageKey": image_key
            }
        )
        
        # 7. Trả về kết quả
        response_body = {
            "message": "Check-in thành công" if not is_unknown else "Ảnh không rõ biển số, đã gán UNKNOWN để bảo vệ can thiệp thủ công",
            "ticketId": ticket_id,
            "plateNumber": plate_number,
            "vehicleType": vehicle_type,
            "checkinTime": checkin_time,
            "status": "PARKED",
            "inImageKey": image_key
        }
        
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(response_body, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Check-in Exception: {str(e)}")
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": f"Lỗi máy chủ nội bộ: {str(e)}"}, ensure_ascii=False)
        }
