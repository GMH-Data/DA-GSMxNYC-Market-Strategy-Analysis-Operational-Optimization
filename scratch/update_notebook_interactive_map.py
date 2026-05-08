import nbformat as nbf
import os

def update_1_2_c_with_interactive_map():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    interactive_map_code = """# 1.2.C Competition Areas Visualization (Uber vs Lyft) - Interactive Map
import geopandas as gpd
import plotly.express as px
import json

# 1. Query trip data for all zones
query_map = \"\"\"
SELECT 
    PULocationID,
    count(CASE WHEN hvfhs_license_num = 'HV0003' THEN 1 END) as uber_trips,
    count(CASE WHEN hvfhs_license_num = 'HV0005' THEN 1 END) as lyft_trips,
    count(*) as total_trips
FROM fhvhv_2019_2025_cleaned
WHERE hvfhs_license_num IN ('HV0003', 'HV0005')
  AND year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1
\"\"\"
df_map = con.execute(query_map).df()

# 2. Calculate Uber's Market Share (%) and Enriched Data
df_map['uber_share'] = (df_map['uber_trips'] / df_map['total_trips']) * 100
df_map['lyft_share'] = 100 - df_map['uber_share']

# 3. Load NYC Taxi Zones and Convert to GeoJSON for Plotly
gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')
gdf = gdf.to_crs(epsg=4321) # Convert to standard lat/lon
gdf['LocationID'] = gdf['LocationID'].astype(int)

# Merge to get zone names for hover info
df_map = df_map.merge(gdf[['LocationID', 'zone']], left_on='PULocationID', right_on='LocationID').drop(columns=['LocationID'])

# Convert GeoDataFrame to GeoJSON format
geojson = json.loads(gdf.to_json())

# 4. Create Interactive Choropleth Map using Plotly
fig = px.choropleth_mapbox(df_map, 
                           geojson=geojson, 
                           locations='PULocationID', 
                           featureidkey="properties.LocationID",
                           color='uber_share',
                           color_continuous_scale="RdBu", # Red for Lyft, Blue for Uber (Standard political/competition colors)
                           range_color=[0, 100],
                           mapbox_style="carto-positron",
                           zoom=9, 
                           center = {"lat": 40.7128, "lon": -74.0060},
                           opacity=0.6,
                           hover_name='zone',
                           hover_data={
                               'PULocationID': False,
                               'uber_trips': ':,',
                               'lyft_trips': ':,',
                               'uber_share': ':.2f'
                           },
                           labels={
                               'uber_share': 'Uber Share (%)',
                               'uber_trips': 'Uber Trips',
                               'lyft_trips': 'Lyft Trips'
                           },
                           title='Interactive Competition Map: Uber vs Lyft Market Share (2019-2025)')

fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig.show()

# Quick Insight: Most Contested Zones
df_map['competition_index'] = abs(df_map['uber_share'] - 50)
print("\\n--- TOP 5 MOST CONTESTED ZONES (Near 50/50 split) ---")
display(df_map.sort_values('competition_index').head(5)[['zone', 'uber_share', 'total_trips']])"""

    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and '# 1.2.C Competition Areas' in cell.source:
            cell.source = interactive_map_code
            found = True
            break
    
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Updated section 1.2.C with Plotly interactive map.")
    else:
        print("Could not find the target code cell.")

if __name__ == "__main__":
    update_1_2_c_with_interactive_map()
