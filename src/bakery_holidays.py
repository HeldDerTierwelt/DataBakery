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
