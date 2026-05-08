import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 12 is the growth analysis
cell = nb['cells'][12]
cell['source'] = [
    "# 1.2 Focused Growth Analysis: From July 2017 Onwards (Post-June 2017)\n",
    "# This analysis focuses on the market performance after the significant shift in mid-2017.\n",
    "\n",
    "import plotly.express as px\n",
    "import pandas as pd\n",
    "\n",
    "# --- DATA PROCESSING ---\n",
    "df_growth = df_full.copy()\n",
    "df_growth['month'] = pd.to_datetime(df_growth['month'])\n",
    "df_growth = df_growth.sort_values(['type', 'month'])\n",
    "df_growth['mom_growth_pct'] = df_growth.groupby('type')['trip_count'].pct_change() * 100\n",
    "\n",
    "# Filter for July 2017 onwards (Post-June 2017)\n",
    "limit_date = pd.Timestamp('2017-07-01')\n",
    "df_focused = df_growth[df_growth['month'] >= limit_date]\n",
    "\n",
    "# Calculate Mean and Median Monthly Growth\n",
    "df_stats = df_focused.groupby('type')['mom_growth_pct'].agg(['mean', 'median']).reset_index()\n",
    "df_stats.columns = ['type', 'Mean (%)', 'Median (%)']\n",
    "\n",
    "# Calculate YOY (2018 vs 2017 Growth)\n",
    "df_yearly_sum = df_growth.groupby(['type', df_growth['month'].dt.year])['trip_count'].sum().reset_index()\n",
    "df_yearly_sum.columns = ['type', 'year', 'total_trips']\n",
    "\n",
    "yoy_list = []\n",
    "for taxi in ['Yellow', 'Green', 'FHV']:\n",
    "    try:\n",
    "        trips_2017 = df_yearly_sum[(df_yearly_sum['type'] == taxi) & (df_yearly_sum['year'] == 2017)]['total_trips'].values[0]\n",
    "        trips_2018 = df_yearly_sum[(df_yearly_sum['type'] == taxi) & (df_yearly_sum['year'] == 2018)]['total_trips'].values[0]\n",
    "        yoy_val = ((trips_2018 - trips_2017) / trips_2017) * 100\n",
    "        yoy_list.append({'type': taxi, 'YOY (%)': yoy_val})\n",
    "    except IndexError:\n",
    "        continue\n",
    "df_yoy = pd.DataFrame(yoy_list)\n",
    "\n",
    "# --- PART 1: Summary Table (DISPLAY AT THE TOP) ---\n",
    "df_summary = pd.merge(df_stats, df_yoy, on='type')\n",
    "df_summary.columns = ['Service Type', 'Mean Monthly (%)', 'Median Monthly (%)', 'YOY (%)']\n",
    "df_summary = df_summary.set_index('Service Type').round(2)\n",
    "\n",
    "print(\"\\n--- GROWTH SUMMARY: JULY 2017 - DEC 2018 ---\")\n",
    "display(df_summary.loc[['FHV', 'Green', 'Yellow']])\n",
    "\n",
    "# --- PART 2: Visualizations (CONSISTENT ORDER: FHV, Green, Yellow) ---\n",
    "cat_order = {'type': ['FHV', 'Green', 'Yellow']}\n",
    "\n",
    "# Melting stats for comparison plot\n",
    "df_plot_stats = df_stats.melt(id_vars='type', var_name='Metric', value_name='Value (%)')\n",
    "\n",
    "fig_growth = px.bar(df_plot_stats, x='type', y='Value (%)', color='Metric', barmode='group', text_auto='.2f',\n",
    "                 title='Monthly Growth Rate Metrics (Mean vs Median, July 2017 - Dec 2018)',\n",
    "                 color_discrete_sequence=['#2a3f5f', '#1f77b4'],\n",
    "                 category_orders=cat_order)\n",
    "fig_growth.update_layout(template='plotly_white', xaxis_title='Service Type')\n",
    "fig_growth.show()\n",
    "\n",
    "fig_yoy = px.bar(df_yoy, x='type', y='YOY (%)', color='type', text_auto='.2f', \n",
    "                 title='Overall Yearly Growth Rate (2018 vs 2017)',\n",
    "                 color_discrete_map={'Yellow': '#f7d117', 'Green': '#2b9c3b', 'FHV': '#555555'},\n",
    "                 category_orders=cat_order)\n",
    "fig_yoy.update_layout(template='plotly_white', showlegend=False)\n",
    "fig_yoy.show()\n"
]

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
    print("Notebook updated successfully.")
