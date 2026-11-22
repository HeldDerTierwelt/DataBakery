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
**Decision:** how much of each product group (1 Bread, 2 Rolls, 3 Croissants, 4 Patisserie, 5 Cakes, 6 Seasonal bread) to bake for tomorrow.
**When / how often:** every opening day, plan fixed around 14:00 the day before. Closed holidays are not planned.
**Output:** expected sales value (€ revenue) per group. Converted to pieces once the client supplies average prices per group (see Open questions).
**Scope notes:** Seasonal bread (6) only October–January. Patisserie (4) days without an entry still to be clarified (block 7).
**Today (assumed):** the manager bakes roughly what sold on the same weekday last week. To be confirmed by the client.

### 2. Questions 👤
<!-- The analysis questions that would change the decision. For each: what the data can answer, and what it cannot. -->
- **A (main):** What revenue (€) should we expect per product group tomorrow, and within what range? The range lets the manager decide whether to bake above or below the forecast.
- **B (explaining):** Which factors shift demand per group, and by how much? Candidates: weekday, season, holidays, Kiel Week, temperature, rain.
- **C (sold out):** On which days did a group probably sell out, so that more could have been sold? Answered only by estimating from the sales data (*suspected sell-out days*). No sold-out records exist and none will be collected, so the estimate **cannot be verified** and is reported as an unverified hint.

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
- **Split (by time):** train 2013-07-01 – 2017-07-31; validation 2017-08-01 – 2018-07-31. The course's held-back period after 2018-07-31 is used once, at the end.
- **Segments reported separately:** product group; weekday (Mon–Sun); December/holidays; Kiel Week; summer vs. winter. The validation year holds only one Christmas and one Kiel Week, so segment results there are single cases.

---

## Data and method

### 5. Data 🤖
<!-- Sources, unit of observation, period covered, keys, known gaps. Link the data fact sheet. -->

### 6. Known in advance 👤
<!-- What information is available at the moment the result is needed? Everything else is leakage. -->
**Moment:** around 14:00 on day D−1, for day D.
- **Sales history:** complete up to **D−2** only. Every lag or rolling feature uses data up to D−2 at the latest. D−1 (today) is incomplete, so it is never used. The baseline (D−7) is allowed.
- **Weather for D:** only a forecast exists at that moment. Observed weather serves as a stand-in for the forecast, so results with weather are **somewhat optimistic**. One model run without weather shows how much weather contributes.
- **Calendar:** weekday, month, public and school holidays (Schleswig-Holstein), Kiel Week dates. All are known months ahead.
- **Not known:** sales of any group on D or D−1; observed weather on D (only as a stand-in, see above); sell-out status.

### 7. Data decisions 👤
<!-- Joins, missing values, encodings, exclusions, each with a reason. Link the entries in DECISIONS.md. -->

### 8. Checks 🤖
<!-- Checkpoints and the invariants that must hold at each (row counts, keys, date ranges, IDs, baseline). Link checks/. -->

---

## Evidence and action

### 9. Experiments 🤖
<!-- Experiment cards and their status; best result so far vs. baseline. Link experiments/LOG.md. -->

### 10. Findings 🤖
<!-- What we learned, how sure we are, and what the data cannot tell. -->

### 11. Recommendation 👤
<!-- What the decision-maker should do, under which conditions. Signed off by the team. -->

---

## Open questions
<!-- Parking lot. Each item names who resolves it. -->
- Average price per product group, to convert € into pieces. **Client** (via team).
- How is the baking quantity decided today? We assume "same weekday last week". **Client** (via team).
- Is running out (too little baked) worse than leftovers (too much), and for which groups? Decides whether to bake above the forecast. **Client** (via team).
- How exactly is a *suspected sell-out day* flagged (which rule, which threshold)? **Team**, during /explore-data.
- Patisserie (4) has no entry on 53 days: counter closed, or zero sales? **Team**, block 7 (ask client if needed).

## Decision log
See `DECISIONS.md`.
