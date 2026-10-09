"""
Script hỗ trợ Người 2 (Nguyễn Trung Hải - 24110207)
Tự động nén và chuẩn hóa bộ Dataset ảnh biển số xe:
- Giữ tỉ lệ, nén dung lượng về khoảng 200KB - 800KB.
- Đổi tên ảnh theo quy chuẩn: test_motor_xx.jpg hoặc test_car_xx.jpg.

Cách dùng:
1. Copy ảnh thô đã che mặt vào thư mục test-images/raw/
2. Chạy lệnh: python scripts/compress_and_rename_dataset.py
"""

import os
from pathlib import Path
try:
    from PIL import Image
except ImportError:
    print("Vui lòng cài đặt thư viện Pillow trước: pip install pillow")
    exit(1)

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "test-images" / "raw"
OUTPUT_DIR = BASE_DIR / "test-images"

def process_images():
    if not RAW_DIR.exists():
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        print(f"[*] Đã tạo thư mục: {RAW_DIR}")
        print(f"[*] Hãy copy ảnh biển số (đã che mặt) vào thư mục '{RAW_DIR}' rồi chạy lại script này.")
        return

    valid_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    raw_files = [f for f in RAW_DIR.iterdir() if f.suffix.lower() in valid_extensions]

    if not raw_files:
        print(f"[!] Không tìm thấy ảnh nào trong thư mục '{RAW_DIR}'.")
        print("[!] Hãy bỏ ảnh vào đó rồi chạy lại.")
        return

    print(f"[*] Tìm thấy {len(raw_files)} ảnh cần xử lý...")

    motor_idx = 1
    car_idx = 1

    for file_path in raw_files:
        filename_lower = file_path.name.lower()
        if "car" in filename_lower or "oto" in filename_lower:
            new_name = f"test_car_{car_idx:02d}.jpg"
            car_idx += 1
        else:
            new_name = f"test_motor_{motor_idx:02d}.jpg"
            motor_idx += 1

        output_path = OUTPUT_DIR / new_name

        with Image.open(file_path) as img:
            img = img.convert("RGB")
            # Resize nếu ảnh quá lớn (> 1920px)
            max_size = 1920
            if max(img.size) > max_size:
                img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            # Nén chất lượng về khoảng 80-85% để đạt dung lượng 200KB - 800KB
            quality = 85
            img.save(output_path, "JPEG", optimize=True, quality=quality)

            size_kb = os.path.getsize(output_path) / 1024
            while size_kb > 800 and quality > 40:
                quality -= 10
                img.save(output_path, "JPEG", optimize=True, quality=quality)
                size_kb = os.path.getsize(output_path) / 1024

            print(f"[OK] Đã xử lý: {file_path.name} -> {new_name} ({size_kb:.1f} KB)")

    print(f"\n[DONE] Đã lưu toàn bộ ảnh chuẩn hóa vào: {OUTPUT_DIR}")

if __name__ == "__main__":
    process_images()
