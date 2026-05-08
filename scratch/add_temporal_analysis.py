import nbformat as nbf
import os

def add_temporal_competition_cell():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    temporal_code = """# 1.2.F Temporal Competition Analysis: Peaks by Hour and Month
import plotly.express as px
import pandas as pd

# 1. Query: Trips by Hour and Day of Week (Competition Density)
query_hourly = \"\"\"
SELECT 
    hour(pickup_datetime) as hr,
    dayofweek(pickup_datetime) as dow,
    count(*) as trips
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1, 2
\"\"\"
df_hourly = con.execute(query_hourly).df()

# Mapping day of week
dow_map = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
df_hourly['day_name'] = df_hourly['dow'].map(dow_map)

# Pivot for Heatmap
df_pivot_hr = df_hourly.pivot(index='day_name', columns='hr', values='trips')
# Reorder days
df_pivot_hr = df_pivot_hr.reindex(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

# 2. Query: Trips by Month (Seasonal Trends)
query_monthly = \"\"\"
SELECT 
    month(pickup_datetime) as mo,
    CASE WHEN hvfhs_license_num = 'HV0003' THEN 'Uber' ELSE 'Lyft' END as provider,
    count(*) as trips
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1, 2
\"\"\"
df_monthly = con.execute(query_monthly).df()

# 3. Visualizations
# Heatmap 1: Hourly/Weekly Density
fig1 = px.imshow(df_pivot_hr, 
                labels=dict(x="Hour of Day", y="Day of Week", color="Total Trips"),
                x=list(range(24)),
                y=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                color_continuous_scale='Viridis',
                title='Competition Density Heatmap: Peak Hours vs Day of Week (2019-2025)')
fig1.show()

# Line Chart 2: Monthly Trends
fig2 = px.line(df_monthly.sort_values('mo'), x='mo', y='trips', color='provider',
              title='Monthly Competition Trends: Seasonal Volume Comparison',
              labels={'mo': 'Month (1-12)', 'trips': 'Total Trips'},
              markers=True)
fig2.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1), template='plotly_white')
fig2.show()

# 4. Insights
print("\\n--- PEAK COMPETITION TIME SLOTS ---")
top_hr = df_hourly.sort_values('trips', ascending=False).head(3)
for _, row in top_hr.iterrows():
    print(f"Peak detected on {row['day_name']} at {row['hr']}:00 with {row['trips']:,} trips.")"""

    header_f = nbf.v4.new_markdown_cell("### F. Temporal Competition Analysis: Time of Day & Year\nPhân tích sự thay đổi của mật độ cạnh tranh theo các khung giờ trong ngày và các tháng trong năm.")
    new_cell = nbf.v4.new_code_cell(temporal_code)
    
    # Find the end of 1.2.E to insert after it
    insert_pos = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and '# 1.2.E Market Share Comparison' in cell.source:
            insert_pos = i + 1
            break
            
    if insert_pos != -1:
        nb.cells.insert(insert_pos, header_f)
        nb.cells.insert(insert_pos + 1, new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Section 1.2.F added successfully.")
    else:
        print("Could not find section 1.2.E to insert after.")

if __name__ == "__main__":
    add_temporal_competition_cell()
