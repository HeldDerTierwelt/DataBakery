"""Checkpoint "features": the holiday feature (checks K14-K16, canvas block 8).

Run all checks with:  uv run pytest checks
"""

import pandas as pd
import pytest

import bakery_holidays as hol
import bakery_prep as prep
import invariants as inv


@pytest.fixture(scope="session")
def prepared(joined) -> pd.DataFrame:
    """Prepared rows (weather filled) with a `split` column, as in data preparation."""
    filled = prep.fill_weather_gaps(joined, prep.weather_fill_values(joined))
    train, val = prep.split(filled)
    return pd.concat([train.assign(split="train"), val.assign(split="validation")])


@pytest.fixture(scope="session")
def columns(prepared) -> list[str]:
    return hol.interaction_columns(prepared[prepared["split"] == "train"])


def test_k14_holiday_feature_uses_date_only(prepared, columns):
    inv.check_holiday_feature_date_only(lambda d: hol.holiday_features(d, columns), prepared)


def test_k15_holiday_day_types(prepared):
    inv.check_holiday_day_types(hol.day_type(prepared["Datum"]), prepared, hol.day_type)


def test_k16_holiday_interactions(prepared, columns):
    features = hol.holiday_features(prepared, columns)
    inv.check_holiday_interactions(features, columns, prepared["split"] == "train")
