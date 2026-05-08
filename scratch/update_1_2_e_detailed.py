import nbformat as nbf
import os

def update_1_2_e_temporal_detailed():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    temporal_detailed_code = """# 1.2.E Temporal Competition Analysis: Peaks by Hour and Month
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

# 1. Query: Trips by Hour and Day of Week (2019-2025)
query_temporal = \"\"\"
SELECT 
    hour(pickup_datetime) as hr,
    dayofweek(pickup_datetime) as dow,
    count(*) as total_trips
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1, 2
\"\"\"
df_temporal = con.execute(query_temporal).df()

# Mapping day names and sorting
dow_map = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
df_temporal['day_name'] = df_temporal['dow'].map(dow_map)
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# 2. Visualization 1: Heatmap (The "Where" of Time)
df_pivot = df_temporal.pivot(index='day_name', columns='hr', values='total_trips').reindex(day_order)

fig1 = px.imshow(df_pivot, 
                labels=dict(x="Hour of Day", y="Day of Week", color="Competition Density (Trips)"),
                x=list(range(24)),
                y=day_order,
                color_continuous_scale='Turbo', # High contrast for peaks
                title='Peak Competition Heatmap: Hour vs Day of Week (2019-2025)')
fig1.update_xaxes(side="top", dtick=1)
fig1.show()

# 3. Visualization 2: Hourly Trends per Day (Line Chart)
fig2 = px.line(df_temporal.sort_values(['dow', 'hr']), x='hr', y='total_trips', color='day_name',
              category_orders={"day_name": day_order},
              title='Hourly Competition Trends: Weekdays vs. Weekends',
              labels={'hr': 'Hour (0-23)', 'total_trips': 'Total Trips', 'day_name': 'Day'},
              line_shape='spline', render_mode='svg')
fig2.update_layout(xaxis=dict(tickmode='linear', dtick=1), template='plotly_white')
fig2.show()

# 4. Summary Table: Peak Hours for Each Day
print(\"\\n--- PEAK COMPETITION HOURS BY DAY OF THE WEEK ---\")
peak_hours = df_temporal.loc[df_temporal.groupby('day_name')['total_trips'].idxmax()]
display(peak_hours.sort_values('dow')[['day_name', 'hr', 'total_trips']].rename(columns={'hr': 'Peak Hour', 'total_trips': 'Max Trips'}).reset_index(drop=True))

# 5. Insights
print(\"\\n--- STRATEGIC OBSERVATION ---\")
print(\"Note: Weekend peaks (Sat-Sun) usually shift to late night (0h-3h), while Weekday peaks focus on 17h-19h (Rush hour).\")"""

    for cell in nb.cells:
        if cell.cell_type == 'code' and ('# 1.2.E' in cell.source or 'Temporal Competition Analysis' in cell.source):
            cell.source = temporal_detailed_code
            break
            
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Section 1.2.E updated with detailed hourly/weekly peak analysis.")

if __name__ == "__main__":
    update_1_2_e_temporal_detailed()
