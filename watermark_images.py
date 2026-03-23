#!/usr/bin/env python3
"""Add phone watermark to AI-generated images and copy to site articles folder."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BRAIN = Path(r"C:\Users\Abdalgani\.gemini\antigravity\brain\1de9acef-d79b-4af4-8f76-1dbdfab3d35b")
OUT = Path(__file__).parent / "adwaaksa-site" / "static" / "images" / "articles"
OUT.mkdir(parents=True, exist_ok=True)

PHONE = "0558697397"
SITE = "adwaaksa.com"
W, H = 1200, 675

# Map: source image glob pattern -> target filename
IMAGES = {
    "home_electrical_maintenance_*.png": "home_electrical_maintenance_riyadh.png",
    "wire_burning_walls_*.png": "wire_burning_inside_walls.png",
    "repair_underground_cable_*.png": "repair_underground_cable_faults.png",
    "electrical_leakage_home_*.png": "electrical_leakage_home.png",
    "short_circuit_rain_*.png": "short_circuit_rain.png",
    "detection_device_*.png": "short_circuit_detection_device.png",
    "emergency_electrician_*.png": "emergency_electrician_riyadh.png",
}

def add_watermark(img_path, out_path):
    img = Image.open(img_path).convert("RGBA")
    img = img.resize((W, H), Image.LANCZOS)
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Find best font size for phone to fill ~80% width
    target_w = int(W * 0.80)
    phone_size = 200
    font_phone = None
    while phone_size > 30:
        try:
            font_phone = ImageFont.truetype("arial", phone_size)
        except:
            font_phone = ImageFont.load_default()
            break
        bb = draw.textbbox((0, 0), PHONE, font=font_phone)
        if (bb[2] - bb[0]) <= target_w:
            break
        phone_size -= 5

    # Site name font
    try:
        font_site = ImageFont.truetype("arial", 40)
    except:
        font_site = ImageFont.load_default()

    # Semi-transparent dark banner behind phone number
    banner_h = phone_size + 80
    banner_y = (H - banner_h) // 2
    draw.rectangle([(0, banner_y), (W, banner_y + banner_h)], fill=(0, 0, 0, 140))
    
    # Draw site name above phone
    site_bb = draw.textbbox((0, 0), SITE, font=font_site)
    site_w = site_bb[2] - site_bb[0]
    draw.text(((W - site_w) // 2, banner_y + 10), SITE, fill=(255, 255, 255, 220), font=font_site)

    # Draw phone number (huge, centered, gold/yellow)
    phone_bb = draw.textbbox((0, 0), PHONE, font=font_phone)
    pw = phone_bb[2] - phone_bb[0]
    ph = phone_bb[3] - phone_bb[1]
    px = (W - pw) // 2
    py = banner_y + 50
    
    # Shadow
    draw.text((px + 3, py + 3), PHONE, fill=(0, 0, 0, 200), font=font_phone)
    # Main text - bright gold
    draw.text((px, py), PHONE, fill=(255, 215, 0, 255), font=font_phone)

    # Composite
    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(str(out_path), "PNG", quality=95)
    print(f"  ✅ {out_path.name} ({out_path.stat().st_size // 1024} KB)")


def main():
    print("🎨 إضافة العلامة المائية على الصور الاحترافية...\n")
    ok = 0
    for pattern, target_name in IMAGES.items():
        matches = list(BRAIN.glob(pattern))
        if not matches:
            print(f"  ❌ لم أجد: {pattern}")
            continue
        src = matches[0]  # Take first match
        dst = OUT / target_name
        add_watermark(src, dst)
        ok += 1
    
    print(f"\n📊 النتائج: {ok}/{len(IMAGES)} صور تمت معالجتها")


if __name__ == "__main__":
    main()
