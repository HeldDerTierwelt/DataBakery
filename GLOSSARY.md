# Glossary

One entry per term, variable or code the project uses. Keep the canonical name, the meaning, the unit and anything that is easy to get wrong.

| Term | Meaning | Unit / values | Notes |
|---|---|---|---|
| `Datum` | Calendar day of the sales record | date (YYYY-MM-DD) | Sales data covers 2013-07-01 to 2018-07-31. 38 calendar days are missing, mostly holidays the branch was closed. |
| `Warengruppe` | Product group | 1 Bread, 2 Rolls, 3 Croissants, 4 Confectionery, 5 Cakes, 6 Seasonal bread | Group 6 only October–January. Group 4 has no entry on 53 days. |
| `id` | Row key of the sales data: `YYMMDD` followed by the group digit, e.g. `1307011` = 2013-07-01, group 1 | integer | Unique. The Kaggle sample submission shows 9-digit ids (`YYYYMMDD` + group, e.g. `201808011`), not this 7-digit format; check the test file. |
| `Umsatz` | Revenue of one product group on one day | currency unit, **not stated in the source** (probably €; written "€" in this project) | Revenue, **not** pieces. It measures what was sold, not what customers wanted (see *Sales vs. demand*). |
| Sales vs. demand | Sales are capped by what was baked. On a sold-out day, real demand was higher than recorded sales. | – | The data does not show sold-out days or leftovers, so demand above the baked amount is invisible. |
| Possible sell-out day | A day × group whose actual revenue was far below the model's forecast | flag (yes/no) | **Not** an observation: it could equally be low demand. No sold-out records exist. The data shows no sell-out ceiling. The threshold is set once a model exists. |
| Not offered | A confectionery or seasonal-bread day without a row while the shop was open | – | Rows are left out, never filled with 0. Confectionery gaps fall mostly on busy days (2013–2016). |
| Decision moment | When tomorrow's baking plan is fixed | around 14:00 the day before | Defines what is known in advance (canvas block 6). |
| D, D−1, D−2 | D = the day being predicted. D−1 = the day the plan is made (sales incomplete). D−2 = the newest day with complete sales. | days | Sales features may use D−2 and earlier only. |
| Opening day | A day the branch sells and therefore needs a baking plan | – | Closed holidays are not predicted. |
| Expected sales value | The model's output: predicted `Umsatz` per product group for tomorrow | € | Converted to pieces once average prices per group are known. |
| MAPE | Mean absolute percentage error: average of \|actual − predicted\| / actual | % | Main metric. Computed per group and overall. Days with zero or missing revenue are excluded (division by zero). |
| MAE | Mean absolute error: average of \|actual − predicted\| | € | Secondary metric, easier for the manager to picture. |
| Baseline | "Same weekday last week": the prediction for day D is the revenue of the same group on D−7 | € | The bar the model must beat (canvas block 4). |
| Validation period | 2017-08-01 – 2018-07-31 | dates | Used for choosing and tuning models. Training data is strictly before it. |
| `Bewoelkung` | Cloud cover, daily mean | octas, 0 (clear) – 8 (overcast) | Missing on 10 days (2017-10-30 – 11-08). Observed, not forecast. |
| `Temperatur` | Temperature, daily mean | °C | No missing values. Observed, not forecast. |
| `Windgeschwindigkeit` | Wind speed, daily mean | m/s per documentation | Values 3–35, high for m/s; the unit is uncertain. |
| `Wetter_fehlt` | Flag: at least one of cloud cover, temperature or wind was missing and filled with the training mean of the calendar month | 0 / 1 | 1 on 12 dates (70 rows) in the sales period. Created in data preparation, not in the raw data. |
| `Wettercode` | WMO present-weather code of the day | code 00–99 (e.g. 61 = slight continuous rain) | Missing on 669 days. Missing mostly on clear, warm days, so "no notable weather", not random. |
| `KielerWoche` | 1 on a Kiel Week day | 0/1 | The file lists only Kiel Week days. After joining, missing values = 0. 9 days per year. |
| Open public holiday | A public holiday in Schleswig-Holstein other than Good Friday. By law (LÖffZG SH § 4) a bakery may open on all of them for five hours; other closures are the bakery's own choice | date | In the sales data, the branch was open (had sales) on Easter Monday, Ascension Day, Whit Monday, German Unity Day (each 5×, Whit Monday 2018 closed) and 1 May 2016: 17 in training, 3 in validation. Built from the calendar, never from sales. DECISIONS 2026-11-26. |
| Holiday day type | Feature: which kind of day a date is | normal day (reference) / open public holiday / Easter-Whit Sunday / Christmas Eve / New Year's Eve | Training days: 17 / 8 / 4 / 4. One-hot, combined with the product group (interaction). DECISIONS 2026-11-27. |
| Special day | Open days with a holiday character that are not public holidays (or fall on a Sunday) | date | Easter Sunday, Whit Sunday, Christmas Eve, New Year's Eve. Analysed separately from H3. |
| Holiday ratio | Revenue of a group on a holiday ÷ median revenue of the same group on the same weekday in the 4 weeks before and after (holidays and special days excluded) | ratio (1.10 = 10 % more) | Descriptive only: uses weeks after the holiday, so never a model feature. |
| Closed day | A date with no sales row for any group | – | 38 in the sales period: 26 public holidays, 12 other days. |
| Test period | The course's held-back year 2018-08-01 – 2019-07-31 (Kaggle) | dates | Used **once**, for the final estimate. |
| Current practice (assumed) | Bake what sold on the same weekday last week | – | Assumption until the client confirms. Candidate baseline. |
