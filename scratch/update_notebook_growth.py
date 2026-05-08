import nbformat as nbf
import os

def update_1_2_d_with_growth_map():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    growth_code = """# 1.2.D Strategic Expansion Analysis: Uber vs Lyft Growth Velocity (2024 vs 2023)
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

# 1. Query Growth Data per Zone
query_growth = \"\"\"
WITH YearlyStats AS (
    SELECT 
        PULocationID,
        hvfhs_license_num,
        year(pickup_datetime) as yr,
        count(*) as trips
    FROM fhvhv_2019_2025_cleaned
    WHERE year(pickup_datetime) IN (2023, 2024)
      AND hvfhs_license_num IN ('HV0003', 'HV0005')
    GROUP BY 1, 2, 3
),
PivotStats AS (
    SELECT 
        PULocationID,
        MAX(CASE WHEN hvfhs_license_num = 'HV0003' AND yr = 2023 THEN trips END) as uber_23,
        MAX(CASE WHEN hvfhs_license_num = 'HV0003' AND yr = 2024 THEN trips END) as uber_24,
        MAX(CASE WHEN hvfhs_license_num = 'HV0005' AND yr = 2023 THEN trips END) as lyft_23,
        MAX(CASE WHEN hvfhs_license_num = 'HV0005' AND yr = 2024 THEN trips END) as lyft_24
    FROM YearlyStats
    GROUP BY 1
)
SELECT 
    PULocationID,
    ((uber_24 - uber_23) * 100.0 / NULLIF(uber_23, 0)) as uber_growth,
    ((lyft_24 - lyft_23) * 100.0 / NULLIF(lyft_23, 0)) as lyft_growth
FROM PivotStats
\"\"\"
df_growth = con.execute(query_growth).df()

# 2. Load Map and Join
gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')
gdf['LocationID'] = gdf['LocationID'].astype(int)
gdf_merged = gdf.merge(df_growth, left_on='LocationID', right_on='PULocationID', how='left')

# 3. Plot Growth Velocity (Side by Side)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(22, 11))

# Uber Growth Map
gdf_merged.plot(column='uber_growth', ax=ax1, cmap='RdYlGn', legend=True,
                vmin=-20, vmax=20, # Normalize scale to see relative expansion
                legend_kwds={'label': "Uber Growth Velocity (%)", 'orientation': "horizontal"})
ax1.set_title('Uber: Strategic Expansion Areas (2024 vs 2023)', fontsize=16, fontweight='bold')
ax1.set_axis_off()

# Lyft Growth Map
gdf_merged.plot(column='lyft_growth', ax=ax2, cmap='RdYlGn', legend=True,
                vmin=-20, vmax=20,
                legend_kwds={'label': "Lyft Growth Velocity (%)", 'orientation': "horizontal"})
ax2.set_title('Lyft: Strategic Expansion Areas (2024 vs 2023)', fontsize=16, fontweight='bold')
ax2.set_axis_off()

plt.tight_layout()
plt.show()

# 4. Insights: Top Expansion Zones
print("\\n--- TOP 5 FASTEST GROWING ZONES FOR UBER ---")
display(gdf_merged.sort_values('uber_growth', ascending=False).head(5)[['zone', 'uber_growth']])

print("\\n--- TOP 5 FASTEST GROWING ZONES FOR LYFT ---")
display(gdf_merged.sort_values('lyft_growth', ascending=False).head(5)[['zone', 'lyft_growth']])"""

    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and ('# 1.2.D' in cell.source or 'Competition Analysis: Uber vs Lyft Detailed' in cell.source):
            cell.source = growth_code
            found = True
            break
            
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Updated section 1.2.D with Growth Velocity maps.")
    else:
        print("Target cell for 1.2.D not found.")

if __name__ == "__main__":
    update_1_2_d_with_growth_map()
