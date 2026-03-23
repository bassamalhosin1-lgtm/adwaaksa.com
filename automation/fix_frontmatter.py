#!/usr/bin/env python3
"""Fix frontmatter: rename 'url' to 'slug', add category if missing."""
from pathlib import Path
import re

CONTENT = Path(r"C:\Users\Abdalgani\Desktop\myapp\adwaaksa.com\adwaaksa-site\content")

for md_file in sorted(CONTENT.glob("*.md")):
    content = md_file.read_text(encoding="utf-8")
    modified = False

    # Replace 'url:' with 'slug:' in frontmatter
    if "\nurl:" in content and "\nslug:" not in content:
        content = content.replace("\nurl:", "\nslug:")
        modified = True

    # Add category if missing
    if "\ncategory:" not in content:
        # Insert before 'keywords:' if exists, else before '---' closing
        if "\nkeywords:" in content:
            content = content.replace("\nkeywords:", '\ncategory: "صيانة كهرباء"\nkeywords:')
        elif "\nimage:" in content:
            content = content.replace("\nimage:", '\ncategory: "صيانة كهرباء"\nimage:')
        modified = True

    if modified:
        md_file.write_text(content, encoding="utf-8")
        print(f"FIXED: {md_file.name}")
    else:
        print(f"OK: {md_file.name}")

print("\nDone!")
