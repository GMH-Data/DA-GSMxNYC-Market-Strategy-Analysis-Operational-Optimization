import json

def update_investigation_with_pie(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    target_header = "# 1.3.2.B - Deep Dive Investigation: fhv_Pre_2019 Data Loss"
    found = False
    
    new_code = [
        "# 1.3.2.B - Deep Dive Investigation: fhv_Pre_2019 Data Loss\n",
        "table_to_investigate = 'fhv_Pre_2019_std'\n",
        "\n",
        "print(f\"--- Analyzing Data Loss Reasons for {table_to_investigate} ---\")\n",
        "query_analysis = f\"\"\"\n",
        "SELECT \n",
        "    COUNT(*) FILTER (WHERE year(pickup_datetime) < {YEAR_MIN}) AS 'Before {YEAR_MIN}',\n",
        "    COUNT(*) FILTER (WHERE year(pickup_datetime) > {YEAR_MAX}) AS 'After {YEAR_MAX}',\n",
        "    COUNT(*) FILTER (WHERE NOT (dropoff_datetime > pickup_datetime)) AS 'Invalid Duration',\n",
        "    COUNT(*) FILTER (WHERE NOT (pickup_location_id BETWEEN {ZONE_MIN} AND {ZONE_MAX} AND dropoff_location_id BETWEEN {ZONE_MIN} AND {ZONE_MAX})) AS 'Invalid Zones'\n",
        "FROM {table_to_investigate}\n",
        "\"\"\"\n",
        "\n",
        "loss_stats = con.execute(query_analysis).df()\n",
        "\n",
        "# Reshape data for Pie Chart\n",
        "df_pie = loss_stats.melt(var_name='Reason', value_name='Count')\n",
        "df_pie = df_pie[df_pie['Count'] > 0] # Only show reasons with actual data loss\n",
        "\n",
        "# Visualization\n",
        "import plotly.express as px\n",
        "fig = px.pie(df_pie, values='Count', names='Reason', \n",
        "             title=f'Reasons for Data Loss in {table_to_investigate}',\n",
        "             color_discrete_sequence=px.colors.qualitative.Pastel,\n",
        "             template='plotly_dark')\n",
        "fig.update_traces(textposition='inside', textinfo='percent+label')\n",
        "fig.show()\n",
        "\n",
        "# Display the raw counts for reference\n",
        "display(df_pie.style.format({'Count': '{:,}'}))\n",
        "\n",
        "print(\"\\n--- Top 5 Earliest Years in Dataset ---\")\n",
        "display(con.execute(f\"SELECT year(pickup_datetime) as year, COUNT(*) as count FROM {table_to_investigate} GROUP BY 1 ORDER BY 1 LIMIT 5\").df())\n"
    ]
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code' and target_header in "".join(cell['source']):
            cell['source'] = new_code
            found = True
            break
            
    if found:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print("Successfully updated 1.3.2.B with Pie Chart.")
    else:
        print("Target cell not found.")

if __name__ == "__main__":
    update_investigation_with_pie("Data.ipynb")
