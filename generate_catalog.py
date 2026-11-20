
import json
import re
from pathlib import Path

THUMBNAIL_DIR = Path("images/thumbnails")
PORTFOLIO_DIR = Path("images/portfolio")
OUTPUT_FILE = Path("catalog.json")

COLORS = ["RED", "BLU", "BLK"]

pattern = re.compile(
    r"^(D-[A-Z]{2}-M-[A-Z]{2})-RED\.jpg$",
    re.IGNORECASE
)

catalog = []
missing = []

for image in sorted(THUMBNAIL_DIR.glob("*-RED.jpg")):
    match = pattern.match(image.name)

    if not match:
        continue

    sku = match.group(1).upper()

    # Confirm all three colors exist in both folders.
    expected_files = [
        f"{sku}-{color}.jpg"
        for color in COLORS
    ]

    thumbnail_files = [
        (THUMBNAIL_DIR / filename).exists()
        for filename in expected_files
    ]

    portfolio_files = [
        (PORTFOLIO_DIR / filename).exists()
        for filename in expected_files
    ]

    if all(thumbnail_files) and all(portfolio_files):
        catalog.append({"sku": sku})
    else:
        missing.append(sku)

OUTPUT_FILE.write_text(
    json.dumps(catalog, indent=2),
    encoding="utf-8"
)

print(f"Catalog generated: {OUTPUT_FILE}")
print(f"Complete designs: {len(catalog)}")
print(f"Missing/incomplete designs: {len(missing)}")

if missing:
    print("\nIncomplete designs:")
    for sku in missing:
        print(f"  {sku}")
