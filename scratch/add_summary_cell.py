import nbformat as nbf
import os

def add_market_share_summary_cell():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    summary_code = """# 1.2.D.2 Market Share Summary & Top 10 High-Volume Zones
import json
import plotly.express as px
import pandas as pd

# 1. Query for overall market share per zone (2019-2025)
query_sum = \"\"\"
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
df_sum = con.execute(query_sum).df()
df_sum['uber_pct'] = (df_sum['uber_trips'] / df_sum['total_trips']) * 100
df_sum['lyft_pct'] = (df_sum['lyft_trips'] / df_sum['total_trips']) * 100

# 2. Large Interactive Map (Plotly)
gdf_base = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')
gdf_base['LocationID'] = gdf_base['LocationID'].astype(int)
geojson_sum = json.loads(gdf_base.to_crs(epsg=4326).to_json())

df_sum_enriched = df_sum.merge(gdf_base[['LocationID', 'zone']], left_on='PULocationID', right_on='LocationID')

fig_sum = px.choropleth_mapbox(df_sum_enriched, 
                           geojson=geojson_sum, 
                           locations='PULocationID', 
                           featureidkey="properties.LocationID",
                           color='uber_pct',
                           color_continuous_scale="Viridis",
                           range_color=[0, 100],
                           mapbox_style="carto-positron",
                           zoom=10, 
                           center = {"lat": 40.7128, "lon": -74.0060},
                           opacity=0.7,
                           hover_name='zone',
                           hover_data={'uber_pct': ':.2f', 'lyft_pct': ':.2f', 'total_trips': ':,', 'PULocationID': False},
                           labels={'uber_pct': 'Uber Share %', 'lyft_pct': 'Lyft Share %'},
                           title='Interactive Market Dominance: Uber vs Lyft Share % (Total 2019-2025)')

fig_sum.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig_sum.show()

# 3. Top 10 Zones DF with Styled Output
top_10 = df_sum_enriched.sort_values('total_trips', ascending=False).head(10)
top_10 = top_10[['zone', 'total_trips', 'uber_trips', 'lyft_trips', 'uber_pct', 'lyft_pct']]

print("\\n--- TOP 10 ZONES BY TOTAL TRIP VOLUME (Uber + Lyft) ---")
display(top_10.style.format({
    'uber_pct': '{:.2f}%', 
    'lyft_pct': '{:.2f}%', 
    'total_trips': '{:,}', 
    'uber_trips': '{:,}', 
    'lyft_trips': '{:,}'
}))"""

    new_cell = nbf.v4.new_code_cell(summary_code)
    
    # Find the position of the first 1.2.D cell to insert after it
    insert_pos = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and '# 1.2.D Strategic Expansion Analysis' in cell.source:
            insert_pos = i + 1
            break
            
    if insert_pos != -1:
        nb.cells.insert(insert_pos, new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Market share summary cell added successfully.")
    else:
        print("Could not find the Strategic Expansion cell to insert after.")

if __name__ == "__main__":
    add_market_share_summary_cell()
