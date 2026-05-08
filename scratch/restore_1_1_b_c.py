import nbformat as nbf
import os

def restore_1_1_b_c():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Define the code for 1.1.B
    code_b = """# 1.1.B Market Growth Rate Analysis (2016-2018)
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- DATA PROCESSING ---
# Assuming df_full was created in 1.1.A
df_table = df_full.copy()
df_table['month_str'] = df_table['month'].dt.strftime('%Y-%m')
df_table = df_table.sort_values(['type', 'month'])
df_table['growth_pct'] = df_table.groupby('type')['trip_count'].pct_change() * 100

# Fix for FHV early data
df_table.loc[(df_table['type'] == 'FHV') & (df_table['month'] <= '2017-06-01'), 'growth_pct'] = 0

df_monthly_growth_rate_pct = df_table.pivot(index='month_str', columns='type', values='growth_pct').fillna(0).round(2)

# Calculate Stats
stats_df = pd.DataFrame({
    'FHV': [df_monthly_growth_rate_pct.loc[df_monthly_growth_rate_pct['FHV'] != 0, 'FHV'].mean(), 
            df_monthly_growth_rate_pct.loc[df_monthly_growth_rate_pct['FHV'] != 0, 'FHV'].median()],
    'Green': [df_monthly_growth_rate_pct['Green'].mean(), df_monthly_growth_rate_pct['Green'].median()],
    'Yellow': [df_monthly_growth_rate_pct['Yellow'].mean(), df_monthly_growth_rate_pct['Yellow'].median()]
}, index=['MEAN (%)', 'MEDIAN (%)'])

print("\\n--- 1.1.B GROWTH STATISTICS SUMMARY (2016-2018) ---")
display(stats_df.round(2))

df_display = pd.concat([df_monthly_growth_rate_pct, stats_df.round(2)])
print("\\n--- 1.1.B DETAILED MONTHLY GROWTH RATE TABLE ---")
display(df_display.tail(15))

# Visualizations
fig_b = go.Figure()
fig_b.add_trace(go.Scatter(x=df_monthly_growth_rate_pct.index, y=df_monthly_growth_rate_pct['Yellow'], name='Yellow Taxi', line=dict(color='#f7d117')))
fig_b.add_trace(go.Scatter(x=df_monthly_growth_rate_pct.index, y=df_monthly_growth_rate_pct['Green'], name='Green Taxi', line=dict(color='#2b9c3b')))
fig_b.add_trace(go.Scatter(x=df_monthly_growth_rate_pct.index, y=df_monthly_growth_rate_pct['FHV'], name='FHV', line=dict(color='#555555')))
fig_b.update_layout(title='Monthly Growth Rate (%) Trends (2016-2018)', template='plotly_white')
fig_b.show()"""

    # Define the code for 1.1.C
    code_c = """# 1.1.C Pre-2019 Location Analysis
query_c = \"\"\"
SELECT 
    z.Borough,
    z.Zone,
    count(*) as total_trips
FROM (
    SELECT PULocationID FROM yellow_Pre_2019_cleaned
    UNION ALL
    SELECT PULocationID FROM green_Pre_2019_cleaned
    UNION ALL
    SELECT PUlocationID as PULocationID FROM fhv_Pre_2019_cleaned
) t
JOIN taxi_zone_lookup z ON t.PULocationID = z.LocationID
GROUP BY 1, 2
ORDER BY 3 DESC
LIMIT 10
\"\"\"
df_zones = con.execute(query_c).df()

import plotly.express as px
fig_c = px.bar(df_zones, x='Zone', y='total_trips', color='Borough',
             title='Top 10 Pickup Zones (All Services, Pre-2019)',
             labels={'total_trips': 'Total Trips', 'Zone': 'Taxi Zone'})
fig_c.update_layout(template='plotly_white', xaxis_tickangle=-45)
fig_c.show()"""

    # Insert cells
    idx_b = -1
    idx_c = -1
    
    for i, cell in enumerate(nb.cells):
        if '### B. Market Growth Rate Analysis' in cell.source:
            idx_b = i
        if '### C. Pre-2019 Location Analysis' in cell.source:
            idx_c = i

    # Important: Insert from bottom to top or adjust indices
    if idx_c != -1:
        nb.cells.insert(idx_c + 1, nbf.v4.new_code_cell(code_c))
        print(f"Restored code for 1.1.C at index {idx_c + 1}")
    
    # Re-find idx_b because the insertion above might have shifted it
    for i, cell in enumerate(nb.cells):
        if '### B. Market Growth Rate Analysis' in cell.source:
            idx_b = i
            break
            
    if idx_b != -1:
        nb.cells.insert(idx_b + 1, nbf.v4.new_code_cell(code_b))
        print(f"Restored code for 1.1.B at index {idx_b + 1}")

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Notebook restored successfully.")

if __name__ == "__main__":
    restore_1_1_b_c()
