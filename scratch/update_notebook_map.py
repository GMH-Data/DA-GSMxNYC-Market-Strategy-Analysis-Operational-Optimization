import nbformat as nbf
import os

def update_1_2_c_with_map():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    map_code = """# 1.2.C Competition Areas Visualization (Uber vs Lyft) - Geospatial Analysis
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

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

# 2. Calculate Uber's Market Share (%)
df_map['uber_share'] = (df_map['uber_trips'] / df_map['total_trips']) * 100

# 3. Load NYC Taxi Zones Shapefile
shapefile_path = 'Dataset/taxi_zones/taxi_zones.shp'
gdf = gpd.read_file(shapefile_path)

# 4. Merge data with geometry
# Ensure LocationID is integer for merging
gdf['LocationID'] = gdf['LocationID'].astype(int)
gdf_merged = gdf.merge(df_map, left_on='LocationID', right_on='PULocationID', how='left')

# 5. Plotting
fig, ax = plt.subplots(1, 1, figsize=(15, 12))
gdf_merged.plot(column='uber_share', 
               ax=ax, 
               legend=True,
               cmap='RdPu', # Red-Purple: Higher share is Purple (Lyft), Lower is Red (Uber)
               missing_kwds={'color': 'lightgrey', 'label': 'No Data'},
               legend_kwds={'label': \"Uber Market Share (%)\", 'orientation': \"horizontal\"})

ax.set_title('NYC Competition Map: Uber vs Lyft Dominance (2019-2025)\\n(Darker Purple = Lyft Dominance | Darker Red = Uber Dominance)', fontsize=15)
ax.set_axis_off()

plt.tight_layout()
plt.show()

# Quick Insight: List Top 5 Most Contested Zones (closest to 50/50 share)
df_map['competition_index'] = abs(df_map['uber_share'] - 50)
contested = df_map.merge(gdf[['LocationID', 'zone']], left_on='PULocationID', right_on='LocationID')
print("\\n--- TOP 5 MOST CONTESTED ZONES (Near 50/50 split) ---")
print(contested.sort_values('competition_index').head(5)[['zone', 'uber_share', 'total_trips']])"""

    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and '# 1.2.C Competition Areas' in cell.source:
            cell.source = map_code
            found = True
            break
    
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Updated section 1.2.C with Geopandas visualization.")
    else:
        print("Could not find the target code cell for section 1.2.C.")

if __name__ == "__main__":
    update_1_2_c_with_map()
