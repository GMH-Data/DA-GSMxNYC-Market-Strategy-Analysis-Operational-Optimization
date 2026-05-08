import nbformat as nbf
import os

def add_peak_hours_geo_cell():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    peak_geo_code = """# 1.2.E.3 Geospatial Hotspots During Critical Peak Hours
import geopandas as gpd
import plotly.express as px
import json

# 1. Query Trip Volumes for the 3 Specific Time Windows
query_peak_geo = \"\"\"
SELECT 
    PULocationID,
    count(CASE WHEN dayofweek(pickup_datetime) BETWEEN 1 AND 5 AND hour(pickup_datetime) = 8 THEN 1 END) as morning_rush,
    count(CASE WHEN dayofweek(pickup_datetime) = 5 AND hour(pickup_datetime) BETWEEN 17 AND 23 THEN 1 END) as friday_night,
    count(CASE WHEN dayofweek(pickup_datetime) = 6 AND hour(pickup_datetime) BETWEEN 17 AND 23 THEN 1 END) as saturday_night
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1
\"\"\"
df_peaks = con.execute(query_peak_geo).df()

# 2. Geometry Setup
gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp').to_crs(epsg=4326)
gdf['LocationID'] = gdf['LocationID'].astype(int)
gdf.columns = [c.lower() for c in gdf.columns]

merged_peaks = gdf.merge(df_peaks, left_on='locationid', right_on='PULocationID', how='left').fillna(0)
geojson_peaks = json.loads(merged_peaks.to_json())

# 3. Plotting the 3 Maps
def plot_peak_map(column_name, title_text, color_scale="OrRd"):
    fig = px.choropleth(merged_peaks, geojson=geojson_peaks, locations='locationid', featureidkey='properties.locationid',
                             color=column_name, color_continuous_scale=color_scale,
                             title=title_text,
                             labels={column_name: 'Total Trips'}, hover_data=['zone', 'borough', column_name])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template='plotly_white')
    fig.show()

# Map 1: Morning Rush (Mon-Fri 8AM-9AM)
plot_peak_map('morning_rush', 'Hotspots: Morning Commute (Mon-Fri 08:00 - 08:59)', 'Blues')

# Map 2: Friday Night (Fri 5PM - Midnight)
plot_peak_map('friday_night', 'Hotspots: Friday Night out (17:00 - 23:59)', 'Purples')

# Map 3: Saturday Night (Sat 5PM - Midnight)
plot_peak_map('saturday_night', 'Hotspots: Saturday Night out (17:00 - 23:59)', 'Reds')

# 4. Top 3 Zones Printout
print("\\n--- TOP ZONES FOR EACH CRITICAL TIME WINDOW ---")
print("\\n[Morning Commute (Mon-Fri 8AM)]")
display(merged_peaks.sort_values('morning_rush', ascending=False).head(3)[['zone', 'borough', 'morning_rush']])

print("\\n[Friday Night (17:00 - Midnight)]")
display(merged_peaks.sort_values('friday_night', ascending=False).head(3)[['zone', 'borough', 'friday_night']])

print("\\n[Saturday Night (17:00 - Midnight)]")
display(merged_peaks.sort_values('saturday_night', ascending=False).head(3)[['zone', 'borough', 'saturday_night']])"""

    new_cell = nbf.v4.new_code_cell(peak_geo_code)

    insert_pos = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and '# 1.2.E.2' in cell.source:
            insert_pos = i + 1
            break

    if insert_pos == -1:
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code' and '# 1.2.E' in cell.source:
                insert_pos = i + 1

    if insert_pos != -1:
        nb.cells.insert(insert_pos, new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Added peak hours geospatial cell successfully.")
    else:
        print("Could not find section to insert after.")

if __name__ == "__main__":
    add_peak_hours_geo_cell()
