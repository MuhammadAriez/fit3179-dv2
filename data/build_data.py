"""
Build the tidy CSVs that the Vega-Lite specs load.

Run from the repository root:
    python data/build_data.py

Inputs  : data/raw/  (the four files downloaded from ACARA, the Productivity
          Commission and the ABS; see data/README.md for links)
Outputs : data/*.csv  (small, long-format files; every column traces to a
          named source table)

No values are estimated or imputed. The only transformations are filtering,
renaming, summing ABS FTE rows to state x sector totals, and parsing "$1,234"
strings to numbers.
"""
import re
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "raw"

# Full state names match the STATE_NAME property in geo/aus_states.topojson,
# so Vega-Lite lookups join without a crosswalk.
STATE_ORDER = [
    "New South Wales", "Victoria", "Queensland", "South Australia",
    "Western Australia", "Tasmania", "Northern Territory",
    "Australian Capital Territory", "Australia",
]
ABBR = {
    "New South Wales": "NSW", "Victoria": "Vic", "Queensland": "Qld",
    "South Australia": "SA", "Western Australia": "WA", "Tasmania": "Tas",
    "Northern Territory": "NT", "Australian Capital Territory": "ACT",
    "Australia": "Aust",
}
FULL = {v: k for k, v in ABBR.items()}


def money(series):
    """'$1,234' -> 1234.0 ; '-' (suppressed) -> NaN"""
    s = series.astype(str).str.replace(r"[\$,]", "", regex=True).str.strip()
    return pd.to_numeric(s.where(s != "-"), errors="coerce")


def fy_end(fy):
    """'2023-24' or '2023–24' -> 2024"""
    a, b = re.split(r"[-–]", fy)
    return int(a[:2] + b) if len(b) == 2 else int(b)


# --------------------------------------------------------------------------
# 1. ACARA School finance dataset (National Report on Schooling, Feb 2026)
# --------------------------------------------------------------------------
print("Reading ACARA School finance dataset ...")
acara = pd.read_excel(
    RAW / "School finance dataset.xlsx",
    sheet_name=["Government Funding", "School income"],
    dtype=str,
)

# 1a. Government recurrent funding, by state, sector and source (nominal $)
g = acara["Government Funding"].copy()
g.columns = ["year", "state", "sector", "source", "total_aud", "per_student_aud"]
g["year"] = g["year"].str.replace("–", "-", regex=False)
g["year_end"] = g["year"].map(fy_end)
g["sector"] = g["sector"].replace({"All non-government": "Non-government"})
g["source"] = g["source"].replace({
    "State and territory governments": "State and territory government",
    "Total Australian/State/territory government expenditure": "Total government",
})
g["total_aud"] = money(g["total_aud"])
g["per_student_aud"] = money(g["per_student_aud"])
g["state_abbr"] = g["state"].map(ABBR)
gov_nominal = g[["year", "year_end", "state", "state_abbr", "sector", "source",
                 "total_aud", "per_student_aud"]]

# 1b. School income by source, three sectors, all levels, all locations
s = acara["School income"].copy()
s.columns = ["year", "state", "sector", "level", "location", "item",
             "total_aud", "per_student_aud"]
ITEMS = {
    "Australian government recurrent funding": "Australian Government",
    "State/territory government recurrent funding": "State and territory government",
    "Income from fees, charges and parent contributions": "Fees and parent contributions",
    "Income from other private sources": "Other private sources",
    "Total gross income": "Total gross income",
}
GROUP = {
    "Australian Government": "Government", "State and territory government": "Government",
    "Fees and parent contributions": "Private", "Other private sources": "Private",
    "Total gross income": "Total",
}
s = s[(s["level"] == "All") & (s["location"] == "All")
      & s["sector"].isin(["Government", "Catholic", "Independent"])
      & s["item"].isin(ITEMS)].copy()
s["source"] = s["item"].map(ITEMS)
s["source_group"] = s["source"].map(GROUP)
s["year"] = s["year"].astype(int)
s["total_aud"] = money(s["total_aud"])
s["per_student_aud"] = money(s["per_student_aud"])
s["state_abbr"] = s["state"].map(ABBR)
cols = ["year", "state", "state_abbr", "sector", "source", "source_group",
        "total_aud", "per_student_aud"]
income_2024 = s[s["year"] == 2024][cols]
income_trend = s[s["state"] == "Australia"][cols]

# --------------------------------------------------------------------------
# 2. Productivity Commission RoGS 2026, Table 4A.32
#    Real government recurrent expenditure per FTE student, 2023-24 dollars
# --------------------------------------------------------------------------
print("Reading RoGS 2026 Table 4A.32 ...")
r = pd.read_excel(
    RAW / "rogs-202606-partb-section4-school-education-data-tables.xlsx",
    sheet_name="Table 4A.32", header=None,
)
state_cols = list(range(12, 21))
state_names = [FULL[re.sub(r"[\s\xa0].*$", "", str(r.iat[1, c]))] for c in state_cols]
SECTOR = {"Government schools": "Government",
          "Non-government schools": "Non-government",
          "All schools": "All"}
SOURCE = {"Australian Government payments": "Australian Government",
          "State and territory government expenditure": "State and territory government",
          "Australian, state and territory government expenditure": "Total government"}
rows, sector, source = [], None, None
for i in range(2, len(r)):
    c0, c2, c4 = r.iat[i, 0], r.iat[i, 2], r.iat[i, 4]
    if isinstance(c0, str) and c0 in SECTOR:
        sector = SECTOR[c0]
    if isinstance(c2, str) and c2 in SOURCE:
        source = SOURCE[c2]
    if isinstance(c4, str) and re.fullmatch(r"\d{4}-\d{2}", c4) and sector and source:
        for c, st in zip(state_cols, state_names):
            rows.append({"year": c4, "year_end": fy_end(c4), "state": st,
                         "state_abbr": ABBR[st], "sector": sector, "source": source,
                         "per_student_real_2023_24_aud": float(r.iat[i, c])})
    if isinstance(c0, str) and c0.startswith("(a)"):
        break
gov_real = pd.DataFrame(rows)

# --------------------------------------------------------------------------
# 3. ABS Schools 2025, Table 43a  FTE students by state and affiliation
# --------------------------------------------------------------------------
print("Reading ABS Table 43a ...")
a = pd.read_excel(
    RAW / "Table 43a Full-time equivalent (FTE) students, 2006-2025.xlsx",
    sheet_name="Table 2 Data table", header=3, dtype=str,
)
a.columns = [c.strip() for c in a.columns]
a = a[a["Year"].str.fullmatch(r"\d{4}", na=False)].copy()
strip = lambda x: re.sub(r"^[a-z]{1,2} ", "", x).rstrip(".")
a["state"] = a["State/Territory"].map(strip).map(FULL)
a["sector"] = a["Affiliation (Gov/Cath/Ind)"].map(strip)
a["fte"] = pd.to_numeric(a["FTE All Students"], errors="coerce")
enr = (a.groupby(["Year", "state", "sector"], as_index=False)["fte"].sum()
         .rename(columns={"Year": "year", "fte": "fte_students"}))
aus = enr.groupby(["year", "sector"], as_index=False)["fte_students"].sum()
aus["state"] = "Australia"
enr = pd.concat([enr, aus], ignore_index=True)
enr["year"] = enr["year"].astype(int)
enr["fte_students"] = enr["fte_students"].round(1)
enr["state_abbr"] = enr["state"].map(ABBR)
enr = enr[["year", "state", "state_abbr", "sector", "fte_students"]]

# --------------------------------------------------------------------------
# 4. One row per state, for the maps
#    A Vega-Lite "lookup" joins on a key, so the table it looks values up in
#    must have exactly one row per state (like covid_10_10_2020.csv in the
#    Week 8 studio had one row per country).
# --------------------------------------------------------------------------
pts = (pd.read_csv(HERE / "geo" / "state_points.csv")
         .rename(columns={"STATE_NAME": "state"})[["state", "lon", "lat"]])
states = pd.DataFrame({"state": STATE_ORDER[:-1]})          # 8 states, no "Australia"
states["state_abbr"] = states["state"].map(ABBR)
states = states.merge(pts, on="state")
states["lon"] = states["lon"].round(4)
states["lat"] = states["lat"].round(4)

# Government funding per student, all schools, real 2023-24 dollars (RoGS 4A.32)
for fy in ["2014-15", "2018-19", "2023-24"]:
    q = gov_real[(gov_real["year"] == fy) & (gov_real["sector"] == "All")
                 & (gov_real["source"] == "Total government")].set_index("state")
    states["funding_per_student_" + fy.replace("-", "_")] = states["state"].map(q["per_student_real_2023_24_aud"])

# Australian Government money to each state, all schools, 2023-24 (ACARA)
q = gov_nominal[(gov_nominal["year"] == "2023-24") & (gov_nominal["sector"] == "All")
                & (gov_nominal["source"] == "Australian Government")].set_index("state")
states["cwlth_funding_2023_24"] = states["state"].map(q["total_aud"])

# Students in 2025, all sectors and non-government only (ABS 43a)
e25 = enr[enr["year"] == 2025]
states["students_2025"] = states["state"].map(e25.groupby("state")["fte_students"].sum()).round(0).astype(int)
states["nongov_students_2025"] = states["state"].map(
    e25[e25["sector"] != "Government"].groupby("state")["fte_students"].sum()).round(0).astype(int)

# --------------------------------------------------------------------------
# Sort and write
# --------------------------------------------------------------------------
order = {s: i for i, s in enumerate(STATE_ORDER)}
def tidy(df, keys):
    return df.assign(_o=df["state"].map(order)).sort_values(keys).drop(columns="_o")

outputs = {
    "gov_funding_nominal.csv": tidy(gov_nominal, ["year_end", "_o", "sector", "source"]),
    "gov_funding_real.csv": tidy(gov_real, ["year_end", "_o", "sector", "source"]),
    "school_income_2024.csv": tidy(income_2024, ["_o", "sector", "source"]),
    "school_income_trend.csv": tidy(income_trend, ["year", "sector", "source"]),
    "enrolments.csv": tidy(enr, ["year", "_o", "sector"]),
    "states.csv": states,
}
for name, df in outputs.items():
    df.to_csv(HERE / name, index=False)
    print(f"  wrote {name:28s} {len(df):5d} rows  {(HERE / name).stat().st_size/1024:6.1f} KB")

# --------------------------------------------------------------------------
# Verification against published headline figures and across sources
# --------------------------------------------------------------------------
print("\nVerification")
def check(label, got, want, tol=0):
    ok = abs(got - want) <= tol
    print(f"  [{'OK' if ok else 'FAIL'}] {label}: {got:,.2f} (expected {want:,.2f})")
    assert ok, label

q = gov_nominal.query("year == '2023-24' and state == 'Australia'").set_index(["sector", "source"])
check("2023-24 total government recurrent funding", q.loc[("All", "Total government"), "total_aud"], 91_039_813_000)
check("2023-24 Australian Government share", q.loc[("All", "Australian Government"), "total_aud"], 29_158_736_000)
check("2023-24 state and territory share", q.loc[("All", "State and territory government"), "total_aud"], 61_881_077_000)
check("Government schools per student", q.loc[("Government", "Total government"), "per_student_aud"], 26_140)
check("Non-government schools per student", q.loc[("Non-government", "Total government"), "per_student_aud"], 15_262)

# RoGS real 2023-24 dollars must equal ACARA nominal in the base year 2023-24
m = gov_real.query("year == '2023-24'").merge(
    gov_nominal.query("year == '2023-24'"), on=["state", "sector", "source"])
d = (m["per_student_real_2023_24_aud"] - m["per_student_aud"]).abs()
# The two publications round each cell to whole dollars independently, so a
# few totals differ by $1 (e.g. SA non-government: RoGS 13,042 + 3,402 = 16,444,
# ACARA 16,443). Anything larger would mean a parsing error.
check(f"RoGS 4A.32 vs ACARA, 2023-24, {len(m)} cells, max difference ($)", d.max(), 0, 1)
print(f"  [info] {int((d == 0).sum())} of {len(m)} cells identical; {int((d > 0).sum())} differ by $1 (rounding)")

inc = income_2024.query("state == 'Australia'").pivot(index="source", columns="sector", values="per_student_aud")
for sec, want in [("Government", 20_368), ("Catholic", 22_067), ("Independent", 28_642)]:
    check(f"2024 gross income per student, {sec}", inc.loc["Total gross income", sec], want)
# ACARA's School income page publishes government-school shares as whole
# percentages and Catholic/independent shares to one decimal place, so the
# tolerance follows the published precision.
shares = {"Government": (21, 75, 4, 0.5), "Catholic": (60.4, 14.8, 24.8, 0.05),
          "Independent": (38.4, 9.8, 51.7, 0.05)}
for sec, (cw, st, pv, tol) in shares.items():
    tot = inc.loc["Total gross income", sec]
    check(f"{sec} Australian Government share %", 100 * inc.loc["Australian Government", sec] / tot, cw, tol)
    check(f"{sec} state share %", 100 * inc.loc["State and territory government", sec] / tot, st, tol)
    check(f"{sec} private share %", 100 * (inc.loc["Fees and parent contributions", sec] + inc.loc["Other private sources", sec]) / tot, pv, tol)

# ABS Table 90a gives 2025 headcounts (full-time + part-time) per state.
# FTE counts part-timers fractionally, so FTE must sit just below headcount.
t90 = RAW / "Table 90a Key information by states and territories, 2024 to 2025.xlsx"
e25 = enr.query("year == 2025").groupby("state")["fte_students"].sum()
for n, st in enumerate(STATE_ORDER, start=1):
    sheet = pd.read_excel(t90, sheet_name=f"Table {n}", header=None)
    hit = sheet.index[sheet[0].astype(str).str.startswith("Number of students")][0]
    total_row = sheet.index[(sheet.index > hit) & (sheet[0] == "Total")][0]
    headcount = float(sheet.iat[total_row, 3])
    ratio = e25[st] / headcount
    ok = 0.98 <= ratio <= 1.0
    print(f"  [{'OK' if ok else 'FAIL'}] 2025 {ABBR[st]:4s} FTE {e25[st]:>12,.0f} vs headcount {headcount:>12,.0f} ({100*ratio:.2f}%)")
    assert ok, st
st = states.set_index("state_abbr")
check("states.csv: NT funding per student 2023-24", st.loc["NT", "funding_per_student_2023_24"], 30_845)
check("states.csv: Vic funding per student 2023-24", st.loc["Vic", "funding_per_student_2023_24"], 20_715)
check("states.csv: Commonwealth money to states adds to the national total",
      st["cwlth_funding_2023_24"].sum(), 29_158_736_000, 1_000)
check("states.csv: students add to the 2025 national FTE total",
      st["students_2025"].sum(), enr.query("year == 2025 and state == 'Australia'")["fte_students"].sum(), 5)
print("\nAll checks passed.")
