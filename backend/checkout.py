import json
import datetime
import math
# import boto3

def calculate_fee(vehicle_type, checkin_time_str, checkout_time_str):
    """
    Thuật toán tính tiền theo block giờ.
    - Xe máy: 5.000đ/4h đầu, mỗi giờ tiếp theo +2.000đ
    - Ô tô: 20.000đ/2h đầu, mỗi giờ tiếp theo +10.000đ
    """
    # Chuyển đổi chuỗi ISO 8601 sang đối tượng datetime
    checkin = datetime.datetime.fromisoformat(checkin_time_str.replace('Z', '+00:00'))
    checkout = datetime.datetime.fromisoformat(checkout_time_str.replace('Z', '+00:00'))
    
    delta = checkout - checkin
    # Quy đổi ra tổng số giờ đỗ (làm tròn lên, ví dụ đỗ 1h15p tính là 2h)
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
            
    return fee

def lambda_handler(event, context):
    """
    Hàm Lambda xử lý yêu cầu Check-out (Xe ra)
    """
    try:
        body = json.loads(event.get("body", "{}"))
        ticket_id = body.get("ticketId")
        
        # 1. Lấy thông tin vé từ DynamoDB (Giả lập)
        # Giả sử xe máy này đã đỗ được 5 tiếng (vượt 4h đầu) -> Phí dự kiến: 5000 + 1*2000 = 7000đ
        mock_db_record = {
            "ticketId": ticket_id,
            "vehicleType": "MOTORBIKE",
            "checkinTime": (datetime.datetime.utcnow() - datetime.timedelta(hours=5)).isoformat() + "Z",
            "status": "PARKED"
        }
        
        if not mock_db_record:
            return {
                "statusCode": 404,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": "Ticket not found"})
            }
            
        checkout_time = datetime.datetime.utcnow().isoformat() + "Z"
        
        # 2. Tính tiền xe
        fee = calculate_fee(
            mock_db_record["vehicleType"], 
            mock_db_record["checkinTime"], 
            checkout_time
        )
        
        # 3. Cập nhật trạng thái COMPLETED và lưu tiền vào DynamoDB (Giả lập)
        # dynamodb.update_item(...)
        
        response_body = {
            "message": "Check-out thành công",
            "ticketId": ticket_id,
            "checkoutTime": checkout_time,
            "totalHours": math.ceil((datetime.datetime.utcnow() - datetime.datetime.fromisoformat(mock_db_record["checkinTime"].replace('Z', '+00:00')).replace(tzinfo=None)).total_seconds() / 3600),
            "fee": fee
        }
        
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
