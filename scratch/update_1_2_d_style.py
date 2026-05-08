import nbformat as nbf
import os

def update_1_2_d_style_to_match_1_1_c():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    new_code_1_2_d = """# 1.2.D Competition Analysis: Uber vs Lyft Detailed Visualizations
import geopandas as gpd
import plotly.express as px
import json
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 1. Data Preparation (Growth & Revenue)
query_d = \"\"\"
WITH YearlyStats AS (
    SELECT PULocationID, hvfhs_license_num, year(pickup_datetime) as yr, 
           count(*) as trips, sum(base_passenger_fare) as revenue
    FROM fhvhv_2019_2025_cleaned WHERE year(pickup_datetime) IN (2023, 2024) AND hvfhs_license_num IN ('HV0003', 'HV0005')
    GROUP BY 1, 2, 3
),
PivotStats AS (
    SELECT PULocationID,
           MAX(CASE WHEN hvfhs_license_num = 'HV0003' AND yr = 2023 THEN trips END) as uber_trips_23,
           MAX(CASE WHEN hvfhs_license_num = 'HV0003' AND yr = 2024 THEN trips END) as uber_trips_24,
           MAX(CASE WHEN hvfhs_license_num = 'HV0005' AND yr = 2023 THEN trips END) as lyft_trips_23,
           MAX(CASE WHEN hvfhs_license_num = 'HV0005' AND yr = 2024 THEN trips END) as lyft_trips_24,
           SUM(revenue) as total_rev_23_24
    FROM YearlyStats GROUP BY 1
)
SELECT PULocationID, 
       ((uber_trips_24 - uber_trips_23) * 100.0 / NULLIF(uber_trips_23, 0)) as uber_growth,
       ((lyft_trips_24 - lyft_trips_23) * 100.0 / NULLIF(lyft_trips_23, 0)) as lyft_growth,
       (uber_trips_24 * 100.0 / NULLIF(uber_trips_24 + lyft_trips_24, 0)) as uber_share_24
FROM PivotStats
\"\"\"
df_metrics = con.execute(query_d).df()

# 2. Load Geometry & Merge
gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')
gdf['LocationID'] = gdf['LocationID'].astype(int)
merged_gdf = gdf.merge(df_metrics, left_on='LocationID', right_on='PULocationID', how='left')
geojson = json.loads(merged_gdf.to_json())

# 3. Visualization 1: Interactive Growth Map (Style matching 1.1.C)
# We show Uber Growth as primary example, you can switch or see both in hover
fig_growth = px.choropleth(
    merged_gdf, geojson=geojson, locations=merged_gdf.index,
    color='uber_growth', color_continuous_scale=\"RdYlGn\",
    range_color=[-30, 30],
    title='Uber Strategic Growth Velocity (2024 vs 2023)',
    labels={'uber_growth': 'Growth %'},
    hover_data=['zone', 'Borough', 'uber_growth', 'lyft_growth']
)
fig_growth.update_geos(fitbounds=\"locations\", visible=False)
fig_growth.update_layout(margin={\"r\":0,\"t\":50,\"l\":0,\"b\":0}, template='plotly_white')
fig_growth.show()

# 4. Visualization 2: Competition Share Map (Style matching 1.1.C)
fig_share = px.choropleth(
    merged_gdf, geojson=geojson, locations=merged_gdf.index,
    color='uber_share_24', color_continuous_scale=\"RdBu\",
    range_color=[0, 100],
    title='Market Competition: Uber Dominance % (2024)',
    labels={'uber_share_24': 'Uber Share %'},
    hover_data=['zone', 'Borough', 'uber_share_24']
)
fig_share.update_geos(fitbounds=\"locations\", visible=False)
fig_share.update_layout(margin={\"r\":0,\"t\":50,\"l\":0,\"b\":0}, template='plotly_white')
fig_share.show()

# 5. Visualization 3: Top 10 Revenue Zones (Bar Chart styled like 1.1.C)
query_rev = \"\"\"
SELECT PULocationID, sum(base_passenger_fare) as total_revenue,
       sum(CASE WHEN hvfhs_license_num = 'HV0003' THEN base_passenger_fare ELSE 0 END) as uber_revenue,
       sum(CASE WHEN hvfhs_license_num = 'HV0005' THEN base_passenger_fare ELSE 0 END) as lyft_revenue
FROM fhvhv_2019_2025_cleaned WHERE year(pickup_datetime) BETWEEN 2019 AND 2025 GROUP BY 1 ORDER BY 2 DESC LIMIT 10
\"\"\"
df_rev = con.execute(query_rev).df().merge(gdf[['LocationID', 'zone', 'Borough']], left_on='PULocationID', right_on='LocationID')
df_rev['uber_rev_share'] = (df_rev['uber_revenue'] / df_rev['total_revenue']) * 100

fig_bar = px.bar(df_rev, x='zone', y='total_revenue', color='Borough',
             title='Top 10 High-Revenue Zones by Borough',
             labels={'total_revenue': 'Total Revenue ($)', 'zone': 'Taxi Zone'},
             hover_data=['uber_rev_share'])
fig_bar.update_layout(template='plotly_white', xaxis_tickangle=-45)
fig_bar.show()"""

    for cell in nb.cells:
        if cell.cell_type == 'code' and '# 1.2.D' in cell.source:
            cell.source = new_code_1_2_d
            break
            
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Updated 1.2.D style to match 1.1.C (Choropleth + Borough-colored bars).")

if __name__ == "__main__":
    update_1_2_d_style_to_match_1_1_c()
