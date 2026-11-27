"""Red before green: every check must fail on deliberately broken data.

If one of these tests fails, the corresponding check cannot catch the error
it is meant to catch.
"""

import pandas as pd
import pytest

import bakery_holidays as hol
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


def _filled(joined):
    return prep.fill_weather_gaps(joined, prep.weather_fill_values(joined))


def test_k5_catches_unflagged_gap(joined):
    broken = _filled(joined)
    # pretend one gap day was filled but not flagged
    broken.loc[broken["Datum"] == pd.Timestamp("2017-10-04"), "Wetter_fehlt"] = 0
    with pytest.raises(AssertionError):
        inv.check_weather_fill(broken, joined)


def test_k5_catches_changed_measured_value(joined):
    broken = _filled(joined)
    # pretend the fill overwrote a measured temperature
    broken.loc[broken.index[0], "Temperatur"] += 1.0
    with pytest.raises(AssertionError):
        inv.check_weather_fill(broken, joined)


def test_k5_catches_dropped_rows(joined):
    filled = _filled(joined)
    broken = filled[filled["Wetter_fehlt"] == 0]  # the old behaviour: gap days removed
    with pytest.raises(AssertionError):
        inv.check_weather_fill(broken, joined)


def test_k5_catches_fill_values_from_all_years(joined):
    def leaky_fill_values(data):
        days = data[["Datum", *prep.WEATHER_REQUIRED]].drop_duplicates("Datum")
        return days.groupby(days["Datum"].dt.month)[prep.WEATHER_REQUIRED].mean()
    with pytest.raises(AssertionError):
        inv.check_fill_values_training_only(leaky_fill_values, joined)


def test_k6_catches_validation_day_in_training(joined):
    kept = _filled(joined)
    train, val = prep.split(kept)
    moved = val[val["Datum"] == val["Datum"].min()]
    with pytest.raises(AssertionError):
        inv.check_split(pd.concat([train, moved]), val.drop(moved.index), kept)


def test_k6_catches_test_year_date(joined):
    kept = _filled(joined)
    future = kept.iloc[[0]].copy()
    future["Datum"] = pd.Timestamp("2018-08-01")
    broken = pd.concat([kept, future], ignore_index=True)
    train, val = prep.split(broken)
    with pytest.raises(AssertionError):
        inv.check_split(train, val, broken)


def test_k13_catches_missing_holiday(sales):
    import bakery_holidays as hol
    public_holidays = hol.public_holidays_sh(inv.FIRST_DATE, inv.LAST_DATE)
    # pretend the source forgot Ascension Day 2015
    broken = public_holidays[public_holidays["Datum"] != pd.Timestamp("2015-05-14")]
    with pytest.raises(AssertionError):
        inv.check_public_holidays(broken, sales)


def test_k13_catches_wrong_holiday_date(sales):
    import bakery_holidays as hol
    public_holidays = hol.public_holidays_sh(inv.FIRST_DATE, inv.LAST_DATE)
    # pretend the source puts German Unity Day 2016 one day late (an ordinary open day)
    broken = public_holidays.copy()
    broken.loc[broken["Datum"] == pd.Timestamp("2016-10-03"), "Datum"] = pd.Timestamp("2016-10-04")
    with pytest.raises(AssertionError):
        inv.check_public_holidays(broken, sales)


# --- K14-K16: holiday feature -------------------------------------------------

@pytest.fixture(scope="module")
def prepared(joined):
    filled = _filled(joined)
    train, val = prep.split(filled)
    return pd.concat([train.assign(split="train"), val.assign(split="validation")])


@pytest.fixture(scope="module")
def columns(prepared):
    return hol.interaction_columns(prepared[prepared["split"] == "train"])


def test_k14_catches_feature_from_sales(prepared, columns):
    def leaky(data):
        # "open" read from the sales: a holiday counts only if revenue is high
        out = hol.holiday_features(data, columns)
        out["open_holiday_g1"] = ((out["day_type"] == "open_holiday") & (data["Umsatz"] > 100)).astype(int)
        return out
    with pytest.raises(AssertionError):
        inv.check_holiday_feature_date_only(leaky, prepared)


def test_k15_catches_good_friday_as_open(prepared):
    def with_good_friday(dates):
        types = hol.day_type(dates)
        is_good_friday = pd.Series(pd.to_datetime(dates)).reset_index(drop=True).isin(inv.GOOD_FRIDAYS)
        return types.mask(is_good_friday, "open_holiday")
    with pytest.raises(AssertionError):
        inv.check_holiday_day_types(hol.day_type(prepared["Datum"]), prepared, with_good_friday)


def test_k15_catches_missing_special_day(prepared):
    broken = hol.day_type(prepared["Datum"])
    broken[(prepared["Datum"] == pd.Timestamp("2015-12-31")).to_numpy()] = "normal"
    with pytest.raises(AssertionError):
        inv.check_holiday_day_types(broken, prepared, hol.day_type)


def test_k16_catches_column_in_wrong_group(prepared, columns):
    broken = hol.holiday_features(prepared, columns)
    # pretend the bread column is also set on the rolls rows of the same holidays
    broken.loc[(broken["day_type"] == "open_holiday") & (broken["Warengruppe"] == 2), "open_holiday_g1"] = 1
    with pytest.raises(AssertionError):
        inv.check_holiday_interactions(broken, columns, prepared["split"] == "train")


def test_k16_catches_always_zero_column(prepared, columns):
    extra = [*columns, "open_holiday_g6"]  # seasonal bread never sells on an open holiday
    with pytest.raises(AssertionError):
        inv.check_holiday_interactions(hol.holiday_features(prepared, extra), extra, prepared["split"] == "train")
