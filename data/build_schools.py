"""
Build data/schools_2025.csv for the hexagon bin map.

Run from the repository root:
    python data/build_schools.py

Input : data/raw/School_Location_2025.xlsx (ACARA, School Location 2025)
Output: data/schools_2025.csv, one row per school location
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

# --------------------------------------------------------------------------
# Read and keep the columns the map needs
# --------------------------------------------------------------------------
raw = pd.read_excel(HERE / "raw" / "School_Location_2025.xlsx", sheet_name="SchoolLocations 2025")
schools = pd.DataFrame({
    "sector": raw["School Sector"],
    "lon": raw["Longitude"].round(4),
    "lat": raw["Latitude"].round(4),
})

# --------------------------------------------------------------------------
# Drop the five schools on islands outside the mapped area
# (Norfolk, Lord Howe, Christmas and Cocos Islands)
# --------------------------------------------------------------------------
on_map = schools["lon"].between(112, 154)
print(f"  dropped {(~on_map).sum()} island schools outside the map")
schools = schools[on_map].sort_values(["sector", "lon", "lat"])

schools.to_csv(HERE / "schools_2025.csv", index=False)
print(f"  wrote schools_2025.csv {len(schools):6d} rows  {(HERE / 'schools_2025.csv').stat().st_size/1024:6.1f} KB")

# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
assert len(raw) == 11039, len(raw)
assert schools["sector"].isin(["Government", "Catholic", "Independent"]).all()
remote = raw[on_map & raw["ABS Remoteness Area Name"].isin(["Remote", "Very Remote"])]
share = (remote["School Sector"] == "Government").mean()
print(f"  government share of remote and very remote schools: {share:.1%}")
print(schools["sector"].value_counts().to_string())
