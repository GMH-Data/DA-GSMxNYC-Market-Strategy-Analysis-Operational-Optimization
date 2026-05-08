import nbformat as nbf
import os

def update_1_2_c_d_final():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # --- 1.2.C Correlation Update ---
    code_c = """# 1.2.C Correlation Analysis: Uber, Lyft & Taxi
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 1. Query for operational factors
query_c = \"\"\"
SELECT 
    PULocationID,
    count(CASE WHEN hvfhs_license_num = 'HV0003' THEN 1 END) * 1.0 / count(*) as uber_market_share,
    count(CASE WHEN hvfhs_license_num = 'HV0005' THEN 1 END) * 1.0 / count(*) as lyft_market_share,
    avg(trip_miles) as avg_miles,
    avg(trip_time) / 60.0 as avg_trip_time_min,
    avg(base_passenger_fare) as avg_fare,
    avg(tips) as avg_tips,
    avg(driver_pay) as avg_driver_pay
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1 HAVING count(*) > 100
\"\"\"
df_corr = con.execute(query_c).df()

# 2. Print the correlation matrix as requested
print(\"\\n--- DETAILED CORRELATION MATRIX ---\")
corr_matrix = df_corr.drop(columns=['PULocationID']).corr()
display(corr_matrix.round(3))

# 3. Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
sns.heatmap(corr_matrix[['uber_market_share']].sort_values('uber_market_share', ascending=False), annot=True, cmap='RdBu', ax=ax1, center=0)
ax1.set_title('Uber Market Share Correlation')
sns.heatmap(corr_matrix[['lyft_market_share']].sort_values('lyft_market_share', ascending=False), annot=True, cmap='RdBu', ax=ax2, center=0)
ax2.set_title('Lyft Market Share Correlation')
plt.show()"""

    # --- 1.2.D Competition Update ---
    code_d = """# 1.2.D Competition Analysis: Uber vs Lyft Detailed Visualizations
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import json
import pandas as pd

# 1. Part 1: Growth Velocity Maps (2024 vs 2023)
query_growth = \"\"\"
WITH YearlyStats AS (
    SELECT PULocationID, hvfhs_license_num, year(pickup_datetime) as yr, count(*) as trips
    FROM fhvhv_2019_2025_cleaned WHERE year(pickup_datetime) IN (2023, 2024) AND hvfhs_license_num IN ('HV0003', 'HV0005')
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
       ((lyft_24 - lyft_23) * 100.0 / NULLIF(lyft_23, 0)) as lyft_growth
FROM PivotStats
\"\"\"
df_growth = con.execute(query_growth).df()
gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')
gdf['LocationID'] = gdf['LocationID'].astype(int)
gdf_merged = gdf.merge(df_growth, left_on='LocationID', right_on='PULocationID', how='left')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
gdf_merged.plot(column='uber_growth', ax=ax1, cmap='RdYlGn', legend=True, vmin=-20, vmax=20)
ax1.set_title('Uber Growth Speed (2024 vs 2023)')
gdf_merged.plot(column='lyft_growth', ax=ax2, cmap='RdYlGn', legend=True, vmin=-20, vmax=20)
ax2.set_title('Lyft Growth Speed (2024 vs 2023)')
plt.show()

# 2. Part 2: Interactive Competition Heatmap (Market Share)
query_share = \"\"\"
SELECT PULocationID, count(CASE WHEN hvfhs_license_num = 'HV0003' THEN 1 END) * 100.0 / count(*) as uber_share
FROM fhvhv_2019_2025_cleaned WHERE year(pickup_datetime) BETWEEN 2019 AND 2025 GROUP BY 1
\"\"\"
df_share = con.execute(query_share).df()
geojson = json.loads(gdf.to_crs(epsg=4326).to_json())
fig_map = px.choropleth_mapbox(df_share, geojson=geojson, locations='PULocationID', featureidkey=\"properties.LocationID\",
                               color='uber_share', color_continuous_scale=\"Viridis\", mapbox_style=\"carto-positron\",
                               zoom=9, center={\"lat\": 40.7128, \"lon\": -74.0060}, opacity=0.6,
                               title='Market Share Dominance (Uber %)')
fig_map.show()

# 3. Part 3: Top 10 Zones by Revenue
query_rev = \"\"\"
SELECT 
    PULocationID,
    sum(base_passenger_fare) as total_revenue,
    sum(CASE WHEN hvfhs_license_num = 'HV0003' THEN base_passenger_fare ELSE 0 END) as uber_revenue,
    sum(CASE WHEN hvfhs_license_num = 'HV0005' THEN base_passenger_fare ELSE 0 END) as lyft_revenue
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1 ORDER BY 2 DESC LIMIT 10
\"\"\"
df_rev = con.execute(query_rev).df()
df_rev = df_rev.merge(gdf[['LocationID', 'zone']], left_on='PULocationID', right_on='LocationID')
df_rev['uber_rev_share_pct'] = (df_rev['uber_revenue'] / df_rev['total_revenue']) * 100
df_rev['lyft_rev_share_pct'] = (df_rev['lyft_revenue'] / df_rev['total_revenue']) * 100

print(\"\\n--- TOP 10 ZONES BY REVENUE & MARKET SHARE BREAKDOWN ---\")
display(df_rev[['zone', 'total_revenue', 'uber_revenue', 'lyft_revenue', 'uber_rev_share_pct', 'lyft_rev_share_pct']].style.format({
    'total_revenue': '${:,.0f}', 'uber_revenue': '${:,.0f}', 'lyft_revenue': '${:,.0f}',
    'uber_rev_share_pct': '{:.2f}%', 'lyft_rev_share_pct': '{:.2f}%'
}))"""

    for cell in nb.cells:
        if cell.cell_type == 'code':
            if '# 1.2.C' in cell.source: cell.source = code_c
            if '# 1.2.D' in cell.source: cell.source = code_d

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Sections 1.2.C and 1.2.D updated with revenue and matrix displays.")

if __name__ == "__main__":
    update_1_2_c_d_final()
