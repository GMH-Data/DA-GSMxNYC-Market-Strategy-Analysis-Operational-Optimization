import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '1.2.1.E Key Zone Analysis' in ''.join(cell['source']):
        new_source = [
            "# 1.2.1.E Key Zone Analysis: Trip Distance, Wait Time & Shared Match Rates\n",
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
            "    z.Zone,\n",
            "    z.Borough,\n",
            "    avg(date_diff('second', f.request_datetime, f.pickup_datetime)) / 60.0 as avg_wait_time_min,\n",
            "    avg(f.trip_miles) as avg_distance_miles,\n",
            "    avg(f.trip_time) / 60.0 as avg_duration_min,\n",
            "    count(CASE WHEN f.shared_match_flag = 'Y' THEN 1 END) * 100.0 / count(*) as shared_match_rate_pct\n",
            "FROM fhvhv_2019_2025_cleaned f\n",
            "JOIN KeyZones k ON f.PULocationID = k.PULocationID\n",
            "JOIN taxi_zone_lookup z ON f.PULocationID = z.LocationID\n",
            "WHERE year(f.pickup_datetime) = 2024\n",
            "GROUP BY 1, 2\n",
            "ORDER BY avg_wait_time_min DESC\n",
            "\"\"\"\n",
            "df_key_zones = con.execute(query_e).df()\n",
            "\n",
            "# 2. Visualization: Wait Time vs Match Rate\n",
            "fig = px.bar(df_key_zones, x='Zone', y=['avg_wait_time_min', 'shared_match_rate_pct'],\n",
            "             barmode='group', \n",
            "             title='Average Wait Time vs Shared Match Rate in Top 10 High-Volume Zones (2024)',\n",
            "             labels={'value': 'Value', 'variable': 'Metric', 'Zone': 'Taxi Zone'},\n",
            "             hover_data=['avg_distance_miles', 'avg_duration_min'],\n",
            "             color_discrete_sequence=['#FF9900', '#EF553B'])\n",
            "\n",
            "fig.update_layout(yaxis_title=\"Minutes / Percentage (%)\", \n",
            "                  legend_title=\"Metrics\",\n",
            "                  template='plotly_white', \n",
            "                  xaxis={'categoryorder':'total descending'})\n",
            "fig.show()\n",
            "\n",
            "# 3. Insights Printout\n",
            "print(\"\\n--- STRATEGIC KEY ZONE METRICS (Wait Time Focus) ---\")\n",
            "display(df_key_zones.round(2))\n",
            "\n",
            "slowest_zone = df_key_zones.loc[df_key_zones['avg_wait_time_min'].idxmax(), 'Zone']\n",
            "fastest_zone = df_key_zones.loc[df_key_zones['avg_wait_time_min'].idxmin(), 'Zone']\n",
            "print(f\"\\nInsight: '{fastest_zone}' has the fastest connection time, while '{slowest_zone}' takes the longest to find a car.\")\n"
        ]
        cell['source'] = new_source
        break

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
