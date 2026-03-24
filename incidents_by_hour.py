import pandas as pd
import matplotlib.pyplot as plt

# Load CLEAN dataset
df = pd.read_csv("Traffic_Incidents_filtered_2020.csv")

# Convert date
df["START_DT"] = pd.to_datetime(df["START_DT"], errors="coerce")

# FILTER 2021–2026
df = df[(df["START_DT"].dt.year >= 2021) & (df["START_DT"].dt.year <= 2026)]

# Extract hour
df["hour"] = df["START_DT"].dt.hour

# Count incidents per hour
hour_counts = df["hour"].value_counts().sort_index()

plt.figure(figsize=(10,5))

plt.plot(hour_counts.index, hour_counts.values, marker="o")

plt.title("Traffic Incidents by Hour (2021–2026)")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Incidents")

plt.xticks(range(0,24))

plt.tight_layout()
plt.savefig("incidents_by_hour.png", dpi=300)

plt.show()