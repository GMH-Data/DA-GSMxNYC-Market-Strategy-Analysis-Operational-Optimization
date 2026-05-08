import nbformat as nbf
import os

def add_trip_vs_revenue_share_cell():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    comparison_code = """# 1.2.E Market Share Comparison: Trip Volume vs. Total Revenue (2019-2025)
import plotly.graph_objects as go
import pandas as pd

# 1. Query metrics for all major players
query_comp = \"\"\"
WITH MarketMetrics AS (
    -- Yellow Taxi
    SELECT 'Yellow' as type, count(*) as trips, sum(fare_amount) as revenue 
    FROM yellow_2019_2025_cleaned
    UNION ALL
    -- Green Taxi
    SELECT 'Green' as type, count(*) as trips, sum(fare_amount) as revenue 
    FROM green_2019_2025_cleaned
    UNION ALL
    -- Uber
    SELECT 'Uber' as type, count(*) as trips, sum(base_passenger_fare) as revenue 
    FROM fhvhv_2019_2025_cleaned WHERE hvfhs_license_num = 'HV0003'
    UNION ALL
    -- Lyft
    SELECT 'Lyft' as type, count(*) as trips, sum(base_passenger_fare) as revenue 
    FROM fhvhv_2019_2025_cleaned WHERE hvfhs_license_num = 'HV0005'
),
Totals AS (
    SELECT sum(trips) as grand_total_trips, sum(revenue) as grand_total_revenue FROM MarketMetrics
)
SELECT 
    m.type,
    m.trips,
    m.revenue,
    (m.trips * 100.0 / t.grand_total_trips) as trip_share_pct,
    (m.revenue * 100.0 / t.grand_total_revenue) as revenue_share_pct
FROM MarketMetrics m, Totals t
\"\"\"
df_metrics = con.execute(query_comp).df()

# 2. Plotly Grouped Bar Chart
fig = go.Figure(data=[
    go.Bar(name='Trip Share (%)', x=df_metrics['type'], y=df_metrics['trip_share_pct'], 
           marker_color='#1f77b4', text=df_metrics['trip_share_pct'].round(1).astype(str) + '%', textposition='auto'),
    go.Bar(name='Revenue Share (%)', x=df_metrics['type'], y=df_metrics['revenue_share_pct'], 
           marker_color='#ff7f0e', text=df_metrics['revenue_share_pct'].round(1).astype(str) + '%', textposition='auto')
])

fig.update_layout(
    title='Market Share Comparison: Trip Volume vs. Total Revenue (2019-2025)',
    xaxis_title='Service Type',
    yaxis_title='Percentage (%)',
    barmode='group',
    template='plotly_white'
)
fig.show()

# 3. Calculation of "Revenue Efficiency Index"
# (Revenue Share / Trip Share) -> > 1 means the service earns more per trip than the market average
df_metrics['efficiency_index'] = df_metrics['revenue_share_pct'] / df_metrics['trip_share_pct']
print("\\n--- MARKET SHARE SUMMARY & REVENUE EFFICIENCY ---")
display(df_metrics[['type', 'trip_share_pct', 'revenue_share_pct', 'efficiency_index']].sort_values('efficiency_index', ascending=False))"""

    header_e = nbf.v4.new_markdown_cell("### E. Market Share Comparison: Trips vs Revenue\nSo sánh sự khác biệt giữa thị phần theo số lượng chuyến đi và thị phần theo doanh thu để đánh giá hiệu quả kinh tế của từng hãng.")
    new_cell = nbf.v4.new_code_cell(comparison_code)
    
    # Find the end of 1.2.D to insert after it
    insert_pos = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and '# 1.2.D.2 Market Share Summary' in cell.source:
            insert_pos = i + 1
            break
            
    if insert_pos != -1:
        nb.cells.insert(insert_pos, header_e)
        nb.cells.insert(insert_pos + 1, new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Section 1.2.E added successfully.")
    else:
        print("Could not find section 1.2.D to insert after.")

if __name__ == "__main__":
    add_trip_vs_revenue_share_cell()
