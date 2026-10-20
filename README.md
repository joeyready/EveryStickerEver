# EveryStickerEver

## Generate WooCommerce product copy

`generate_woocommerce_products.py` reads the root `state_combinations.csv` and
creates `woocommerce_products.csv`, formatted for the WooCommerce product CSV
importer. It creates one draft variable product per design and three draft color
variations (red, blue, and black) per product. Product names and descriptions
are based on the two sticker text fields; no unverified size, material, or
durability claims are added.

Run from the repository root:

```sh
python3 generate_woocommerce_products.py
```

The input and output paths can be changed with `--input` and `--output`. The
generated products are drafts because the source data does not include pricing,
images, or other listing details. Review the CSV and add those details before
publishing or importing as published products.