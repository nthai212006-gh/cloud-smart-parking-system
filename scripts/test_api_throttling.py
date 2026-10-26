"""
Script kiểm thử tự động tính năng Bảo mật API Gateway Throttling & Rate Limiting
Phụ trách: Sinh viên 1 (Lê Cao Việt Tín - MSSV: 24110354)
Đề tài: Hệ thống Quản lý Bãi giữ xe Thông minh (Smart Parking System)
Học phần: Điện toán đám mây · AWS Learner Lab (us-east-1)

Mục tiêu:
  - Gửi dồn dập 30 HTTP requests trong vòng 1 giây đến API Gateway Stage dev.
  - Xác thực cơ chế Throttling (Rate: 10 req/s, Burst: 20 req) hoạt động đúng thiết kế.
  - Kỳ vọng: Các request vượt ngưỡng burst sẽ bị từ chối với mã lỗi HTTP 429 Too Many Requests.

Cách sử dụng:
  python scripts/test_api_throttling.py --endpoint https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev/checkin
"""

import sys
import os
import json
import time
import argparse
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Mã màu ANSI hiển thị trên Terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def send_request(req_id, endpoint_url, payload_data):
    """Gửi một HTTP POST request và ghi nhận status code cùng thời gian đáp ứng."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    encoded_data = json.dumps(payload_data).encode("utf-8")
    req = urllib.request.Request(endpoint_url, data=encoded_data, headers=headers, method="POST")

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            latency = (time.time() - start_time) * 1000
            return req_id, response.getcode(), latency, None
    except urllib.error.HTTPError as e:
        latency = (time.time() - start_time) * 1000
        return req_id, e.code, latency, e.reason
    except Exception as ex:
        latency = (time.time() - start_time) * 1000
        return req_id, 0, latency, str(ex)

def run_throttling_test(endpoint_url, total_requests=30, concurrency=15):
    print(f"\n{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}KIỂM THỬ BẢO MẬT API GATEWAY THROTTLING & RATE LIMITING{RESET}")
    print(f"Người thực hiện: Lê Cao Việt Tín (MSSV: 24110354) | Region: us-east-1")
    print(f"Mục tiêu endpoint: {CYAN}{endpoint_url}{RESET}")
    print(f"Cấu hình thử nghiệm: Gửi dồn dập {total_requests} requests (Độ song song: {concurrency})")
    print(f"Ngưỡng thiết lập: Rate Limit = 10 req/s, Burst Limit = 20 requests")
    print(f"{BOLD}{'='*70}{RESET}\n")

    # Payload tối giản để kích hoạt API Gateway xử lý nhanh
    test_payload = {
        "vehicleType": "MOTORBIKE",
        "image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
    }

    start_all = time.time()
    results = []

    print("[*] Đang gửi đồng thời 30 requests đến API Gateway...")
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(send_request, i + 1, endpoint_url, test_payload) for i in range(total_requests)]
        for f in as_completed(futures):
            results.append(f.result())

    total_duration = time.time() - start_all
    results.sort(key=lambda x: x[0]) # Sắp xếp theo thứ tự request ID

    # Thống kê mã phản hồi
    status_counts = {}
    latencies = []
    for req_id, status_code, latency, reason in results:
        status_counts[status_code] = status_counts.get(status_code, 0) + 1
        latencies.append(latency)

        status_color = GREEN if status_code in [200, 400] else (YELLOW if status_code == 429 else RED)
        status_tag = f"{status_color}[HTTP {status_code}]{RESET}"
        reason_str = f"({reason})" if reason else ""
        print(f"  Request #{req_id:02d}: {status_tag} {latency:6.1f}ms {reason_str}")

    # Bảng phân tích kết quả
    print(f"\n{BOLD}{'-'*70}{RESET}")
    print(f"{BOLD}KẾT QUẢ THỐNG KÊ CHI TIẾT:{RESET}")
    print(f"  - Tổng thời gian hoàn thành : {total_duration:.2f} giây")
    print(f"  - Tốc độ gửi thực tế        : {total_requests / total_duration:.1f} requests/giây")
    print(f"  - Độ trễ trung bình         : {sum(latencies)/len(latencies):.1f} ms")
    print(f"  - Phân bổ mã HTTP phản hồi  :")
    for code, cnt in sorted(status_counts.items()):
        pct = (cnt / total_requests) * 100
        desc = "Thành công / Xử lý" if code in [200, 400] else ("Bị chặn bởi Throttling (ĐẠT YÊU CẦU)" if code == 429 else "Lỗi khác")
        print(f"      + HTTP {code:<3} : {cnt:2d} requests ({pct:5.1f}%) -> {desc}")

    print(f"{BOLD}{'-'*70}{RESET}")
    if 429 in status_counts and status_counts[429] > 0:
        print(f"{GREEN}{BOLD}>>> XÁC THỰC THÀNH CÔNG: API Gateway đã kích hoạt Throttling chặn {status_counts[429]} requests vượt ngưỡng (HTTP 429)! <<<{RESET}")
        print(f"{GREEN}Hệ thống Serverless được bảo vệ an toàn khỏi tấn công DoS và cạn kiệt ngân sách Lab.{RESET}")
    else:
        print(f"{YELLOW}[LƯU Ý] Chưa ghi nhận phản hồi HTTP 429. Hãy đảm bảo bạn đã cấu hình Throttling trên Stage 'dev' (Rate: 10, Burst: 20) và Deploy API.{RESET}")
    print(f"{BOLD}{'='*70}{RESET}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kiểm thử API Gateway Throttling")
    parser.add_argument("--endpoint", default="https://fdbsdxyto1.execute-api.us-east-1.amazonaws.com/dev/checkin",
                        help="API Gateway Checkin URL để kiểm thử Throttling")
    parser.add_argument("--count", type=int, default=30, help="Tổng số request gửi dồn dập (mặc định 30)")
    args = parser.parse_args()

    run_throttling_test(args.endpoint, total_requests=args.count)
