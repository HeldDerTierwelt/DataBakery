"""Public holidays and special days for the bakery project (hypothesis H3).

Public holidays come from the `holidays` package (DECISIONS.md, "Public holidays
from the `holidays` package"). Special days are not public holidays, so no
holiday source lists them; the team defined them (docs/h3-holidays-plan.md).
"""

import holidays
import pandas as pd
from dateutil.easter import easter


def public_holidays_sh(start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Public holidays in Schleswig-Holstein between start and end (both included).

    Returns one row per holiday with the columns `Datum` and `Feiertag` (German name).
    """
    years = range(start.year, end.year + 1)
    calendar = holidays.Germany(subdiv="SH", years=years, language="de")

    rows = [{"Datum": pd.Timestamp(day), "Feiertag": name} for day, name in calendar.items()]
    table = pd.DataFrame(rows).sort_values("Datum").reset_index(drop=True)
    in_period = (table["Datum"] >= start) & (table["Datum"] <= end)
    return table[in_period].reset_index(drop=True)


def special_days(start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
    """Special days between start and end: Easter Sunday, Whit Sunday,
    Christmas Eve and New Year's Eve (not public holidays, defined by the team).
    """
    rows = []
    for year in range(start.year, end.year + 1):
        easter_sunday = pd.Timestamp(easter(year))
        rows += [
            {"Datum": easter_sunday, "Feiertag": "Ostersonntag"},
            {"Datum": easter_sunday + pd.Timedelta(days=49), "Feiertag": "Pfingstsonntag"},
            {"Datum": pd.Timestamp(year, 12, 24), "Feiertag": "Heiligabend"},
            {"Datum": pd.Timestamp(year, 12, 31), "Feiertag": "Silvester"},
        ]
    table = pd.DataFrame(rows).sort_values("Datum").reset_index(drop=True)
    in_period = (table["Datum"] >= start) & (table["Datum"] <= end)
    return table[in_period].reset_index(drop=True)


# --- Holiday feature (DECISIONS.md, 2026-11-26 and 2026-11-27) -----------------

# Day types in a fixed order; "normal" is the reference and gets no column.
DAY_TYPES = ["normal", "open_holiday", "easter_whit_sunday", "christmas_eve", "new_years_eve"]

# The only public holiday on which a bakery must stay closed (LÖffZG SH § 4 Abs. 1).
CLOSED_BY_LAW = "Karfreitag"

SPECIAL_DAY_TYPES = {
    "Ostersonntag": "easter_whit_sunday",
    "Pfingstsonntag": "easter_whit_sunday",
    "Heiligabend": "christmas_eve",
    "Silvester": "new_years_eve",
}


def day_type(dates: pd.Series) -> pd.Series:
    """Holiday day type of each date, from the calendar only (never from sales).

    - open_holiday: a public holiday in Schleswig-Holstein other than Good Friday
      (a bakery may open on all of them by law).
    - easter_whit_sunday, christmas_eve, new_years_eve: the special days.
    - normal: every other date. Good Friday is also "normal" here; the bakery is
      closed by law, so such a date never has a sales row.
    """
    dates = pd.Series(pd.to_datetime(dates)).reset_index(drop=True)
    start, end = dates.min(), dates.max()

    public = public_holidays_sh(start, end)
    public = public[public["Feiertag"] != CLOSED_BY_LAW]
    special = special_days(start, end)

    lookup = {day: "open_holiday" for day in public["Datum"]}
    for day, name in zip(special["Datum"], special["Feiertag"]):
        lookup[day] = SPECIAL_DAY_TYPES[name]

    return dates.map(lookup).fillna("normal").rename("day_type")


def interaction_columns(train: pd.DataFrame) -> list[str]:
    """Names of the interaction columns day type x product group, learned from training.

    A combination is kept only if it occurs at least once in the training rows
    (e.g. seasonal bread never sells on an open public holiday, so that column
    would always be 0). Column names look like "open_holiday_g1".
    """
    types = day_type(train["Datum"])
    seen = set(zip(types, train["Warengruppe"]))
    return [
        f"{t}_g{g}"
        for t in DAY_TYPES[1:]
        for g in sorted(train["Warengruppe"].unique())
        if (t, g) in seen
    ]


def holiday_features(data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Holiday feature table: one row per row of `data`, same index.

    Returns `Datum`, `Warengruppe`, `day_type` and one 0/1 column per name in
    `columns` (from `interaction_columns`). A column "<type>_g<group>" is 1 only
    on that day type and in that product group. Only the date and the product
    group are used.
    """
    out = data[["Datum", "Warengruppe"]].copy()
    out["day_type"] = day_type(out["Datum"]).to_numpy()
    for col in columns:
        t, g = col.rsplit("_g", 1)
        out[col] = ((out["day_type"] == t) & (out["Warengruppe"] == int(g))).astype(int)
    return out
