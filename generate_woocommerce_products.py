import argparse
import csv
import html
from pathlib import Path


COLORS = (("Red", "RED"), ("Blue", "BLU"), ("Black", "BLK"))
REQUIRED_COLUMNS = ("State1", "State2", "SKU")
OUTPUT_COLUMNS = (
    "Type",
    "SKU",
    "Name",
    "Published",
    "Visibility in catalog",
    "Short description",
    "Description",
    "Parent",
    "Attribute 1 name",
    "Attribute 1 value(s)",
    "Attribute 1 visible",
    "Attribute 1 global",
)


def read_products(input_path: Path) -> list[dict[str, str]]:
    products = []
    seen_skus = set()

    with input_path.open(newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        missing_columns = set(REQUIRED_COLUMNS) - set(reader.fieldnames or ())
        if missing_columns:
            raise ValueError(
                f"Input CSV is missing required columns: {', '.join(sorted(missing_columns))}"
            )

        for line_number, row in enumerate(reader, start=2):
            state1 = (row.get("State1") or "").strip()
            state2 = (row.get("State2") or "").strip()
            sku = (row.get("SKU") or "").strip()
            if not state1 or not state2 or not sku:
                raise ValueError(
                    f"Input CSV row {line_number} must have State1, State2, and SKU values"
                )
            if sku in seen_skus:
                raise ValueError(f"Duplicate SKU {sku!r} on input CSV row {line_number}")

            seen_skus.add(sku)
            products.append({"State1": state1, "State2": state2, "SKU": sku})

    if not products:
        raise ValueError("Input CSV contains no products")
    return products


def make_product_rows(product: dict[str, str]) -> list[dict[str, str]]:
    state1 = product["State1"]
    state2 = product["State2"]
    sku = product["SKU"]
    name = f"{state1} {state2} Bumper Sticker"
    design_text = f"{state1} / {state2}"
    short_description = (
        f"Bumper sticker featuring “{design_text}”, available in red, blue, or black."
    )
    description = (
        "<p>Bumper sticker featuring this state-pairing design:</p>"
        f"<p><strong>{html.escape(state1)}<br>{html.escape(state2)}</strong></p>"
        "<p>Choose from red, blue, or black.</p>"
    )

    parent = {
        "Type": "variable",
        "SKU": sku,
        "Name": name,
        "Published": "0",
        "Visibility in catalog": "visible",
        "Short description": short_description,
        "Description": description,
        "Parent": "",
        "Attribute 1 name": "Color",
        "Attribute 1 value(s)": " | ".join(color for color, _ in COLORS),
        "Attribute 1 visible": "1",
        "Attribute 1 global": "0",
    }
    variations = [
        {
            "Type": "variation",
            "SKU": f"{sku}-{sku_suffix}",
            "Name": "",
            "Published": "0",
            "Visibility in catalog": "visible",
            "Short description": "",
            "Description": "",
            "Parent": sku,
            "Attribute 1 name": "Color",
            "Attribute 1 value(s)": color,
            "Attribute 1 visible": "0",
            "Attribute 1 global": "0",
        }
        for color, sku_suffix in COLORS
    ]
    return [parent, *variations]


def write_woocommerce_csv(input_path: Path, output_path: Path) -> int:
    products = read_products(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        for product in products:
            writer.writerows(make_product_rows(product))

    return len(products)


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Generate draft variable products for WooCommerce from state combinations."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=script_dir / "state_combinations.csv",
        help="Source CSV containing State1, State2, and SKU columns.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=script_dir / "woocommerce_products.csv",
        help="Destination WooCommerce import CSV.",
    )
    args = parser.parse_args()

    try:
        product_count = write_woocommerce_csv(args.input, args.output)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))

    print(
        f"Wrote {product_count} draft products and {product_count * len(COLORS)} "
        f"color variations to {args.output}"
    )


if __name__ == "__main__":
    main()
