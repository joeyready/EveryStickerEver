# Every Sticker Ever

**"Don't [State] My [State]"**: a bumper sticker for every pairing of the 50 US states, produced by a small creative-automation pipeline.

> **Status:** portfolio / experimental project. The stickers are **not for sale**.


## The idea

50 states × 50 states = **2,500 designs** (including each state paired with itself). Each design comes in **3 colorways** (red, blue, black), for **7,500 variations**. Making that by hand isn't realistic, so one Photoshop template and a handful of scripts do the repetitive work.

## The pipeline

```
combo_maker.py              state_combinations.csv  (State1, State2, SKU)
        │
        ▼
open_psd_edit_text_layers.py   Photoshop template → RED / BLU / BLK PSDs + 3-up composite
        │
        ▼
(JPG export)                images/thumbnails/  and  images/portfolio/
        │
        ▼
generate_catalog.py         catalog.json  (only designs with all 3 colors in both folders)
        │
        ▼
index.html / styles.css / script.js     static portfolio site

generate_woocommerce_products.py   state_combinations.csv → woocommerce_products.csv
```

### SKU format

`D-<State1 abbr>-M-<State2 abbr>`, for example `D-AL-M-AK` is "Don't Alabama / My Alaska". Color variations append `-RED`, `-BLU`, or `-BLK`.

## Repository contents

| File | Purpose |
| --- | --- |
| `combo_maker.py` | Builds every state pairing and its SKU, and writes `state_combinations.csv`. |
| `open_psd_edit_text_layers.py` | Drives Photoshop (via AppleScript/ExtendScript) to swap the `line_1` / `line_2` text layers, recolor the background, and save each colorway plus a stacked 3-up composite. |
| `generate_catalog.py` | Scans the image folders and writes `catalog.json` for designs that have all three colors in both thumbnail and portfolio sizes. |
| `generate_woocommerce_products.py` | Converts the CSV into a WooCommerce product import: one draft variable product per design with red/blue/black variations. |
| `test_generate_woocommerce_products.py` | Unit tests for the WooCommerce generator. |
| `index.html`, `styles.css`, `script.js` | The static portfolio site. |
| `state_combinations.csv` | Source data: `State1, State2, SKU`. |

## Requirements

- **Python 3.9+** (standard library only; no packages to install).
- **For the artwork automation only:** macOS and Adobe Photoshop 2026, plus a PSD template with text layers named `line_1` and `line_2` and a layer named `background`. The script calls Photoshop by name, so a different version means editing the app name in the AppleScript blocks. Photoshop files are gitignored and not included in this repo.

Everything else (data generation, catalog, WooCommerce CSV, site) runs on any OS.

## Usage

**1. Generate the state pairings**

```sh
python3 combo_maker.py
```

**2. Generate artwork** (macOS + Photoshop required)

```sh
python3 open_psd_edit_text_layers.py
```

The script processes only the first few CSV rows by default, as a test run. Increase or remove the row limit in `process_csv_and_generate_psd_files()` to do the full set.

**3. Build the catalog**

Export the finished designs as JPGs named `<SKU>-RED.jpg`, `<SKU>-BLU.jpg`, `<SKU>-BLK.jpg` into `images/thumbnails/` and `images/portfolio/`, then run:

```sh
python3 generate_catalog.py
```

It prints how many designs are complete and lists any with missing colors.

**4. Generate the WooCommerce import file**

```sh
python3 generate_woocommerce_products.py
# optional: --input path/to/source.csv --output path/to/output.csv
```

Products are created as **drafts**. The source data has no pricing, images, or sizing details, so add those before publishing. Product copy uses only the sticker text; no material or durability claims are made.

**5. Run the site locally**

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. No build step is needed.

**Run the tests**

```sh
python3 -m unittest
```

## Deploying the site

The site is plain HTML, CSS, and JavaScript. On Vercel: import the repo, choose **Other** as the framework preset, leave the build command empty, and keep the output directory at the repository root.

## Known limitations

- The Photoshop automation is macOS-only, depends on Photoshop's AppleScript support, and uses fixed `time.sleep` delays between steps.
- JPG export from the PSDs is currently a manual step.
- Only a small selection of designs is featured on the site; the full 2,500 aren't all rendered.

## What I'd do next

- Make the row limit a command-line flag (`--limit`) instead of a hard-coded value.
- Script the PSD → JPG export so the pipeline runs end to end.
- Add a short screen recording of the automation running.

## License

All rights reserved unless a license is added.
