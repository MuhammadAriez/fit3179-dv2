# Data — Who pays for Australia's schools?

FIT3179 Data Visualisation 2 · Muhammad Ariez Zuhayr · 34599959

Everything the page loads lives in this folder. `raw/` holds the original
downloads; `build_data.py` turns them into the small CSVs below and checks the
results against published figures. Rebuild with:

    python data/build_data.py

Total size of what the page loads: about 230 KB.

## Sources

| # | Publisher | Dataset | Used for | Link |
|---|---|---|---|---|
| 1 | ACARA (Australian Curriculum, Assessment and Reporting Authority) | *School finance dataset*, National Report on Schooling in Australia data portal, Feb 2026 release — sheets "Government Funding" and "School income" | Government funding by source; school income by source and sector | https://dataandreporting.blob.core.windows.net/anrdataportal/ANR-ExcelDownloads/202602/School%20finance%20dataset.xlsx |
| 2 | Productivity Commission | *Report on Government Services 2026*, Part B Section 4 School education, Table 4A.32 — real government recurrent expenditure per FTE student, 2023-24 dollars | Change over time, inflation-adjusted | https://www.pc.gov.au/ongoing/report-on-government-services/child-care-education-and-training/school-education/ |
| 3 | Australian Bureau of Statistics | *Schools, 2025*, Table 43a Full-time equivalent (FTE) students, 2006–2025 | Enrolments by state and sector | https://www.abs.gov.au/statistics/people/education/schools/latest-release |
| 4 | Australian Bureau of Statistics | *Schools, 2025*, Table 90a Key information by states and territories | Cross-check only (headcounts) | same page as 3 |
| 5 | ABS ASGS state boundaries, via github.com/rowanhogan/australian-states | `states.geojson`, simplified to 10% with mapshaper and converted to TopoJSON | All maps | https://github.com/rowanhogan/australian-states |

The ABS and the Productivity Commission publish under Creative Commons
Attribution 4.0. Check ACARA's copyright page before publishing, and credit
every source in the page footer either way.

## Files

| File | Rows | Grain | Key columns | Panels |
|---|---:|---|---|---|
| `enrolments.csv` | 540 | year (2006–2025) × state × sector | `fte_students` | 1 waffle · 7 symbol map · 12 butterfly |
| `gov_funding_real.csv` | 810 | financial year (2014-15 – 2023-24) × state × sector × source | `per_student_real_2023_24_aud` | 6 choropleth · 8 lollipop · 9 small multiples · 10 slope · 11 heatmap |
| `gov_funding_nominal.csv` | 1,179 | financial year (2005-06 – 2023-24) × state × sector × source | `total_aud`, `per_student_aud` | 3 flow map |
| `school_income_2024.csv` | 135 | state × sector × source, calendar 2024 | `total_aud`, `per_student_aud`, `source_group` | 2 Sankey · 4 dumbbell · 5 stacked bar · 12 butterfly · 13 treemap |
| `school_income_trend.csv` | 240 | calendar year (2009–2024) × sector × source, Australia | as above | spare |
| `states.csv` | 8 | state (one row each, so a `lookup` is safe) | `state_abbr`, `lon`, `lat`, `funding_per_student_2014_15` / `_2018_19` / `_2023_24` (all schools, 2023-24 dollars), `cwlth_funding_2023_24`, `students_2025`, `nongov_students_2025` | 6 choropleth · 3 flow map · 7 symbol map · 9 small multiples |
| `geo/aus_states.topojson` | 8 shapes | state | `STATE_NAME`, `STATE_CODE` | all maps |
| `geo/state_points.csv` | 8 | state | `lon`, `lat` (a point guaranteed inside each state) | 3 flow map · 7 symbol map |

**Shared vocabulary across every file** (so legends never need renaming):

- `state` — full names, identical to `STATE_NAME` in the TopoJSON, plus `Australia` for national totals. `state_abbr` gives NSW, Vic, Qld, SA, WA, Tas, NT, ACT, Aust for labels.
- `sector` — `Government`, `Catholic`, `Independent`; the funding files use `Non-government` where the source does not split Catholic from independent, and `All` for every school.
- `source` — `Australian Government`, `State and territory government`, `Total government`; the income files add `Fees and parent contributions`, `Other private sources` and `Total gross income`.

## Transformations

Filtering, renaming, and summing only. Nothing is estimated or imputed.

- ACARA dollar strings (`$1,234`) parsed to numbers; suppressed cells (`-`) left empty.
- ACARA School income filtered to all school levels and all locations. Catholic and Independent follow ACARA's headline split (non-systemic Catholic schools sit inside Independent); the two add exactly to ACARA's "All non-government".
- RoGS 4A.32 reshaped from its printed layout into one row per year × state × sector × source.
- ABS 43a: FTE rows summed over sex, full/part-time, school level and year level to give state × sector × year; Australia is the sum of the states.

## Two funding measures — do not mix them in one chart

| | Government Funding (files `gov_funding_*`) | School income (files `school_income_*`) |
|---|---|---|
| What | What governments spent on schools | What schools report receiving |
| Period | Financial year (July–June) | Calendar year |
| Sectors | Government / Non-government | Government / Catholic / Independent |
| Includes | User cost of capital for government schools | Fees and private income |
| 2023-24 / 2024 total from government | **$91.04 bn** | **$74.7 bn** |

They differ in scope: Government Funding counts everything governments spend
on schooling, including system-level costs and, for government schools, the user
cost of capital (the notional cost of the land and buildings they occupy — see
the RoGS 4A.32 heading). School income counts only what each school reports
receiving. Label every chart with its measure and year.

## Caveats worth an annotation

From the RoGS 4A.32 footnotes:

- **2019-20**: non-government spikes in several states — grant payments brought forward from 2020-21 to help non-government schools through COVID-19 (+$195 m nationally).
- **SA 2022-23**: state funding of non-government schools drops to $1,246 per student because SA brought it forward into 2021-22.
- **NSW**: non-government expenditure moved from cash to accrual accounting from 2018-19.
- Real values use the General Government Final Consumption Expenditure chain price deflator, 2023-24 = 100.

## Verification

`build_data.py` stops with an error if any check fails. Current results:

- 2023-24 total government recurrent funding $91,039,813,000; Australian Government $29,158,736,000; states $61,881,077,000 — matches ACARA National Report on Schooling 2024, Chapter 9.
- Per student: government schools $26,140, non-government $15,262 — matches.
- RoGS 4A.32 against ACARA for 2023-24: 77 of 81 state × sector × source cells identical, 4 differ by $1 because the two publications round independently.
- 2024 gross income per student: government $20,368, Catholic $22,067, independent $28,642, and every source share — matches ACARA's School income page.
- `states.csv`: NT $30,845 and Victoria $20,715 per student in 2023-24; Australian Government funding summed across states equals the national figure within $1,000; students summed across states equal the national FTE within 5.
- ABS FTE students for 2025 sit at 99.65–99.95% of the Table 90a headcount in every state, as expected (part-time students count as less than one FTE).

## Not in the repository

`raw/` is about 19 MB and the page never loads it. Add `data/raw/` to
`.gitignore` and rely on the links above, or commit it if you want the build
to be reproducible from the repository alone.
