"""Data preparation steps for the bakery project.

The notebooks and the checks in `checks/` both use these functions, so the
checks test exactly the code that produces our data.

Decisions behind each step: see DECISIONS.md and canvas block 7.
"""

import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/opencampus-sh/intro-to-data-science-and-ml/main/data/bakery/"

# Split by time (canvas block 4): training strictly before validation.
VALIDATION_START = pd.Timestamp("2017-08-01")
VALIDATION_END = pd.Timestamp("2018-07-31")

# Weather columns that are filled where missing, with the flag `Wetter_fehlt`
# (DECISIONS.md, "Weather gaps filled and flagged"). `Wettercode` is not in this
# list: a missing code means "no notable weather" and becomes its own class.
WEATHER_REQUIRED = ["Bewoelkung", "Temperatur", "Windgeschwindigkeit"]


def load_sales() -> pd.DataFrame:
    """Sales: one row per date and product group (only days with sales)."""
    return pd.read_csv(DATA_URL + "umsatzdaten_gekuerzt.csv", parse_dates=["Datum"])


def load_weather() -> pd.DataFrame:
    """Observed daily weather in Kiel (a stand-in for the forecast, canvas block 6)."""
    return pd.read_csv(DATA_URL + "wetter.csv", parse_dates=["Datum"])


def load_kiwo() -> pd.DataFrame:
    """Kiel Week days only (KielerWoche = 1)."""
    return pd.read_csv(DATA_URL + "kiwo.csv", parse_dates=["Datum"])


def join(sales: pd.DataFrame, weather: pd.DataFrame, kiwo: pd.DataFrame) -> pd.DataFrame:
    """Add weather and Kiel Week to each sales row (left joins on the date).

    Days that are not in the Kiel Week file get KielerWoche = 0.
    """
    data = sales.merge(weather, on="Datum", how="left").merge(kiwo, on="Datum", how="left")
    data["KielerWoche"] = data["KielerWoche"].fillna(0).astype(int)
    return data


def weather_fill_values(data: pd.DataFrame) -> pd.DataFrame:
    """Mean of each required weather column per calendar month (1-12).

    Uses the training period only (dates before VALIDATION_START), one value per
    date, so the validation and test years never influence the fill values.
    """
    days = (data.loc[data["Datum"] < VALIDATION_START, ["Datum", *WEATHER_REQUIRED]]
                .drop_duplicates("Datum"))
    return days.groupby(days["Datum"].dt.month)[WEATHER_REQUIRED].mean()


def fill_weather_gaps(data: pd.DataFrame, fill_values: pd.DataFrame) -> pd.DataFrame:
    """Fill missing required weather values and flag the affected rows.

    A missing value gets the training mean of its calendar month (from
    `weather_fill_values`). The new column `Wetter_fehlt` is 1 on rows where at
    least one required weather value was missing, else 0. Values that were
    measured are never changed, and no row is removed.
    """
    out = data.copy()
    out["Wetter_fehlt"] = out[WEATHER_REQUIRED].isna().any(axis=1).astype(int)
    month = out["Datum"].dt.month
    for col in WEATHER_REQUIRED:
        out[col] = out[col].fillna(month.map(fill_values[col]))
    return out


def split(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split by time into training (before VALIDATION_START) and validation."""
    train = data[data["Datum"] < VALIDATION_START].copy()
    val = data[(data["Datum"] >= VALIDATION_START) & (data["Datum"] <= VALIDATION_END)].copy()
    return train, val
