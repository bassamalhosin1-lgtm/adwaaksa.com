#!/usr/bin/env python3
"""
سكريبت إضافة النصوص على صور المقالات
يضيف: عنوان الخدمة + رقم الهاتف + اسم الشركة
"""
import os, re, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

CONTENT_DIR = "c:/Users/Abdalgani/Desktop/myapp/adwaaksa.com/adwaaksa-site/content"
IMAGES_DIR = "c:/Users/Abdalgani/Desktop/myapp/adwaaksa.com/adwaaksa-site/static/images/blog"
PHONE = "0558697397"
COMPANY = "صحراء الشرق"
WEBSITE = "adwaaksa.com"

# Fonts
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_REGULAR = "C:/Windows/Fonts/arial.ttf"

# Colors matching the dark gold theme
GOLD = (249, 174, 20)
WHITE = (255, 255, 255)
DARK_BG = (11, 15, 26)
DARK_OVERLAY = (0, 0, 0, 160)

def reshape_arabic(text):
    """Try to use arabic_reshaper if available, fallback to raw text"""
    try:
        import arabic_reshaper
        from bidi.algorithm import get_display
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except ImportError:
        return text

def add_text_overlay(image_path, title, slug):
    """Add professional text overlay to image"""
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size
    
    # Create dark gradient overlay
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    
    # Bottom gradient (darker at bottom)
    for y in range(h // 3, h):
        alpha = int(200 * ((y - h // 3) / (h - h // 3)))
        draw_overlay.rectangle([(0, y), (w, y + 1)], fill=(11, 15, 26, alpha))
    
    # Top gradient (subtle)
    for y in range(0, h // 4):
        alpha = int(120 * (1 - y / (h // 4)))
        draw_overlay.rectangle([(0, y), (w, y + 1)], fill=(11, 15, 26, alpha))
    
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # Gold accent line at top
    draw.rectangle([(0, 0), (w, 5)], fill=GOLD + (255,))
    
    # Gold accent line at bottom
    draw.rectangle([(0, h - 5), (w, h)], fill=GOLD + (255,))
    
    # --- PHONE NUMBER (big, gold, center-bottom) ---
    try:
        font_phone = ImageFont.truetype(FONT_BOLD, 72)
    except:
        font_phone = ImageFont.load_default()
    
    phone_text = PHONE
    bbox = draw.textbbox((0, 0), phone_text, font=font_phone)
    phone_w = bbox[2] - bbox[0]
    phone_x = (w - phone_w) // 2
    phone_y = h - 120
    
    # Phone shadow
    draw.text((phone_x + 2, phone_y + 2), phone_text, fill=(0, 0, 0, 200), font=font_phone)
    # Phone text
    draw.text((phone_x, phone_y), phone_text, fill=GOLD + (255,), font=font_phone)
    
    # --- COMPANY NAME (small, white, above phone) ---
    try:
        font_company = ImageFont.truetype(FONT_BOLD, 28)
    except:
        font_company = ImageFont.load_default()
    
    company_text = reshape_arabic(COMPANY + " | " + WEBSITE)
    bbox = draw.textbbox((0, 0), company_text, font=font_company)
    company_w = bbox[2] - bbox[0]
    company_x = (w - company_w) // 2
    company_y = phone_y - 45
    
    draw.text((company_x + 1, company_y + 1), company_text, fill=(0, 0, 0, 180), font=font_company)
    draw.text((company_x, company_y), company_text, fill=WHITE + (255,), font=font_company)
    
    # --- TITLE (large, white, top area) ---
    try:
        font_title = ImageFont.truetype(FONT_BOLD, 42)
    except:
        font_title = ImageFont.load_default()
    
    # Shorten title if too long
    short_title = title
    if "—" in short_title:
        short_title = short_title.split("—")[0].strip()
    if len(short_title) > 40:
        short_title = short_title[:37] + "..."
    
    title_text = reshape_arabic(short_title)
    bbox = draw.textbbox((0, 0), title_text, font=font_title)
    title_w = bbox[2] - bbox[0]
    title_x = (w - title_w) // 2
    title_y = 40
    
    # Title bg pill
    pill_padding = 16
    pill_left = title_x - pill_padding
    pill_top = title_y - pill_padding // 2
    pill_right = title_x + title_w + pill_padding
    pill_bottom = title_y + (bbox[3] - bbox[1]) + pill_padding // 2
    draw.rounded_rectangle(
        [(pill_left, pill_top), (pill_right, pill_bottom)],
        radius=12,
        fill=(11, 15, 26, 200)
    )
    
    # Title shadow + text
    draw.text((title_x + 1, title_y + 1), title_text, fill=(0, 0, 0, 200), font=font_title)
    draw.text((title_x, title_y), title_text, fill=WHITE + (255,), font=font_title)
    
    # --- "اتصل الآن" chip above phone ---
    try:
        font_chip = ImageFont.truetype(FONT_BOLD, 22)
    except:
        font_chip = ImageFont.load_default()
    
    chip_text = reshape_arabic("📞 اتصل الآن")
    bbox = draw.textbbox((0, 0), chip_text, font=font_chip)
    chip_w = bbox[2] - bbox[0]
    chip_x = (w - chip_w) // 2
    chip_y = company_y - 40
    
    # Chip background
    chip_pad = 10
    draw.rounded_rectangle(
        [(chip_x - chip_pad, chip_y - chip_pad // 2), (chip_x + chip_w + chip_pad, chip_y + (bbox[3] - bbox[1]) + chip_pad // 2)],
        radius=20,
        fill=GOLD + (230,)
    )
    draw.text((chip_x, chip_y), chip_text, fill=DARK_BG + (255,), font=font_chip)
    
    # Convert back to RGB and save
    final = img.convert("RGB")
    final.save(image_path, "WEBP", quality=90)
    print(f"  ✅ {os.path.basename(image_path)} — overlay added")

def main():
    md_files = sorted(glob.glob(os.path.join(CONTENT_DIR, "*.md")))
    print(f"🎨 معالجة {len(md_files)} صورة...")
    
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        slug_match = re.search(r'slug:\s*"([^"]+)"', content)
        title_match = re.search(r'title:\s*"([^"]+)"', content)
        
        if slug_match and title_match:
            slug = slug_match.group(1)
            title = title_match.group(1)
            img_path = os.path.join(IMAGES_DIR, f"{slug}.webp")
            
            if os.path.exists(img_path):
                print(f"\n📷 {slug}")
                add_text_overlay(img_path, title, slug)
            else:
                print(f"\n⚠️  صورة غير موجودة: {slug}.webp")
    
    print(f"\n✅ تم إضافة النصوص على جميع الصور!")

if __name__ == "__main__":
    main()
