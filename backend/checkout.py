import json
import datetime
import math
import base64
import os
import boto3
from decimal import Decimal

# Lấy cấu hình từ biến môi trường
BUCKET_NAME = os.environ.get("BUCKET_NAME", "smart-parking-images-24110207")
TABLE_NAME = os.environ.get("TABLE_NAME", "ParkingTickets")
REGION_NAME = os.environ.get("REGION_NAME", "us-east-1")

# Khởi tạo các AWS SDK clients
s3_client = boto3.client("s3", region_name=REGION_NAME)
dynamodb_resource = boto3.resource("dynamodb", region_name=REGION_NAME)
table = dynamodb_resource.Table(TABLE_NAME)

def calculate_fee(vehicle_type, checkin_time_str, checkout_time_str):
    """
    Thuật toán tính phí gửi xe theo block thời gian quy chuẩn:
    - Xe máy (MOTORBIKE): 5.000 VNĐ cho 4 giờ đầu, mỗi giờ tiếp theo +2.000 VNĐ.
    - Ô tô (CAR): 20.000 VNĐ cho 2 giờ đầu, mỗi giờ tiếp theo +10.000 VNĐ.
    """
    checkin = datetime.datetime.fromisoformat(checkin_time_str.replace("Z", "+00:00"))
    checkout = datetime.datetime.fromisoformat(checkout_time_str.replace("Z", "+00:00"))
    
    delta = checkout - checkin
    total_hours = math.ceil(delta.total_seconds() / 3600)
    if total_hours <= 0:
        total_hours = 1
        
    fee = 0
    if vehicle_type == "MOTORBIKE":
        fee = 5000
        if total_hours > 4:
            fee += (total_hours - 4) * 2000
    elif vehicle_type == "CAR":
        fee = 20000
        if total_hours > 2:
            fee += (total_hours - 2) * 10000
    else:
        # Mặc định tính như xe máy nếu loại xe khác
        fee = 5000
        if total_hours > 4:
            fee += (total_hours - 4) * 2000
            
    return fee, total_hours

def lambda_handler(event, context):
    """
    AWS Lambda Handler xử lý sự kiện Check-out (Xe ra & Tính tiền).
    """
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,Authorization"
    }
    
    # Xử lý CORS Preflight
    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": cors_headers, "body": json.dumps({"message": "OK"})}
        
    try:
        # 1. Parse request body
        body = event.get("body", {})
        if isinstance(body, str):
            body = json.loads(body) if body else {}
            
        ticket_id = body.get("ticketId")
        image_base64 = body.get("image")  # Ảnh xe ra (nếu có gửi kèm)
        
        if not ticket_id:
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({"error": "Mã vé (ticketId) là bắt buộc"}, ensure_ascii=False)
            }
            
        # 2. Truy vấn thông tin vé từ DynamoDB
        db_response = table.get_item(Key={"ticketId": ticket_id})
        ticket = db_response.get("Item")
        
        if not ticket:
            return {
                "statusCode": 404,
                "headers": cors_headers,
                "body": json.dumps({"error": f"Không tìm thấy vé xe với mã: {ticket_id}"}, ensure_ascii=False)
            }
            
        # 3. Kiểm tra tính hợp lệ: Vé đã thanh toán chưa?
        if ticket.get("status") == "COMPLETED":
            return {
                "statusCode": 400,
                "headers": cors_headers,
                "body": json.dumps({
                    "error": "Vé này đã được thanh toán và hoàn tất trước đó!",
                    "ticketId": ticket_id,
                    "previousCheckoutTime": ticket.get("checkoutTime"),
                    "fee": int(ticket.get("fee", 0))
                }, ensure_ascii=False)
            }
            
        # 4. Tính toán thời gian và phí gửi xe
        checkout_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
        fee, total_hours = calculate_fee(
            ticket.get("vehicleType", "MOTORBIKE"),
            ticket.get("checkinTime"),
            checkout_time
        )
        
        # 5. Nếu có ảnh xe ra, lưu vào S3 thư mục out/
        out_image_key = None
        if image_base64:
            try:
                if "," in image_base64:
                    image_base64 = image_base64.split(",")[1]
                out_bytes = base64.b64decode(image_base64)
                out_image_key = f"out/{ticket_id}.jpg"
                s3_client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=out_image_key,
                    Body=out_bytes,
                    ContentType="image/jpeg"
                )
            except Exception as img_err:
                print(f"Lỗi lưu ảnh out: {str(img_err)}")
                
        # 6. Cập nhật trạng thái COMPLETED và lưu tiền vào DynamoDB
        update_expr = "SET #st = :completed, checkoutTime = :checkoutTime, fee = :fee, totalHours = :totalHours"
        expr_names = {"#st": "status"}
        expr_values = {
            ":completed": "COMPLETED",
            ":checkoutTime": checkout_time,
            ":fee": Decimal(str(fee)),
            ":totalHours": Decimal(str(total_hours))
        }
        
        if out_image_key:
            update_expr += ", outImageKey = :outImageKey"
            expr_values[":outImageKey"] = out_image_key
            
        table.update_item(
            Key={"ticketId": ticket_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values
        )
        
        # 7. Trả về kết quả thanh toán
        response_data = {
            "message": "Check-out và thanh toán thành công",
            "ticketId": ticket_id,
            "plateNumber": ticket.get("plateNumber"),
            "vehicleType": ticket.get("vehicleType"),
            "checkinTime": ticket.get("checkinTime"),
            "checkoutTime": checkout_time,
            "totalHours": total_hours,
            "fee": fee,
            "status": "COMPLETED",
            "outImageKey": out_image_key
        }
        
        return {
            "statusCode": 200,
            "headers": cors_headers,
            "body": json.dumps(response_data, ensure_ascii=False)
        }
        
    except Exception as e:
        print(f"Check-out Exception: {str(e)}")
        return {
            "statusCode": 500,
            "headers": cors_headers,
            "body": json.dumps({"error": f"Lỗi máy chủ nội bộ: {str(e)}"}, ensure_ascii=False)
        }
