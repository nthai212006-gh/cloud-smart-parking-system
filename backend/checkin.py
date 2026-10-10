import json
import uuid
import datetime
# import boto3 # Sẽ dùng khi deploy lên AWS thật

def lambda_handler(event, context):
    """
    Hàm Lambda xử lý yêu cầu Check-in (Xe vào)
    """
    try:
        # 1. Parse body từ API Gateway
        body = json.loads(event.get("body", "{}"))
        image_base64 = body.get("image")
        vehicle_type = body.get("vehicleType", "MOTORBIKE")
        
        # 2. Gọi AWS Rekognition để nhận diện biển số (Giả lập)
        plate_number = extract_plate(image_base64)
        
        # Nếu ảnh mờ không đọc được biển số -> Gán cờ UNKNOWN để bảo vệ nhập tay
        if not plate_number:
            plate_number = "UNKNOWN"
            
        # 3. Tạo thông tin vé
        ticket_id = str(uuid.uuid4())
        # Lưu thời gian theo chuẩn ISO 8601 (UTC)
        checkin_time = datetime.datetime.utcnow().isoformat() + "Z"
        
        # 4. Lưu vào DynamoDB (Giả lập PutItem)
        # dynamodb.put_item(...)
        
        # 5. Lưu ảnh vào S3 (Giả lập PutObject)
        # s3.put_object(Bucket="smart-parking-images", Key=f"in/{ticket_id}.jpg", ...)
        
        response_body = {
            "message": "Check-in thành công" if plate_number != "UNKNOWN" else "Ảnh mờ, cần nhập biển số thủ công",
            "ticketId": ticket_id,
            "plateNumber": plate_number,
            "checkinTime": checkin_time,
            "status": "PARKED"
        }
        
        # BẮT BUỘC: Luôn trả về CORS headers để frontend gọi không bị lỗi chéo domain
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps(response_body)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": str(e)})
        }

def extract_plate(image_base64):
    """ Hàm mô phỏng Rekognition """
    if not image_base64 or "BLURRY" in image_base64:
        return None
    return "59X112345"
