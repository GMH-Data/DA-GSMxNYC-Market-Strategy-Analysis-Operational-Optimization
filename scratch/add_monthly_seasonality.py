import nbformat as nbf
import os

def add_monthly_competition_cell():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    monthly_code = """# 1.2.E.2 Monthly Competition Trends (Seasonality Across Years)
import plotly.express as px
import pandas as pd

# 1. Query: Trips by Month and Year for Uber and Lyft
query_monthly_yearly = \"\"\"
SELECT 
    year(pickup_datetime) as yr,
    month(pickup_datetime) as mo,
    CASE WHEN hvfhs_license_num = 'HV0003' THEN 'Uber' ELSE 'Lyft' END as provider,
    count(*) as total_trips
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1, 2, 3
\"\"\"
df_my = con.execute(query_monthly_yearly).df()

# 2. Visualization 1: Seasonality Line Chart
# Treat year as string/category for discrete colors
df_my['yr'] = df_my['yr'].astype(str)

fig1 = px.line(df_my.sort_values(['yr', 'mo']), 
              x='mo', y='total_trips', color='yr', facet_col='provider',
              title='Monthly Competition Seasonality Across Years (Uber vs Lyft)',
              labels={'mo': 'Month (1-12)', 'total_trips': 'Total Trips', 'yr': 'Year'},
              markers=True)

fig1.update_layout(xaxis=dict(tickmode='linear', dtick=1), template='plotly_white')
fig1.show()

# 3. Aggregate Monthly Trend (All Years Combined)
query_monthly_agg = \"\"\"
SELECT 
    month(pickup_datetime) as mo,
    CASE WHEN hvfhs_license_num = 'HV0003' THEN 'Uber' ELSE 'Lyft' END as provider,
    count(*) as total_trips
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1, 2
\"\"\"
df_agg = con.execute(query_monthly_agg).df()

fig2 = px.bar(df_agg.sort_values('mo'), 
                 x='mo', y='total_trips', color='provider', barmode='group',
                 title='Aggregated Monthly Trip Volume: Finding the Peak Season (2019-2025)',
                 labels={'mo': 'Month (1-12)', 'total_trips': 'Total Trips'})
fig2.update_layout(xaxis=dict(tickmode='linear', dtick=1), template='plotly_white')
fig2.show()

# 4. Insights Printout
peak_month = df_agg.groupby('mo')['total_trips'].sum().idxmax()
print(f"\\n--- STRATEGIC INSIGHT ---")
print(f"The most competitive month overall is Month {peak_month}.")
print("Look at the line chart to identify anomalies (like the massive drop in Q2 2020 due to COVID-19) and recovery trends.")"""

    new_cell = nbf.v4.new_code_cell(monthly_code)

    insert_pos = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and '# 1.2.E' in cell.source and 'Temporal Competition Analysis' in cell.source:
            insert_pos = i + 1
            break

    if insert_pos != -1:
        nb.cells.insert(insert_pos, new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Added monthly competition cell successfully.")
    else:
        print("Could not find section 1.2.E to insert after.")

if __name__ == "__main__":
    add_monthly_competition_cell()
