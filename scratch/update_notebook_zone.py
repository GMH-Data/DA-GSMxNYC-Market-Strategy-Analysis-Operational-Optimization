import nbformat
import os

notebook_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

new_source = """# 1.1.C Pre-2019 Location Analysis
query_c = \"\"\"
SELECT 
    PULocationID,
    count(*) as total_trips
FROM (
    SELECT PULocationID FROM yellow_Pre_2019_cleaned
    UNION ALL
    SELECT PULocationID FROM green_Pre_2019_cleaned
    UNION ALL
    SELECT PUlocationID as PULocationID FROM fhv_Pre_2019_cleaned
) t
GROUP BY 1
\"\"\"
df_zones_all = con.execute(query_c).df()

import geopandas as gpd
import plotly.express as px
import json

# Load shapefile
zones_gdf = gpd.read_file(r'Dataset/taxi_zones/taxi_zones.shp').to_crs(epsg=4326)

# Merge data
zones_gdf['LocationID'] = zones_gdf['LocationID'].astype(int)
df_zones_all['PULocationID'] = df_zones_all['PULocationID'].astype(int)
merged_gdf = zones_gdf.merge(df_zones_all, left_on='LocationID', right_on='PULocationID', how='left').fillna(0)

# Convert to GeoJSON for Plotly
geojson = json.loads(merged_gdf.to_json())

fig_map = px.choropleth(
    merged_gdf, 
    geojson=geojson, 
    locations=merged_gdf.index, 
    color='total_trips',
    color_continuous_scale="OrRd",
    title='NYC Taxi Trip Density (Pre-2019 Pickup Zones)',
    labels={'total_trips': 'Total Trips'},
    hover_data=['zone', 'borough', 'total_trips']
)

fig_map.update_geos(fitbounds="locations", visible=False)
fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0}, template='plotly_white')
fig_map.show()

# Also keep the top 10 bar chart for numerical context
df_top10 = merged_gdf.sort_values('total_trips', ascending=False).head(10)
fig_bar = px.bar(df_top10, x='zone', y='total_trips', color='borough',
             title='Top 10 Pickup Zones (Numerical View)',
             labels={'total_trips': 'Total Trips', 'zone': 'Taxi Zone'})
fig_bar.update_layout(template='plotly_white', xaxis_tickangle=-45)
fig_bar.show()"""

found = False
for cell in nb.cells:
    if cell.cell_type == 'code' and '# 1.1.C Pre-2019 Location Analysis' in cell.source:
        cell.source = new_source
        found = True
        break

if found:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Successfully updated the cell in Data.ipynb")
else:
    print("Could not find the target cell.")
