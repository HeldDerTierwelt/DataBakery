# Agentic Data Science Canvas

**Project:** DataBakery
**Team:** c-avery, zzhang-90, HeldDerTierwelt
**Version:** 2026-11-17

> Owners: 👤 human decides · 🤖 agent drafts, human approves.
> Keep each block short. Details go in linked files; decisions go in `DECISIONS.md`.

---

## Problem

### 1. Decision 👤
<!-- Who decides what, when and how often? What happens today without this analysis? -->
**Decision-maker:** the bakery's operations manager (single branch).
**Decision:** how much of each product group (1 Bread, 2 Rolls, 3 Croissants, 4 Confectionery, 5 Cakes, 6 Seasonal bread) to bake for tomorrow.
**When / how often:** every opening day, plan fixed around 14:00 the day before. Closed holidays are not planned.
**Output:** expected sales value (€ revenue) per group. Converted to pieces once the client supplies average prices per group (see Open questions).
**Scope notes:** Seasonal bread (6) only October–January. Confectionery (4) days without an entry still to be clarified (block 7).
**Today (assumed):** the manager bakes roughly what sold on the same weekday last week. To be confirmed by the client.

### 2. Questions 👤
<!-- The analysis questions that would change the decision. For each: what the data can answer, and what it cannot. -->
- **A (main):** What revenue (€) should we expect per product group tomorrow, and within what range? The range lets the manager decide whether to bake above or below the forecast.
- **B (explaining):** Which factors shift demand per group, and by how much? Candidates: weekday, season, holidays, Kiel Week, temperature, rain.
  Hypotheses to test (chosen by the team, 2026-11-22):
  - **H1 (weekend):** All product groups sell more on weekends (Sat, Sun) than on weekdays (Mon–Fri).
  - **H2 (Kiel Week):** Sales are higher during Kiel Week, and there are more sold-out days. *Note:* only the revenue part can be tested. Sold-out days cannot be seen in the data (see C), and there are only 5 Kiel Weeks.
  - **H3 (holidays):** Per product group, revenue is higher on public holidays (Schleswig-Holstein) on which the shop is open (20 of 46; 17 in training) than on the same weekday without a holiday. Special days (Easter/Whit Sunday, Christmas Eve, New Year's Eve) separately; school holidays not part of H3. *Limit:* only 4 cases per holiday. Plan: [docs/h3-holidays-plan.md](docs/h3-holidays-plan.md).
- **C (sold out):** On which days did a group probably sell out, so that more could have been sold? Answered only from the sales data. No sold-out records exist and none will be collected. /explore-data found **no detectable sell-out pattern** (no ceiling in revenue). The answer is reported as that limit, plus, once a model exists, a list of days with revenue far below the forecast, each labelled "possible sell-out or low demand – not distinguishable".

**What the data cannot answer:** real demand on sold-out days (sales are capped by what was baked), sold-out days themselves, waste/leftovers, the effect of prices or new products, local events other than Kiel Week, other branches. Patterns around Christmas, Kiel Week and the seasonal-bread season rest on only 5 cases each.

### 3. Audiences 👤
<!-- Who receives which result, in which form? At least: the decision-maker and the technical reader. -->
- **Operations manager (decision-maker):** short memo, answer first. It gives expected € per group for a typical week, the range, and when not to trust the forecast (December, Kiel Week, suspected sell-out days). Plus a simple daily table per group.
- **Technical reader (course instructors, future team):** README and notebooks that run top to bottom, `experiments/LOG.md`, `DECISIONS.md`.
- **Course presentation:** told from the manager's point of view (decision → answer → limits), with method details in the backup slides.

### 4. Success 👤
<!-- Metric(s), the baseline to beat, what is good enough to act on. Which errors are worse than others? -->
- **Metric:** MAPE (main), per group and overall. MAE in € as the figure the manager can picture.
- **Baseline:** "same weekday last week" (revenue on D−7, per group).
- **Good enough to act on:** overall MAPE at least 10% lower than the baseline (relative), **and** lower MAPE than the baseline in each of groups 1 Bread, 2 Rolls, 5 Cakes.
- **Error cost:** treated as symmetric for now. Whether running out is worse than leftovers is an open question for the client.
- **H3** counts as supported for a group at a median holiday ratio ≥ 1.10 on at least 13 of 17 training holidays (details in the plan).
- **Split (by time):** train 2013-07-01 – 2017-07-31; validation 2017-08-01 – 2018-07-31. The course's held-back period after 2018-07-31 is used once, at the end.
- **Segments reported separately:** product group; weekday (Mon–Sun); December/holidays; Kiel Week; summer vs. winter. The validation year holds only one Christmas and one Kiel Week, so segment results there are single cases.

---

## Data and method

### 5. Data 🤖
<!-- Sources, unit of observation, period covered, keys, known gaps. Link the data fact sheet. -->
Details: [docs/data-fact-sheet.md](docs/data-fact-sheet.md). Source: meteolytix GmbH via the opencampus.sh course; one branch in Kiel; license not stated.
- **Sales:** 9,334 rows; one row = date × product group, only for days with sales. 2013-07-01 – 2018-07-31. Key (`Datum`, `Warengruppe`) is unique; no missing values. **Currency not stated** (probably €).
- **Gaps:** 38 dates with no rows (26 public holidays, 12 other days). Group 4 is missing on 53 open days, none after 2016-07. Group 6 only late Oct – early Jan, with 15 in-season gaps.
- **Peaks:** Cakes on 31 Dec (about 6× the median), Bread before Easter, the day after a 3-day closure (2014-05-05). Revenue level fell about 17% from 2014 to 2016.
- **Weather:** 2012-01-01 – 2019-08-01, one row per date. 3 sales dates have no weather row. `Bewoelkung` missing on 10 days (2017-10-30 – 11-08). `Wettercode` missing on 669 days, mostly on clear, warm days, so not random. Wind speed unit unclear.
- **Kiel Week:** 9 days per year. 5 Kiel Weeks (2014–2018) fall in the sales period.
- **Public holidays (SH):** from the Python package `holidays` (pinned in `uv.lock`). 46 in the sales period: 20 open, 26 closed.
- **Joins** on `Datum` (left) keep 9,334 rows.
- **Sell-out signal:** none visible (no ceiling in revenue). See fact sheet §1.

### 6. Known in advance 👤
<!-- What information is available at the moment the result is needed? Everything else is leakage. -->
**Moment:** around 14:00 on day D−1, for day D.
- **Sales history:** complete up to **D−2** only. Every lag or rolling feature uses data up to D−2 at the latest. D−1 (today) is incomplete, so it is never used. The baseline (D−7) is allowed.
- **Weather for D:** only a forecast exists at that moment. Observed weather serves as a stand-in for the forecast, so results with weather are **somewhat optimistic**. One model run without weather shows how much weather contributes.
- **Calendar:** weekday, month, public and school holidays (Schleswig-Holstein), Kiel Week dates. All are known months ahead.
  - **Holiday day type** (normal day / open public holiday / Easter-Whit Sunday / Christmas Eve / New Year's Eve): built from the `holidays` package and fixed dates. Fixed years ahead, so no leakage. Built from the calendar only, never from sales. By law (LÖffZG SH § 4) the bakery may open on every public holiday except Good Friday, so all of them count as open; the bakery knows its own closures in advance. In the data, a date without sales means closed. Owner: HeldDerTierwelt (DECISIONS 2026-11-26).
- **Not known:** sales of any group on D or D−1; observed weather on D (only as a stand-in, see above); sell-out status.

### 7. Data decisions 👤
<!-- Joins, missing values, encodings, exclusions, each with a reason. Link the entries in DECISIONS.md. -->
See `DECISIONS.md` (2026-11-22, /explore-data).
- **Joins:** sales ⟕ weather ⟕ Kiel Week on `Datum` (left). `KielerWoche` missing → 0.
- **Closed days (38 dates without any row):** not predicted and not evaluated. Never added as 0.
- **Confectionery gaps (53 open days):** treated as "not offered". The rows are left out of training and evaluation, never filled with 0.
- **Seasonal bread:** predicted only on days it is on offer (the season start is set by the manager). In-season gaps are handled like confectionery gaps.
- **Baseline fallback:** D−7 → D−14 → D−21 → median of the group's previous season. Model and baseline are scored on identical rows.
- **Missing weather:** rows are **kept**. Missing cloud cover, temperature or wind is filled with the training mean of the same calendar month; `Wetter_fehlt` = 1 flags the 12 dates (70 rows; 64 in the validation year). The same rule fills the 13 dates without weather in the test year. Decision 2026-11-24 (replaces the drop of 2026-11-22).
- **Holiday day type:** four day types (open public holiday, Easter/Whit Sunday, Christmas Eve, New Year's Eve) plus normal day as reference; one-hot and combined with the product group (interaction). Built from the calendar only. DECISIONS 2026-11-27.
- **Weather code:** grouped into a few classes; "missing" becomes its own class, "no notable weather". The class scheme is set at feature building.
- **Peaks** (31 Dec, Easter, day after a closure, February Sundays): kept as real demand, to be explained with calendar features.
- **Revenue drop 2014→2016:** all years kept with a time-trend feature; training from 2016 onward is run as one comparison experiment.
- **Units:** currency written as € ("not stated in the source, assumed €"). Wind speed used unchanged.
- **`id`:** never a model input (it encodes the date).
- **Question C:** "no detectable sell-out pattern in daily revenue" is reported as a limit. Once a model exists, days with actual revenue far below the forecast are listed as "possible sell-out or low demand – not distinguishable".

### 8. Checks 🤖
<!-- Checkpoints and the invariants that must hold at each (row counts, keys, date ranges, IDs, baseline). Link checks/. -->
Run with `uv run pytest checks`. Confirmed by the team on 2026-11-22.
**Status (2026-11-22):** K1–K6 implemented and passing: [checks/invariants.py](checks/invariants.py) holds the checks, [checks/test_data_loads.py](checks/test_data_loads.py) and [checks/test_prepare.py](checks/test_prepare.py) run them on the real data, and [checks/test_checks_can_fail.py](checks/test_checks_can_fail.py) proves each one fails on deliberately broken data. They test the pipeline steps in [src/bakery_prep.py](src/bakery_prep.py). K7–K12 are still to be written, once features, baseline and model exist. K13 (added 2026-11-22 for H3) is implemented and passing: [checks/test_holidays.py](checks/test_holidays.py), with the holiday code in [src/bakery_holidays.py](src/bakery_holidays.py).

| # | Checkpoint | Invariant |
|---|---|---|
| K1 | raw sales | 9,334 rows, 4 columns; (`Datum`, `Warengruppe`) unique; `id` = `YYMMDD`·10 + group |
| K2 | raw sales | `Umsatz` > 0, never missing |
| K3 | raw sales | dates 2013-07-01 – 2018-07-31; 1,819 sales dates; exactly the 38 known closed days missing |
| K4 | after joins | row count unchanged; `KielerWoche` ∈ {0, 1}; 223 rows / 45 dates = 1 |
| K5 | after weather-gap fill | no row lost; no missing weather left; exactly the 12 known dates / 70 rows flagged; measured values unchanged; fill values unchanged when post-training weather changes (no leakage) |
| K6 | split | training < 2017-08-01; validation = 2017-08-01 – 2018-07-31; no test-year date anywhere |
| K7 | features | no sales-history feature for D uses data newer than D−2 |
| K8 | prepared data | no added zero-revenue rows (closed days, not-offered days) |
| K9 | preprocessing | learned steps fitted on the training period only |
| K10 | baseline | covers every evaluated row; its MAPE matches `experiments/LOG.md` |
| K11 | model inputs | `id` not among the features |
| K12 | outputs | weekdays ordered Monday → Sunday |
| K13 | public holidays (`holidays` package) | 46 public holidays (SH) in the sales period; exactly the 20 known ones have sales; the other 26 are all known closed days |

---

## Evidence and action

### 9. Experiments 🤖
<!-- Experiment cards and their status; best result so far vs. baseline. Link experiments/LOG.md. -->

### 10. Findings 🤖
<!-- What we learned, how sure we are, and what the data cannot tell. -->
- **H3 (2026-11-22): supported for rolls, croissants, confectionery and cakes; contradicted for bread.** On open public holidays, compared with the same weekday in the 4 weeks around, typical revenue was rolls +78 %, croissants +90 %, confectionery +98 %, cakes +33 %, bread −41 % (15–17 of 17 training holidays point the same way per group). The D−7 baseline misses on these days by 26–49 % too low (bread: about 1.8× too high). *How sure:* direction clear, size uncertain (17 days, 4 per holiday, almost all Mondays/Thursdays; weekend holidays showed a much smaller effect). Sell-outs unknown. Special days: New Year's Eve cakes about 7×. Details: [Alexander-Holidays.ipynb](1_DatasetCharacteristics/Alexander-Holidays.ipynb).

### 11. Recommendation 👤
<!-- What the decision-maker should do, under which conditions. Signed off by the team. -->

---

## Open questions
<!-- Parking lot. Each item names who resolves it. -->
- Average price per product group, to convert € into pieces. **Client** (via team).
- How is the baking quantity decided today? We assume "same weekday last week". **Client** (via team).
- Is running out (too little baked) worse than leftovers (too much), and for which groups? Decides whether to bake above the forecast. **Client** (via team).
- What is "far below the forecast" for the possible-sell-out list (threshold)? **Team**, once the first model exists.
- Currency of `Umsatz` (assumed €). **Client** (via team).
- Why does confectionery peak on some February Sundays (2014-02-09, 2014-02-23, 2015-02-22, 2016-02-21)? **Client** (via team).
- Confectionery (4) has no entry on 53 days. They are mostly busy days (December, next to closures, 2013–2015) and fade out by 2016. Was it not offered, or not recorded? **Client** (via team). Handling in the data: Q2 of /explore-data.

- Do the days around public holidays (e.g. the day before Good Friday, the day after Easter Monday) sell differently? Not part of H3; possible own hypothesis. **Team**.
- Idea from the H3 analysis: does an open holiday sell like a Sunday (quick check: only 6–18 % above nearby Sundays)? Could become a simple model feature. See [docs/h3-holidays-plan.md](docs/h3-holidays-plan.md), "Ideas for later". **Team**.

## Decision log
See `DECISIONS.md`.
