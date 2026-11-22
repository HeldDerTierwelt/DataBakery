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
