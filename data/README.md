# Data — Who pays for Australia's schools?

FIT3179 Data Visualisation 2 · Muhammad Ariez Zuhayr · 34599959

Everything the page loads lives in this folder (about 560 KB in total). The
original downloads were cleaned in Python into the small CSV files below.

## Sources

| # | Publisher | Dataset | Used for | Link |
|---|---|---|---|---|
| 1 | Australian Curriculum, Assessment and Reporting Authority (ACARA) | *School finance dataset*, National Report on Schooling in Australia data portal, February 2026 release | School income by source and sector, 2009–2024 | https://dataandreporting.blob.core.windows.net/anrdataportal/ANR-ExcelDownloads/202602/School%20finance%20dataset.xlsx |
| 2 | Productivity Commission | *Report on Government Services 2026*, Part B Section 4, Table 4A.32: government recurrent expenditure per full-time student, 2023-24 dollars | Funding per student by state, sector and funder, 2014-15 to 2023-24 | https://www.pc.gov.au/ongoing/report-on-government-services/child-care-education-and-training/school-education/ |
| 3 | Australian Bureau of Statistics (ABS) | *Schools, 2025*, Table 43a: full-time equivalent students, 2006–2025 | Students by state and sector | https://www.abs.gov.au/statistics/people/education/schools/latest-release |
| 4 | ACARA | *School Location 2025*, one row per school with sector, latitude and longitude, used under the My School terms of use | Hexagon bin map | https://acara.edu.au/contact-us/acara-data-access |
| 5 | ABS state boundaries, via github.com/rowanhogan/australian-states | `states.geojson`, simplified to 10% with mapshaper and converted to TopoJSON | All maps | https://github.com/rowanhogan/australian-states |

## Files

| File | Rows | Grain | Key columns | Figures |
|---|---:|---|---|---|
| `enrolments.csv` | 540 | year (2006–2025) × state × sector | `fte_students` | 1 pictogram · 12 butterfly |
| `gov_funding_real.csv` | 810 | financial year (2014-15 to 2023-24) × state × sector × source | `per_student_real_2023_24_aud` | 5 choropleth · 8 lollipop · 9 small multiples · 10 slope · 11 heatmap |
| `school_income_2024.csv` | 135 | state × sector × source, calendar 2024 | `total_aud`, `per_student_aud`, `source_group` | 2 Sankey · 3 dumbbell · 12 butterfly · 13 treemap |
| `school_income_trend.csv` | 240 | calendar year (2009–2024) × sector × source, Australia | as above | 4 stacked bar (year slider) |
| `schools_2025.csv` | 11,034 | one row per school, 2025 (five island schools outside the map removed) | `sector`, `lon`, `lat` | 7 hexagon bin map |
| `states.csv` | 8 | state | `state_abbr`, `lon`, `lat`, `students_2025`, `nongov_students_2025` | 5 choropleth labels · 6 symbol map |
| `geo/aus_states.topojson` | 8 shapes | state | `STATE_NAME` | 5, 6, 7, 9 |

**Shared names in every file**, so charts can be joined without renaming:

- `state`: full names, identical to `STATE_NAME` in the TopoJSON, plus `Australia` for national totals. `state_abbr` gives NSW, Vic, Qld, SA, WA, Tas, NT, ACT and Aust.
- `sector`: `Government`, `Catholic`, `Independent`; the funding file uses `Non-government` where the source doesn't split Catholic from independent, and `All` for every school.
- `source`: `Australian Government`, `State and territory government`, `Total government`; the income files add `Fees and parent contributions`, `Other private sources` and `Total gross income`.

## How the files were made

Filtering, renaming, reshaping and summing only. Nothing is estimated or imputed.

- ACARA dollar text (`$1,234`) parsed to numbers; suppressed cells (`-`) left empty.
- ACARA school income filtered to all school levels and all locations. Catholic and independent follow ACARA's headline split, and the two add exactly to ACARA's "All non-government".
- RoGS Table 4A.32 reshaped from its printed layout into one row per year × state × sector × source. Real values are the Productivity Commission's own, in 2023-24 dollars.
- ABS Table 43a: rows summed over sex, full/part-time, school level and year level to give state × sector × year; Australia is the sum of the states.

Results were checked against published totals: 2023-24 government funding of $91.04 billion matches ACARA's National Report on Schooling, and the Northern Territory ($30,845) and Victoria ($20,715) per-student figures match RoGS.

## Two funding measures — never mixed in one chart

| | Government funding (`gov_funding_real.csv`) | School income (`school_income_*.csv`) |
|---|---|---|
| What | What governments spent on schools | What schools report receiving |
| Period | Financial year (July–June) | Calendar year |
| Sectors | Government / Non-government | Government / Catholic / Independent |
| 2023-24 / 2024 total from government | $91.04 billion | $74.7 billion |

## Caveats from the RoGS 4A.32 footnotes

- **2019-20**: non-government funding spikes in several states because some COVID-19 grants were paid early (annotated on Figure 9).
- **SA 2022-23**: state funding of non-government schools drops because South Australia paid it early, in 2021-22.
- **NSW**: non-government expenditure moved from cash to accrual accounting from 2018-19.

`raw/` holds the original downloads (about 21 MB). It is git-ignored, so it is not published.
