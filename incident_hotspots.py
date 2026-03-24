import pandas as pd
import folium
from folium.plugins import HeatMap

# Load data
df = pd.read_csv("Traffic_Incidents_filtered_2020.csv")

# Convert date
df["START_DT"] = pd.to_datetime(df["START_DT"], errors="coerce")

# FILTER LAST 5 YEARS (2021–2026)
df = df[(df["START_DT"].dt.year >= 2021) & (df["START_DT"].dt.year <= 2026)]

# Remove missing coords
df = df.dropna(subset=["Latitude", "Longitude"])

# Round coordinates
df["lat_round"] = df["Latitude"].round(4)
df["lon_round"] = df["Longitude"].round(4)

location_counts = (
    df.groupby(["lat_round", "lon_round"])
    .size()
    .reset_index(name="incident_count")
)

# Create base map
calgary_map = folium.Map(
    location=[51.0447, -114.0719],
    zoom_start=11,
    tiles="cartodbpositron"
)

# -------- ALL INCIDENTS --------
all_data = df[["Latitude", "Longitude"]].values.tolist()

all_layer = folium.FeatureGroup(name="All Incidents")

HeatMap(all_data, radius=8, blur=6).add_to(all_layer)
all_layer.add_to(calgary_map)

# -------- 50+ HOTSPOTS --------
hotspots50 = location_counts[location_counts["incident_count"] >= 50]

heat50 = [
    [row["lat_round"], row["lon_round"], row["incident_count"]]
    for _, row in hotspots50.iterrows()
]

layer50 = folium.FeatureGroup(name="50+ Incident Hotspots")
HeatMap(heat50, radius=16, blur=12).add_to(layer50)
layer50.add_to(calgary_map)

# -------- 150+ HOTSPOTS --------
hotspots150 = location_counts[location_counts["incident_count"] >= 150]

heat150 = [
    [row["lat_round"], row["lon_round"], row["incident_count"]]
    for _, row in hotspots150.iterrows()
]

layer150 = folium.FeatureGroup(name="150+ Incident Hotspots")
HeatMap(heat150, radius=18, blur=14).add_to(layer150)
layer150.add_to(calgary_map)

# -------- TOP 10 --------
top10 = location_counts.sort_values(
    "incident_count", ascending=False
).head(10)

top_layer = folium.FeatureGroup(name="Top 10 Intersections")

for _, row in top10.iterrows():
    folium.CircleMarker(
        location=[row["lat_round"], row["lon_round"]],
        radius=10,
        color="red",
        fill=True,
        fill_color="red",
        popup=f"Incidents: {row['incident_count']}"
    ).add_to(top_layer)

top_layer.add_to(calgary_map)

# Layer control
folium.LayerControl().add_to(calgary_map)

# Save map
calgary_map.save("calgary_incident_interactive_map.html")

print("Interactive map created!")