"""Shared test data: each file is downloaded once per test run."""

import pandas as pd
import pytest
import requests

import bakery_prep as prep


@pytest.fixture(scope="session")
def sales() -> pd.DataFrame:
    return prep.load_sales()


@pytest.fixture(scope="session")
def raw_sales_data_lines() -> int:
    """Number of data lines in the raw sales file (header and blank lines excluded).

    Counted from the text itself, independent of pandas.
    """
    text = requests.get(prep.DATA_URL + "umsatzdaten_gekuerzt.csv", timeout=60).text
    lines = [line for line in text.splitlines() if line.strip()]
    return len(lines) - 1


@pytest.fixture(scope="session")
def joined(sales) -> pd.DataFrame:
    return prep.join(sales, prep.load_weather(), prep.load_kiwo())
