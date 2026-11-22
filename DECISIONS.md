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
**Decision:** Predict all six groups. Seasonal bread (6) only October–January. Patisserie (4) days without an entry are not treated as zero sales; this is left to block 7.
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
