#!/usr/bin/env python3
"""Generate professional article images with phone watermark for adwaaksa.com"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random

OUT = Path(__file__).parent / "adwaaksa-site" / "static" / "images" / "articles"
OUT.mkdir(parents=True, exist_ok=True)

PHONE = "0558697397"
W, H = 1200, 675

PALETTES = [
    [(15, 32, 65), (25, 55, 109), (45, 85, 150)],
    [(10, 25, 45), (20, 50, 80), (35, 80, 130)],
    [(20, 40, 30), (35, 70, 50), (50, 100, 75)],
    [(30, 15, 50), (55, 30, 85), (80, 50, 120)],
    [(40, 20, 15), (70, 35, 25), (100, 55, 40)],
    [(15, 15, 35), (30, 30, 65), (50, 50, 95)],
    [(25, 35, 45), (45, 60, 75), (65, 85, 105)],
]

ARTICLES = [
    ("home_electrical_maintenance_riyadh", "صيانة كهرباء منازل"),
    ("wire_burning_inside_walls", "احتراق أسلاك الجدار"),
    ("repair_underground_cable_faults", "إصلاح كابلات أرضية"),
    ("electrical_leakage_home", "تسريب الكهرباء"),
    ("short_circuit_rain", "التماس في المطر"),
    ("short_circuit_detection_device", "جهاز كشف التماس"),
    ("emergency_electrician_riyadh", "طوارئ كهرباء 24/7"),
]


def draw_gradient(draw, w, h, colors):
    c1, c2, c3 = colors
    for y in range(h):
        ratio = y / h
        if ratio < 0.5:
            r2 = ratio * 2
            r = int(c1[0]*(1-r2) + c2[0]*r2)
            g = int(c1[1]*(1-r2) + c2[1]*r2)
            b = int(c1[2]*(1-r2) + c2[2]*r2)
        else:
            r2 = (ratio-0.5)*2
            r = int(c2[0]*(1-r2) + c3[0]*r2)
            g = int(c2[1]*(1-r2) + c3[1]*r2)
            b = int(c2[2]*(1-r2) + c3[2]*r2)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def create_image(slug, title_ar, palette_idx):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    colors = PALETTES[palette_idx % len(PALETTES)]
    draw_gradient(draw, W, H, colors)

    accent = tuple(min(255, c+100) for c in colors[1])
    # Diagonal lines
    for i in range(0, W+H, 80):
        draw.line([(i, 0), (i-H, H)], fill=(*accent, 15), width=1)
    # Corner accents
    ac = (*accent, 80)
    draw.line([(30,30),(30,80)], fill=ac, width=3)
    draw.line([(30,30),(80,30)], fill=ac, width=3)
    draw.line([(W-30,H-30),(W-30,H-80)], fill=ac, width=3)
    draw.line([(W-30,H-30),(W-80,H-30)], fill=ac, width=3)

    try:
        font_site = ImageFont.truetype("arial", 36)
        font_title = ImageFont.truetype("arial", 48)
    except:
        font_site = ImageFont.load_default()
        font_title = font_site

    # Site name
    site_text = "adwaaksa.com"
    bbox = draw.textbbox((0,0), site_text, font=font_site)
    draw.text(((W-(bbox[2]-bbox[0]))//2, 40), site_text, fill=(255,255,255,200), font=font_site)
    draw.line([(W//4,95),(3*W//4,95)], fill=(*accent,150), width=2)

    # Title
    bbox = draw.textbbox((0,0), title_ar, font=font_title)
    draw.text(((W-(bbox[2]-bbox[0]))//2, 120), title_ar, fill=(255,255,255,230), font=font_title)

    # HUGE PHONE NUMBER
    # Find maximum font size that fits ~85% of width
    target_w = int(W * 0.85)
    phone_size = 200
    while phone_size > 20:
        try:
            fnt = ImageFont.truetype("arial", phone_size)
        except:
            fnt = ImageFont.load_default()
            break
        bb = draw.textbbox((0,0), PHONE, font=fnt)
        if (bb[2]-bb[0]) <= target_w:
            break
        phone_size -= 5

    bb = draw.textbbox((0,0), PHONE, font=fnt)
    pw, ph = bb[2]-bb[0], bb[3]-bb[1]
    px, py = (W-pw)//2, (H-ph)//2 + 30
    draw.text((px+4, py+4), PHONE, fill=(0,0,0,150), font=fnt)
    draw.text((px, py), PHONE, fill=(255,215,0,255), font=fnt)

    # Bottom bar
    draw.rectangle([(0,H-55),(W,H)], fill=(0,0,0,150))
    bot = "صحراء الشرق | كشف التماس | الرياض"
    bb = draw.textbbox((0,0), bot, font=font_site)
    draw.text(((W-(bb[2]-bb[0]))//2, H-48), bot, fill=(255,255,255,200), font=font_site)

    out_path = OUT / f"{slug}.png"
    img.convert("RGB").save(str(out_path), "PNG", quality=95)
    print(f"  ✅ {slug}.png ({out_path.stat().st_size//1024} KB)")
    return True


def main():
    print("🎨 توليد صور المقالات الجديدة...")
    ok = 0
    for i, (slug, title) in enumerate(ARTICLES):
        if create_image(slug, title, i):
            ok += 1
    print(f"\n📊 النتائج: {ok}/{len(ARTICLES)} صور")

if __name__ == "__main__":
    main()
