import nbformat as nbf
import os

def update_1_1_b_charts_with_table():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    new_code = """# 1.1.B Market Growth Rate Analysis (2016-2018)
import pandas as pd
import plotly.express as px

# --- 1. Calculate Mean Monthly Growth Rate ---
df_table = df_full.copy()
df_table['month_str'] = df_table['month'].dt.strftime('%Y-%m')
df_table = df_table.sort_values(['type', 'month'])
df_table['growth_pct'] = df_table.groupby('type')['trip_count'].pct_change() * 100
df_table.loc[(df_table['type'] == 'FHV') & (df_table['month'] <= '2017-06-01'), 'growth_pct'] = 0

df_pivot = df_table.pivot(index='month_str', columns='type', values='growth_pct').fillna(0)

# Display the growth rate table as requested
print("\\n--- 1.1.B DETAILED MONTHLY GROWTH RATE TABLE (%) ---")
display(df_pivot.round(2))

mean_growth_data = {
    'Service Type': ['FHV', 'Yellow', 'Green'],
    'Mean Monthly Growth (%)': [
        df_pivot.loc[df_pivot['FHV'] != 0, 'FHV'].mean(),
        df_pivot['Yellow'].mean(),
        df_pivot['Green'].mean()
    ]
}
df_mean_growth = pd.DataFrame(mean_growth_data)

# --- 2. Calculate YoY Growth (2018 vs 2017) ---
df_yearly = df_full.groupby(['type', df_full['month'].dt.year])['trip_count'].sum().reset_index()
df_yearly.columns = ['type', 'year', 'total_trips']

yoy_results = []
for taxi in ['FHV', 'Yellow', 'Green']:
    try:
        val_2017 = df_yearly[(df_yearly['type'] == taxi) & (df_yearly['year'] == 2017)]['total_trips'].values[0]
        val_2018 = df_yearly[(df_yearly['type'] == taxi) & (df_yearly['year'] == 2018)]['total_trips'].values[0]
        yoy_pct = ((val_2018 - val_2017) / val_2017) * 100
        yoy_results.append({'Service Type': taxi, 'YoY Growth (%)': yoy_pct})
    except:
        continue
df_yoy = pd.DataFrame(yoy_results)

# --- 3. Visualizations ---
colors_map = {'Yellow': '#f7d117', 'Green': '#2b9c3b', 'FHV': '#555555'}

# Chart 1: Mean Monthly Growth Rate
fig1 = px.bar(df_mean_growth, x='Service Type', y='Mean Monthly Growth (%)', 
             color='Service Type', text_auto='.2f',
             title='Average Monthly Growth Rate (%) (2016-2018)',
             color_discrete_map=colors_map,
             category_orders={'Service Type': ['FHV', 'Yellow', 'Green']})
fig1.update_layout(template='plotly_white', showlegend=False)
fig1.show()

# Chart 2: YoY Growth Rate
fig2 = px.bar(df_yoy, x='Service Type', y='YoY Growth (%)',
             color='Service Type', text_auto='.2f',
             title='Year-over-Year (YoY) Growth Rate (%) (2018 vs 2017)',
             color_discrete_map=colors_map,
             category_orders={'Service Type': ['FHV', 'Yellow', 'Green']})
fig2.update_layout(template='plotly_white', showlegend=False)
fig2.show()"""

    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and '# 1.1.B Market Growth Rate Analysis' in cell.source:
            cell.source = new_code
            found = True
            break
    
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Section 1.1.B updated with growth table.")
    else:
        print("Could not find section 1.1.B code cell.")

if __name__ == "__main__":
    update_1_1_b_charts_with_table()
