#!/usr/bin/env python3
"""Convert cabltexperts articles to adwaaksa branding."""
import os
from pathlib import Path

SRC = Path(r"C:\Users\Abdalgani\Desktop\myapp\cabltexperts.com\content\articles")
DST = Path(r"C:\Users\Abdalgani\Desktop\myapp\adwaaksa.com\adwaaksa-site\content")

FILES = [
    "how-to-detect-electrical-short-circuit-home.md",
    "solve-frequent-power-outage-apartment.md",
    "causes-of-flickering-lights-home-repair.md",
    "how-to-choose-best-electrical-cables-home.md",
    "importance-of-proper-apartment-electrical-foundation.md",
    "steps-for-electrical-foundation-in-homes.md",
    "tips-before-hiring-electrical-contractor-riyadh.md",
]

REPLACEMENTS = [
    ('author: "خبراء الكابلات"', 'author: "شركة صحراء الشرق"'),
    ('بخبراء الكابلات', 'بشركة صحراء الشرق'),
    ('لخبراء الكابلات', 'لشركة صحراء الشرق'),
    ('خبراء الكابلات:', 'شركة صحراء الشرق:'),
    ('خبراء الكابلات بالرياض', 'شركة صحراء الشرق بالرياض'),
    ('خبراء الكابلات', 'شركة صحراء الشرق'),
]

count = 7
for i, fname in enumerate(FILES):
    src_path = SRC / fname
    if not src_path.exists():
        print(f"SKIP: {fname} not found")
        continue
    content = src_path.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    num = str(count + i).zfill(2)
    dst_path = DST / f"{num}-{fname}"
    dst_path.write_text(content, encoding="utf-8")
    print(f"OK: {num}-{fname}")

print(f"\nDone! {len(FILES)} articles converted.")
