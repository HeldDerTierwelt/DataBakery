# Analysis plan: DataBakery

**Version:** 2026-11-27 · **Status:** draft v1. The checkpoints were confirmed by HeldDerTierwelt; the team still has to review them. Team members add their own features and the checks that go with them (see "Open questions").
**Sources:** the canvas, the decision log and the glossary as of 2026-11-27. Terms follow the glossary.

## Decision and questions

Every opening day at around 14:00, the operations manager of one bakery branch in Kiel decides how much of each of the six product groups to bake for tomorrow. Today we assume the rule is "same weekday last week". The analysis answers **A**: the expected revenue per group for tomorrow, with a range. It also answers **B**: which factors (weekday, season, holidays, Kiel Week, weather) shift demand, and by how much. **C** (suspected sell-out days) is reported as a limit: the data shows no sell-out pattern. Once a model exists, it adds a list of days with revenue far below the forecast.

## Hypotheses

1. **H1 (weekend):** all product groups sell more on Saturdays and Sundays than on Monday–Friday.
   *Analysis:* compare revenue per group, weekend vs. weekdays, in the training period only. *Expected direction:* higher on weekends. *Decision rule:* not written down yet (open question).
2. **H2 (Kiel Week):** revenue is higher during Kiel Week. The sold-out part cannot be tested, because there is no sell-out signal.
   *Analysis:* compare revenue per group on Kiel Week days with comparable days, training period only. *Expected direction:* higher. *Decision rule:* not written down yet (open question). *Limit:* only 5 Kiel Weeks.
3. **H3 (open public holidays):** per group, revenue on open public holidays is higher than on the same weekday without a holiday.
   *Analysis:* holiday ratio (same weekday, 4 weeks before and after; other holidays, special days and Kiel Week excluded), 17 training holidays. *Decision rule:* supported for a group if the median ratio is ≥ 1.10 and revenue was higher on at least 13 of 17 holidays.
   *Status:* already tested (2026-11-22). Supported for rolls, croissants, confectionery and cakes; contradicted for bread. This plan records the rule afterwards. The rule itself was set before the result was seen.
4. **Model (question A):** a linear regression with calendar features (and weather as a stand-in) predicts better than the baseline.
   *Decision rule:* the model is good enough to act on if its overall MAPE in the validation period is at least 10 % lower (relative) than the baseline's, **and** its MAPE is lower than the baseline's in groups 1 Bread, 2 Rolls and 5 Cakes. If it misses this, the manager keeps the current rule, and the report says where the model fails.

## Target and unit

- **Target:** `Umsatz` (revenue, assumed €) of one product group on one day.
- **Unit (row):** date × product group, only on opening days and only for groups that are offered that day. Closed days and not-offered days are never predicted and never added as 0.
- **Moment:** the forecast for day D is made at around 14:00 on D−1.

## Data and known in advance

- **Sources:** course sales data (2013-07-01 – 2018-07-31), weather (observed), Kiel Week dates, and public holidays for Schleswig-Holstein from the `holidays` package. Special days are fixed dates or depend on the Easter date.
- **Joins:** sales ⟕ weather ⟕ Kiel Week on the date (left join). The row count stays at 9,334.
- **Data decisions** (details in the decision log): weather gaps are filled with the training monthly mean and flagged in `Wetter_fehlt`. A missing `Wettercode` becomes its own class. Peaks are kept. All years are kept, with a time trend. `id` is never a model input.
- **Holiday feature (HeldDerTierwelt):**
  - An open public holiday is every public holiday in Schleswig-Holstein except Good Friday (LÖffZG SH § 4). In the data, a date without sales means the bakery was closed.
  - Holiday day type: normal day, open public holiday, Easter/Whit Sunday, Christmas Eve, New Year's Eve. One-hot, combined with the product group (interaction).
  - Built from the calendar only.
- **Leakage boundary (canvas block 6):**
  - Sales features use data up to D−2 only. The baseline D−7 is allowed.
  - Calendar features are allowed.
  - Observed weather serves as a stand-in for the forecast, so results with weather are somewhat optimistic. One run without weather is the comparison.

## Split and evaluation

- **By time:** training 2013-07-01 – 2017-07-31, validation 2017-08-01 – 2018-07-31.
- **Tuning and model choice:** on the validation period only. Learned steps (filling, scaling, encoding) are fitted on training only.
- **Test period:** 2018-08-01 – 2019-07-31 (Kaggle). Used **once**, for the final estimate. No decision is taken after looking at test results.

## Baseline and success

- **Baseline:** "same weekday last week" (revenue on D−7, same group). Fallback D−14 → D−21 → median of the group's previous season. Baseline and model are scored on identical rows.
- **Metrics:** MAPE (main), per group and overall. MAE in € as a secondary metric.
- **Good enough:** see hypothesis 4.
- **Segments, reported separately:** product group; weekday (Mon–Sun); December/holidays; Kiel Week; summer vs. winter. The validation year has only one Christmas, one Kiel Week, one Christmas Eve and one New Year's Eve, so these segments are single cases.

## Checkpoints

Confirmed by HeldDerTierwelt on 2026-11-27; the team still has to review them. Status as of 2026-11-27: ✅ implemented and passing · ⏳ planned.

### 1. Load (raw sales)
| # | Check | Source of truth | Status |
|---|---|---|---|
| K1 | 9,334 rows, 4 columns; (`Datum`, `Warengruppe`) unique; `id` = `YYMMDD`·10 + group | line count of the raw file; key definition | ✅ |
| K2 | `Umsatz` > 0, never missing | domain bound | ✅ |
| K3 | dates 2013-07-01 – 2018-07-31; 1,819 sales dates; exactly the 38 known closed days missing | calendar; fixed list from data exploration | ✅ |

### 2. Merge and weather fill
| # | Check | Source of truth | Status |
|---|---|---|---|
| K4 | row count unchanged; `KielerWoche` ∈ {0, 1}; 223 rows / 45 dates = 1 | sales file; Kiel Week file | ✅ |
| K5 | no row lost; no missing weather left; exactly the 12 known dates / 70 rows flagged; measured values unchanged; fill values unchanged when weather after the training period changes | fixed list of gap dates; raw weather; perturbation test | ✅ |
| K13 | 46 public holidays in the sales period; exactly the 20 known ones have sales; the other 26 are known closed days | fixed date list; independent calculation of 2026-11-22 | ✅ |

### 3. Features
| # | Check | Source of truth | Status |
|---|---|---|---|
| K7 | no sales-history feature for D uses data newer than D−2. Test: change revenue on D and D−1, and the feature stays the same | leakage boundary (canvas block 6) | ⏳ |
| K8 | no added zero-revenue rows (closed days, not-offered days) | K1–K3 | ⏳ |
| K14 | the holiday day type depends on the date only: shuffling `Umsatz` leaves the column identical | leakage boundary (canvas block 6) | ⏳ |
| K15 | holiday day types in training 17 / 8 / 4 / 4 and in validation 3 / 2 / 1 / 1 (open public holiday / Easter-Whit Sunday / Christmas Eve / New Year's Eve), as a fixed date list. Good Friday is never an open public holiday | decision log 2026-11-26/27; LÖffZG SH § 4 | ⏳ |
| K16 | holiday interaction columns: at most one 1 per row, only in the row's own product group; no column that is always 0 | definition of the interaction | ⏳ |
| … | checks for the team's other features | to be added by each feature owner | open |

### 4. Split
| # | Check | Source of truth | Status |
|---|---|---|---|
| K6 | training < 2017-08-01; validation = 2017-08-01 – 2018-07-31; no test-year date anywhere | split decision | ✅ |
| K6b | 1,462 training dates and 357 validation dates (calendar days minus known closed days) | calendar + closed-day list | ⏳ |
| K9 | learned steps fitted on training only. Test: change the validation data, and the fitted values stay the same | split decision | ⏳ |

### 5. Predictions
| # | Check | Source of truth | Status |
|---|---|---|---|
| K11 | `id` not among the model inputs | decision log | ⏳ |
| K17 | submission file: header `id,umsatz`; its ids are exactly the ids of the Kaggle test file, none missing, none duplicated; all values > 0 | Kaggle test file / sample submission | ⏳ |
| K12 | weekdays in outputs ordered Monday → Sunday | project convention | ⏳ |

### 6. Metrics
| # | Check | Source of truth | Status |
|---|---|---|---|
| K10 | the baseline covers every evaluated row; model and baseline are scored on the same rows; the baseline MAPE matches the experiment log | decision log (fallback rule); experiment log | ⏳ |
| K10b | for a few fixed rows, the baseline equals the revenue on D−7 looked up directly in the raw file (e.g. bread on 2017-08-08 = bread on 2017-08-01). Needed because the first value in the experiment log comes from the same code | raw file | ⏳ |

## Out of scope

- Real demand on sold-out days, waste and leftovers (not in the data).
- Price effects, new products, other branches.
- Local events other than Kiel Week, until the branch location is known.
- School holidays, the days around holidays and bridge days: possible later experiments, not in the baseline.
- Converting € to pieces, until the client supplies average prices.

## Open questions

- **Team:** which features each member adds, and their checks in checkpoint 3.
- **Team:** which features go into the baseline model (proposal in the feature candidates draft).
- **Team:** decision rules for H1 and H2.
- **Team:** the class scheme for `Wettercode`.
- **Team:** predict `Umsatz` or log(`Umsatz`)?
- **Team:** threshold for "far below the forecast" (possible sell-out days), once a model exists.
- **Team:** review the checkpoints of this draft (planned as a team call in the workbook).
- **Client:** average prices per group; current baking practice; whether running out is worse than leftovers; currency; the February confectionery peaks; the branch location.
- **Check:** whether the Kaggle test file has rows on Reformation Day (2018-10-31) and on 1 May 2019. Both count as open public holidays.
