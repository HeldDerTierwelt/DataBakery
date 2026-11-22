"""Checkpoints "merge", "weather-gap drop" and "split" (checks K4-K6, canvas block 8)."""

import bakery_prep as prep
import invariants as inv


def test_k4_join(joined, sales):
    inv.check_join(joined, sales)


def test_k5_weather_drop(joined):
    kept, removed = prep.drop_weather_gaps(joined)
    inv.check_weather_drop(kept, removed, joined)


def test_k6_split(joined):
    kept, _ = prep.drop_weather_gaps(joined)
    train, val = prep.split(kept)
    inv.check_split(train, val, kept)
