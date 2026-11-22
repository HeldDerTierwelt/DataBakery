# Data fact sheet

Profiled on 2026-11-22 from the course repository (`https://raw.githubusercontent.com/opencampus-sh/intro-to-data-science-and-ml/main/data/bakery/`). All numbers come from running the profiling code, not from the documentation. Where the two disagree, this sheet says so.

**Origin:** provided by meteolytix GmbH (a former Kiel forecasting company) for the opencampus.sh course *Introduction to Data Science and Machine Learning*. One bakery branch in Kiel. **License:** not stated in the source.

## 1. Sales – `umsatzdaten_gekuerzt.csv`

- **Shape / grain:** 9,334 rows × 4 columns (`id`, `Datum`, `Warengruppe`, `Umsatz`). One row = one date × one product group, **only for days with sales**.
- **Keys:** `id` is unique. (`Datum`, `Warengruppe`) is unique. `id` = `YYMMDD`·10 + group for every row.
- **Time coverage:** 2013-07-01 – 2018-07-31, 1,819 dates with sales. The test year 2018-08-01 – 2019-07-31 is held back by the course (Kaggle).
- **Missing values:** none in any column.
- **Currency:** **not stated in the source.** Probably €, but unconfirmed.

### Revenue per product group

| Group | Name | Rows | Mean | Median | Min | Max |
|---|---|---|---|---|---|---|
| 1 | Bread (Brot) | 1,819 | 122.1 | 120.1 | 23.1 | 416.8 |
| 2 | Rolls (Brötchen) | 1,819 | 402.5 | 370.8 | 175.0 | 1,203.4 |
| 3 | Croissants | 1,819 | 163.3 | 142.8 | 37.7 | 565.9 |
| 4 | Confectionery (Konditorei) | 1,766 | 88.0 | 80.0 | 27.4 | 430.5 |
| 5 | Cakes (Kuchen) | 1,819 | 276.8 | 266.0 | 121.5 | 1,879.5 |
| 6 | Seasonal bread (Saisonbrot) | 292 | 66.9 | 62.9 | 7.1 | 172.9 |

No revenue ≤ 0.

### Days with no row at all (38)

All groups are missing on these dates. Most are public holidays: 25/26 Dec, 1 Jan, Good Friday, 1 May, Whit Monday 2018-05-21, Reformation Day 2017-10-31. **12 are not public holidays in Schleswig-Holstein:** 2013-12-28, 2014-05-03, 2014-05-04, 2014-08-17, 2016-03-24, 2016-07-07, 2016-07-18, 2016-08-14, 2016-08-15, 2016-12-17, 2017-07-04, 2017-10-23. 2014-05-01/03/04 form a closed block; the day after, 2014-05-05 (Mon), is the highest day of the whole period for groups 2 and 3.

Full list: 2013-12-25, 2013-12-26, 2013-12-28, 2014-01-01, 2014-04-18, 2014-05-01, 2014-05-03, 2014-05-04, 2014-08-17, 2014-12-25, 2014-12-26, 2015-01-01, 2015-04-03, 2015-05-01, 2015-12-25, 2015-12-26, 2016-01-01, 2016-03-24, 2016-03-25, 2016-07-07, 2016-07-18, 2016-08-14, 2016-08-15, 2016-12-17, 2016-12-25, 2016-12-26, 2017-01-01, 2017-04-14, 2017-05-01, 2017-07-04, 2017-10-23, 2017-10-31, 2017-12-25, 2017-12-26, 2018-01-01, 2018-03-30, 2018-05-01, 2018-05-21.

### Group 4 (Confectionery) missing on 53 open days

16 in December (incl. 24 and 31 Dec in 2013 and 2014, 2015-12-31), 11 in July. 37 of them fall in 2013–2014. The last gap is 2016-07-26; **there are no gaps from 2016-08 onward**, so the validation year has none.

Patterns in the gaps:
- **Fading out:** share of open days without group 4 was 8.8% (2013), 6.4% (2014), 2.8% (2015), 1.1% (2016), 0% (2017, 2018).
- **December:** 11.2% of December open days, compared with 0–3% in other months. None in January or February.
- **Next to closed days:** 15.1% of gaps are within ±1 day of a closed day, compared with 3.2% of all open days.
- **Weekday:** Mon 7, Tue 9, Wed 13, Thu 5, Fri 9, Sat 9, **Sun 1**.
- **Runs:** 32 single days, 5 × 2 days, 2 × 3 days, 1 × 5 days (2013-07-27 – 07-31).
- **Other groups on gap days:** revenue relative to the typical same-weekday value (median) was bread 1.04, rolls 1.08, croissants 1.06, cakes 1.00. The shop was open and busy.
- **Confectionery next to gaps:** ratio to typical was 1.00 the day before (n = 37) and 1.00 the day after (n = 34). No fade.

Reading: these are not low-demand days. The data cannot tell whether confectionery was not offered or simply not recorded.

### Group 6 (Seasonal bread)

| Season | First | Last | Rows | Open days without a row inside the span |
|---|---|---|---|---|
| 2013/14 | 2013-10-24 | 2014-01-02 | 65 | 2 |
| 2014/15 | 2014-10-24 | 2015-01-06 | 66 | 6 |
| 2015/16 | 2015-11-02 | 2015-12-31 | 53 | 5 |
| 2016/17 | 2016-11-03 | 2016-12-29 | 52 | 2 |
| 2017/18 | 2017-10-30 | 2017-12-27 | 56 | 0 |

By month: Oct 13, Nov 140, Dec 133, Jan 6 rows. The start of the season varies between late October and early November.

### Extreme values (> Q3 + 3·IQR per group)

- **Group 5 (Cakes):** 31 December of every year (1,432–1,879, about 6× the median), probably New Year's Eve pastries.
- **Group 1 (Bread):** Maundy Thursday and Holy Saturday (e.g. 2018-03-29/31, 2017-04-13/15).
- **Group 4 (Confectionery):** 27 days, the highest on Sundays in February (2014-02-09, 2014-02-23, 2015-02-22, 2016-02-21). Cause unknown.
- **2014-05-05 (Mon):** high in groups 1–4, the day after a 3-day closure.

These look like real demand peaks, not data errors.

### Level over time

| Year | Days | Mean daily total |
|---|---|---|
| 2013 (from Jul) | 181 | 1,178.5 |
| 2014 | 357 | 1,188.6 |
| 2015 | 360 | 1,049.1 |
| 2016 | 356 | 988.9 |
| 2017 | 357 | 990.0 |
| 2018 (to Jul) | 208 | 1,004.9 |

Revenue fell about 17% from 2014 to 2016, then stayed flat.

**Weekday (mean daily total):** Mon 994, Tue 965, Wed 957, Thu 995, Fri 1,008, Sat 1,235, Sun 1,272.

### Sell-out signal (canvas question C)

If sell-outs were frequent, revenue would bunch up just below a ceiling. Check: revenue ÷ rolling median of the same group and weekday (9 weeks, centred).
- The upper tail is **wider**, not compressed: (q95 − q50)/(q50 − q05) = 1.41 / 1.81 / 1.70 / 1.73 / 1.45 / 1.91 for groups 1–6.
- Consecutive same-weekday values within 1% of each other: 2.9% / 5.2% / 2.8% / 2.4% / 4.3% / 1.0%.

**No ceiling is visible.** The data shows no detectable sell-out pattern.

## 2. Weather – `wetter.csv`

- **Shape / grain:** 2,601 rows × 5 columns. One row = one date. `Datum` is unique.
- **Coverage:** 2012-01-01 – 2019-08-01. 169 dates have no row; **3 of them are sales days:** 2016-12-11, 2017-10-04, 2017-10-05. The last two fall in the validation year.
- **Columns:**

| Column | Meaning | Unit | Range | Missing |
|---|---|---|---|---|
| `Bewoelkung` | cloud cover | octas 0–8 (integers) | 0–8 | 10 |
| `Temperatur` | mean temperature | °C | −10.25 – 32.67 | 0 |
| `Windgeschwindigkeit` | mean wind speed | m/s (per docs) | 3 – 35 | 0 |
| `Wettercode` | WMO present-weather code | code 00–99 (41 distinct values used) | 0 – 95 | 669 |

- **`Bewoelkung` missing:** 10 consecutive days, 2017-10-30 – 2017-11-08, all in the validation year.
- **`Wettercode` missing is not random:**

| Days | Mean cloud cover | Mean temperature |
|---|---|---|
| without a code | 3.29 | 15.44 °C |
| with a code | 5.32 | 10.94 °C |

  So a missing code means calm, clear, warm weather. The share of missing codes falls over time (2014: 129 days, 2018: 39 days, partial year).
- **Wind speed caveat:** a minimum of 3 and a maximum of 35 is high for daily means in m/s. The unit may be knots or km/h; this is unconfirmed.
- **Known in advance:** these are observed values. A stand-in for the forecast (canvas block 6).

## 3. Kiel Week – `kiwo.csv`

- **Shape:** 72 rows × 2 columns (`Datum`, `KielerWoche` = always 1). No duplicates.
- **Coverage:** 2012–2019, 9 consecutive days per year (Saturday to Sunday, mid/late June).
- **Inside the sales period:** 45 days = **5 Kiel Weeks (2014–2018)**. Kiel Week 2013 (22–30 Jun) is before the sales data starts. All 45 days have sales.

| Group | Mean revenue during Kiel Week | Mean otherwise |
|---|---|---|
| 1 Bread | 136.0 | 121.8 |
| 2 Rolls | 538.6 | 399.0 |
| 3 Croissants | 223.3 | 161.8 |
| 4 Confectionery | 81.2 | 88.1 |
| 5 Cakes | 315.7 | 275.8 |

These means are not adjusted for weekday or season, so they are only a first look.

## 4. Joins

- **Sales ⟕ weather** (left join on `Datum`): 9,334 rows before and after. 1,816 of 1,819 sales dates (99.84%) find a weather row. 3 dates have none.
- **Sales ⟕ Kiel Week** (left join on `Datum`): 9,334 rows before and after. 223 rows get `KielerWoche = 1`; all others are missing and must be set to 0.
- No join changes the row count.
