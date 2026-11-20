# Every Sticker Ever — Static Portfolio Site

A lightweight, static landing page for the Every Sticker Ever creative-automation project.

## Run locally

No build step or package installation is required.

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Deploy to Vercel

1. Import this GitHub repository into Vercel.
2. Select **Other** as the framework preset if prompted.
3. Leave the build command empty.
4. Leave the output directory as the repository root (or `.`).
5. Deploy.

The site is plain HTML, CSS, and JavaScript. The original Python scripts, CSV source data, and Photoshop files remain in the repository and are not part of a build pipeline.

## Notes

- The collection cards are illustrative previews generated from the project's documented sticker format, not product photography.
- Color swatches update the preview cards between red, blue, and black.
- The page clearly identifies the project as a portfolio/experimental project and says the stickers are not currently for sale.
- The site is structured to be easy to migrate or rebuild in WordPress later.

## Project source

The original scripts and source data remain in the repository:
- `combo_maker.py`
- `open_psd_edit_text_layers.py`
- `generate_woocommerce_products.py`
- `state_combinations.csv`
- `woocommerce_products.csv`
