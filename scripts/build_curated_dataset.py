"""
Script tự động trích xuất, phân loại và chuẩn hóa 120 ảnh Dataset cho Người 2 (Nguyễn Trung Hải)
Theo đúng quy cách bảng yêu cầu của Đề tài / Giảng viên:
1. Ô tô - biển số rõ: 40 ảnh (Kiểm tra nhận diện cơ bản)
2. Xe máy - biển số rõ: 40 ảnh (Kiểm tra nhận diện biển số xe máy)
3. Ô tô - điều kiện khó: 10 ảnh (Góc nghiêng, xa, thiếu sáng)
4. Xe máy - điều kiện khó: 10 ảnh (Biển số nhỏ, góc nghiêng, thiếu sáng)
5. Ảnh không có biển số hoặc biển số khó đọc: 20 ảnh (Kiểm tra xử lý lỗi / Edge cases)
Tổng cộng: 120 ảnh
"""

import os
import io
import sys
import json
import zipfile
import random
from pathlib import Path
from PIL import Image, ImageStat, ImageFilter, ImageEnhance, ImageDraw

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
ZIP_PATH = BASE_DIR / "vietnamese license plate.v1i.coco.zip"
RAW_USER_DIR = BASE_DIR / "test-images" / "raw"
DATASET_DIR = BASE_DIR / "test-images"

FOLDERS = {
    "car_clear": DATASET_DIR / "01_car_clear",
    "motor_clear": DATASET_DIR / "02_motor_clear",
    "car_hard": DATASET_DIR / "03_car_hard",
    "motor_hard": DATASET_DIR / "04_motor_hard",
    "error_cases": DATASET_DIR / "05_error_cases",
}

for folder in FOLDERS.values():
    folder.mkdir(parents=True, exist_ok=True)

def save_optimized_jpeg(img, target_path, max_dim=1280, target_min_kb=150, target_max_kb=800):
    img = img.convert("RGB")
    if max(img.size) > max_dim:
        img.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
    
    quality = 85
    img.save(target_path, "JPEG", optimize=True, quality=quality)
    size_kb = os.path.getsize(target_path) / 1024
    
    while size_kb > target_max_kb and quality > 35:
        quality -= 10
        img.save(target_path, "JPEG", optimize=True, quality=quality)
        size_kb = os.path.getsize(target_path) / 1024

print("[*] Đang đọc file zip Roboflow và COCO annotations...")
z = zipfile.ZipFile(ZIP_PATH)
coco_data = json.loads(z.read("train/_annotations.coco.json").decode("utf-8"))

img_id_to_file = {img["id"]: img["file_name"] for img in coco_data["images"]}
img_to_anns = {}
for ann in coco_data["annotations"]:
    img_to_anns.setdefault(ann["image_id"], []).append(ann)

# Phân nhóm ảnh từ zip
zip_car_clear_pool = []
zip_motor_clear_pool = []
zip_car_hard_pool = []
zip_motor_hard_pool = []

for img in coco_data["images"]:
    fn = img["file_name"]
    zip_entry = "train/" + fn
    if zip_entry not in z.namelist():
        continue
    anns = img_to_anns.get(img["id"], [])
    if not anns:
        continue
    ann = max(anns, key=lambda a: a.get("area", 0))
    area = ann.get("area", 0)

    if "CarLongPlate" in fn and "Gen" not in fn:
        if 4000 < area < 20000:
            zip_car_clear_pool.append(zip_entry)
        elif area <= 4000:
            zip_car_hard_pool.append(zip_entry)
    elif "CarLongPlateGen" in fn:
        if area <= 2000:
            zip_car_hard_pool.append(zip_entry)
    elif "xemay" in fn and "Gen" not in fn:
        if 5000 < area < 40000:
            zip_motor_clear_pool.append(zip_entry)
        elif area <= 3000:
            zip_motor_hard_pool.append(zip_entry)

# Thêm từ augmented / rotate / crop / darkness pool
hard_augmented = [x for x in z.namelist() if x.startswith("train/") and any(k in x for k in ["rotate", "brightness", "crop"])]
random.shuffle(hard_augmented)

for fn in hard_augmented:
    if "Car" in fn:
        zip_car_hard_pool.append(fn)
    else:
        zip_motor_hard_pool.append(fn)

random.shuffle(zip_car_clear_pool)
random.shuffle(zip_motor_clear_pool)
random.shuffle(zip_car_hard_pool)
random.shuffle(zip_motor_hard_pool)

print(f"[*] Pool ô tô rõ: {len(zip_car_clear_pool)}")
print(f"[*] Pool xe máy rõ: {len(zip_motor_clear_pool)}")
print(f"[*] Pool ô tô khó: {len(zip_car_hard_pool)}")
print(f"[*] Pool xe máy khó: {len(zip_motor_hard_pool)}")

# ==========================================
# 1. NHÓM 1: Ô TÔ - BIỂN SỐ RÕ (40 ẢNH)
# ==========================================
print("\n[1/5] Đang xử lý Nhóm 1: Ô tô - Biển số rõ (40 ảnh)...")
car_clear_idx = 1

# Ưu tiên lấy ảnh người dùng tự chụp
user_cars = [f for f in RAW_USER_DIR.iterdir() if "hoi" in f.name.lower() or "car" in f.name.lower()] if RAW_USER_DIR.exists() else []
for uc in sorted(user_cars):
    with Image.open(uc) as im:
        out_path = FOLDERS["car_clear"] / f"car_clear_{car_clear_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        print(f"  + car_clear_{car_clear_idx:02d}.jpg (Từ ảnh bạn chụp: {uc.name})")
        car_clear_idx += 1

# Bổ sung từ zip cho đủ 40
for zip_fn in zip_car_clear_pool:
    if car_clear_idx > 40:
        break
    im_bytes = z.read(zip_fn)
    with Image.open(io.BytesIO(im_bytes)) as im:
        out_path = FOLDERS["car_clear"] / f"car_clear_{car_clear_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        car_clear_idx += 1

# ==========================================
# 2. NHÓM 2: XE MÁY - BIỂN SỐ RÕ (40 ẢNH)
# ==========================================
print("\n[2/5] Đang xử lý Nhóm 2: Xe máy - Biển số rõ (40 ảnh)...")
motor_clear_idx = 1

# Ưu tiên lấy ảnh người dùng tự chụp (các ảnh chụp rõ)
user_motors_clear = []
if RAW_USER_DIR.exists():
    for f in RAW_USER_DIR.iterdir():
        fn_lower = f.name.lower()
        if ("may" in fn_lower or "motor" in fn_lower) and "4" not in fn_lower and "6" not in fn_lower:
            user_motors_clear.append(f)

for um in sorted(user_motors_clear):
    with Image.open(um) as im:
        out_path = FOLDERS["motor_clear"] / f"motor_clear_{motor_clear_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        print(f"  + motor_clear_{motor_clear_idx:02d}.jpg (Từ ảnh bạn chụp: {um.name})")
        motor_clear_idx += 1

# Bổ sung từ zip cho đủ 40
for zip_fn in zip_motor_clear_pool:
    if motor_clear_idx > 40:
        break
    im_bytes = z.read(zip_fn)
    with Image.open(io.BytesIO(im_bytes)) as im:
        out_path = FOLDERS["motor_clear"] / f"motor_clear_{motor_clear_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        motor_clear_idx += 1

# ==========================================
# 3. NHÓM 3: Ô TÔ - ĐIỀU KIỆN KHÓ (10 ẢNH)
# ==========================================
print("\n[3/5] Đang xử lý Nhóm 3: Ô tô - Điều kiện khó (10 ảnh)...")
car_hard_idx = 1
for zip_fn in zip_car_hard_pool:
    if car_hard_idx > 10:
        break
    im_bytes = z.read(zip_fn)
    with Image.open(io.BytesIO(im_bytes)) as im:
        out_path = FOLDERS["car_hard"] / f"car_hard_{car_hard_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        car_hard_idx += 1

# ==========================================
# 4. NHÓM 4: XE MÁY - ĐIỀU KIỆN KHÓ (10 ẢNH)
# ==========================================
print("\n[4/5] Đang xử lý Nhóm 4: Xe máy - Điều kiện khó (10 ảnh)...")
motor_hard_idx = 1

# Lấy các ảnh khó từ user (xe_may_4 góc nghiêng, xe_may_6 mờ/nhỏ)
user_motors_hard = []
if RAW_USER_DIR.exists():
    for f in RAW_USER_DIR.iterdir():
        fn_lower = f.name.lower()
        if "xe_may_4" in fn_lower or "xe_may_6" in fn_lower:
            user_motors_hard.append(f)

for um in sorted(user_motors_hard):
    with Image.open(um) as im:
        out_path = FOLDERS["motor_hard"] / f"motor_hard_{motor_hard_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        print(f"  + motor_hard_{motor_hard_idx:02d}.jpg (Từ ảnh bạn chụp: {um.name})")
        motor_hard_idx += 1

# Bổ sung từ zip cho đủ 10
for zip_fn in zip_motor_hard_pool:
    if motor_hard_idx > 10:
        break
    im_bytes = z.read(zip_fn)
    with Image.open(io.BytesIO(im_bytes)) as im:
        out_path = FOLDERS["motor_hard"] / f"motor_hard_{motor_hard_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        motor_hard_idx += 1

# ==========================================
# 5. NHÓM 5: KHÔNG CÓ BIỂN / BIỂN KHÓ ĐỌC (20 ẢNH)
# ==========================================
print("\n[5/5] Đang xử lý Nhóm 5: Không có biển số / Biển số khó đọc (20 ảnh)...")
error_idx = 1

# 5.1: 5 ảnh che khuất biển số (bị che bằng vật cản, băng keo, rách mờ)
sample_source = zip_car_clear_pool[50:55]
for src in sample_source:
    im_bytes = z.read(src)
    with Image.open(io.BytesIO(im_bytes)) as im:
        im = im.convert("RGB")
        draw = ImageDraw.Draw(im)
        w, h = im.size
        # Vẽ một mảng che khuất ngẫu nhiên ở khu vực biển số
        draw.rectangle([w*0.35, h*0.55, w*0.65, h*0.75], fill=(50, 50, 50))
        out_path = FOLDERS["error_cases"] / f"error_case_{error_idx:02d}.jpg"
        save_optimized_jpeg(im, out_path)
        print(f"  + error_case_{error_idx:02d}.jpg (Biển số bị che khuất vật cản)")
        error_idx += 1

# 5.2: 5 ảnh mờ nhòe do xe chuyển động nhanh (Motion Blur)
sample_source = zip_motor_clear_pool[50:55]
for src in sample_source:
    im_bytes = z.read(src)
    with Image.open(io.BytesIO(im_bytes)) as im:
        im = im.convert("RGB")
        # Áp dụng GaussianBlur mạnh mô phỏng motion blur
        im_blur = im.filter(ImageFilter.GaussianBlur(radius=8))
        out_path = FOLDERS["error_cases"] / f"error_case_{error_idx:02d}.jpg"
        save_optimized_jpeg(im_blur, out_path)
        print(f"  + error_case_{error_idx:02d}.jpg (Mờ nhòe do xe di chuyển nhanh)")
        error_idx += 1

# 5.3: 5 ảnh quá tối (thiếu sáng cực độ ban đêm, không đọc được số)
sample_source = zip_car_clear_pool[55:60]
for src in sample_source:
    im_bytes = z.read(src)
    with Image.open(io.BytesIO(im_bytes)) as im:
        im = im.convert("RGB")
        enhancer = ImageEnhance.Brightness(im)
        im_dark = enhancer.enhance(0.12) # giảm sáng 88%
        out_path = FOLDERS["error_cases"] / f"error_case_{error_idx:02d}.jpg"
        save_optimized_jpeg(im_dark, out_path)
        print(f"  + error_case_{error_idx:02d}.jpg (Thiếu sáng cực độ ban đêm)")
        error_idx += 1

# 5.4: 5 ảnh chói lóa đèn xe / lóa nắng (Overexposure Glare)
sample_source = zip_motor_clear_pool[55:60]
for src in sample_source:
    im_bytes = z.read(src)
    with Image.open(io.BytesIO(im_bytes)) as im:
        im = im.convert("RGB")
        enhancer = ImageEnhance.Brightness(im)
        im_bright = enhancer.enhance(2.8) # tăng sáng cháy màn hình
        out_path = FOLDERS["error_cases"] / f"error_case_{error_idx:02d}.jpg"
        save_optimized_jpeg(im_bright, out_path)
        print(f"  + error_case_{error_idx:02d}.jpg (Lóa sáng đèn pha / chói nắng)")
        error_idx += 1

print("\n" + "=" * 60)
print("TỔNG KẾT BỘ DATASET HOÀN CHỈNH:")
for k, v in FOLDERS.items():
    cnt = len(list(v.glob("*.jpg")))
    print(f" - {v.name}: {cnt} ảnh")
print(f"TỔNG CỘNG: {sum(len(list(v.glob('*.jpg'))) for v in FOLDERS.values())} / 120 ảnh")
print("=" * 60)
