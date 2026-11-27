"""Checkpoints "merge", "weather-gap fill" and "split" (checks K4-K6, canvas block 8)."""

import bakery_prep as prep
import invariants as inv


def test_k4_join(joined, sales):
    inv.check_join(joined, sales)


def test_k5_weather_fill(joined):
    filled = prep.fill_weather_gaps(joined, prep.weather_fill_values(joined))
    inv.check_weather_fill(filled, joined)


def test_k5_fill_values_from_training_only(joined):
    inv.check_fill_values_training_only(prep.weather_fill_values, joined)


def test_k6_split(joined):
    filled = prep.fill_weather_gaps(joined, prep.weather_fill_values(joined))
    train, val = prep.split(filled)
    inv.check_split(train, val, filled)
