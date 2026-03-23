import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import urllib.request
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

PHONE = "0558697397"
WEBSITE = "adwaaksa.com"

FONT_PATH_PRIMARY = "C:/Windows/Fonts/impact.ttf"
FONT_PATH_SECONDARY = "C:/Windows/Fonts/arialbd.ttf"

def ensure_font():
    if os.path.exists(FONT_PATH_PRIMARY):
        return FONT_PATH_PRIMARY
    elif os.path.exists(FONT_PATH_SECONDARY):
        return FONT_PATH_SECONDARY
    else:
        logging.error("No suitable bold font found on Windows system.")
        return None

def apply_huge_watermark(image_path):
    try:
        img = Image.open(image_path).convert("RGBA")
        base_w, base_h = img.size

        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)
        
        font_path = ensure_font()
        if not font_path:
            logging.error("Font missing. Cannot proceed with huge watermark.")
            return

        # تحديد حجم الخط: التكبير حتى يملأ 85% من عرض الصورة للرقم
        font_size = 50
        font = ImageFont.truetype(font_path, font_size)
        text_phone = f" {PHONE} "
        while True:
            bbox = draw.textbbox((0, 0), text_phone, font=font)
            w = bbox[2] - bbox[0]
            if w > base_w * 0.85:
                font_size -= 5
                font = ImageFont.truetype(font_path, max(10, font_size))
                break
            font_size += 5
            font = ImageFont.truetype(font_path, font_size)

        small_size = max(int(font_size * 0.3), 20)
        small_font = ImageFont.truetype(font_path, small_size)

        text_phone = f" {PHONE} "
        text_web = f" {WEBSITE} "

        # حساب الأبعاد بطريقة آمنة
        phone_bbox = draw.textbbox((0, 0), text_phone, font=font)
        phone_w, phone_h = phone_bbox[2] - phone_bbox[0], phone_bbox[3] - phone_bbox[1]

        web_bbox = draw.textbbox((0, 0), text_web, font=small_font)
        web_w, web_h = web_bbox[2] - web_bbox[0], web_bbox[3] - web_bbox[1]

        padding = int(base_h * 0.03)
        banner_height = phone_h + web_h + (padding * 4)
        banner_y = base_h - banner_height
        
        # خلفية سوداء صلبة شبه شفافة في الأسفل لضمان قراءة الرقم
        draw.rectangle(
            [(0, banner_y), (base_w, base_h)], 
            fill=(10, 10, 15, 240) # شبه معتم جداً
        )

        # خط برتقالي فخم
        draw.rectangle([(0, banner_y), (base_w, banner_y + int(padding*0.3))], fill=(255, 140, 0, 255))

        # رسم الموقع
        web_x = (base_w - web_w) // 2
        web_y = banner_y + padding
        draw.text((web_x, web_y), text_web, fill=(200, 200, 200, 255), font=small_font)

        # رسم الرقم ضخماً باللون البرتقالي
        phone_x = (base_w - phone_w) // 2
        phone_y = web_y + web_h + padding
        draw.text((phone_x, phone_y), text_phone, fill=(255, 160, 0, 255), font=font)

        out_img = Image.alpha_composite(img, txt_layer).convert("RGB")
        out_img.save(image_path, quality=95)
        logging.info(f"✅ Watermarked and saved: {image_path.name}")
        
    except Exception as e:
        logging.error(f"Failed to watermark {image_path}: {e}")

if __name__ == "__main__":
    images_dir = Path("adwaaksa-site/static/images/articles/")
    if not images_dir.exists():
        images_dir.mkdir(parents=True, exist_ok=True)
    
    for img_path in images_dir.glob("*.[pjP][nNpP][gG]"): # match png, jpg
        apply_huge_watermark(img_path)
