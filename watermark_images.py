#!/usr/bin/env python3
"""Add phone watermark to new cable article images."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BRAIN = Path(r"C:\Users\Abdalgani\.gemini\antigravity\brain\1de9acef-d79b-4af4-8f76-1dbdfab3d35b")
OUT = Path(__file__).parent / "adwaaksa-site" / "static" / "images" / "articles"
OUT.mkdir(parents=True, exist_ok=True)

PHONE = "0558697397"
W, H = 1200, 675

IMAGES = {
    "cable_fault_detection_*.png": "cable_fault_detection.png",
    "cable_short_circuit_*.png": "cable_short_circuit.png",
    "cable_testing_*.png": "cable_testing.png",
    "cable_repair_splicing_*.png": "cable_repair_splicing.png",
    "cable_maintenance_*.png": "cable_maintenance.png",
    "breaker_tripping_*.png": "breaker_tripping.png",
    "cable_damage_locator_*.png": "cable_damage_locator.png",
}

def add_watermark(img_path, out_path):
    img = Image.open(img_path).convert("RGBA")
    img = img.resize((W, H), Image.LANCZOS)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

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

    try:
        font_site = ImageFont.truetype("arial", 40)
    except:
        font_site = ImageFont.load_default()

    banner_h = phone_size + 80
    banner_y = (H - banner_h) // 2
    draw.rectangle([(0, banner_y), (W, banner_y + banner_h)], fill=(0, 0, 0, 140))

    site_bb = draw.textbbox((0, 0), "adwaaksa.com", font=font_site)
    draw.text(((W - (site_bb[2]-site_bb[0])) // 2, banner_y + 10), "adwaaksa.com", fill=(255, 255, 255, 220), font=font_site)

    phone_bb = draw.textbbox((0, 0), PHONE, font=font_phone)
    pw = phone_bb[2] - phone_bb[0]
    px = (W - pw) // 2
    py = banner_y + 50
    draw.text((px + 3, py + 3), PHONE, fill=(0, 0, 0, 200), font=font_phone)
    draw.text((px, py), PHONE, fill=(255, 215, 0, 255), font=font_phone)

    result = Image.alpha_composite(img, overlay)
    result.convert("RGB").save(str(out_path), "PNG", quality=95)
    print(f"  ✅ {out_path.name} ({out_path.stat().st_size // 1024} KB)")

def main():
    print("🎨 إضافة العلامة المائية على صور الكابلات الجديدة...\n")
    ok = 0
    for pattern, target in IMAGES.items():
        matches = list(BRAIN.glob(pattern))
        if not matches:
            print(f"  ❌ لم أجد: {pattern}")
            continue
        add_watermark(matches[0], OUT / target)
        ok += 1
    print(f"\n📊 النتائج: {ok}/{len(IMAGES)} صور")

if __name__ == "__main__":
    main()
