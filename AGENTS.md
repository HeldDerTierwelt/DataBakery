# Project constitution

This file tells coding agents (Claude Code, Codex, Cursor, …) what this project is about and which rules apply. It is read at the start of every agent session. The course infrastructure below is filled in. Your team adds the rest in week 3: `/setup-ds-project` adds a section that points to your canvas, glossary and decision log, and `/grill-question` fills the canvas.

## Team

Christine Avery, Zhouling Zhang, Alexander Goy  

Responsibilites (tbd)
## Data

- Sales, weather and Kiel Week data: see the [dataset documentation](https://github.com/opencampus-sh/intro-to-data-science-and-ml/blob/main/data/bakery/README.md). Load the files from `https://raw.githubusercontent.com/opencampus-sh/intro-to-data-science-and-ml/main/data/bakery/`.
- Additional data sources: [list them with link and the variables created from them]
  - Public holidays in Schleswig-Holstein: Python package [`holidays`](https://github.com/vacanza/holidays) (`holidays.Germany(subdiv="SH")`, version pinned in `uv.lock`). Special days (Easter Sunday, Whit Sunday, Christmas Eve, New Year's Eve) are not public holidays and are defined by the team from fixed dates and the Easter date. Variables: holiday day type (normal day / open public holiday / Easter-Whit Sunday / Christmas Eve / New Year's Eve; DECISIONS 2026-11-27). Which holidays count as open follows the Ladenöffnungszeitengesetz Schleswig-Holstein, § 4 (DECISIONS 2026-11-26). Plan: `docs/h3-holidays-plan.md`.
- Kaggle competition (course competition by opencampus.sh, data from meteolytix; rules recorded 2026-11-24 from the competition page):
  - **Task:** forecast daily revenue (`Umsatz`) of one bakery branch for six product groups: 1 Bread, 2 Rolls, 3 Croissants, 4 Confectionery, 5 Cakes, 6 Seasonal bread.
  - **Test period:** "the 12 months after the last date in the training data", i.e. 2018-08-01 – 2019-07-31 (first id in the sample submission is `201808011`). The overview page says the training data runs to 2018-07-30, but the sales file ends on 2018-07-31 (check K3).
  - **Files on Kaggle:** `train.csv` (`id`, `Datum`, `Warengruppe`, `Umsatz`), `test.csv` (same columns without `Umsatz`, so date and group can be read directly, not from the `id`), `sample_submission.csv`, `wetter.csv`, `kiwo.csv`. We load the course copies (`umsatzdaten_gekuerzt.csv` etc.); whether `train.csv` is identical is unchecked.
  - **Branch location:** "somewhere in Kiel", no more detail.
  - **Where the Kaggle description differs from the data:** temperature column is called `Temperatur` (not `Temperature`); wind speed is stated as m/s (values 3–35 make this doubtful, see glossary); Kiel Week is described as 10 days for 2013–2019, but `kiwo.csv` has 9 days per year for 2012–2019 (data fact sheet §3).
  - **Metric:** MAPE (mean absolute percentage error), lower is better. Same as the main metric in canvas block 4.
  - **Submission format:** a CSV with header `id,umsatz` (lower case) and exactly one prediction per `id` of the test file, e.g. `201808011,0.0`. The sample ids have 9 digits (`YYYYMMDD` + group), while the training ids have 7 (`YYMMDD` + group); check the test file before joining.
  - **Dates on the page:** start 2025-11-13, close 2026-01-08. These are past dates; check whether this course run uses a new competition.

## Conventions

- Environment: managed with **uv**. Install with `uv sync`; add packages only with `uv add <package>` (never `pip install`), and commit `pyproject.toml` and `uv.lock`.
- Work in Jupyter notebooks in the folder of the respective project step (`0_DataPreparation`, `1_DatasetCharacteristics`, `2_BaselineModel`, `3_Model`). Notebooks must run from top to bottom without errors.
- Every notebook starts with a short markdown cell explaining its purpose; important steps are explained in plain language.
- Weekdays are ordered Monday to Sunday, never alphabetically.
- [Further team conventions, e.g. naming of files and variables]

## How the agent should work

- Explain what you do in plain language and name the concept behind it. Many team members are not programmers.
- State your plan before you change code, and point out what we should check in the results.
- Never invent results: run the code and report what it actually returns.
- Questions about the decision, the audiences, what counts as success, what is known in advance, how to split the data and which checks to run are the team’s to decide. If the canvas or the decision log does not settle them yet, ask; do not decide them yourself.
- Only work inside this repository. Ask before deleting files, installing software outside the project environment or pushing to GitHub.
- Never write passwords, API keys or personal data into files.

## Agentic data science

- Canvas: `CANVAS.md` (read before any analysis work; update when something is decided)
- Glossary: `GLOSSARY.md`; decisions: `DECISIONS.md`
- Checks: `checks/`, run with `uv run pytest checks`; experiment log: `experiments/LOG.md`
- Tracker: GitHub Issues on `HeldDerTierwelt/DataBakery` with labels `analysis-plan`, `experiment`, `ready-for-agent`
- Data: sales, weather and Kiel Week CSVs loaded from `https://raw.githubusercontent.com/opencampus-sh/intro-to-data-science-and-ml/main/data/bakery/` (`umsatzdaten_gekuerzt.csv`, `wetter.csv`, `kiwo.csv`). Raw data is read-only.
