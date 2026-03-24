import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("Traffic_Incidents_20260310.csv")

# Remove rows without coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Create hotspot map
plt.figure(figsize=(9,7))

hb = plt.hexbin(
    df["Longitude"],
    df["Latitude"],
    gridsize=45,
    cmap="inferno",
    mincnt=1
)

plt.title("Calgary Traffic Incident Hotspots")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

cb = plt.colorbar(hb)
cb.set_label("Incident Density")

plt.tight_layout()

plt.savefig("hotspot_map.png", dpi=300)

plt.show()