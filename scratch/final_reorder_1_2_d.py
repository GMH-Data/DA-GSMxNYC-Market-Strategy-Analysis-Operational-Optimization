import nbformat as nbf
import os

def update_1_2_d_final_structure():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    final_code_1_2_d = """# 1.2.D Competition Analysis: Uber vs Lyft Detailed Visualizations
import geopandas as gpd
import plotly.express as px
import json
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 1. Data Preparation (Growth & Competition)
query_d = '''
WITH YearlyStats AS (
    SELECT PULocationID, hvfhs_license_num, year(pickup_datetime) as yr, count(*) as trips
    FROM fhvhv_2019_2025_cleaned 
    WHERE year(pickup_datetime) IN (2023, 2024) AND hvfhs_license_num IN ('HV0003', 'HV0005')
    GROUP BY 1, 2, 3
),
PivotStats AS (
    SELECT PULocationID,
           MAX(CASE WHEN hvfhs_license_num = 'HV0003' AND yr = 2023 THEN trips END) as uber_23,
           MAX(CASE WHEN hvfhs_license_num = 'HV0003' AND yr = 2024 THEN trips END) as uber_24,
           MAX(CASE WHEN hvfhs_license_num = 'HV0005' AND yr = 2023 THEN trips END) as lyft_23,
           MAX(CASE WHEN hvfhs_license_num = 'HV0005' AND yr = 2024 THEN trips END) as lyft_24
    FROM YearlyStats GROUP BY 1
)
SELECT PULocationID, 
       ((uber_24 - uber_23) * 100.0 / NULLIF(uber_23, 0)) as uber_growth,
       ((lyft_24 - lyft_23) * 100.0 / NULLIF(lyft_23, 0)) as lyft_growth,
       (uber_24 * 100.0 / NULLIF(uber_24 + lyft_24, 0)) as uber_share
FROM PivotStats
'''
df_metrics = con.execute(query_d).df()

# 2. Geometry Setup
gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')
gdf['LocationID'] = gdf['LocationID'].astype(int)
merged_gdf = gdf.merge(df_metrics, left_on='LocationID', right_on='PULocationID', how='left')
geojson = json.loads(merged_gdf.to_json())

# --- PART 1: TWO SIMPLE GROWTH MAPS (Uber & Lyft) ---
# Uber Growth Map
fig_uber = px.choropleth(merged_gdf, geojson=geojson, locations=merged_gdf.index,
                         color='uber_growth', color_continuous_scale="RdYlGn", range_color=[-20, 20],
                         title='Uber Development Velocity (2024 vs 2023)',
                         labels={'uber_growth': 'Growth %'}, hover_data=['zone', 'borough', 'uber_growth'])
fig_uber.update_geos(fitbounds="locations", visible=False)
fig_uber.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template='plotly_white')
fig_uber.show()

# Lyft Growth Map
fig_lyft = px.choropleth(merged_gdf, geojson=geojson, locations=merged_gdf.index,
                         color='lyft_growth', color_continuous_scale="RdYlGn", range_color=[-20, 20],
                         title='Lyft Development Velocity (2024 vs 2023)',
                         labels={'lyft_growth': 'Growth %'}, hover_data=['zone', 'borough', 'lyft_growth'])
fig_lyft.update_geos(fitbounds="locations", visible=False)
fig_lyft.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template='plotly_white')
fig_lyft.show()

# --- PART 2: TOP 5 STRATEGIC EXPANSION ZONES ---
print("\\n--- TOP 5 FASTEST DEVELOPING ZONES BY PROVIDER ---")
top_uber = merged_gdf.sort_values('uber_growth', ascending=False).head(5)[['zone', 'borough', 'uber_growth']]
top_lyft = merged_gdf.sort_values('lyft_growth', ascending=False).head(5)[['zone', 'borough', 'lyft_growth']]

print("\\n[UBER EXPANSION PEAKS]")
display(top_uber.style.format({'uber_growth': '{:.2f}%'}))
print("\\n[LYFT EXPANSION PEAKS]")
display(top_lyft.style.format({'lyft_growth': '{:.2f}%'}))

# --- PART 3: COMPETITION MAP (1.1.C STYLE) ---
fig_comp = px.choropleth(merged_gdf, geojson=geojson, locations=merged_gdf.index,
                         color='uber_share', color_continuous_scale="RdBu", range_color=[0, 100],
                         title='Market Competition: Uber vs Lyft Share % (2024 Style matching 1.1.C)',
                         labels={'uber_share': 'Uber Market Share %'}, hover_data=['zone', 'borough', 'uber_share'])
fig_comp.update_geos(fitbounds="locations", visible=False)
fig_comp.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template='plotly_white')
fig_comp.show()"""

    for cell in nb.cells:
        if cell.cell_type == 'code' and '# 1.2.D' in cell.source:
            cell.source = final_code_1_2_d
            break
            
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Section 1.2.D updated successfully.")

if __name__ == "__main__":
    update_1_2_d_final_structure()
