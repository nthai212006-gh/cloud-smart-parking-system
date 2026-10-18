"""
Script kiểm thử tự động API Gateway Endpoints (/checkin và /checkout)
Dự án: Hệ thống quản lý bãi giữ xe thông minh (Smart Parking System)
Học phần: Điện toán đám mây · Đợt 1 (2026 - 2027)
"""

import sys
import os
import base64
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

def send_http_post(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            status_code = response.getcode()
            res_body = json.loads(response.read().decode("utf-8"))
            return status_code, res_body
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_body)
        except Exception:
            return e.code, {"error": err_body}
    except Exception as ex:
        return 500, {"error": str(ex)}

def test_api_flow(api_base_url, sample_image_path):
    print("=" * 65)
    print("BẮT ĐẦU KIỂM THỬ TÍCH HỢP TOÀN TRÌNH API GATEWAY (TUẦN 2)")
    print(f"Endpoint: {api_base_url}")
    print("=" * 65)

    checkin_url = f"{api_base_url.rstrip('/')}/checkin"
    checkout_url = f"{api_base_url.rstrip('/')}/checkout"

    # Chuẩn bị ảnh Base64
    if not os.path.exists(sample_image_path):
        print(f"[!] Không tìm thấy file ảnh mẫu tại: {sample_image_path}")
        return

    with open(sample_image_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")

    # KỊCH BẢN 1: TEST CHECK-IN (XE VÀO)
    print("\n[KỊCH BẢN 1] Gửi yêu cầu Check-in xe máy...")
    checkin_payload = {
        "image": img_base64,
        "vehicleType": "MOTORBIKE"
    }
    status, checkin_res = send_http_post(checkin_url, checkin_payload)
    print(f"  --> HTTP Status: {status}")
    print(f"  --> Phản hồi từ Server: {json.dumps(checkin_res, ensure_ascii=False, indent=2)}")

    if status != 200 or "ticketId" not in checkin_res:
        print("[!] Check-in THẤT BẠI. Dừng kiểm thử.")
        return

    ticket_id = checkin_res["ticketId"]
    plate_number = checkin_res.get("plateNumber", "UNKNOWN")
    print(f"  ==> TẠO VÉ THÀNH CÔNG! Mã vé: {ticket_id} | Biển số nhận diện: {plate_number}")

    # Giả lập thời gian xe đỗ trong bãi (nghỉ 1 giây)
    print("\n[*] Giả lập thời gian xe đỗ trong bãi...")
    time.sleep(1)

    # KỊCH BẢN 2: TEST CHECK-OUT (XE RA & TÍNH PHÍ)
    print("\n[KỊCH BẢN 2] Gửi yêu cầu Check-out cho mã vé vừa tạo...")
    checkout_payload = {
        "ticketId": ticket_id
    }
    status, checkout_res = send_http_post(checkout_url, checkout_payload)
    print(f"  --> HTTP Status: {status}")
    print(f"  --> Phản hồi từ Server: {json.dumps(checkout_res, ensure_ascii=False, indent=2)}")

    if status == 200 and checkout_res.get("status") == "COMPLETED":
        fee = checkout_res.get("fee", 0)
        total_hours = checkout_res.get("totalHours", 1)
        print(f"  ==> THANH TOÁN THÀNH CÔNG! Số giờ đỗ: {total_hours}h | Tiền cước: {fee:,} VNĐ")
    else:
        print("[!] Check-out thất bại.")

    # KỊCH BẢN 3: TEST CHECK-OUT LẦN 2 (BẮT NGOẠI LỆ THANH TOÁN TRÙNG)
    print("\n[KỊCH BẢN 3] Thử gửi lại Check-out lần 2 cho vé đã thanh toán...")
    status3, res3 = send_http_post(checkout_url, checkout_payload)
    print(f"  --> HTTP Status: {status3} (Kỳ vọng: 400 Bad Request)")
    if status3 == 400:
        print("  ==> Bắt ngoại lệ thanh toán trùng lặp: ĐẠT TIÊU CHUẨN!")
    else:
        print("  [!] Chưa chặn được thanh toán trùng lặp.")

    # KỊCH BẢN 4: TEST VÉ KHÔNG TỒN TẠI (404)
    print("\n[KỊCH BẢN 4] Thử Check-out mã vé rác không tồn tại...")
    status4, res4 = send_http_post(checkout_url, {"ticketId": "fake-invalid-ticket-id"})
    print(f"  --> HTTP Status: {status4} (Kỳ vọng: 404 Not Found)")
    if status4 == 404:
        print("  ==> Bắt ngoại lệ 404 Not Found: ĐẠT TIÊU CHUẨN!")

    print("\n" + "=" * 65)
    print("HOÀN TẤT KIỂM THỬ TOÀN DIỆN API GATEWAY!")
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", type=str, default="http://localhost:3000", help="Invoke URL của API Gateway")
    parser.add_argument("--image", type=str, default="test-images/02_motor_clear/motor_clear_01.jpg", help="Đường dẫn ảnh test")
    args = parser.parse_args()
    test_api_flow(args.endpoint, args.image)
