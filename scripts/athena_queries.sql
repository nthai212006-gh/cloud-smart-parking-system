-- ====================================================================
-- DỰ ÁN: HỆ THỐNG QUẢN LÝ BÃI GIỮ XE THÔNG MINH (SMART PARKING)
-- HỌC PHẦN: ĐIỆN TOÁN ĐÁM MÂY (CLOUD COMPUTING) - GVHD: THS. HUỲNH XUÂN PHỤNG
-- PHẦN VIỆC SINH VIÊN 2: NGUYỄN TRUNG HẢI (MSSV: 24110207)
-- BỘ TRUY VẤN SQL PHÂN TÍCH KINH DOANH VÀ LƯU LƯỢNG TRÊN AMAZON ATHENA
-- ====================================================================

-- BƯỚC 1: KHỞI TẠO CƠ SỞ DỮ LIỆU ATHENA
CREATE DATABASE IF NOT EXISTS smart_parking_db;

-- BƯỚC 2: KHỞI TẠO EXTERNAL TABLE ĐỌC DỮ LIỆU JSON TỪ S3
-- Lưu ý: Thay thế tên bucket 'smart-parking-images-24110207' nếu dùng bucket khác
CREATE EXTERNAL TABLE IF NOT EXISTS smart_parking_db.parking_tickets_analytics (
    ticketId string,
    plateNumber string,
    vehicleType string,
    checkinTime string,
    checkoutTime string,
    fee int,
    totalHours int,
    status string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
WITH SERDEPROPERTIES (
    'ignore.malformed.json' = 'TRUE'
)
LOCATION 's3://smart-parking-images-24110207/analytics-data/';

-- ====================================================================
-- BỘ 5 CÂU TRUY VẤN SQL NGHIỆP VỤ (BUSINESS ANALYTICS)
-- ====================================================================

-- 1. TRUY VẤN 1: TỔNG DOANH THU VÀ TỔNG SỐ LƯỢT XE ĐÃ HOÀN TẤT THANH TOÁN
-- Mục đích: Báo cáo tài chính tổng quan của bãi xe
SELECT 
    COUNT(*) AS total_completed_tickets,
    SUM(fee) AS total_revenue_vnd,
    AVG(fee) AS avg_fee_per_ticket_vnd,
    MIN(fee) AS min_fee_vnd,
    MAX(fee) AS max_fee_vnd
FROM smart_parking_db.parking_tickets_analytics
WHERE status = 'COMPLETED';


-- 2. TRUY VẤN 2: THỐNG KÊ DOANH THU VÀ SỐ LƯỢNG THEO TỪNG LOẠI PHƯƠNG TIỆN
-- Mục đích: Đánh giá cơ cấu đóng góp doanh thu giữa Xe máy (MOTORBIKE) và Ô tô (CAR)
SELECT 
    vehicleType,
    COUNT(*) AS total_vehicles,
    SUM(fee) AS revenue_vnd,
    ROUND(SUM(fee) * 100.0 / (SELECT SUM(fee) FROM smart_parking_db.parking_tickets_analytics WHERE status = 'COMPLETED'), 2) AS revenue_percentage,
    ROUND(AVG(fee), 0) AS avg_fee_vnd
FROM smart_parking_db.parking_tickets_analytics
WHERE status = 'COMPLETED'
GROUP BY vehicleType
ORDER BY revenue_vnd DESC;


-- 3. TRUY VẤN 3: PHÂN TÍCH LƯU LƯỢNG XE THEO TỪNG KHUNG GIỜ TRONG NGÀY (PEAK HOURS)
-- Mục đích: Giúp ban quản lý xác định giờ cao điểm để bố trí bảo vệ/nhân sự bãi xe
SELECT 
    SUBSTR(checkinTime, 12, 2) AS checkin_hour,
    COUNT(*) AS checkin_volume,
    SUM(CASE WHEN vehicleType = 'MOTORBIKE' THEN 1 ELSE 0 END) AS motorbike_count,
    SUM(CASE WHEN vehicleType = 'CAR' THEN 1 ELSE 0 END) AS car_count
FROM smart_parking_db.parking_tickets_analytics
GROUP BY SUBSTR(checkinTime, 12, 2)
ORDER BY checkin_volume DESC;


-- 4. TRUY VẤN 4: THỜI GIAN ĐỖ XE TRUNG BÌNH THEO LOẠI XE
-- Mục đích: Đánh giá vòng quay chỗ đỗ (Parking Turnover Rate)
SELECT 
    vehicleType,
    ROUND(AVG(totalHours), 1) AS avg_parked_hours,
    MIN(totalHours) AS min_parked_hours,
    MAX(totalHours) AS max_parked_hours
FROM smart_parking_db.parking_tickets_analytics
WHERE status = 'COMPLETED'
GROUP BY vehicleType;


-- 5. TRUY VẤN 5: BÁO CÁO TỶ LỆ NHẬN DIỆN BIỂN SỐ THÀNH CÔNG VS CỜ NGOẠI LỆ 'UNKNOWN'
-- Mục đích: Đánh giá chất lượng mô hình AI Rekognition và mức độ cần can thiệp thủ công
SELECT 
    CASE 
        WHEN plateNumber = 'UNKNOWN' THEN 'UNRECOGNIZED (UNKNOWN)'
        ELSE 'RECOGNIZED (SUCCESS)'
    END AS recognition_status,
    COUNT(*) AS ticket_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM smart_parking_db.parking_tickets_analytics), 2) AS percentage
FROM smart_parking_db.parking_tickets_analytics
GROUP BY 
    CASE 
        WHEN plateNumber = 'UNKNOWN' THEN 'UNRECOGNIZED (UNKNOWN)'
        ELSE 'RECOGNIZED (SUCCESS)'
    END;
