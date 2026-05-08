import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 1.2.1.E Key Zone Analysis: Trip Distance & Shared Match Rates\n",
        "import plotly.express as px\n",
        "\n",
        "# 1. Query: Metrics for Top 10 High-Volume Zones in 2024\n",
        "query_e = \"\"\"\n",
        "WITH KeyZones AS (\n",
        "    SELECT PULocationID, count(*) as total_trips\n",
        "    FROM fhvhv_2019_2025_cleaned\n",
        "    WHERE year(pickup_datetime) = 2024\n",
        "    GROUP BY 1\n",
        "    ORDER BY total_trips DESC\n",
        "    LIMIT 10\n",
        ")\n",
        "SELECT \n",
        "    z.zone,\n",
        "    z.borough,\n",
        "    avg(f.trip_miles) as avg_distance_miles,\n",
        "    avg(f.trip_time) / 60.0 as avg_duration_min,\n",
        "    count(CASE WHEN f.shared_match_flag = 'Y' THEN 1 END) * 100.0 / count(*) as shared_match_rate_pct\n",
        "FROM fhvhv_2019_2025_cleaned f\n",
        "JOIN KeyZones k ON f.PULocationID = k.PULocationID\n",
        "JOIN taxi_zone_lookup z ON f.PULocationID = z.LocationID\n",
        "WHERE year(f.pickup_datetime) = 2024\n",
        "GROUP BY 1, 2\n",
        "ORDER BY avg_distance_miles DESC\n",
        "\"\"\"\n",
        "df_key_zones = con.execute(query_e).df()\n",
        "\n",
        "# 2. Visualization: Dual Axis Style (using grouping for simplicity)\n",
        "fig = px.bar(df_key_zones, x='zone', y=['avg_distance_miles', 'shared_match_rate_pct'],\n",
        "             barmode='group', \n",
        "             title='Trip Distance vs Shared Match Rate in Top 10 High-Volume Zones (2024)',\n",
        "             labels={'value': 'Value', 'variable': 'Metric', 'zone': 'Taxi Zone'},\n",
        "             hover_data=['avg_duration_min'],\n",
        "             color_discrete_sequence=['#636EFA', '#EF553B'])\n",
        "\n",
        "fig.update_layout(yaxis_title=\"Miles / Percentage (%)\", \n",
        "                  legend_title=\"Metrics\",\n",
        "                  template='plotly_white', \n",
        "                  xaxis={'categoryorder':'total descending'})\n",
        "fig.show()\n",
        "\n",
        "# 3. Insights Printout\n",
        "print(\"\\n--- STRATEGIC KEY ZONE METRICS (2024 Data) ---\")\n",
        "display(df_key_zones.round(2))\n",
        "\n",
        "max_match_zone = df_key_zones.loc[df_key_zones['shared_match_rate_pct'].idxmax(), 'zone']\n",
        "print(f\"\\nInsight: The zone '{max_match_zone}' has the highest shared match rate among high-volume areas.\")\n"
    ]
}

# Find index of 1.2.1.D and insert after
target_idx = -1
for i, cell in enumerate(nb['cells']):
    if '1.2.1.D Competition Analysis' in ''.join(cell['source']):
        target_idx = i
        break

if target_idx != -1:
    nb['cells'].insert(target_idx + 1, new_cell)

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
