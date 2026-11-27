# Decisions

Newest first. One entry per decision taken at a stop point.

<!--
## YYYY-MM-DD: <short title>
**Canvas block:** <number>
**Decision:** <what was decided>
**Reason:** <why>
**Alternatives considered:** <what else, and why not>
**Decided by:** <names>
-->

## 2026-11-27: Holiday feature with four day types
**Canvas block:** 6, 7
**Decision:** The holiday feature has five values: **normal day** (reference, no column of its own) and four day types:
1. **Open public holiday:** Easter Monday, Ascension Day, Whit Monday, German Unity Day, 1 May, Reformation Day (every public holiday except Good Friday, see "Definition of an open public holiday"). 17 days in training, 3 in validation.
2. **Easter/Whit Sunday:** 8 / 2.
3. **Christmas Eve (24 Dec):** 4 / 1.
4. **New Year's Eve (31 Dec):** 4 / 1.
Each day type is one-hot encoded and combined with the product group (interaction): a column is 1 only on that day type and in that group. There are only interaction columns, no extra main column per day type (it would be the sum of the interaction columns). Combinations without any case are left out (e.g. seasonal bread on open public holidays). That gives up to 22 columns.
This replaces the three-value category (normal / open public holiday / special day) in "Holiday feature owned by HeldDerTierwelt".
**Reason:** Holiday ratio in the training period (same weekday, 4 weeks before and after; median):
- Open public holidays and special days differ, for bread even in direction (0.59 vs. 1.85).
- The open public holidays look alike: bread about 0.5–0.75, sweet groups clearly above.
- The special days differ among themselves: Easter/Whit Sunday mild (1.06–1.44), Christmas Eve strong for bread and rolls (1.88 / 1.64), New Year's Eve cakes 7.3× and confectionery 0.58.
**Alternatives considered:** Three values (hides the differences between special days). One column per holiday (4–5 cases each for open public holidays that look alike, so mostly noise). Treating a weekday holiday as a Sunday (more economical, possible later experiment). Ridge regression if the coefficients swing too much (later experiment).
**Limit:** Christmas Eve and New Year's Eve rest on 4 training days each, and validation has 1 case each, so they can only be checked together with the other special days. In validation (2017) both fall on a Sunday, which never happens in training; in the test year both are Mondays. The split was set on training data and is not changed after looking at validation results.
**Decided by:** HeldDerTierwelt (analysis by the agent)

## 2026-11-26: Definition of an open public holiday (law + sales data)
**Canvas block:** 6, 7
**Decision:**
- **Law:** public holidays come from the `holidays` package (`holidays.Germany(subdiv="SH")`). The Ladenöffnungszeitengesetz Schleswig-Holstein (LÖffZG) closes shops on Sundays and public holidays (§ 3 Abs. 2 Nr. 1). § 4 Abs. 1 makes an exception for shops that mainly sell Back- und Konditorwaren: they may open on Sundays and public holidays for five hours, "allerdings nicht am Karfreitag". On a weekday, 24 December closes from 14:00 (§ 3 Abs. 2 Nr. 2); that shortens the day but does not close it.
- **Definition:** every public holiday in Schleswig-Holstein **except Good Friday** is a day on which the bakery may legally open, so it counts as an **open public holiday** for now. Good Friday is always closed by law. Other closures (e.g. Christmas, New Year) are the bakery's own choice, and the bakery knows them in advance.
- **Training and validation data:** a date without any sales means the bakery was closed. It is not plausible that an open bakery sold nothing at all. These dates are not predicted (entry "Closed days not predicted", 2026-11-22).
- **Feature:** the holiday category is built from the calendar alone (date → public holiday / special day / normal day), never from the sales. On every row that exists, a public holiday is then an open public holiday.
**Reason:** The feature should rest on a rule that is known in advance and does not use the target. Before, the H3 notebook marked a holiday as "open" by checking whether it had sales. That is fine for the analysis, but as a feature it would use information about the target.
**Consequence:** in the sales period the bakery was open on 20 of 46 public holidays. Of the 26 closed ones, only Good Friday is closed by law; the rest were the bakery's own choice. In the test year, Reformation Day (2018-10-31, a public holiday in SH since 2018) counts as open. It was closed in 2017, so whether it has rows is visible in `test.csv`.
**Limit:** the law text was read in its 2026 version (umwelt-online, gesetze.co), not on the official portal. Whether § 4 read the same in 2013–2019 is unchecked. §§ 9 ff. (e.g. rules for resort towns) were not read.
**Decided by:** HeldDerTierwelt (law research by the agent)

## 2026-11-26: Holiday feature owned by HeldDerTierwelt
**Canvas block:** 6
**Decision:** HeldDerTierwelt builds the holiday feature: one holiday category per date (normal day / open public holiday / special day), from [src/bakery_holidays.py](src/bakery_holidays.py), one-hot encoded and combined with the product group (interaction). The feature is listed as known in advance in canvas block 6.
**Reason:** H3 showed a strong effect that differs by product group (rolls +78 %, confectionery +98 %, bread −41 %), and the D−7 baseline misses on these days by 26–49 %. The H3 analysis and the holiday code come from the same team member. Proposal **A** in [docs/feature-candidates.md](docs/feature-candidates.md).
**Alternatives considered:** another feature from the candidate list.
**Open:** whether the feature goes into the baseline model is decided by the team. Days around holidays and bridge days are possible extensions (proposal B).
**Decided by:** HeldDerTierwelt

## 2026-11-24: Weather gaps filled and flagged
**Canvas block:** 7
**Decision:** Replaces "Weather gaps dropped" (2026-11-22). Rows with missing cloud cover, temperature or wind are **kept**. A missing value is filled with the mean of the same calendar month in the training period (one value per date, dates before 2017-08-01). The new column `Wetter_fehlt` = 1 marks the 12 dates (70 rows) where at least one value was filled. Measured values are never changed. The weather code is still grouped into classes, with "missing" as its own class.
**Reason:** Dropping whole sales rows because of a weather gap is too harsh: validation lost 3.5 % of its rows, including the first 9 days of the 2017 seasonal-bread season. The course's test year has 13 dates without weather, and those days need a forecast too. Runs with and without weather can now be scored on the same, complete rows.
**Alternatives considered:** Dropping the rows (the old decision). Turning the weather values into classes with "unknown" as one class (loses detail such as 20 °C vs. 25 °C). Filling from neighbouring days.
**Limit:** in training, weather is missing on one date only (2016-12-11, 6 rows), so a model learns almost nothing about `Wetter_fehlt`. Filling with training means is checked for leakage (K5).
**Consequence:** the prepared data has 9,334 rows (before: 9,264). H3 results unchanged; H1 numbers shift by at most 0.4 percentage points.
**Decided by:** HeldDerTierwelt (proposed by the agent), to be confirmed by the team

## 2026-11-22: Kiel Week days not used as H3 comparison days
**Canvas block:** 2
**Decision:** For the holiday ratio, Kiel Week days are excluded from the comparison days, like other holidays and special days.
**Reason:** Whit Monday is sometimes 2–4 weeks before Kiel Week. Kiel Week days sell more, so they would raise the "usual" level and make the holiday effect look smaller.
**Alternatives considered:** Keeping Kiel Week days as comparison days (simpler, but biases the ratio downwards around Whit Monday).
**Decided by:** team (HeldDerTierwelt), proposed by the agent during the H3 analysis

## 2026-11-22: Public holidays from the `holidays` package
**Canvas block:** 5, 7
**Decision:** Public holidays for Schleswig-Holstein are loaded from the Python package `holidays` (`holidays.Germany(subdiv="SH")`, added with `uv add holidays`, version 0.109 pinned in `uv.lock`). In the notebook, the list is checked against the sales data (46 public holidays, 20 open, 26 closed). Special days are defined by the team (fixed dates and Easter date), because no holiday source lists them.
**Reason:** The team wants a reliable, documented source instead of a self-made calculation. The package is open source, widely used, maintained, knows historical changes per state, runs offline and is pinned for everyone. Checked: it gives exactly the same 46 dates as the independent calculation.
**Alternatives considered:** OpenHolidays API (no data for SH before 2020). feiertage-api.de (works, but a private hobby project, needs internet on every run, not versioned). Own calculation (no external confirmation).
**Decided by:** team (HeldDerTierwelt)

## 2026-11-22: H3 means open public holidays
**Canvas block:** 2
**Decision:** H3 is tested as "revenue is higher on public holidays (Schleswig-Holstein) on which the shop is open than on the same weekday without a holiday". Open public holidays: Easter Monday, Ascension Day, Whit Monday, German Unity Day (5 each, Whit Monday 2018 closed) and 1 May 2016. Easter Sunday, Whit Sunday, Christmas Eve and New Year's Eve are analysed as a separate category, "special days". School holidays are not part of H3; they may be tried later as a model feature.
**Reason:** A check of the raw sales showed that the shop is open on 20 of the 46 public holidays in the sales period, always on the same holidays, with revenue mostly 1.2–1.9× a normal day with the same weekday. The baseline (D−7) misses single days like these, so the effect matters most for the forecast. The dates come from the `holidays` package (see the entry "Public holidays from the `holidays` package").
**Alternatives considered:** School holidays (more days, but the D−7 baseline already absorbs a several-week effect, and summer holidays cannot be separated from the high season; needs an external source). Both together.
**Limit:** only 17 open holidays in the training period and 3 in the validation year (4 per holiday), so the result is a tendency, not proof.
**Decided by:** team (HeldDerTierwelt)

## 2026-11-22: How H3 is tested
**Canvas block:** 2, 3, 4, 6
**Decision:**
- Comparison: each open holiday against the median revenue of the same group on the same weekday in the 4 weeks before and after, other holidays and special days excluded (holiday ratio). Additionally the D−7 baseline error on these days.
- Supported for a group if the median holiday ratio is ≥ 1.10 and revenue was higher on at least 13 of 17 training holidays; range always reported, Wilcoxon test only as an extra.
- Reported pooled **and** per holiday, each per group, because the holidays differ (Easter/Whit Monday are outing days, German Unity Day is in autumn). Per holiday: values only, no yes/no (4 cases).
- Special days (Easter Sunday, Whit Sunday, Christmas Eve, New Year's Eve) as a separate table in the same notebook.
- Training period only (17 holidays); validation year untouched.
- Days around holidays are not part of H3 (open question).
- Manager gets one sentence per group in the memo; technical reader the notebook.
**Reason:** The ±4-week same-weekday window controls for weekday and season. 10 % is a difference that would change the baking amount. With 17 cases a test says little.
**Alternatives considered:** Same weekday over the whole training period (mixes seasons). D−7 only (one random day). Test-based criterion (p < 0.05). Pooled only (hides differences between holidays).
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Three hypotheses for Question B
**Canvas block:** 2
**Decision:** Test H1 (all groups sell more on weekends), H2 (higher sales and more sold-out days during Kiel Week) and H3 (higher sales on holidays).
**Reason:** Course exercise. These factors are known in advance (calendar), so they can become model features.
**Alternatives considered:** Weather hypotheses (rain, temperature) and season. Not chosen for now.
**Decided by:** team
**Open:** the sold-out part of H2 cannot be tested (no sell-out signal, see Question C). For H3, the team still has to say which kind of holiday is meant.

## 2026-11-22: Checks K1–K12 adopted
**Canvas block:** 8
**Decision:** Keep all 12 proposed checks (see canvas block 8).
**Reason:** Each protects a fact that later steps depend on: keys, row counts, the leakage boundary, the split, and a fair baseline.
**Alternatives considered:** A smaller set (would leave the D−2 rule and the split unguarded).
**Decided by:** team (HeldDerTierwelt), during /explore-data

## 2026-11-22: Closed days not predicted
**Canvas block:** 7
**Decision:** The 38 dates without any sales row are neither predicted nor evaluated, and are never added as 0.
**Reason:** The branch was closed, so there was no demand, and the manager knows closure days in advance.
**Alternatives considered:** Adding them as 0 (would drag the averages down and teach a demand that doesn't exist).
**Decided by:** team (HeldDerTierwelt), during /explore-data

## 2026-11-22: Question C answered as a limit plus a later list
**Canvas block:** 2, 7
**Decision:** Report "no detectable sell-out pattern in daily revenue per group". Once a model exists, list days with actual revenue far below the forecast, each labelled "possible sell-out or low demand – not distinguishable".
**Reason:** The profile shows no revenue ceiling: the upper tail is wider than the lower tail (ratio 1.41–1.91), and near-identical same-weekday values occur in only 1–5% of cases.
**Alternatives considered:** A threshold rule on high revenue (rejected: it would flag high-demand days, the opposite of sell-outs). Reporting only the limit.
**Decided by:** team (HeldDerTierwelt), during /explore-data

## 2026-11-22: Units, trend and peaks
**Canvas block:** 7
**Decision:** Currency is written as € with the note "not stated in the source, assumed €". Wind speed is used unchanged. Peaks (31 Dec, Easter, day after a closure, February Sundays) are kept. All years are kept with a time-trend feature, and training from 2016 onward runs as one comparison experiment. `id` is never a model input.
**Reason:** The peaks are real demand on costly days. Older years carry the seasonal and holiday patterns that occur only 5 times. Units don't affect the model.
**Alternatives considered:** Capping or removing peaks (loses the most important days). Training only from 2016 (loses holiday cases).
**Decided by:** team (HeldDerTierwelt), during /explore-data

## 2026-11-22: Weather gaps dropped, weather code grouped
**Superseded** on 2026-11-24 by "Weather gaps filled and flagged".
**Canvas block:** 7
**Decision:** Days with a missing weather row (2016-12-11, 2017-10-04, 2017-10-05) or missing cloud cover (2017-10-30 – 11-08) are dropped: 12 dates, 70 rows, 64 of them in the validation year. The weather code is grouped into a few classes, with "missing" as its own class, "no notable weather".
**Reason:** The team prefers no invented weather values. A missing code means calm, clear weather (mean cloud 3.3 vs 5.3), so it carries information.
**Alternatives considered:** Filling from neighbouring days and monthly training means (keeps the rows). Raw codes (41 values, too many). Dropping the code.
**Consequence:** Validation loses 3.5% of its rows, including the first 9 days of the 2017 seasonal-bread season (9 of 56 rows). Baseline and model are scored on the same rows.
**Decided by:** team (HeldDerTierwelt), during /explore-data

## 2026-11-22: Baseline fallback
**Canvas block:** 7, 4
**Decision:** If D−7 is missing, use D−14, then D−21, then the group's median from its previous season.
**Reason:** The baseline and the model must be scored on identical rows.
**Alternatives considered:** Leaving those days out of the evaluation (an unfair comparison).
**Decided by:** team (HeldDerTierwelt), during /explore-data

## 2026-11-22: Not-offered days (confectionery gaps, seasonal bread)
**Canvas block:** 7
**Decision:** The 53 open days without confectionery and the 15 in-season days without seasonal bread are treated as "not offered" and left out of training and evaluation. Seasonal bread is predicted only on days it is on offer. Kiel Week is set to 0 on non-Kiel-Week days.
**Reason:** No revenue ≤ 0 exists anywhere. Confectionery gaps fall on busy days (other groups +0–8%, December, next to closures) and fade out by 2016, so 0 would be wrong. None fall in the validation year.
**Alternatives considered:** Filling with 0 (teaches the model "no confectionery on busy days"). Estimating values (invented data).
**Decided by:** team (HeldDerTierwelt), during /explore-data

## 2026-11-22: Known in advance (leakage boundary)
**Canvas block:** 6
**Decision:** Sales features use data up to D−2 only. Observed weather is a stand-in for the forecast, and one run without weather is the comparison. Calendar features (weekday, month, public/school holidays for Schleswig-Holstein, Kiel Week) are allowed. Holidays are added as an extra data source.
**Reason:** The plan is fixed at 14:00 on D−1, when today's sales are incomplete and tomorrow's weather is only forecast. Calendar data is known months ahead.
**Alternatives considered:** Using D−1 sales (leakage). Leaving weather out entirely (would lose a likely driver). Collecting historical forecasts (not available in the course data).
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Time-based train/validation split
**Canvas block:** 4
**Decision:** Train 2013-07-01 – 2017-07-31, validate 2017-08-01 – 2018-07-31. The course's held-back period after 2018-07-31 serves as the test set and is used once.
**Reason:** Training strictly before validation mimics daily use. One full validation year covers every season once.
**Alternatives considered:** Random split (leaks the future into training). Shorter validation period (misses seasons such as Christmas or Kiel Week).
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Success criteria
**Canvas block:** 4
**Decision:** MAPE is the main metric, MAE in € is secondary. Baseline is "same weekday last week". Good enough means at least 10% lower overall MAPE than the baseline and lower MAPE in groups 1, 2 and 5. Errors are treated as symmetric until the client says otherwise. Segments: group, weekday, December/holidays, Kiel Week, summer/winter.
**Reason:** Percentages compare small and large groups fairly, and € is concrete for the manager. Groups 1, 2 and 5 carry most of the revenue.
**Alternatives considered:** MAE only (dominated by rolls and cakes). Asymmetric cost (no client information yet).
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Audiences
**Canvas block:** 3
**Decision:** Three audiences: the operations manager (memo and daily table), the technical reader (README, notebooks, logs) and a course presentation told from the manager's point of view.
**Reason:** The decision-maker and the technical reader need different depth. The team chose to include a course presentation.
**Alternatives considered:** Only memo and notebooks.
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Analysis questions A, B, C; sold-out days estimated only
**Canvas block:** 2
**Decision:** Three questions. A: expected revenue per group tomorrow, with a range. B: which factors shift demand. C: suspected sell-out days, estimated from the existing sales data and reported as an unverified hint.
**Reason:** The manager wants to know whether more could have been sold. The data has no sold-out records, and the project collects no new data.
**Alternatives considered:** Client records sell-outs from now on (rejected: the project does not collect future data). Dropping C (rejected: the team wants the hint).
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Assume "same weekday last week" as current practice
**Canvas block:** 1
**Decision:** Until the client says otherwise, today's practice is assumed to be "bake what sold on the same weekday last week".
**Reason:** The client hasn't told us their method yet. We need a stated current practice to define the baseline.
**Alternatives considered:** Gut feeling or a fixed plan. Neither can be reproduced from the data.
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: All six product groups in scope
**Canvas block:** 1
**Decision:** Predict all six groups. Seasonal bread (6) only October–January. Confectionery (4) days without an entry are not treated as zero sales; this is left to block 7.
**Reason:** The manager plans every group. Group 6 has no sales outside its season.
**Alternatives considered:** Dropping group 6 (only 292 days), but the manager still has to plan it in season.
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Predict € revenue, convert to pieces later
**Canvas block:** 1
**Decision:** The model predicts revenue (€) per group. Once the client supplies average prices per group, revenue is translated into pieces.
**Reason:** The data contains only revenue. The manager ultimately needs pieces.
**Alternatives considered:** Revenue only (less directly usable). Pieces only (impossible without prices).
**Decided by:** team (HeldDerTierwelt), during /grill-question

## 2026-11-22: Decision moment and frequency
**Canvas block:** 1, 6
**Decision:** The baking plan is fixed every opening day around 14:00 the day before, one day ahead.
**Reason:** Bakeries prepare dough and order ingredients the day before.
**Alternatives considered:** Evening after closing (would allow today's full sales). Same morning (too late for dough preparation).
**Decided by:** team (HeldDerTierwelt), during /grill-question
