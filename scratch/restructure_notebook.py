import nbformat as nbf
import os

def restructure():
    notebook_path = 'Data.ipynb'
    if not os.path.exists(notebook_path):
        print(f"Error: {notebook_path} not found")
        return

    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    new_cells = []
    
    # Define new cells for 1.2
    header_1_2 = nbf.v4.new_markdown_cell("## 1.2. HVFHS Market Analysis (2019-2025)\nAnalysis of High Volume For-Hire Services (Uber, Lyft, etc.) growth, market share, and competitive landscape.")
    
    cell_a_md = nbf.v4.new_markdown_cell("### A. Quy mô tổng thể và Tháng đỉnh điểm\nQuy mô tổng thể của thị trường HVFHS (tổng số chuyến đi) thay đổi như thế nào qua từng tháng từ 2019 đến 2025 so với Green và Yellow? Đâu là tháng đỉnh điểm?")
    cell_a_code = nbf.v4.new_code_cell("""# 1.2.A Monthly Volume Comparison (2019-2025)
import plotly.express as px
import pandas as pd

query_a = \"\"\"
SELECT 
    date_trunc('month', pickup_datetime) as month,
    'HVFHS' as type,
    count(*) as trip_count
FROM fhvhv_2019_2025_cleaned
GROUP BY 1
UNION ALL
SELECT 
    date_trunc('month', pickup_datetime) as month,
    'Yellow' as type,
    count(*) as trip_count
FROM yellow_2019_2025_cleaned
GROUP BY 1
UNION ALL
SELECT 
    date_trunc('month', pickup_datetime) as month,
    'Green' as type,
    count(*) as trip_count
FROM green_2019_2025_cleaned
GROUP BY 1
ORDER BY month, type
\"\"\"
df_a = con.execute(query_a).df()

# Line chart for trends
fig_a = px.line(df_a, x='month', y='trip_count', color='type',
              title='Monthly Trip Volume: HVFHS vs Traditional Taxis (2019-2025)',
              labels={'trip_count': 'Total Trips', 'month': 'Month', 'type': 'Service Type'},
              color_discrete_map={'HVFHS': '#555555', 'Yellow': '#f7d117', 'Green': '#2b9c3b'})
fig_a.update_layout(template='plotly_white')
fig_a.show()

# Identify peak month for HVFHS
peak_hvfhs = df_a[df_a['type'] == 'HVFHS'].sort_values('trip_count', ascending=False).iloc[0]
print(f"Peak month for HVFHS: {peak_hvfhs['month'].strftime('%B %Y')} with {peak_hvfhs['trip_count']:,} trips.")""")

    cell_b_md = nbf.v4.new_markdown_cell("### B. Tỷ lệ thị phần của 4 ông lớn\nTỷ lệ thị phần chuyến đi của 4 ông lớn (Uber, Lyft, Via, Juno) phân bổ ra sao theo từng năm?")
    cell_b_code = nbf.v4.new_code_cell("""# 1.2.B HVFHS Company Market Share (Yearly)
query_b = \"\"\"
SELECT 
    year(pickup_datetime) as year,
    CASE 
        WHEN hvfhs_license_num = 'HV0002' THEN 'Juno'
        WHEN hvfhs_license_num = 'HV0003' THEN 'Uber'
        WHEN hvfhs_license_num = 'HV0004' THEN 'Via'
        WHEN hvfhs_license_num = 'HV0005' THEN 'Lyft'
        ELSE 'Other'
    END as company,
    count(*) as trip_count
FROM fhvhv_2019_2025_cleaned
GROUP BY 1, 2
\"\"\"
df_b = con.execute(query_b).df()

# Calculate Share %
df_b['share_pct'] = df_b.groupby('year')['trip_count'].transform(lambda x: (x / x.sum()) * 100)

fig_b = px.bar(df_b, x='year', y='share_pct', color='company', 
             title='Yearly Market Share within HVFHS Sector (%)',
             labels={'share_pct': 'Market Share (%)', 'year': 'Year'},
             text_auto='.1f',
             category_orders={'year': sorted(df_b['year'].unique())},
             color_discrete_sequence=px.colors.qualitative.Safe)
fig_b.update_layout(template='plotly_white')
fig_b.show()""")

    cell_c_md = nbf.v4.new_markdown_cell("### C. Khu vực cạnh tranh khốc liệt\nCác hãng (Uber vs Lyft) thường cạnh tranh nhau ở khu vực nào? (Top 10 khu vực có lưu lượng lớn nhất)")
    cell_c_code = nbf.v4.new_code_cell("""# 1.2.C Competition Areas (Uber vs Lyft)
query_c = \"\"\"
WITH zone_stats AS (
    SELECT 
        z.Zone,
        CASE 
            WHEN hvfhs_license_num = 'HV0003' THEN 'Uber'
            WHEN hvfhs_license_num = 'HV0005' THEN 'Lyft'
        END as company,
        count(*) as trip_count
    FROM fhvhv_2019_2025_cleaned f
    JOIN taxi_zone_lookup z ON f.PULocationID = z.LocationID
    WHERE hvfhs_license_num IN ('HV0003', 'HV0005')
    GROUP BY 1, 2
)
SELECT 
    Zone,
    SUM(trip_count) as total_trips,
    MAX(CASE WHEN company = 'Uber' THEN trip_count ELSE 0 END) as uber_trips,
    MAX(CASE WHEN company = 'Lyft' THEN trip_count ELSE 0 END) as lyft_trips
FROM zone_stats
GROUP BY 1
ORDER BY total_trips DESC
LIMIT 10
\"\"\"
df_c = con.execute(query_c).df()

# Prepare data for plotting
df_c_plot = df_c.melt(id_vars=['Zone', 'total_trips'], 
                      value_vars=['uber_trips', 'lyft_trips'],
                      var_name='Company', value_name='Trips')
df_c_plot['Company'] = df_c_plot['Company'].str.replace('_trips', '').str.capitalize()

fig_c = px.bar(df_c_plot, x='Zone', y='Trips', color='Company', barmode='group',
             title='Top 10 Competitive Zones: Uber vs Lyft Volume',
             color_discrete_map={'Uber': '#000000', 'Lyft': '#FF00BF'})
fig_c.update_layout(template='plotly_white', xaxis_tickangle=-45)
fig_c.show()""")

    restructured_1_2 = [header_1_2, cell_a_md, cell_a_code, cell_b_md, cell_b_code, cell_c_md, cell_c_code]
    
    i = 0
    while i < len(nb.cells):
        cell = nb.cells[i]
        source = cell.source
        
        # 1. Identify old 1.2 section (often starts with # 1.2 comment in code)
        if cell.cell_type == 'code' and '# 1.2 Focused Growth Analysis' in source:
            print(f"Replacing old 1.2 section at cell {i}")
            # Replace this one cell with our new list of cells
            for j, new_c in enumerate(restructured_1_2):
                nb.cells.insert(i + j, new_c)
            # Remove the old one (now shifted by restructured_1_2)
            del nb.cells[i + len(restructured_1_2)]
            i += len(restructured_1_2)
            continue
            
        # 2. Rename Pre-2019 Location Analysis header
        if cell.cell_type == 'markdown' and '### C. Location and Zone Analysis' in source:
            print(f"Renaming Pre-2019 Location header at cell {i}")
            cell.source = source.replace('### C. Location and Zone Analysis', '### D. Pre-2019 Location Analysis')
            
        # 3. Rename/Consolidate redundant 1.2 sections
        if cell.cell_type == 'markdown' and '## 1.2. Analysis from 2019-2025 HVFHS' in source:
            print(f"Consolidating redundant 1.2 header at cell {i}")
            cell.source = source.replace('## 1.2. Analysis from 2019-2025 HVFHS', '## 1.3. Financial & Efficiency Analysis (2019-2025)')
            
        i += 1

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Notebook restructured successfully.")

if __name__ == "__main__":
    restructure()
