"""Check functions K1-K6 (canvas block 8).

Each function compares pipeline output with an independent source of truth
(the raw file, the calendar, a fixed list from the data fact sheet, or the
split dates written out literally) and raises AssertionError with a plain
message when something is off.

The tests in this folder call them on the real data (they must pass) and on
deliberately broken data (they must fail), see test_checks_can_fail.py.
"""

import pandas as pd

# --- Independent sources of truth (from docs/data-fact-sheet.md) -------------

SALES_COLUMNS = ["id", "Datum", "Warengruppe", "Umsatz"]
FIRST_DATE = pd.Timestamp("2013-07-01")
LAST_DATE = pd.Timestamp("2018-07-31")

# The 38 dates without any sales row (branch closed).
CLOSED_DAYS = pd.to_datetime([
    "2013-12-25", "2013-12-26", "2013-12-28", "2014-01-01", "2014-04-18", "2014-05-01",
    "2014-05-03", "2014-05-04", "2014-08-17", "2014-12-25", "2014-12-26", "2015-01-01",
    "2015-04-03", "2015-05-01", "2015-12-25", "2015-12-26", "2016-01-01", "2016-03-24",
    "2016-03-25", "2016-07-07", "2016-07-18", "2016-08-14", "2016-08-15", "2016-12-17",
    "2016-12-25", "2016-12-26", "2017-01-01", "2017-04-14", "2017-05-01", "2017-07-04",
    "2017-10-23", "2017-10-31", "2017-12-25", "2017-12-26", "2018-01-01", "2018-03-30",
    "2018-05-01", "2018-05-21",
])

# Sales dates dropped because weather is missing (DECISIONS.md, "Weather gaps dropped").
# 2017-10-31 is a closed day, so 12 of the 13 weather-gap dates are sales dates.
WEATHER_GAP_DATES = pd.to_datetime([
    "2016-12-11", "2017-10-04", "2017-10-05",
    "2017-10-30", "2017-11-01", "2017-11-02", "2017-11-03", "2017-11-04",
    "2017-11-05", "2017-11-06", "2017-11-07", "2017-11-08",
])
WEATHER_GAP_ROWS = 70
WEATHER_REQUIRED = ["Bewoelkung", "Temperatur", "Windgeschwindigkeit"]

KIWO_ROWS = 223   # sales rows on Kiel Week days
KIWO_DATES = 45   # 5 Kiel Weeks x 9 days, 2014-2018

LAST_TRAIN_DATE = pd.Timestamp("2017-07-31")
VAL_FIRST = pd.Timestamp("2017-08-01")
VAL_LAST = pd.Timestamp("2018-07-31")


# --- K1: raw sales shape and keys -------------------------------------------

def check_sales_shape_and_keys(sales: pd.DataFrame, raw_data_lines: int) -> None:
    assert list(sales.columns) == SALES_COLUMNS, f"Unexpected columns: {list(sales.columns)}"
    assert len(sales) == raw_data_lines, (
        f"Loaded {len(sales)} rows, but the raw file has {raw_data_lines} data lines"
    )
    dup = sales.duplicated(["Datum", "Warengruppe"])
    assert not dup.any(), f"{dup.sum()} duplicated (Datum, Warengruppe) pairs"
    assert sales["id"].is_unique, "id is not unique"
    expected_id = sales["Datum"].dt.strftime("%y%m%d").astype(int) * 10 + sales["Warengruppe"]
    wrong = sales["id"] != expected_id
    assert not wrong.any(), f"{wrong.sum()} ids do not match YYMMDD + product group"


# --- K2: revenue present and positive ----------------------------------------

def check_revenue_positive(sales: pd.DataFrame) -> None:
    missing = sales["Umsatz"].isna().sum()
    assert missing == 0, f"Umsatz missing in {missing} rows"
    nonpos = (sales["Umsatz"] <= 0).sum()
    assert nonpos == 0, f"Umsatz <= 0 in {nonpos} rows (no zero-revenue rows may be added)"


# --- K3: calendar coverage ---------------------------------------------------

def check_calendar(sales: pd.DataFrame) -> None:
    dates = pd.DatetimeIndex(sales["Datum"].unique())
    assert dates.min() == FIRST_DATE, f"First date is {dates.min().date()}, expected {FIRST_DATE.date()}"
    assert dates.max() == LAST_DATE, f"Last date is {dates.max().date()}, expected {LAST_DATE.date()}"
    calendar = pd.date_range(FIRST_DATE, LAST_DATE)
    missing = calendar.difference(dates)
    assert missing.equals(CLOSED_DAYS), (
        f"Missing dates differ from the 38 known closed days. "
        f"Unexpectedly missing: {[d.date() for d in missing.difference(CLOSED_DAYS)]}; "
        f"unexpectedly present: {[d.date() for d in CLOSED_DAYS.difference(missing)]}"
    )
    assert len(dates) == 1819, f"{len(dates)} sales dates, expected 1,819"


# --- K4: joins ---------------------------------------------------------------

def check_join(joined: pd.DataFrame, sales: pd.DataFrame) -> None:
    assert len(joined) == len(sales), (
        f"Join changed the row count: {len(sales)} -> {len(joined)} (duplicate keys on the right side?)"
    )
    assert not joined.duplicated(["Datum", "Warengruppe"]).any(), "Join created duplicate (Datum, Warengruppe)"
    values = set(joined["KielerWoche"].unique())
    assert values <= {0, 1}, f"KielerWoche has values other than 0/1: {values}"
    kw = joined[joined["KielerWoche"] == 1]
    assert len(kw) == KIWO_ROWS, f"{len(kw)} Kiel Week rows, expected {KIWO_ROWS}"
    assert kw["Datum"].nunique() == KIWO_DATES, f"{kw['Datum'].nunique()} Kiel Week dates, expected {KIWO_DATES}"


# --- K5: weather-gap drop ------------------------------------------------------

def check_weather_drop(kept: pd.DataFrame, removed: pd.DataFrame, joined: pd.DataFrame) -> None:
    assert len(kept) + len(removed) == len(joined), "Rows were lost or added while dropping weather gaps"
    removed_dates = pd.DatetimeIndex(sorted(removed["Datum"].unique()))
    assert removed_dates.equals(WEATHER_GAP_DATES), (
        f"Removed dates differ from the 12 known weather-gap dates: {[d.date() for d in removed_dates]}"
    )
    assert len(removed) == WEATHER_GAP_ROWS, f"{len(removed)} rows removed, expected {WEATHER_GAP_ROWS}"
    left = kept[WEATHER_REQUIRED].isna().sum()
    assert left.sum() == 0, f"Missing weather left after the drop: {left[left > 0].to_dict()}"


# --- K6: time split ----------------------------------------------------------

def check_split(train: pd.DataFrame, val: pd.DataFrame, data: pd.DataFrame) -> None:
    assert len(train) + len(val) == len(data), (
        f"Split lost or duplicated rows: {len(train)} + {len(val)} != {len(data)}"
    )
    assert train["Datum"].max() <= LAST_TRAIN_DATE, (
        f"Training contains {train['Datum'].max().date()}, after {LAST_TRAIN_DATE.date()}"
    )
    assert val["Datum"].min() >= VAL_FIRST and val["Datum"].max() <= VAL_LAST, (
        f"Validation spans {val['Datum'].min().date()} - {val['Datum'].max().date()}, "
        f"expected within {VAL_FIRST.date()} - {VAL_LAST.date()}"
    )
    assert data["Datum"].max() <= VAL_LAST, (
        f"Data contains {data['Datum'].max().date()}, inside the held-back test year"
    )
    overlap = set(train["Datum"]) & set(val["Datum"])
    assert not overlap, f"{len(overlap)} dates are in both training and validation"
