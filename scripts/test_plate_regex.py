import re

def clean_license_plate(text_lines):
    """
    Hàm làm sạch và ghép các dòng văn bản nhận diện được thành một biển số hoàn chỉnh.
    - Loại bỏ các ký tự không phải là chữ cái và số (ví dụ: dấu chấm, dấu gạch ngang, dấu cách).
    - Ghép nối các dòng lại với nhau.
    """
    # Nối các dòng lại với nhau thành một chuỗi duy nhất
    raw_text = "".join(text_lines)
    
    # Sử dụng Regex để chỉ giữ lại chữ cái (A-Z) và chữ số (0-9)
    # Lệnh re.sub r'[^A-Z0-9]' sẽ thay thế bất kỳ ký tự nào KHÔNG phải A-Z hoặc 0-9 bằng chuỗi rỗng
    cleaned_plate = re.sub(r'[^A-Z0-9]', '', raw_text.upper())
    
    return cleaned_plate

def extract_plate_from_rekognition(rekognition_response):
    """
    Trích xuất biển số từ kết quả trả về của API AWS Rekognition (DetectText).
    Chúng ta ưu tiên lấy các object có Type là 'LINE' để giữ nguyên thứ tự.
    """
    text_lines = []
    
    for item in rekognition_response.get("TextDetections", []):
        # Chỉ xử lý các khối văn bản dạng LINE (đại diện cho cả 1 dòng)
        # Bỏ qua dạng WORD vì LINE đã bao trùm các WORD bên trong nó rồi
        if item.get("Type") == "LINE":
            # Tùy chọn: Chỉ lấy những dòng có độ tin cậy (Confidence) > 80%
            if item.get("Confidence", 0) > 80.0:
                text_lines.append(item.get("DetectedText"))
                
    return clean_license_plate(text_lines)

# --- MOCK DATA (DỮ LIỆU GIẢ LẬP) ĐỂ TEST TỪ AWS REKOGNITION ---

# 1. Mô phỏng biển số xe máy (thường có 2 dòng)
mock_motor_response = {
    "TextDetections": [
        {"DetectedText": "59-X1", "Type": "LINE", "Confidence": 99.5},
        {"DetectedText": "123.45", "Type": "LINE", "Confidence": 98.2},
        {"DetectedText": "59-X1", "Type": "WORD", "Confidence": 99.5},
        {"DetectedText": "123.45", "Type": "WORD", "Confidence": 98.2}
    ]
}

# 2. Mô phỏng biển số ô tô dài (thường trên 1 dòng)
mock_car_long_response = {
    "TextDetections": [
        {"DetectedText": "51A-123.45", "Type": "LINE", "Confidence": 99.1},
        {"DetectedText": "51A-123.45", "Type": "WORD", "Confidence": 99.1}
    ]
}

# 3. Mô phỏng biển số bị nhận diện rời rạc có chứa ký tự nhiễu
mock_noise_response = {
    "TextDetections": [
        {"DetectedText": "30H", "Type": "LINE", "Confidence": 97.0},
        {"DetectedText": "-", "Type": "LINE", "Confidence": 90.0},
        {"DetectedText": "999.88", "Type": "LINE", "Confidence": 98.5}
    ]
}

if __name__ == "__main__":
    print("=== KIỂM THỬ THUẬT TOÁN BÓC TÁCH BIỂN SỐ ===")
    
    motor_plate = extract_plate_from_rekognition(mock_motor_response)
    print(f"1. Xe máy (59-X1 / 123.45)   => Kết quả: {motor_plate}")
    
    car_plate = extract_plate_from_rekognition(mock_car_long_response)
    print(f"2. Ô tô   (51A-123.45)       => Kết quả: {car_plate}")
    
    noise_plate = extract_plate_from_rekognition(mock_noise_response)
    print(f"3. Rời rạc(30H / - / 999.88) => Kết quả: {noise_plate}")
    
    print("=============================================")
