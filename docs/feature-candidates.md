# Feature candidates: draft for discussion

**As of:** 2026-11-24 · **Status:** draft (the agent's proposal). The team decides which features are used. Decisions go into `DECISIONS.md`.

This draft rates the ideas the team collected, plus a few additions (marked below). The numbers come from [data-fact-sheet.md](data-fact-sheet.md), the H3 results in the canvas, and a count over the 1,819 sales dates run on 2026-11-24.

## How each feature is rated

1. **Known in advance?** Is the value known at 14:00 on D−1 for day D (canvas block 6)? If not, it is leakage and the feature is dropped.
   ✅ yes · ⚠️ only as a stand-in (observed weather instead of the forecast) · ❌ no
2. **Data available?** Do values exist for **2013-07 to 2019-07**? The course's test period (2018-08 – 2019-07) needs the features too.
3. **Evidence of an effect:** what we already know, or why an effect is plausible.
4. **Proposal:**
   - **A:** into the baseline model (linear regression), because the data is available and there is evidence of an effect
   - **B:** test later in the model, because the feature is plausible and the data can be obtained
   - **C:** put on hold, because the data is hard to get or the effect is unclear
   - **D:** do not use

> Terms: the course calls the linear regression the "baseline model". In the canvas, the "baseline" is the rule "same weekday last week" (D−7). The linear regression has to beat this D−7 rule.

## Calendar

| Feature | Known in advance? | Data | Evidence of an effect | Proposal |
|---|---|---|---|---|
| Weekday | ✅ | from the date | mean daily revenue Sat €1,235, Sun €1,272, Mon–Fri €957–1,008 | **A**, as 7 yes/no columns (one-hot) |
| Weekend | ✅ | from the date | H1 (Zhouling) | **A or leave out**: already contained in the weekday. Use only one of the two, otherwise the information is duplicated |
| Open public holiday | ✅ | done ([src/bakery_holidays.py](../src/bakery_holidays.py)) | H3: rolls +78 %, croissants +90 %, confectionery +98 %, cakes +33 %, **bread −41 %**. D−7 misses by 26–49 % on these days | **A**. The effect differs by product group, see "Interactions" |
| Special days (New Year's Eve, Christmas Eve, Easter/Whit Sunday) | ✅ | done (same holiday category) | New Year's Eve: cakes about 7× the usual level | **A**, as the third level of the holiday category. Only 5 cases per day, so the size of the effect is uncertain |
| Kiel Week | ✅ | `kiwo.csv`, 2012–2019 | rolls on average €539 instead of €399 (not adjusted for weekday/season) | **A**. Only 5 Kiel Weeks |
| Christmas season | ✅ | from the date | December is its own segment in the canvas; not analysed yet | **B**. The team has to define the period (Advent? 1–23 Dec?) |
| School holidays (SH) | ✅ (published years ahead) | external source needed (SH holiday dates), not in the `holidays` package | DECISIONS: D−7 already absorbs part of an effect lasting several weeks; summer holidays coincide with the high season | **B** |
| University semester breaks (Kiel University) | ✅ | lecture periods of Kiel University (CAU), source needed | depends on the branch's location (unknown) | **C**. Ask the client about the location first |

## Weather

All weather values are **observed**, not forecast. They serve as a stand-in for the forecast, so results come out somewhat too optimistic (canvas block 6). One run without weather shows how much weather contributes.

| Feature | Known in advance? | Data | Evidence of an effect | Proposal |
|---|---|---|---|---|
| Temperature *(addition)* | ⚠️ | `Temperatur`, daily mean, no gaps | plausible (ice-cream/cake weather, outing days); not analysed yet | **B**. Probably the most important weather feature |
| Rain | ⚠️ | only via `Wettercode` (type, no amount). 822 days with a rain/drizzle code | plausible: fewer passers-by | **B**. Group the codes into classes. A missing code means "no notable weather" and gets its own class (DECISIONS) |
| Snowfall | ⚠️ | `Wettercode`: 57 days with a snow code | plausible, but rare | **B**, as a class in the same weather-code feature |
| Frost | ⚠️ | only the daily mean, no daily minimum. 63 days with a mean < 0 °C | overlaps strongly with temperature and winter | **B, low priority**. Only helps if frost does more than "cold" |
| Sunshine | ⚠️ | no sunshine hours, only `Bewoelkung` (cloud cover, 0–8 octas) as a stand-in. 451 days with ≤ 2 octas. 10 missing days in the validation year | plausible | **B**, via `Bewoelkung`. Missing days are filled with the training monthly mean and flagged in `Wetter_fehlt` (DECISIONS 2026-11-24) |
| Wind | ⚠️ | `Windgeschwindigkeit`, median 10, range 3–35. Unit unclear | unclear | **C** |
| Weather forecast from the day before | ✅ (exactly what is known at 14:00) | we do not have archived forecasts for 2013–2019. Whether freely available ones exist is unchecked | would be the honest version of all weather features | **C**: briefly look for a source. If there is none, it stays a limitation in the report (as decided in the canvas) |

## Local events

**Location unknown:** neither the course data nor the fact sheet names the branch's location (only "Kiel"). Whether a city-centre event reaches the branch is therefore open. Only the data can tell: is revenue on event days above the usual level for that weekday?

In general, the dates are mostly known in advance. The hard part is getting a **complete list of dates from 2013 to 2019**. Also, there are often only 5–6 cases.

### City-centre events (research 2026-11-24)

The main source is the event calendar of Kiel-Marketing ([kiel-sailing-city.de](https://kiel-sailing-city.de/en/events)). The current pages give dates for 2025/2026. Whether the events already existed in 2013–2019, and on which days, is still to be checked.

| Feature | Known in advance? | Data | Evidence of an effect | Proposal |
|---|---|---|---|---|
| Kieler Umschlag (traditional city festival) | ✅ | late Feb/early Mar, e.g. 27 Feb – 2 Mar 2025 with Sunday shop opening. Dates for 2013–2019 not found | **interesting**: the highest confectionery revenues fall on Sun 23 Feb 2014, 22 Feb 2015 and 21 Feb 2016, right in this window. Other February Sundays are high too (2014: 2, 9, 16 Feb), so the event probably explains only part of it | **B**: obtain the dates for 2014–2019 (Kiel-Marketing, newspaper archive) and compare them with the peaks |
| Christmas market (Holstenplatz, Rathausplatz, Asmus-Bremer-Platz) | ✅ | roughly late November to 23 Dec in the city centre. The market on Holstenplatz has existed since 1973 | more people in the city centre | **B**: gives a concrete definition of the "Christmas season" (market period instead of December) |
| Sunday shop openings | ✅ (announced in advance) | according to Kiel-Marketing four times a year, tied to events (Kieler Umschlag, "Kiel blüht auf" in April, farmers' and regional market in October, Lichtermeer in November). Research the past dates | a Sunday with shops open means many more passers-by | **B**: one shared yes/no feature for all Sunday openings |
| Bootshafensommer (summer concerts) | ✅ | concerts at the Bootshafen in the city centre, July/August. 2023 was the 15th edition, so it already existed in the data period | coincides with summer holidays and high season, so hard to separate | **C** |
| Flea markets | ✅ | according to the city several per year (April–October) in the city centre, including Holstenplatz and Holstenstraße. Past dates missing | depends on the location | **C** (B if dates can be found) |
| Lichtermeer, "Kiel blüht auf", farmers' and regional market | ✅ | current events. Whether they existed in 2013–2019 is unclear | like Sunday openings | include in "Sunday shop openings" if they existed back then |

### Other events

| Feature | Known in advance? | Data | Evidence of an effect | Proposal |
|---|---|---|---|---|
| Cruise ships in port | ✅ (call schedules are published in advance) | annual totals exist (2015: 132, 2016: 147, 2018: 166 calls), daily lists for 2013–2019 not found | the Ostseekai terminal is close to the city centre. But in 2011–2015 more than half of the calls fell on weekends, and all within the April–October season. Weekday and season would already cover much of it | **C**: only if daily data exists |
| Black Friday / Black Week | ✅ (computable: Friday after the 4th Thursday in November) | from the date | more passers-by is only plausible if the branch is in a shopping location (location unknown). In Germany the day only became big in the mid-2010s (unchecked), so there are few real cases | **C**: cheap to build. Take a quick look whether revenue stands out in that week |
| Concerts/games in the arena | ✅ | THW Kiel (handball) home games are well documented historically, concerts less so | games mostly in the evening, the bakery probably notices little | **C** |
| Holstein Kiel (football) home games | ✅ (match days fixed weeks ahead) | historical fixtures are public (e.g. kicker, Wikipedia). Roughly 17–19 home games per season, so about 100 in the data period. 3rd division, from 2017/18 2nd Bundesliga with more spectators | the stadium is in the north of Kiel, not in the city centre. Whether the branch notices anything depends on the location (unknown). Games mostly Fri–Sun | **B/C**: of all events the one with the **most cases**, so it can be tested well statistically. First take a quick look whether home-game days are above the usual weekday level |
| Kiellauf (city run) | ✅ | one day per year, research the dates | unclear, few cases | **C** |
| Demonstrations | ❌ mostly spontaneous or known only shortly before | no collected source | unclear | **D** |

### Idea: one shared "city-centre event" feature

Many events have only 5–6 cases. As separate columns, the model learns a value for each that depends heavily on chance. Combining them into **one** yes/no column (Sunday opening, Kieler Umschlag, flea market …) gives enough cases for a stable effect. As a next step, only an event with clear evidence deserves its own column, e.g. the Kieler Umschlag with the confectionery peaks.

## More calendar ideas

| Feature | Known in advance? | Data | Why | Proposal |
|---|---|---|---|---|
| Bridge day (working day between a holiday and the weekend) | ✅ | from the holiday list | many people off, outing or shopping day | **B**, cheap |
| Valentine's Day (14 Feb) | ✅ | from the date | 14 Feb 2016 (a Sunday) is among the 12 highest confectionery days. But this may also be due to the February Sunday | **C**: cheap, look at it together with the February peaks |
| Mother's Day (2nd Sunday in May) | ✅ | from the date | cakes and tortes | **C**, cheap |
| Start of month / payday | ✅ | from the date | people spend more after payday | **C**, cheap. Probably a small effect for a bakery |
| Football World Cup/Euros (tournament period, Germany games, public viewing) | ✅ | fixtures are public: World Cup 2014, Euro 2016, World Cup 2018, each mid-June to mid-July | **All three tournaments overlap with Kiel Week** (Kiel Week 21–29 Jun 2014, 18–26 Jun 2016, 16–24 Jun 2018, per `kiwo.csv`), and even Germany games fell within Kiel Week (e.g. 26 Jun 2014, 21 Jun 2016, 17 and 23 Jun 2018). The model can hardly separate the two effects. Also, there is **no tournament in the test year 2018-08 – 2019-07**, so the feature would never be switched on there | **D** for the model. At most, check afterwards whether large errors during Kiel Week/tournament time fall on match days |

## Additions missing from the list

| Feature | Known in advance? | Data | Why | Proposal |
|---|---|---|---|---|
| **Product group** | ✅ | `Warengruppe` | the groups have very different revenue (rolls ~€400, seasonal bread ~€67) | **A, mandatory**, as one-hot columns |
| Revenue D−7 (same group) | ✅ (D−7 is before D−2) | from the sales data | this is current practice. As a feature, the model can build on it | **A** |
| Average of recent weeks (same group and same weekday, e.g. D−7, D−14, D−21, D−28) | ✅ | from the sales data | smooths outliers such as a single holiday in D−7 | **B** |
| Month or season | ✅ | from the date | summer/winter is its own segment in the canvas | **A** |
| Time trend | ✅ | from the date | revenue fell by ~17 % from 2014 to 2016. Already decided as a feature in DECISIONS | **A or B** |
| Day before a holiday / day after a closure | ✅ | from the holiday list | bread peak before Easter, peak after the 3-day closure (2014-05-05). Open question in the canvas | **B** |
| Interactions product group × weekday, × holiday | ✅ | from the columns above | otherwise linear regression gives each feature **one** effect for all groups. For holidays, though, H3 shows bread −41 % and confectionery +98 % | **A** for holiday, **B** for weekday. Alternative: one model per product group |

## What to watch for in linear regression

- **Categories as yes/no columns (one-hot):** applies to weekday, month, product group, holiday category and weather class, never as a number 0, 1, 2, …
- **No duplicated information:** weekday and weekend together, or frost next to temperature, make the coefficients hard to read.
- **Rare features:** Kiel Week, New Year's Eve and Kieler Umschlag have only 5–6 cases. The model learns a value for them that depends on chance. So check them as a segment in the validation year (canvas block 4).
- **Check K7** (still to be written): no sales feature for D uses data newer than D−2.

## Proposal for the baseline model (for decision)

Product group, weekday, month, holiday category (normal / open public holiday / special day) with interaction with product group, Kiel Week, revenue D−7. Weather (temperature, weather class, cloud cover) once with and once without.

## Questions

- **Team:** Which A features go into the baseline? How is the "Christmas season" defined? Who obtains the school holiday dates?
- **Client / course instructors:** Where is the branch located? All city-centre events, semester breaks, cruise ships and home games depend on it.
- **Team:** Who looks up the 2013–2019 dates for the Kieler Umschlag and Sunday openings (ask Kiel-Marketing, newspaper archive)? Should rare events be combined into one "city-centre event" feature?
