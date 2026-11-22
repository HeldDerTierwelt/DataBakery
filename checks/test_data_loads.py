"""First check: the main sales dataset loads and has the documented shape.

Run all checks with:  uv run pytest checks
"""

import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/opencampus-sh/intro-to-data-science-and-ml/main/data/bakery/"


def test_sales_data_loads():
    sales = pd.read_csv(DATA_URL + "umsatzdaten_gekuerzt.csv")

    # Columns as described in the dataset documentation
    assert list(sales.columns) == ["id", "Datum", "Warengruppe", "Umsatz"]
    # Row count as documented (9,334 rows, 01.07.2013 - 31.07.2018)
    assert len(sales) == 9334
    # The id is a unique key
    assert sales["id"].is_unique
