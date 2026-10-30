# 🎬 KỊCH BẢN QUAY VIDEO DEMO TOÀN TRÌNH (DƯỚI 10 PHÚT)
### HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING SYSTEM)
* **Học phần:** Điện toán đám mây (Cloud Computing) – GVHD: **ThS. Huỳnh Xuân Phụng**
* **Nhóm thực hiện:** Lê Cao Việt Tín (24110354) & Nguyễn Trung Hải (24110207)
* **Quy chuẩn thời lượng:** Tối đa 10 phút (Chuẩn video thực tế: **~8 phút**).
* **Link lưu trữ Video Demo:** [Google Drive - DEMO.mp4](https://drive.google.com/drive/folders/1iYy8aeg6JkXlWysBVxFYQMlPEZcbFLb6?usp=drive_link)
* **Bộ ảnh test chính thức:** Ô tô (`test-images/01_car_clear/car_clear_05.jpg`) và Xe máy (`test-images/02_motor_clear/motor_clear_06.jpg`).

---

## ⏱️ PHÂN BỔ THỜI LƯỢNG (TIMELINE TỔNG QUAN)

```
00:00 - 01:00 (1p)  : Mở đầu, giới thiệu nhóm, kiến trúc AWS Serverless & công nghệ
01:00 - 03:00 (2p)  : Kịch bản 1 - Xe vào Cổng Làn 1 (Ô tô car_05 & Xe máy motor_06)
03:00 - 05:00 (2p)  : Kịch bản 2 - Xe ra Cổng Làn 2 (Smart Search & 1-Click Checkout)
05:00 - 06:45 (1.75p): Kịch bản 3 - Điểm nhấn kỹ thuật: Chống Double-Checkout & Bảo mật
06:45 - 08:00 (1.25p): Kịch bản 4 - Minh chứng trên AWS Console (S3, DynamoDB, Athena, Billing $0.03)
08:00 - 08:30 (30s) : Kết luận & Kế hoạch dọn dẹp tài nguyên (IaC)
```

---

## 🎙️ KỊCH BẢN CHI TIẾT TỪNG PHÚT: LỜI THOẠI & THAO TÁC MÀN HÌNH

### PHẦN 1: MỞ ĐẦU & GIỚI THIỆU TỔNG QUAN (00:00 - 01:00)

* **Màn hình hiển thị:** Giao diện POS Desktop (`http://localhost:8000`) và mở sẵn 1 tab sơ đồ kiến trúc AWS (hoặc trang GitHub repo).
* **Thao tác chuột:** Di chuột lướt nhẹ qua thanh Header (Đồng hồ, trạng thái AWS Online, bộ đếm xe trong bãi).

> **Lời thoại thuyết minh:**
> *"Kính chào Thầy Huỳnh Xuân Phụng và các bạn. Hôm nay, nhóm Domain Apps gồm hai thành viên: Lê Cao Việt Tín và Nguyễn Trung Hải xin phép trình bày video demo toàn trình của đồ án: **Hệ thống quản lý bãi giữ xe thông minh - Smart Parking System** trên nền tảng AWS Cloud.*
>
> *Về mặt kiến trúc, đồ án được xây dựng 100% theo mô hình **AWS Serverless Decoupled**:*
> - *Frontend là giao diện POS Desktop chuyên nghiệp dành cho nhân viên bãi xe, đồng bộ lưới 5 tầng đối xứng.*
> - *Hệ thống giao tiếp qua **AWS API Gateway**, xử lý nghiệp vụ bằng **AWS Lambda Python 3.12**.*
> - *Nhận diện biển số tự động bằng **Amazon Rekognition**.*
> - *Lưu trữ ảnh bất biến trên **Amazon S3**, quản lý dữ liệu vé bằng cơ sở dữ liệu **Amazon DynamoDB** NoSQL có tốc độ phản hồi mili-giây, giám sát bằng **CloudWatch** và phân tích dữ liệu lớn bằng **Amazon Athena**.*
> 
> *Sau đây, nhóm em xin bắt đầu quy trình vận hành thực tế tại trạm kiểm soát."*

---

### PHẦN 2: KỊCH BẢN LÀN 1 - XE VÀO & CẤP VÉ TỰ ĐỘNG (01:00 - 03:00)

#### Case 2.1: Tiếp nhận Ô tô vào bãi
* **Màn hình hiển thị:** Khung **LÀN 1 · CỔNG VÀO**.
* **Thao tác chuột:**
  1. Click vào khung **CAM 01 · 1080P** $\rightarrow$ Chọn ảnh `test-images/01_car_clear/car_clear_05.jpg`.
  2. Click chọn thẻ **Ô TÔ** (`20.000đ / 2h đầu`).
  3. Bấm nút màu xanh **`[XÁC NHẬN VÀO & CẤP VÉ]`**.

> **Lời thoại thuyết minh:**
> *"Đầu tiên là luồng xe vào tại Cổng Làn 1. Khi có một chiếc ô tô tiến vào làn kiểm soát, camera CAM 01 chụp ảnh phương tiện. Em chọn ảnh chụp thực tế `car_clear_05.jpg` và chọn loại phương tiện là Ô tô, sau đó bấm Xác nhận vào & Cấp vé.*
>
> *(Chờ 1 giây)*
> *Như Thầy thấy, hệ thống phản hồi cực kỳ nhanh chóng:*
> - *Ảnh xe được mã hóa Base64 gửi lên API Gateway, Lambda lập tức lưu ảnh gốc vào S3 bucket ở thư mục `in/`.*
> - *Amazon Rekognition tự động trích xuất chuỗi ký tự, và thuật toán Regex thông minh của nhóm em đã làm sạch chuỗi, loại bỏ các watermark ngày giờ camera để lấy chính xác biển số.*
> - *Hệ thống phát hành ngay Thẻ vé điện tử màu vàng chuẩn POS với mã UUID duy nhất, thời gian vào chuẩn xác đến từng giây.*
> - *Đồng thời, xe tự động được đưa vào danh sách theo dõi **Live Yard Monitor** ở bảng phía dưới, số lượng xe trong bãi tăng lên 1.*
> - *Đặc biệt, form CAM 01 tự động làm mới để nhân viên sẵn sàng tiếp nhận xe tiếp theo mà không bị đơ giao diện."*

#### Case 2.2: Tiếp nhận Xe máy vào bãi
* **Thao tác chuột:**
  1. Click vào CAM 01 $\rightarrow$ Chọn ảnh `test-images/02_motor_clear/motor_clear_06.jpg`.
  2. Click chọn thẻ **XE MÁY** (`5.000đ / 4h đầu`).
  3. Bấm **`[XÁC NHẬN VÀO & CẤP VÉ]`**.

> **Lời thoại thuyết minh:**
> *"Tiếp theo, một chiếc xe máy tiến vào. Em chọn ảnh `motor_clear_06.jpg` với mức giá 5.000đ cho 4 giờ đầu và bấm cấp vé. Hệ thống tiếp tục nhận diện chính xác biển số xe máy 2 dòng và thêm vào bảng theo dõi. Hiện tại bãi xe đang có đồng thời cả 2 phương tiện đang gửi."*

---

### PHẦN 3: KỊCH BẢN LÀN 2 - XE RA & TÍNH CƯỚC CHECK-OUT (03:00 - 05:00)

#### Case 3.1: Đối soát thông minh tại Cổng Ra (Smart Plate / UUID Search)
* **Màn hình hiển thị:** Khung **LÀN 2 · CỔNG RA**.
* **Thao tác chuột:**
  1. Tại ô **TRA CỨU XE RA**, bấm nút **`[Dán mã vừa tạo]`** (hoặc gõ vài ký tự biển số xe máy vừa vào).
  2. Quan sát tooltip xanh lá hiện lên ngay dưới input.
  3. Chọn lại ảnh xe máy `motor_clear_06.jpg` ở CAM 02.
  4. Bấm nút màu xanh lá **`[TÍNH CƯỚC & CHO XE RA]`**.

> **Lời thoại thuyết minh:**
> *"Bây giờ là quy trình xe ra tại Cổng Làn 2. Nhân viên có thể linh hoạt nhập biển số hoặc mã vé. Ở đây em bấm nút **Dán mã vừa tạo**, hệ thống lập tức đối soát dữ liệu real-time và hiện gợi ý màu xanh xác nhận xe này đang có mặt trong bãi.*
>
> *Ô CAM 02 cho phép chụp ảnh xe lúc ra để lưu vết đối chứng lên S3 thư mục `out/`, giúp bảo vệ quan sát bằng mắt xem xe ra có đúng là chiếc xe đã vào hay không, chống hiện tượng tráo biển số.*
>
> *Em bấm **Tính cước & cho xe ra**.*
> *(Hóa đơn hiện lên)*
> *Hóa đơn cước phí xuất bãi lập tức được hiển thị: Tổng cước là 5.000 VNĐ, thời gian đỗ 1 giờ, trạng thái chuyển thành COMPLETED và mở Barie. Đồng thời, chiếc xe máy này tự động được gạch khỏi danh sách xe trong bãi."*

#### Case 3.2: Tính năng 1-Click Checkout trực tiếp từ Bảng theo dõi
* **Màn hình hiển thị:** Bảng *Danh sách xe đang trong bãi*.
* **Thao tác chuột:** 
  - Tại dòng của chiếc Ô tô còn lại, bấm trực tiếp nút **`[Cho xe ra]`** ở cột Thao tác.

> **Lời thoại thuyết minh:**
> *"Đối với chiếc ô tô còn lại, vào những giờ cao điểm bãi xe đông đúc, nhân viên có thể sử dụng tính năng **1-Click Checkout** ngay tại Bảng giám sát. Em bấm nút 'Cho xe ra' của chiếc ô tô, hệ thống tự động hoàn tất tính cước 20.000 VNĐ cho ô tô và xuất bãi trong chưa đầy 1 giây."*

---

### PHẦN 4: ĐIỂM NHẤN BẢO MẬT & ĐIỆN TOÁN ĐÁM MÂY (05:00 - 06:45)
*(Đây là phần Thầy Phụng khen nhất trong nhận xét, cần nói to, tự tin và rõ ràng!)*

#### Test 4.1: Chống Double-Checkout / Race Condition (DynamoDB Atomic Conditional Write)
* **Thao tác chuột:** 
  - Giữ nguyên mã vé vừa xuất bãi ở Cổng Ra, bấm nút **`[TÍNH CƯỚC & CHO XE RA]`** một lần nữa.
  - Toast màu đỏ báo lỗi `HTTP 400` xuất hiện.

> **Lời thoại thuyết minh:**
> *"Bây giờ, em xin trình bày điểm kỹ thuật quan trọng nhất mà nhóm em đã giải quyết triệt để theo đúng nhận xét của Thầy: **Xử lý Race Condition và chống thanh toán trùng lặp (Double-Checkout)**.*
>
> *Em thử bấm tính tiền lại chiếc xe vừa ra. Hệ thống lập tức chặn đứng và trả về lỗi HTTP 400: 'Vé này đã được thanh toán và hoàn tất trước đó!'.*
>
> *Cơ chế hoạt động bên dưới: Trong file `backend/checkout.py`, nhóm em không kiểm tra thủ công bằng `if-else` mà sử dụng **DynamoDB Atomic Conditional Write** với biểu thức:*
> ```python
> ConditionExpression="#st = :parked OR #st = :active"
> ```
> *Điều này đảm bảo lệnh cập nhật vé chỉ thành công duy nhất một lần ở tầng Database mức nguyên tử (Atomic), ngăn chặn 100% tình trạng hai nhân viên bấm cùng lúc hoặc mạng lag bấm đúp gây sai lệch doanh thu bãi xe."*

#### Test 4.2: Bảo vệ tầng API Gateway & Giới hạn tải
* **Màn hình hiển thị:** Mở icon **Bánh răng cài đặt** trên Header xem API Endpoint hoặc chạy script test tải `scripts/test_api_throttling.py`.

> **Lời thoại thuyết minh:**
> *"Bên cạnh đó, nhóm đã kiểm thử bảo mật toàn diện:*
> - *Nếu gửi ảnh payload Base64 vượt quá 5MB, hệ thống trả về lỗi `HTTP 413 Payload Too Large`.*
> - *Tại API Gateway, nhóm cấu hình Throttling với ngưỡng 10 requests/giây, burst 20. Khi script kiểm thử bắn 30 requests/giây, hệ thống chặn đúng chuẩn `HTTP 429 Too Many Requests`, bảo vệ Lambda không bị quá tải và chống tấn công từ chối dịch vụ (DDoS)."*

---

### PHẦN 5: MINH CHỨNG TRÊN AWS CONSOLE & DỮ LIỆU THẬT (06:45 - 08:00)

* **Màn hình hiển thị:** Chuyển sang trình duyệt đang mở AWS Console.
* **Thao tác lướt qua các tab:**

1. **Amazon DynamoDB (Bảng `ParkingTickets`):**
   > *"Tại DynamoDB Console, bảng ParkingTickets lưu trữ đầy đủ các thuộc tính: `ticketId`, `plateNumber`, `vehicleType`, `checkinTime`, `checkoutTime`, `fee`, và `status`. Các vé xe đã xuất bãi chuyển sang COMPLETED."*
2. **Amazon S3 (`smart-parking-images`):**
   > *"Trên S3 bucket, dữ liệu được phân cấp rành mạch: thư mục `in/` chứa ảnh xe vào và thư mục `out/` chứa ảnh xe ra để lưu vết đối soát pháp lý."*
3. **Amazon Athena (Truy vấn phân tích dữ liệu lớn):**
   > *"Tại Athena, nhóm em đã thực hiện 5 câu truy vấn SQL trên tập dữ liệu thật, thống kê tổng doanh thu đạt 1.124.000 VNĐ, trong đó ô tô chiếm 83.6%, tốc độ truy vấn chỉ 462ms quét 11.6KB dữ liệu."*
4. **AWS Cost & Billing:**
   > *"Về mặt chi phí: Trên trang AWS Billing, tổng chi phí phát sinh thực tế xuyên suốt quá trình kiểm thử tải và demo nhiều lượt chỉ vỏn vẹn **$0.03** (trong đó CloudWatch chiếm $0.02, Rekognition chiếm $0.01). Nhóm đã bảo toàn trọn vẹn 99.97% hạn mức ngân sách $100 của AWS Learner Lab."*

---

### PHẦN 6: KẾT LUẬN & DỌN DẸP TÀI NGUYÊN (08:00 - 08:30)

* **Màn hình hiển thị:** Mở file `iac/cloudformation_template.yaml` trong VS Code.

> **Lời thoại thuyết minh:**
> *"Để đảm bảo tính tự động hóa cao nhất, toàn bộ hạ tầng từ S3, DynamoDB, Lambda, API Gateway đến CloudWatch Alarms đều được định nghĩa trong file **Infrastructure as Code (CloudFormation)**.*
>
> *Sau buổi báo cáo kết thúc, nhóm em chỉ cần thực thi một lệnh hủy stack CloudFormation duy nhất là toàn bộ tài nguyên sẽ được dọn dẹp sạch sẽ 100%, tuân thủ nghiêm ngặt quy định không để lãng phí tài nguyên của môn học.*
>
> *Nhóm em xin chân thành cảm ơn Thầy Huỳnh Xuân Phụng đã theo sát và hướng dẫn nhóm hoàn thành đồ án. Em xin kết thúc phần trình bày video demo tại đây!"*
