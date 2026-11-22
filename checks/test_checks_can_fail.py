"""Red before green: every check must fail on deliberately broken data.

If one of these tests fails, the corresponding check cannot catch the error
it is meant to catch.
"""

import pandas as pd
import pytest

import bakery_prep as prep
import invariants as inv


def test_k1_catches_duplicate_row(sales, raw_sales_data_lines):
    broken = pd.concat([sales, sales.iloc[[0]]], ignore_index=True)
    with pytest.raises(AssertionError):
        inv.check_sales_shape_and_keys(broken, raw_sales_data_lines)


def test_k1_catches_wrong_id(sales, raw_sales_data_lines):
    broken = sales.copy()
    broken.loc[0, "id"] = 1307019  # unique, but says group 9 for a group-1 row
    with pytest.raises(AssertionError):
        inv.check_sales_shape_and_keys(broken, raw_sales_data_lines)


def test_k2_catches_zero_revenue(sales):
    broken = sales.copy()
    broken.loc[0, "Umsatz"] = 0.0
    with pytest.raises(AssertionError):
        inv.check_revenue_positive(broken)


def test_k3_catches_missing_date(sales):
    broken = sales[sales["Datum"] != pd.Timestamp("2016-06-15")]
    with pytest.raises(AssertionError):
        inv.check_calendar(broken)


def test_k3_catches_added_closed_day(sales):
    extra = sales.iloc[[0]].copy()
    extra["Datum"] = pd.Timestamp("2015-12-25")
    with pytest.raises(AssertionError):
        inv.check_calendar(pd.concat([sales, extra], ignore_index=True))


def test_k4_catches_duplicate_weather_date(sales):
    weather = prep.load_weather()
    weather_dup = pd.concat([weather, weather[weather["Datum"] == pd.Timestamp("2016-06-15")]])
    broken = prep.join(sales, weather_dup, prep.load_kiwo())
    with pytest.raises(AssertionError):
        inv.check_join(broken, sales)


def test_k4_catches_unfilled_kiel_week(joined, sales):
    broken = joined.copy()
    broken.loc[broken["KielerWoche"] == 0, "KielerWoche"] = float("nan")
    with pytest.raises(AssertionError):
        inv.check_join(broken, sales)


def test_k5_catches_missing_drop(joined):
    kept, removed = prep.drop_weather_gaps(joined)
    # pretend one gap day was not dropped
    leaked = removed[removed["Datum"] == pd.Timestamp("2017-10-04")]
    with pytest.raises(AssertionError):
        inv.check_weather_drop(
            pd.concat([kept, leaked]), removed.drop(leaked.index), joined
        )


def test_k6_catches_validation_day_in_training(joined):
    kept, _ = prep.drop_weather_gaps(joined)
    train, val = prep.split(kept)
    moved = val[val["Datum"] == val["Datum"].min()]
    with pytest.raises(AssertionError):
        inv.check_split(pd.concat([train, moved]), val.drop(moved.index), kept)


def test_k6_catches_test_year_date(joined):
    kept, _ = prep.drop_weather_gaps(joined)
    future = kept.iloc[[0]].copy()
    future["Datum"] = pd.Timestamp("2018-08-01")
    broken = pd.concat([kept, future], ignore_index=True)
    train, val = prep.split(broken)
    with pytest.raises(AssertionError):
        inv.check_split(train, val, broken)
