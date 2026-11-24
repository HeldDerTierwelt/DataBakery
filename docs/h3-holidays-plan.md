# Analysis plan H3: open public holidays

**Hypothesis (canvas block 2, H3):** per product group, revenue (€) is higher on public holidays (Schleswig-Holstein) on which the shop is open than on the same weekday without a holiday.
**Notebook:** [`1_DatasetCharacteristics/Alexander-Holidays.ipynb`](../1_DatasetCharacteristics/Alexander-Holidays.ipynb)
**Decisions:** `DECISIONS.md`, entries "H3 means open public holidays" and "How H3 is tested" (2026-11-22). Terms: `GLOSSARY.md` (*Open public holiday*, *Special day*, *Holiday ratio*).

## Facts from the data

- The shop is open on 20 of the 46 public holidays in the sales period, always on the same ones: Easter Monday, Ascension Day, Whit Monday, German Unity Day (5 each, Whit Monday 2018 closed), 1 May 2016 (a Sunday). Closed: New Year, Good Friday, 1 May (except 2016), Christmas Day, Boxing Day, Reformation Day 2017, Whit Monday 2018.
- **Training period:** 17 open holidays (4 each of Easter Monday, Ascension Day, Whit Monday, German Unity Day; 1 May once). **Validation year:** 3 (2017-10-03, 2018-04-02, 2018-05-10).
- Groups 1–5 have a row on all 20 days. Seasonal bread (6) never occurs: its season starts 24 Oct at the earliest.
- Weekdays: Easter and Whit Monday are always Mondays, Ascension Day always a Thursday; only German Unity Day moves through the week.
- **Source of public holidays:** the Python package [`holidays`](https://github.com/vacanza/holidays) (version 0.109, pinned in `uv.lock`), `holidays.Germany(subdiv="SH")`. It covers historical changes such as Reformation Day (once in 2017, permanent in SH from 2018). Checked on 2026-11-22: it gives the same 46 public holidays in the sales period (20 open, 26 closed) as an independent calculation from fixed and Easter-based dates.
- **Special days** are not public holidays, so no holiday source lists them. They are defined by the team: Easter Sunday and Whit Sunday (from the Easter date, `dateutil.easter`), Christmas Eve (24 Dec), New Year's Eve (31 Dec).

## Method

0. **Source check:** in the notebook, the holiday list from `holidays` is matched against the raw sales: exactly 46 public holidays in the sales period, 20 with sales, 26 without, and all 26 among the 38 closed days. If this fails, the notebook stops.
1. **Holiday ratio** per holiday × group: revenue on the holiday ÷ median revenue of the same group on the same weekday in the 4 weeks before and after (up to 8 days; other holidays, special days and Kiel Week days excluded).
2. **Baseline check:** how far the D−7 baseline misses on these days compared with normal days.
3. **Reported pooled** over all 17 holidays **and per holiday** (Easter Monday, Ascension Day, Whit Monday, German Unity Day, 1 May), each per group.
4. **Special days** (Easter Sunday, Whit Sunday, Christmas Eve, New Year's Eve): same ratio, as a separate table. Not part of H3.
5. **Data:** training period only. The validation year stays untouched.

## When H3 counts as supported (per group)

- Median holiday ratio ≥ 1.10 (at least 10 % more) **and** revenue higher than the comparison on at least 13 of the 17 training holidays.
- The range (min–max of the ratio) is always reported. A Wilcoxon signed-rank test only as an extra, not as the criterion.
- Per holiday: values only, no yes/no (4 cases, 1 May only 1).

## Audiences

- **Operations manager:** one sentence per group in the memo, e.g. "on open public holidays about +X % rolls (range Y–Z %)".
- **Technical reader:** the notebook.

## Known in advance

Public holidays are known months ahead, so a 0/1 holiday feature is allowed in the model. The holiday ratio uses the weeks *after* a holiday; that is fine for this descriptive analysis only and never becomes a model feature.

## What the data cannot answer

- Sold-out holidays: true demand may be higher than revenue.
- Only 4 independent cases per holiday (17 in total), so the result is a tendency, not proof.
- Mostly Mondays and Thursdays, so a holiday effect on other weekdays cannot be told apart.
- Days around holidays (e.g. the day before Good Friday) are not covered; open question on the canvas.

## Ideas for later (not decided)

- **"A holiday sells like a Sunday."** A quick check outside the notebook (2026-11-22) compared each open holiday with the Sundays in the 4 weeks before and after: per group, holidays were only about 6–18 % above those Sundays (median). If this holds, a simple model feature could be "treat an open holiday like a Sunday". Not yet in the notebook; the team decides whether to add it.
