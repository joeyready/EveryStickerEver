import csv
import tempfile
import unittest
from pathlib import Path

from generate_woocommerce_products import make_product_rows, write_woocommerce_csv


class WooCommerceProductTests(unittest.TestCase):
    def test_product_rows_include_parent_and_three_variations(self):
        rows = make_product_rows(
            {"State1": "Don't Alabama", "State2": "My Alaska", "SKU": "D-AL-M-AK"}
        )

        self.assertEqual([row["Type"] for row in rows], ["variable"] + ["variation"] * 3)
        self.assertEqual(
            [row["SKU"] for row in rows],
            ["D-AL-M-AK", "D-AL-M-AK-RED", "D-AL-M-AK-BLU", "D-AL-M-AK-BLK"],
        )
        self.assertEqual([row["Parent"] for row in rows[1:]], ["D-AL-M-AK"] * 3)
        self.assertEqual(rows[0]["Published"], "0")
        self.assertIn("Don't Alabama", rows[0]["Name"])
        self.assertIn("My Alaska", rows[0]["Description"])
        self.assertEqual(rows[0]["Attribute 1 value(s)"], "Red | Blue | Black")

    def test_write_csv_outputs_one_parent_and_variations_per_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.csv"
            output = Path(temp_dir) / "woocommerce.csv"
            with source.open("w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["State1", "State2", "SKU"])
                writer.writeheader()
                writer.writerow(
                    {"State1": "Don't Alabama", "State2": "My Alaska", "SKU": "D-AL-M-AK"}
                )
                writer.writerow(
                    {"State1": "Don't Alabama", "State2": "My Arizona", "SKU": "D-AL-M-AZ"}
                )

            self.assertEqual(write_woocommerce_csv(source, output), 2)
            with output.open(newline="", encoding="utf-8") as csvfile:
                rows = list(csv.DictReader(csvfile))

        self.assertEqual(len(rows), 8)
        self.assertEqual([row["Type"] for row in rows].count("variable"), 2)

    def test_duplicate_skus_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "source.csv"
            source.write_text(
                "State1,State2,SKU\nDon't Alabama,My Alaska,D-AL-M-AK\n"
                "Don't Alabama,My Arizona,D-AL-M-AK\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Duplicate SKU"):
                write_woocommerce_csv(source, Path(temp_dir) / "woocommerce.csv")


if __name__ == "__main__":
    unittest.main()
