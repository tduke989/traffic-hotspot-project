import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Plot starting...")
# Load CLEAN dataset
df = pd.read_csv("Traffic_Incidents_filtered_2020.csv")

# Convert date
df["START_DT"] = pd.to_datetime(df["START_DT"], errors="coerce")

# FILTER 2021–2026
df = df[(df["START_DT"].dt.year >= 2021) & (df["START_DT"].dt.year <= 2026)]

# Clean location text
df["INCIDENT INFO"] = df["INCIDENT INFO"].str.strip()

# Count incidents
top_locations = df["INCIDENT INFO"].value_counts().head(10)

# Reverse for horizontal chart
top_locations = top_locations[::-1]

# Highlight top 2
colors = ["lightgrey"] * len(top_locations)
colors[-1] = "red"
colors[-2] = "red"

plt.figure(figsize=(11,6))

plt.barh(top_locations.index, top_locations.values, color=colors)

plt.title("Top Traffic Incident Locations (2021-2026)")
plt.xlabel("Number of Incidents")
plt.ylabel("Location")
sns.despine()
plt.grid(axis="x", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.savefig("top_intersections.png", dpi=300)

plt.show()