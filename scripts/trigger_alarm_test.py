"""
Script kích hoạt lỗi kiểm thử CloudWatch Alarms (Tuần 3)
Dự án: Hệ thống quản lý bãi giữ xe thông minh (Smart Parking System)
Học phần: Điện toán đám mây · Đợt 1 (2026 - 2027)

Mục đích:
Gửi các payload không hợp lệ liên tục để cố tình gây lỗi nội bộ tại Lambda,
làm tăng metric 'Errors', giúp kích hoạt CloudWatch Alarm 'SmartParking-Lambda-Errors'
chuyển sang trạng thái 'In ALARM' để phục vụ chụp ảnh minh chứng.
"""

import sys
import json
import time
import argparse
import urllib.request
import urllib.error

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def trigger_lambda_errors(endpoint_url, count=5):
    checkin_url = f"{endpoint_url.rstrip('/')}/checkin"
    print("=" * 65)
    print("BẮT ĐẦU KÍCH HOẠT LỖI KIỂM THỬ CLOUDWATCH ALARMS")
    print(f"Target URL: {checkin_url}")
    print(f"Số lượng requests lỗi dự kiến: {count}")
    print("=" * 65)

    # Payload cố tình chứa chuỗi Base64 hỏng để gây lỗi giải mã / Rekognition
    corrupt_payload = {
        "image": "THIS_IS_AN_INVALID_CORRUPT_BASE64_STRING_FOR_TESTING_ALARMS!!!",
        "vehicleType": "INVALID_VEHICLE_TYPE"
    }
    data = json.dumps(corrupt_payload).encode("utf-8")

    for i in range(1, count + 1):
        print(f"\n[*] Đang gửi request lỗi #{i}...")
        req = urllib.request.Request(
            checkin_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                print(f"  --> HTTP Status: {response.getcode()} (Bình thường)")
        except urllib.error.HTTPError as e:
            print(f"  --> HTTP Status: {e.code} (Lỗi như kỳ vọng - Lambda Exception ghi nhận)")
        except Exception as ex:
            print(f"  --> Exception: {str(ex)}")
        time.sleep(1)

    print("\n" + "=" * 65)
    print("ĐÃ GỬI XONG CÁC REQUESTS LỖI!")
    print("Metric 'Errors' trên CloudWatch sẽ cập nhật trong 1-3 phút tới.")
    print("Vui lòng mở CloudWatch Alarms Console để quan sát trạng thái chuyển sang 'In ALARM'!")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--endpoint",
        type=str,
        default="https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev",
        help="Invoke URL của API Gateway Stage dev"
    )
    parser.add_argument("--count", type=int, default=5, help="Số lần gửi lỗi")
    args = parser.parse_args()
    trigger_lambda_errors(args.endpoint, args.count)
