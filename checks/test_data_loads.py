"""Checkpoint "load": raw sales data (checks K1-K3, canvas block 8).

Run all checks with:  uv run pytest checks
"""

import invariants as inv


def test_k1_sales_shape_and_keys(sales, raw_sales_data_lines):
    # Documented: 9,334 rows, 01.07.2013 - 31.07.2018
    assert raw_sales_data_lines == 9334, f"Raw file has {raw_sales_data_lines} data lines, documented 9,334"
    inv.check_sales_shape_and_keys(sales, raw_sales_data_lines)


def test_k2_revenue_positive(sales):
    inv.check_revenue_positive(sales)


def test_k3_calendar(sales):
    inv.check_calendar(sales)
