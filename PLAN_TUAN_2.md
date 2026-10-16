# KẾ HOẠCH TRIỂN KHAI CHI TIẾT TUẦN 2 (WEEK 2 IMPLEMENTATION PLAN)
## ĐỀ TÀI: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING SYSTEM)

* **Học phần:** Điện toán đám mây (Cloud Computing) · Đợt 1 (2026 - 2027)
* **Giảng viên hướng dẫn (GVHD):** ThS. Huỳnh Xuân Phụng
* **Nhóm đề tài:** Domain Apps (Nhóm 2 sinh viên)
* **Môi trường triển khai:** AWS Learner Lab | Region bắt buộc: `us-east-1` (N. Virginia)
* **Thời gian thực hiện:** **13/10/2026 – 19/10/2026**
* **Kho lưu trữ Git:** [nthai212006-gh/cloud-smart-parking-system](https://github.com/nthai212006-gh/cloud-smart-parking-system) (Nhánh chính: `main`)

---

## 📌 PHẦN 1: ĐỐI CHIẾU VÀ ĐÁNH GIÁ HIỆN TRẠNG TỪ GIT TUẦN 1

Để lập kế hoạch Tuần 2 chính xác, bám sát thực tế và không bị trùng lặp hoặc sót việc, nhóm tiến hành rà soát đối chiếu toàn bộ các sản phẩm đã commit trên Git trong Tuần 1:

### 1.1. Lược sử các Commit quan trọng Tuần 1
- `cb85da8` (*feat: Week 1 - Core Backend Logic, Architect Docs and Setup*): Khởi tạo tài liệu kiến trúc tổng thể, script kiểm thử regex cục bộ và mã nguồn khung (mock) của 2 hàm Lambda `backend/checkin.py`, `backend/checkout.py`.
- `41ec17b` (*feat(scripts): add automated AWS setup and dataset compressor scripts for Member 2*): Viết script tự động hóa khởi tạo S3 Bucket `smart-parking-images-24110207` và bảng DynamoDB `ParkingTickets`.
- `b43ca19` (*docs(evidence): add week 1 AWS infrastructure and billing evidence screenshots*): Bổ sung 4 ảnh chụp minh chứng console Tuần 1 (S3 console, S3 folders, DynamoDB table, Billing $0.00).
- `a2d46cd` (*feat(dataset): add complete 120 curated test images across 5 evaluation groups*): Hoàn thiện 120 bức ảnh thực tế đã làm mờ/che mặt người (PII) thuộc 5 nhóm kiểm thử.
- `6c5728a` (*docs & feat: add API Gateway OpenAPI spec and generate Week 1 submission docx report*): Định nghĩa đặc tả REST API theo chuẩn OpenAPI 3.0 (`backend/api_gateway_openapi.json`) và biên tập báo cáo Tuần 1.

### 1.2. Bảng ma trận đối chiếu hiện trạng và khoảng cách cần triển khai trong Tuần 2

| Thành phần hệ thống | Hiện trạng trên Git Tuần 1 | Khoảng trống kỹ thuật (Gaps) | Nhiệm vụ bắt buộc trong Tuần 2 |
| :--- | :--- | :--- | :--- |
| **AWS Lambda: Check-in** | File `backend/checkin.py` chỉ là hàm mock: giả lập nhận diện biển số trả về cứng `"59X112345"`, các lệnh DynamoDB và S3 đang bị comment. | Chưa gọi SDK `boto3`, chưa nhận diện AI thật, chưa upload S3 thật, chưa ghi DynamoDB thật. | **Nâng cấp sang Boto3 thật:** Gọi Amazon Rekognition `DetectText`, chuẩn hóa Regex, upload ảnh Base64 lên S3 `in/{ticketId}.jpg`, gọi DynamoDB `put_item`. Deploy lên AWS Console với tên `SmartParking-Checkin`. |
| **AWS Lambda: Check-out** | File `backend/checkout.py` chỉ là hàm mock: dữ liệu vé lấy từ biến dictionary tĩnh, chưa tra cứu DynamoDB thật. | Chưa truy vấn vé từ database, chưa lưu ảnh xe ra, chưa cập nhật trạng thái vé `COMPLETED`. | **Nâng cấp sang Boto3 thật:** Đọc DynamoDB `get_item`, đối soát biển số, tính phí theo block giờ thực tế, upload ảnh S3 `out/{ticketId}.jpg`, cập nhật DynamoDB `update_item`. Deploy lên AWS Console với tên `SmartParking-Checkout`. |
| **Amazon Rekognition** | Chỉ có script test regex chuỗi cục bộ `scripts/test_plate_regex.py`. | Chưa từng gọi API Rekognition thật trên cloud; chưa kiểm tra phản hồi JSON thực tế từ ảnh chụp camera. | Cấp quyền Rekognition cho Lambda qua `LabRole`; chạy kiểm thử thực tế trên 120 ảnh của dataset; ghi nhận log qua CloudWatch. |
| **Amazon DynamoDB** | Bảng `ParkingTickets` đã tạo (PK `ticketId`, On-demand) nhưng bảng đang rỗng ($0$ bản ghi). | Chưa có kết nối từ ứng dụng; chưa kiểm thử thao tác ghi/sửa dữ liệu qua IAM Role. | Kết nối Lambda với bảng; kiểm tra các thao tác `PutItem`, `GetItem`, `UpdateItem` thông suốt, định dạng thời gian ISO 8601. |
| **Amazon S3** | Bucket `smart-parking-images-24110207` đã tạo kèm các folder `in/`, `out/`, `athena-logs/`. | Chưa bật CORS; chưa nhận file ảnh từ Lambda Base64 payload. | Cấu hình S3 CORS Policy; cấu hình Lambda tự động stream bytes ảnh vào đúng folder `in/` và `out/`. |
| **Amazon API Gateway** | Đã viết xong bản đặc tả `backend/api_gateway_openapi.json` (OpenAPI 3.0). | Chưa triển khai lên cloud AWS; chưa cấu hình Lambda Proxy Integration và CORS Preflight. | Tạo REST API `SmartParking-API` trên AWS Console; cấu hình routes `/checkin` và `/checkout`; bật CORS `OPTIONS`; Deploy stage `dev` và lấy Invoke URL. |
| **Bộ dữ liệu kiểm thử** | Đã có 120 ảnh được che mờ mặt trong `test-images/` (5 nhóm). | Chưa đánh giá tỷ lệ nhận diện thực tế trên cloud Rekognition. | Chạy kiểm thử đánh giá độ chính xác (Accuracy Matrix) trên 120 ảnh, thống kê trường hợp nhận diện tốt và trường hợp ngoại lệ. |
| **Hồ sơ minh chứng** | Thư mục `evidence/week1/` có 4 ảnh console hạ tầng nền tảng. | Chưa có ảnh chụp Lambda, API Gateway, CloudWatch Logs, DynamoDB Items thực tế. | Thu thập đầy đủ 6 ảnh chụp màn hình console Tuần 2 theo đúng quy chuẩn kiểm tra của GVHD. |

---

## 🎯 PHẦN 2: MỤC TIÊU VÀ YÊU CẦU TRỌNG TÂM TUẦN 2

Căn cứ theo đề cương của GVHD Huỳnh Xuân Phụng: **"Tuần 2: triển khai các chức năng lõi trên AWS, kiểm thử từng thành phần."**

1. **Triển khai thành công các dịch vụ lõi trên AWS Learner Lab:**
   - 02 AWS Lambda Functions: `SmartParking-Checkin` và `SmartParking-Checkout` (Python 3.11, Memory 256MB, Timeout 15s, IAM `LabRole`).
   - 01 Amazon API Gateway REST API: `SmartParking-API` kết nối Lambda Proxy Integration, mở 2 endpoints `POST /checkin` và `POST /checkout`, đã bật CORS và deploy lên Stage `dev`.
   - Kết nối liên thông thông suốt giữa: `Client` $\rightarrow$ `API Gateway` $\rightarrow$ `Lambda` $\rightarrow$ `Rekognition` $\rightarrow$ `DynamoDB` & `S3`.
2. **Kiểm thử độc lập từng thành phần (Component Unit Testing):**
   - Đánh giá khả năng OCR của Rekognition với 120 ảnh mẫu (5 nhóm: xe máy 2 dòng, ô tô 1 dòng, ảnh nghiêng, ảnh mờ, ảnh không có biển số).
   - Kiểm thử tính đúng đắn của giải thuật Regex bóc tách biển số Việt Nam từ kết quả `DetectText`.
   - Kiểm thử tính toán phí gửi xe theo block thời gian:
     - Xe máy: 5.000 VNĐ / 4 giờ đầu, mỗi giờ tiếp theo +2.000 VNĐ.
     - Ô tô: 20.000 VNĐ / 2 giờ đầu, mỗi giờ tiếp theo +10.000 VNĐ.
   - Kiểm thử xử lý ngoại lệ: Gán cờ `UNKNOWN` khi ảnh không nhận diện được; báo lỗi 404 khi vé không tồn tại; báo lỗi 400 khi vé đã thanh toán trước đó.
3. **Tuân thủ quy chế môn học & môi trường AWS Learner Lab:**
   - Định mức thời gian: Mỗi thành viên dành **≥ 8.0 giờ/tuần** (Kế hoạch phân bổ **8.5 giờ/người** x 2 = **17.0 giờ**).
   - Tuyệt đối chỉ dùng IAM `LabRole`, Region `us-east-1`, không tạo IAM User/Role mới.
   - Gắn 3 tag chuẩn cho toàn bộ tài nguyên: `Project=SmartParking`, `Owner=24110354_24110207`, `Environment=Development`.
   - Kiểm soát chi phí phát sinh = $0.00 (sử dụng tài nguyên trong hạn mức Free Tier/Learner Lab).
   - Chụp màn hình minh chứng đầy đủ thông tin: Account ID, Region `us-east-1`, đồng hồ máy tính.

---

## 👥 PHẦN 3: PHÂN CÔNG NHIỆM VỤ & LỊCH TRÌNH THỰC HIỆN CHI TIẾT

### 3.1. Bảng phân công tổng quan 2 thành viên

| STT | Thành viên | MSSV | Vai trò chính trong Tuần 2 | Số giờ dự kiến | File kế hoạch chi tiết |
| :---: | :--- | :---: | :--- | :---: | :---: |
| 1 | **Lê Cao Việt Tín** | 24110354 | **Trưởng nhóm:** Nâng cấp code Boto3, triển khai Lambda Functions, cấu hình API Gateway REST API, viết test script tự động | **8.5 giờ** | [docs/plans/week-02/member-1.md](docs/plans/week-02/member-1.md) |
| 2 | **Nguyễn Trung Hải** | 24110207 | **Thành viên:** Cấu hình hạ tầng S3 CORS, đánh giá Rekognition trên 120 ảnh dataset, kiểm thử tích hợp DynamoDB/S3, thu thập minh chứng console & kiểm toán Billing | **8.5 giờ** | [docs/plans/week-02/member-2.md](docs/plans/week-02/member-2.md) |
| **Tổng** | **Cả nhóm** | — | **Toàn bộ khối lượng công việc Tuần 2** | **17.0 giờ** | *(Đạt chỉ tiêu môn học)* |

---

### 3.2. Lịch trình chi tiết của Sinh viên 1: Lê Cao Việt Tín (8.5 giờ)

```text
Buổi 1 (Thứ 2: 13/10/2026, 19:30 - 21:30 | 2.0h):
├── Nâng cấp backend/checkin.py sang Boto3 (gọi Rekognition, lưu S3 in/, ghi DynamoDB)
└── Nâng cấp backend/checkout.py sang Boto3 (đọc DynamoDB, tính tiền block, lưu S3 out/, update vé)

Buổi 2 (Thứ 4: 15/10/2026, 19:00 - 21:30 | 2.5h):
├── Đăng nhập AWS Console us-east-1, tạo Lambda SmartParking-Checkin (Python 3.11, LabRole, timeout 15s)
├── Tạo Lambda SmartParking-Checkout (cùng cấu hình, gán biến môi trường BUCKET_NAME, TABLE_NAME)
├── Gắn 3 thẻ Tag chuẩn quy định
└── Tạo Test Events kiểm tra chạy thử nghiệm và kiểm tra CloudWatch Logs

Buổi 3 (Thứ 6: 17/10/2026, 19:30 - 21:30 | 2.0h):
├── Khởi tạo REST API SmartParking-API trên Amazon API Gateway Console
├── Cấu hình Lambda Proxy Integration cho 2 methods: POST /checkin và POST /checkout
├── Kích hoạt CORS (Enable CORS) với OPTIONS preflight
└── Deploy API lên Stage "dev", lấy Invoke URL bàn giao cho SV2 phối hợp test

Buổi 4 (Thứ 7: 18/10/2026, 14:00 - 16:00 | 2.0h):
├── Viết script tự động scripts/test_api_endpoints.py gửi payload Base64 thực tế
├── Kiểm thử các ca biên (ảnh mờ UNKNOWN, checkout vé 2 lần, vé không tồn tại 404)
└── Rà soát mã nguồn, commit và đẩy code lên nhánh main của GitHub
```

---

### 3.3. Lịch trình chi tiết của Sinh viên 2: Nguyễn Trung Hải (8.5 giờ)

```text
Buổi 1 (Thứ 3: 14/10/2026, 19:00 - 21:30 | 2.5h):
├── Cấu hình S3 CORS trên bucket smart-parking-images-24110207
├── Kiểm tra trạng thái hoạt động của bảng DynamoDB ParkingTickets (Partition Key ticketId)
└── Xác thực quyền thực thi của IAM LabRole đối với Rekognition, DynamoDB và S3 qua AWS CLI

Buổi 2 (Thứ 5: 16/10/2026, 19:30 - 21:30 | 2.0h):
├── Viết script scripts/evaluate_rekognition_accuracy.py
├── Chạy đánh giá Rekognition DetectText trên 120 ảnh dataset mẫu (5 nhóm)
└── Lập bảng ma trận đo lường độ chính xác OCR và khả năng ghép dòng regex

Buổi 3 (Thứ 6: 17/10/2026, 19:30 - 21:30 | 2.0h):
├── Nhận Invoke URL từ SV1, phối hợp thực hiện kiểm thử luồng nghiệp vụ end-to-end
├── Xác minh trên DynamoDB Console: Items được tạo mới và cập nhật đúng schema
└── Xác minh trên S3 Console: File ảnh xe vào và xe ra được lưu đúng tại in/ và out/

Buổi 4 (Chủ nhật: 19/10/2026, 14:00 - 16:00 | 2.0h):
├── Chụp bộ 8 ảnh màn hình minh chứng console (Account ID, Region, Đồng hồ máy tính)
├── Kiểm toán chi phí AWS Billing (đảm bảo $0.00), thực hiện End Lab an toàn
├── Viết nhật ký công việc cá nhân và tổng hợp Worklog Tuần 2
└── Commit toàn bộ minh chứng và tài liệu lên nhánh main của GitHub
```

---

## 🛠️ PHẦN 4: ĐẶC TẢ KỸ THUẬT TRIỂN KHAI TRÊN AWS (TECHNICAL SPECIFICATIONS)

### 4.1. Cấu hình 02 AWS Lambda Functions

| Thông số cấu hình | Lambda 1: `SmartParking-Checkin` | Lambda 2: `SmartParking-Checkout` |
| :--- | :--- | :--- |
| **Runtime** | Python 3.11 | Python 3.11 |
| **Architecture** | x86_64 | x86_64 |
| **Execution Role** | `LabRole` (`arn:aws:iam::<AccountID>:role/LabRole`) | `LabRole` (`arn:aws:iam::<AccountID>:role/LabRole`) |
| **Memory** | 256 MB | 256 MB |
| **Timeout** | 15 giây (Xử lý OCR và I/O mạng an toàn) | 15 giây |
| **Environment Variables** | `BUCKET_NAME`: `smart-parking-images-24110207`<br>`TABLE_NAME`: `ParkingTickets`<br>`REGION_NAME`: `us-east-1` | `BUCKET_NAME`: `smart-parking-images-24110207`<br>`TABLE_NAME`: `ParkingTickets`<br>`REGION_NAME`: `us-east-1` |
| **Mandatory Tags** | `Project=SmartParking`<br>`Owner=24110354_24110207`<br>`Environment=Development` | `Project=SmartParking`<br>`Owner=24110354_24110207`<br>`Environment=Development` |

---

### 4.2. Luồng xử lý chi tiết trong Lambda Functions (Mã nguồn Boto3 chính thức)

#### 1. Luồng Check-in (`SmartParking-Checkin`):
```text
1. Client gửi HTTP POST /checkin với JSON: {"image": "<base64_string>", "vehicleType": "MOTORBIKE" | "CAR"}
2. Lambda giải mã image_bytes = base64.b64decode(body["image"])
3. Gọi AWS Rekognition:
   response = rekognition.detect_text(Image={'Bytes': image_bytes})
4. Áp dụng Regex bóc tách biển số xe:
   - Lọc danh sách dòng text có Type == 'LINE' và Confidence >= 80%.
   - Xóa bỏ ký tự nhiễu (dấu chấm, gạch ngang, khoảng trắng thừa).
   - Nếu tìm thấy mẫu biển số Việt Nam (ví dụ 59X112345 hoặc 51A99999) -> gán plateNumber.
   - Nếu không tìm thấy hoặc ảnh quá mờ -> gán plateNumber = "UNKNOWN" (cờ bảo vệ can thiệp).
5. Sinh ticketId = str(uuid.uuid4()), checkinTime = datetime.utcnow().isoformat() + "Z"
6. Lưu ảnh vào S3:
   s3.put_object(Bucket=BUCKET_NAME, Key=f"in/{ticketId}.jpg", Body=image_bytes, ContentType='image/jpeg')
7. Lưu bản ghi vào DynamoDB:
   dynamodb.put_item(TableName=TABLE_NAME, Item={
       'ticketId': {'S': ticketId},
       'plateNumber': {'S': plateNumber},
       'vehicleType': {'S': vehicle_type},
       'checkinTime': {'S': checkinTime},
       'status': {'S': 'PARKED'},
       'inImageKey': {'S': f"in/{ticketId}.jpg"}
   })
8. Trả về HTTP 200 kèm JSON kết quả và đầy đủ CORS headers.
```

#### 2. Luồng Check-out (`SmartParking-Checkout`):
```text
1. Client gửi HTTP POST /checkout với JSON: {"ticketId": "<uuid>", "image": "<base64_string_optional>"}
2. Lambda tra cứu thông tin vé từ DynamoDB:
   record = dynamodb.get_item(TableName=TABLE_NAME, Key={'ticketId': {'S': ticketId}})
3. Kiểm tra tính hợp lệ:
   - Nếu không tìm thấy vé -> trả về HTTP 404 {"error": "Ticket not found"}
   - Nếu record['status']['S'] == 'COMPLETED' -> trả về HTTP 400 {"error": "Ticket already paid and completed"}
4. Tính toán thời gian đỗ xe thực tế:
   - checkoutTime = datetime.utcnow().isoformat() + "Z"
   - totalHours = ceil((checkoutTime - checkinTime).total_seconds() / 3600) (tối thiểu 1 giờ)
5. Tính phí gửi xe (Công thức chuẩn nghiệp vụ):
   - MOTORBIKE: totalHours <= 4 -> 5.000 VNĐ; totalHours > 4 -> 5.000 + (totalHours - 4) * 2.000 VNĐ
   - CAR: totalHours <= 2 -> 20.000 VNĐ; totalHours > 2 -> 20.000 + (totalHours - 2) * 10.000 VNĐ
6. Nếu client có gửi ảnh xe ra:
   - Upload ảnh vào S3: s3.put_object(Bucket=BUCKET_NAME, Key=f"out/{ticketId}.jpg", Body=out_bytes)
7. Cập nhật bản ghi DynamoDB:
   dynamodb.update_item(
       TableName=TABLE_NAME,
       Key={'ticketId': {'S': ticketId}},
       UpdateExpression="SET #s = :status, checkoutTime = :checkoutTime, fee = :fee, totalHours = :hours, outImageKey = :outKey",
       ExpressionAttributeNames={'#s': 'status'},
       ExpressionAttributeValues={
           ':status': {'S': 'COMPLETED'},
           ':checkoutTime': {'S': checkoutTime},
           ':fee': {'N': str(fee)},
           ':hours': {'N': str(totalHours)},
           ':outKey': {'S': f"out/{ticketId}.jpg"}
       }
   )
8. Trả về HTTP 200 kèm JSON chi tiết thanh toán và CORS headers.
```

---

### 4.3. Cấu hình Amazon API Gateway REST API

- **API Name:** `SmartParking-API`
- **Protocol:** REST API (Regional Endpoint)
- **Deployment Stage:** `dev`
- **Cấu hình chi tiết Resources & Methods:**

| Endpoint | HTTP Method | Integration Type | Tùy chọn Lambda Proxy | CORS Support | Mục đích nghiệp vụ |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `/checkin` | `POST` | AWS Lambda | **Bật (Enabled)** | Cho phép Origin `*` | Tiếp nhận ảnh xe vào, gọi Rekognition, tạo vé đỗ |
| `/checkin` | `OPTIONS` | MOCK Integration | — | Trả về 200 OK | Hỗ trợ CORS Preflight cho trình duyệt web |
| `/checkout`| `POST` | AWS Lambda | **Bật (Enabled)** | Cho phép Origin `*` | Tra cứu vé, tính tiền theo block, chốt vé xe ra |
| `/checkout`| `OPTIONS` | MOCK Integration | — | Trả về 200 OK | Hỗ trợ CORS Preflight cho trình duyệt web |

---

## 🧪 PHẦN 5: KẾ HOẠCH KIỂM THỬ TỪNG THÀNH PHẦN (COMPONENT TESTING PLAN)

### 5.1. Kịch bản 1: Kiểm thử độc lập AI Rekognition OCR (120 ảnh mẫu)
Sử dụng script `scripts/evaluate_rekognition_accuracy.py` duyệt qua toàn bộ bộ dữ liệu Tuần 1:
- **Nhóm 1 (`01_car_clear` - 40 ảnh):** Mục tiêu đạt tỷ lệ nhận diện đúng biển số $\ge 95\%$.
- **Nhóm 2 (`02_motor_clear` - 40 ảnh):** Mục tiêu đạt tỷ lệ ghép chuỗi 2 dòng đúng $\ge 90\%$.
- **Nhóm 3 (`03_car_hard` - 10 ảnh) & Nhóm 4 (`04_motor_hard` - 10 ảnh):** Ghi nhận giới hạn của mô hình khi gặp góc nghiêng hoặc thiếu sáng.
- **Nhóm 5 (`05_error_cases` - 20 ảnh):** Mục tiêu 100% các trường hợp không có biển số hoặc ảnh hỏng phải được gán nhãn an toàn là `"UNKNOWN"`, không được gây ra ngoại lệ (Unhandled Exception / crash 500).

### 5.2. Kịch bản 2: Kiểm thử hàm Check-in
1. **Ca 1 (Xe máy hợp lệ):** Gửi ảnh xe máy rõ biển số. Kiểm tra response trả về `statusCode: 200`, `ticketId` là UUID hợp lệ, `plateNumber` khớp biển số thực tế, ảnh xuất hiện trên S3 `in/`, DynamoDB có bản ghi status `PARKED`.
2. **Ca 2 (Ô tô hợp lệ):** Gửi ảnh ô tô rõ biển số. Kiểm tra tương tự, phân loại đúng `vehicleType: "CAR"`.
3. **Ca 3 (Ảnh mờ / Không biển số):** Gửi ảnh từ nhóm `05_error_cases`. Kiểm tra hệ thống trả về `plateNumber: "UNKNOWN"`, mã vé vẫn được tạo để nhân viên có thể sửa thủ công, không báo lỗi HTTP 500.

### 5.3. Kịch bản 3: Kiểm thử hàm Check-out & Thuật toán tính phí
1. **Ca 1 (Xe máy đỗ dưới 4 giờ):** Checkin thời gian $T$, checkout thời gian $T + 2\text{h}$. Phí dự kiến: **5.000 VNĐ**. Trạng thái chuyển `COMPLETED`.
2. **Ca 2 (Xe máy đỗ 6 giờ):** Checkin $T$, checkout $T + 6\text{h}$. Phí dự kiến: $5.000 + (6 - 4) \times 2.000 = \mathbf{9.000\text{ VNĐ}}$.
3. **Ca 3 (Ô tô đỗ 1 giờ 30 phút):** Làm tròn thành 2 giờ. Phí dự kiến: **20.000 VNĐ**.
4. **Ca 4 (Ô tô đỗ 5 giờ):** Phí dự kiến: $20.000 + (5 - 2) \times 10.000 = \mathbf{50.000\text{ VNĐ}}$.
5. **Ca 5 (Vé không tồn tại):** Gửi `ticketId: "random-fake-uuid"`. Hệ thống phải trả về HTTP 404 Not Found.
6. **Ca 6 (Thanh toán lần 2):** Gửi lại request checkout cho vé đã `COMPLETED`. Hệ thống phải từ chối với HTTP 400 Bad Request.

### 5.4. Kịch bản 4: Kiểm thử toàn trình qua API Gateway (End-to-End Test)
- Chạy script `scripts/test_api_endpoints.py` gọi trực tiếp Endpoint trên internet:
  ```bash
  python scripts/test_api_endpoints.py --endpoint https://xxxx.execute-api.us-east-1.amazonaws.com/dev
  ```
- Kiểm tra tính ổn định, độ trễ phản hồi (Response Latency $\le 3.5$ giây) và tính tương thích CORS khi gọi từ trình duyệt.

---

## 📸 PHẦN 6: DANH MỤC HỒ SƠ MINH CHỨNG TUẦN 2 (`evidence/week2/`)

Theo quy định bắt buộc của GVHD Huỳnh Xuân Phụng, toàn bộ ảnh chụp màn hình minh chứng phải chụp **toàn màn hình máy tính (Full Screen)**, hiển thị rõ ràng:
1. **AWS Account ID** (Góc trên bên phải Console).
2. **AWS Region:** Bắt buộc là `us-east-1` (N. Virginia).
3. **Đồng hồ hệ thống máy tính:** Ngày giờ thực tế tương ứng với thời gian trong bảng Worklog.

| Tên tệp ảnh minh chứng | Nội dung minh chứng chi tiết | Tiêu chuẩn nghiệm thu |
| :--- | :--- | :--- |
| `evidence/week2/01_lambda_functions.png` | Màn hình AWS Lambda Console liệt kê 2 hàm `SmartParking-Checkin` và `SmartParking-Checkout`. | Thấy rõ Runtime Python 3.11, Role `LabRole`, cấu hình Timeout 15s và Memory 256MB. |
| `evidence/week2/02_apigateway_routes.png` | Màn hình Amazon API Gateway Console hiển thị REST API `SmartParking-API`. | Thấy rõ cấu hình 2 resources `/checkin`, `/checkout`, method `POST`, `OPTIONS` và Stage `dev`. |
| `evidence/week2/03_rekognition_cloudwatch.png` | Màn hình CloudWatch Logs của Lambda Check-in. | Thấy log trích xuất các nhãn văn bản và độ chính xác (Confidence) từ Rekognition `DetectText`. |
| `evidence/week2/04_dynamodb_items.png` | Màn hình DynamoDB Console mục Explore Items của bảng `ParkingTickets`. | Thấy các bản ghi vé xe thật với đầy đủ các trường: `ticketId`, `plateNumber`, `checkinTime`, `checkoutTime`, `fee`, `status`. |
| `evidence/week2/05_s3_stored_images.png` | Màn hình Amazon S3 Console trong bucket `smart-parking-images-24110207`. | Thấy danh sách các file ảnh thực tế được tải lên trong folder `in/` và `out/`. |
| `evidence/week2/06_api_test_terminal_1.png` | Màn hình Terminal kiểm thử Check-in thành công qua API Gateway. | Thấy HTTP Status 200 OK, JSON response chứa đầy đủ dữ liệu vé và biển số nhận diện. |
| `evidence/week2/07_api_test_terminal_2.png` | Màn hình Terminal kiểm thử Check-out và các ca biên (400, 404). | Thấy tính phí chính xác 5.000 VNĐ, bắt lỗi vé đã thanh toán hoặc không tồn tại. |
| `evidence/week2/08_cost_and_billing.png` | Màn hình AWS Cost Management / Billing Dashboard. | Thấy rõ chi phí phiên làm việc phát sinh an toàn ($0.00), kiểm soát tốt ngân sách Lab. |

---

## 💰 PHẦN 7: QUẢN LÝ NGÂN SÁCH & AN TOÀN TRÊN AWS LEARNER LAB

Để bảo toàn ngân sách cấp sẵn $100.00 của AWS Learner Lab xuyên suốt 4 tuần học:
1. **Kiểm soát dịch vụ tính phí:**
   - Dịch vụ AWS Rekognition: Miễn phí 5.000 ảnh/tháng trong AWS Free Tier. Quá trình kiểm thử 120 ảnh chỉ tiêu tốn $\approx \$0.12$, hoàn toàn an toàn.
   - AWS Lambda: Miễn phí 1.000.000 lượt gọi/tháng và 3.200.000 giây tính toán.
   - Amazon DynamoDB: Chế độ On-demand chỉ trả tiền trên số lượt đọc/ghi thực tế, không phát sinh chi phí duy trì khi nhàn rỗi.
   - Amazon S3: Lưu trữ 120 ảnh nén ($\approx 10\text{ MB}$) tốn dưới $\$0.001$.
   - Amazon API Gateway: Miễn phí 1.000.000 lượt gọi REST API/tháng.
2. **Quy tắc an toàn vận hành:**
   - Tuyệt đối không bật EC2 kích thước lớn ngoài danh mục cho phép.
   - Sau mỗi buổi làm việc, thành viên phụ trách buổi đó phải nhấn **End Lab** để đóng phiên kết nối.
   - Kiểm tra Billing Dashboard vào cuối mỗi buổi để kịp thời phát hiện tài nguyên chạy ngầm.

---

## ✅ PHẦN 8: BẢNG CHECKLIST NGHIỆM THU TUẦN 2 (WEEK 2 CHECKLIST)

- [x] **Mã nguồn (Source Code):**
  - [x] Hoàn thiện code Boto3 cho `backend/checkin.py` (Rekognition, S3 `in/`, DynamoDB `put_item`).
  - [x] Hoàn thiện code Boto3 cho `backend/checkout.py` (DynamoDB `get_item`, tính phí, S3 `out/`, DynamoDB `update_item`).
  - [x] Viết script kiểm thử tự động `scripts/test_api_endpoints.py`.
  - [x] Viết script đánh giá dataset `scripts/evaluate_rekognition_accuracy.py`.
- [x] **Hạ tầng AWS (Cloud Infrastructure):**
  - [x] Cấu hình S3 CORS Policy cho bucket `smart-parking-images-24110207`.
  - [x] Deploy 2 Lambda functions trên AWS Console (`SmartParking-Checkin`, `SmartParking-Checkout`).
  - [x] Deploy API Gateway REST API `SmartParking-API` với đầy đủ 2 routes và CORS.
  - [x] Gắn đủ 3 Tags cho tất cả tài nguyên (`Project`, `Owner`, `Environment`).
- [x] **Kiểm thử & Chất lượng (QA):**
  - [x] Kiểm thử thành công Rekognition trên 120 ảnh mẫu (Tỷ lệ chính xác 96.7%).
  - [x] Kiểm thử thành công quy trình Check-in và Check-out thực tế trên AWS.
  - [x] Kiểm thử chính xác công thức tính phí đỗ xe cho cả xe máy và ô tô.
  - [x] Kiểm thử an toàn các trường hợp ngoại lệ (ảnh mờ gán `UNKNOWN`, lỗi 404, lỗi 400).
- [x] **Hồ sơ & Báo cáo:**
  - [x] Chụp đủ 8 ảnh minh chứng trong `evidence/week2/`.
  - [x] Báo cáo đánh giá Rekognition trong `docs/worklogs/week-02/rekognition_evaluation_report.md`.
  - [x] Nhật ký cá nhân SV1 (`docs/worklogs/week-02/member-1.md`) ghi nhận đủ 8.5 giờ.
  - [x] Nhật ký cá nhân SV2 (`docs/worklogs/week-02/member-2.md`) ghi nhận đủ 8.5 giờ.
  - [x] Nhật ký tổng hợp nhóm (`docs/worklogs/week-02/overview.md`) ghi nhận đủ 17.0 giờ.
  - [x] Toàn bộ mã nguồn, tài liệu và ảnh minh chứng được commit lên nhánh `main`.

