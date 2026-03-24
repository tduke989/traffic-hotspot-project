import json
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib as plt
import seaborn as sns


# -----------------------------
# 1. Load data
# -----------------------------
incidents = pd.read_csv("cleaned.csv")
wards = gpd.read_file("Ward_Boundaries_20260310.geojson")

# -----------------------------
# 2. Convert incident points
# -----------------------------
incidents_gdf = gpd.GeoDataFrame(
    incidents,
    geometry=gpd.points_from_xy(
        incidents["Longitude"],
        incidents["Latitude"]
    ),
    crs="EPSG:4326"
)

# -----------------------------
# 3. Ensure same CRS
# -----------------------------
wards = wards.to_crs("EPSG:4326")

# -----------------------------
# 4. Spatial join (point → ward)
# -----------------------------
joined = gpd.sjoin(
    incidents_gdf,
    wards[["ward_num", "label", "geometry"]],
    how="left",
    predicate="within"
)

# -----------------------------
# 5. Aggregate incidents per ward
# -----------------------------
ward_summary = (
    joined.groupby(["ward_num", "label"], dropna=False)["Count"]
    .sum()
    .reset_index()
)

# ensure ward numbers match geojson type
ward_summary["ward_num"] = ward_summary["ward_num"].astype(str)
wards["ward_num"] = wards["ward_num"].astype(str)

# include wards with zero incidents
ward_summary = (
    wards[["ward_num", "label"]]
    .merge(ward_summary, on=["ward_num", "label"], how="left")
    .fillna({"Count": 0})
)

# -----------------------------
# 6. Load geojson for Plotly
# -----------------------------
with open("Ward_Boundaries_20260310.geojson") as f:
    ward_geojson = json.load(f)

# -----------------------------
# 7. Create choropleth map
# -----------------------------
fig = px.choropleth_mapbox(
    ward_summary,
    geojson=ward_geojson,
    locations="ward_num",
    featureidkey="properties.ward_num",
    color="Count",
    hover_name="label",
    hover_data={"Count": True},
    color_continuous_scale="YlOrRd",
    mapbox_style="open-street-map",
    zoom=9.5,
    center={"lat": 51.0447, "lon": -114.0719},
    title="Traffic Incidents by Ward"
)

# nicer borders
fig.update_traces(
    marker_line_width=1.5,
    marker_line_color="black",
    marker_opacity=0.62
)

# layout adjustments
fig.update_layout(
    height=800,
    margin={"r":0, "t":50, "l":0, "b":0}
)

# -----------------------------
# 8. Show map
# -----------------------------
fig.show(renderer="browser")

