# Glossary

One entry per term, variable or code the project uses. Keep the canonical name, the meaning, the unit and anything that is easy to get wrong.

| Term | Meaning | Unit / values | Notes |
|---|---|---|---|
| `Datum` | Calendar day of the sales record | date (YYYY-MM-DD) | Sales data covers 2013-07-01 to 2018-07-31. 38 calendar days are missing, mostly holidays the branch was closed. |
| `Warengruppe` | Product group | 1 Bread, 2 Rolls, 3 Croissants, 4 Patisserie, 5 Cakes, 6 Seasonal bread | Group 6 only October–January. Group 4 has no entry on 53 days. |
| `Umsatz` | Revenue of one product group on one day | € | Revenue, **not** pieces. It measures what was sold, not what customers wanted (see *Sales vs. demand*). |
| Sales vs. demand | Sales are capped by what was baked. On a sold-out day, real demand was higher than recorded sales. | – | The data does not show sold-out days or leftovers, so demand above the baked amount is invisible. |
| Suspected sell-out day | A day × group whose revenue pattern suggests the group ran out (e.g. revenue at the top of the usual range for that weekday and season) | flag (yes/no) | An **estimate**, not an observation. No sold-out records exist, so it cannot be checked. The exact rule is still open. |
| Decision moment | When tomorrow's baking plan is fixed | around 14:00 the day before | Defines what is known in advance (canvas block 6). |
| D, D−1, D−2 | D = the day being predicted. D−1 = the day the plan is made (sales incomplete). D−2 = the newest day with complete sales. | days | Sales features may use D−2 and earlier only. |
| Opening day | A day the branch sells and therefore needs a baking plan | – | Closed holidays are not predicted. |
| Expected sales value | The model's output: predicted `Umsatz` per product group for tomorrow | € | Converted to pieces once average prices per group are known. |
| MAPE | Mean absolute percentage error: average of \|actual − predicted\| / actual | % | Main metric. Computed per group and overall. Days with zero or missing revenue are excluded (division by zero). |
| MAE | Mean absolute error: average of \|actual − predicted\| | € | Secondary metric, easier for the manager to picture. |
| Baseline | "Same weekday last week": the prediction for day D is the revenue of the same group on D−7 | € | The bar the model must beat (canvas block 4). |
| Validation period | 2017-08-01 – 2018-07-31 | dates | Used for choosing and tuning models. Training data is strictly before it. |
| Test period | The course's held-back period after 2018-07-31 | dates | Used **once**, for the final estimate. |
| Current practice (assumed) | Bake what sold on the same weekday last week | – | Assumption until the client confirms. Candidate baseline. |
