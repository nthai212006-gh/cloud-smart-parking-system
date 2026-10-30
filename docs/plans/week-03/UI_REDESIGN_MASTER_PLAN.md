# 🅿️ MASTER BLUEPRINT: KẾ HOẠCH TỔNG LỰC TÁI THIẾT KẾ TOÀN DIỆN SMART PARKING POS
### TÀI LIỆU HƯỚNG DẪN KỸ THUẬT & GIAO DIỆN DÀNH CHO THÀNH VIÊN 1 (LÊ CAO VIỆT TÍN)
* **Dự án:** Hệ thống Quản lý Bãi Giữ Xe Thông Minh (Smart Parking System)
* **Học phần:** Điện toán đám mây (Cloud Computing) – Giảng viên hướng dẫn: ThS. Huỳnh Xuân Phụng
* **Phân công trách nhiệm:** Sinh viên 1 phụ trách Backend Core (Lambda), IaC & Giao diện Web (Frontend)
* **Mục tiêu:** Xóa bỏ hoàn toàn giao diện prototype cũ (bị đơ sau 1 lần bấm, thanh URL phô trương, emoji trẻ con, chữ tàng hình) để chuyển sang **Phần mềm Trạm Kiểm Soát Bãi Xe Chuyên Nghiệp (Enterprise Desktop POS)** đạt điểm 10 tuyệt đối.

---

## I. TỔNG QUAN 4 NGUYÊN TẮC VẬN HÀNH BÃI XE THỰC TẾ

1. **Amazon DynamoDB là Nguồn Sự Thật Duy Nhất (Single Source of Truth):**
   - Trạng thái vé (`ACTIVE` hay `COMPLETED`) và doanh thu được lưu trữ và kiểm soát độc quyền tại bảng DynamoDB `ParkingTickets`.
   - Phía Frontend (LocalStorage / biến JavaScript) chỉ đóng vai trò Presentation Cache hiển thị tức thời cho nhân viên soát vé.
2. **Kiểm soát đồng thời nguyên tử (Atomic Concurrency Control):**
   - Sử dụng **DynamoDB Conditional Write** ở mức Database Engine trong Lambda Checkout, loại bỏ 100% rủi ro Race Condition (thu cước 2 lần khi 2 nhân viên cùng bấm xuất bãi 1 xe).
3. **Thao tác 1-Click trên Bảng Giám Sát Xe Đang Đỗ (Live Yard Monitor):**
   - Bãi giữ xe thực tế vận hành liên tục nhiều xe cùng lúc. Không ai nhớ mã UUID 36 ký tự.
   - Khi xe ra, nhân viên chỉ cần **bấm 1 click vào chiếc xe có Biển số đó trên bảng** $\rightarrow$ Hệ thống tự động nạp mã vé, tính cước và in hóa đơn trong 1 giây!
4. **Vận hành liên tiếp không bao giờ đơ (Continuous Form Cycle):**
   - Sau mỗi lần in vé hoặc tính cước, form tự động reset bộ nhớ đệm `fileInput.value = ""` và Base64 cache, sẵn sàng đón lượt xe kế tiếp.

---

## II. CHI TIẾT CÁC BƯỚC TRIỂN KHAI MÃ NGUỒN CỤ THỂ

### BƯỚC 1: CẬP NHẬT BACKEND LAMBDA (`backend/checkout.py`)
Áp dụng **DynamoDB Atomic Conditional Write** với `ConditionExpression="#st = :active"` để chống Race Condition:

```python
# Trong backend/checkout.py (thay thế đoạn table.update_item cũ):
try:
    update_expr = "SET #st = :completed, checkoutTime = :checkoutTime, fee = :fee, totalHours = :totalHours"
    expr_names = {"#st": "status"}
    expr_values = {
        ":completed": "COMPLETED",
        ":active": "ACTIVE",
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
        ConditionExpression="#st = :active",  # Chỉ cập nhật nếu trạng thái đang là ACTIVE
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values
    )
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
        return {
            "statusCode": 400,
            "headers": cors_headers,
            "body": json.dumps({"error": "Vé này đã được thanh toán và hoàn tất trước đó!"}, ensure_ascii=False)
        }
    raise e
```

---

### BƯỚC 2: CẬP NHẬT LOGIC FRONTEND (`frontend/app.js`)

#### 1. Bộ lọc Biển số xe Việt Nam thông minh (Cắt sạch chuỗi rác camera an ninh):
```javascript
function extractCleanPlate(rawText) {
  if (!rawText || rawText === "UNKNOWN") return "UNKNOWN";
  // Loại bỏ khoảng trắng và ký tự đặc biệt
  const clean = rawText.replace(/[^A-Z0-9]/gi, "").toUpperCase();
  
  // Regex bắt chuẩn biển số Việt Nam (2 số tỉnh + 1 chữ + 1 số/chữ + 4-5 số)
  // Ví dụ: 59V200884, 29B155555, 30E12345
  const match = clean.match(/^([0-9]{2}[A-Z]{1,2}[0-9]{4,5})/);
  if (match) {
    return match[1]; // Chỉ lấy đúng phần biển số thật, cắt bỏ chuỗi hash camera F46EC7D6...
  }
  return clean.substring(0, 10);
}
```

#### 2. Phân loại Input tại Cổng Ra (Smart Input Detector):
```javascript
// Cho phép nhập cả Biển số xe HOẶC Mã vé UUID 36 ký tự:
function resolveTicketId(inputValue) {
  const trimmed = inputValue.trim();
  const uuidRegex = /^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;
  
  if (uuidRegex.test(trimmed)) {
    return trimmed; // Đã là UUID chuẩn
  }
  
  // Nếu là biển số xe -> Tìm trong danh sách activeVehicles
  const found = activeVehicles.find(v => v.plateNumber.replace(/[^A-Z0-9]/gi, '') === trimmed.replace(/[^A-Z0-9]/gi, ''));
  return found ? found.ticketId : trimmed;
}
```

#### 3. Quản lý State xe đang đỗ & 1-Click Checkout:
```javascript
let activeVehicles = JSON.parse(localStorage.getItem("smart_parking_active_vehicles") || "[]");

// Khi Check-in thành công:
activeVehicles.unshift({
  ticketId: data.ticketId,
  plateNumber: cleanPlate,
  vehicleType: data.vehicleType,
  checkinTime: data.checkinTime,
  previewImage: checkinBase64
});
saveAndRenderActiveVehicles();

// 1-Click Checkout từ bảng giám sát:
function selectVehicleForCheckout(ticketId) {
  const vehicle = activeVehicles.find(v => v.ticketId === ticketId);
  if (!vehicle) return;
  
  checkoutTicketInput.value = vehicle.ticketId;
  // Hiển thị ảnh vào để đối chiếu bằng mắt
  if (vehicle.previewImage) {
    checkoutPreview.src = vehicle.previewImage;
    checkoutPreview.classList.remove("hidden");
    checkoutPlaceholder.classList.add("hidden");
  }
  showToast(`Đã chọn xe [${vehicle.plateNumber}] cho Cổng Ra!`);
}
```

#### 4. Reset Form sau mỗi lượt xe (Không bao giờ bị đơ):
```javascript
function resetCheckinForm() {
  checkinFileInput.value = "";
  checkinBase64 = null;
  checkinPreview.classList.add("hidden");
  checkinPlaceholder.classList.remove("hidden");
  checkinResult.classList.add("hidden");
}

function resetCheckoutForm() {
  checkoutTicketInput.value = "";
  checkoutFileInput.value = "";
  checkoutBase64 = null;
  checkoutPreview.classList.add("hidden");
  checkoutPlaceholder.classList.remove("hidden");
  checkoutResult.classList.add("hidden");
}
```

---

### BƯỚC 3: CẤU TRÚC GIAO DIỆN POS CHUYÊN NGHIỆP (`frontend/index.html`)

```text
BỐ CỤC KHUNG NHÌN 100VH (ZERO PAGE SCROLL):
+---------------------------------------------------------------------------------------------------+
|  [P] SMART PARKING POS • TRẠM KIỂM SOÁT BÃI XE THÔNG MINH             11:55:00 • Máy chủ: Sẵn sàng|
+---------------------------------------------------------------------------------------------------+
|  [ CỔNG VÀO - LÀN CHECK-IN ]                       [ CỔNG RA - LÀN CHECK-OUT ]                    |
|  - Khung camera 16:9 sắc nét                       - Khung camera đối chiếu 16:9                  |
|  - Radio chọn Xe máy (5k) / Ô tô (20k)             - Ô tìm kiếm: Nhập biển số hoặc mã vé          |
|  - Nút: IN VÉ VÀO & MỞ BARIE                       - Nút: TÍNH TIỀN & XUẤT BÃI                    |
|  - Thẻ vé: Biển số dập nổi, nút [XE TIẾP THEO]     - Hóa đơn: Cước phí to đậm, nút [SOÁT VÉ TIẾP] |
+---------------------------------------------------------------------------------------------------+
|  📊 THỐNG KÊ CA TRỰC: [Xe trong bãi: 3] | [Lượt vào: 5] | [Lượt ra: 2] | [Doanh thu: 10.000 đ]     |
|  📋 BẢNG GIÁM SÁT XE TRONG BÃI (LIVE YARD MONITOR - Cuộn độc lập max-height: 220px)              |
|  [Thumbnail] | [Biển số xe VN] | [Loại xe] | [Giờ vào: HH:mm:ss DD/MM/YYYY] | [➔ Cho Xe Ra]       |
|  💬 Ticker: Nhật ký thao tác thời gian thực phiên ca trực                                         |
+---------------------------------------------------------------------------------------------------+
```

* **Quy chuẩn bắt buộc:**
  - Ẩn hoàn toàn thanh URL API Gateway (nhúng biến ngầm `DEFAULT_API_ENDPOINT = "https://fdbsdxyto1.../dev"` trong JS).
  - Loại bỏ 100% emoji hoạt hình và tia laser viễn tưởng.
  - Chuẩn hóa định dạng thời gian duy nhất: `HH:mm:ss DD/MM/YYYY`.

---

### BƯỚC 4: THẨM MỸ & KIỂU DÁNG CSS (`frontend/style.css`)
* **Hệ màu Enterprise POS:** Nền `#f8fafc`, thanh công cụ `#0f172a`, Làn Vào `#15803d` (Emerald), Làn Ra `#1e40af` (Blue).
* **Khắc phục triệt để lỗi màu chữ:** Các nút bấm hành động dùng màu nền đậm với chữ in hoa màu trắng sáng `#ffffff`, font đậm `font-weight: 700`, `font-size: 15px`.
* **Biển số xe Việt Nam Flat Design:** Nền trắng, viền đen sắc nét, font số Monospace chuẩn biển kiểm soát cơ giới.
* **Tỷ lệ khung Camera:** Cố định tỉ lệ 16:9 chuẩn màn hình CCTV bãi xe, ảnh tự động căn giữa vừa khít.

---

## III. QUY TRÌNH KIỂM THỬ VÀ NGHIỆM THU DÀNH CHO BẠN TÍN

1. Mở file `frontend/index.html` trên trình duyệt.
2. **Kiểm thử Check-in xe 1 (Xe máy):** Chọn ảnh `test-images/02_motor_clear/img_01.jpg` $\rightarrow$ Bấm in vé $\rightarrow$ Thấy biển số chuẩn, vé xuất hiện trong bảng Live Yard phía dưới.
3. **Kiểm thử liên tiếp xe 2 (Ô tô):** Bấm `[ + XE TIẾP THEO ]` $\rightarrow$ Chọn ảnh `test-images/01_car_clear/car_01.jpg` $\rightarrow$ Bấm in vé $\rightarrow$ Form reset mượt mà, bảng Live Yard có cả 2 xe.
4. **Kiểm thử 1-Click Checkout:** Bấm nút `[ ➔ Cho Xe Ra ]` trên dòng xe 2 $\rightarrow$ Cổng Ra tự động nhảy biển số và ảnh đối chiếu $\rightarrow$ Bấm Tính tiền $\rightarrow$ Hoàn tất thanh toán đúng giá cước.
5. Sau khi kiểm thử hoàn hảo, bạn Tín thực hiện commit:
   ```bash
   git add backend/checkout.py frontend/
   git commit -m "feat(ui): redesign enterprise parking POS dashboard and implement atomic conditional checkout"
   git push origin main
   ```
