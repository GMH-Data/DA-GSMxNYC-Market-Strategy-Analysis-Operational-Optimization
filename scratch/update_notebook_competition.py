import nbformat as nbf
import os

def update_1_2_d_competition_restructure():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    new_source = """# 1.2.D Competition Analysis: Uber vs Lyft Detailed Visualizations
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import json

# 1. Data Preparation
query = \"\"\"
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
df = con.execute(query).df()
df['uber_pct'] = (df['uber_trips'] / df['total_trips']) * 100
df['lyft_pct'] = (df['lyft_trips'] / df['total_trips']) * 100

# Load Geometry
gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')
gdf['LocationID'] = gdf['LocationID'].astype(int)
gdf_merged = gdf.merge(df, left_on='LocationID', right_on='PULocationID', how='left')

# 2. TWO SIMPLE DENSITY MAPS (Side by Side)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

gdf_merged.plot(column='uber_trips', ax=ax1, cmap='Reds', legend=True, 
                legend_kwds={'label': "Uber Trip Density", 'orientation': "horizontal"})
ax1.set_title('Uber: Concentration of Services', fontsize=15)
ax1.set_axis_off()

gdf_merged.plot(column='lyft_trips', ax=ax2, cmap='Blues', legend=True,
                legend_kwds={'label': "Lyft Trip Density", 'orientation': "horizontal"})
ax2.set_title('Lyft: Concentration of Services', fontsize=15)
ax2.set_axis_off()

plt.tight_layout()
plt.show()

# 3. LARGE INTERACTIVE COMPETITION MAP (Share %)
gdf_4326 = gdf.to_crs(epsg=4326)
geojson = json.loads(gdf_4326.to_json())

# Join zone names for hover
df_enriched = df.merge(gdf[['LocationID', 'zone']], left_on='PULocationID', right_on='LocationID')

fig_comp = px.choropleth_mapbox(df_enriched, 
                           geojson=geojson, 
                           locations='PULocationID', 
                           featureidkey="properties.LocationID",
                           color='uber_pct',
                           color_continuous_scale="RdBu", # Red for Lyft, Blue for Uber
                           range_color=[0, 100],
                           mapbox_style="carto-positron",
                           zoom=9.5, 
                           center = {"lat": 40.7128, "lon": -74.0060},
                           opacity=0.7,
                           hover_name='zone',
                           hover_data={'uber_pct': ':.2f', 'lyft_pct': ':.2f', 'total_trips': ':,', 'PULocationID': False},
                           labels={'uber_pct': 'Uber Share %', 'lyft_pct': 'Lyft Share %'},
                           title='Market Competition: Uber vs Lyft Market Share % (2019-2025)')

fig_comp.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig_comp.show()

# 4. TOP 10 ZONES BY VOLUME WITH MARKET SHARE %
top_10 = df_enriched.sort_values('total_trips', ascending=False).head(10)
top_10 = top_10[['zone', 'total_trips', 'uber_trips', 'lyft_trips', 'uber_pct', 'lyft_pct']]

print("\\n--- TOP 10 ZONES BY VOLUME & MARKET SHARE BREAKDOWN ---")
display(top_10.style.format({
    'uber_pct': '{:.2f}%', 
    'lyft_pct': '{:.2f}%', 
    'total_trips': '{:,}', 
    'uber_trips': '{:,}', 
    'lyft_trips': '{:,}'
}))"""

    found = False
    for cell in nb.cells:
        # Search for the specific header or previous content of 1.2.D
        if cell.cell_type == 'code' and '# 1.2.D Correlation Analysis' in cell.source:
             # Wait, the user said 1.2.D is Competition... but in my Select-String D was Competition.
             # I should check the source for "Competition Areas" or "Khu vực cạnh tranh"
             pass
        
        if '### D. Khu vực cạnh tranh khốc liệt' in cell.source or '# 1.2.D Correlation Analysis' in cell.source:
            # Check if this cell is code or markdown. We want to find the code cell associated with D.
            pass

    # Better approach: Iterate and find the cell by source content
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and ('# 1.2.D' in cell.source or 'Competition Areas Visualization' in cell.source):
            cell.source = new_source
            found = True
            break
            
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Updated section 1.2.D with restructured visualizations.")
    else:
        print("Target cell for 1.2.D not found.")

if __name__ == "__main__":
    update_1_2_d_competition_restructure()
