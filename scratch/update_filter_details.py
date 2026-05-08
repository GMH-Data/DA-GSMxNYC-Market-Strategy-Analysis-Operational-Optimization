import json

def update_filtering_detailed_stats(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    target_header = "# 1.3.1.2 Row Filtering: Cleaning Invalid Records"
    found = False
    
    new_code = [
        "# 1.3.1.2 Row Filtering: Cleaning Invalid Records\n",
        "import plotly.express as px\n",
        "\n",
        "# Define Filtering Constraints\n",
        "YEAR_MIN, YEAR_MAX = 2016, 2026\n",
        "ZONE_MIN, ZONE_MAX = 1, 265\n",
        "\n",
        "def filter_taxi_rows(source_std_table, extra_where=\"\"):\n",
        "    target_table = source_std_table.replace(\"_std\", \"_cleaned\")\n",
        "    \n",
        "    # 1. Analyze invalid records breakdown\n",
        "    analysis_query = f\"\"\"\n",
        "    SELECT \n",
        "        COUNT(*) AS total,\n",
        "        COUNT(*) FILTER (WHERE NOT (year(pickup_datetime) BETWEEN {YEAR_MIN} AND {YEAR_MAX})) AS bad_date,\n",
        "        COUNT(*) FILTER (WHERE NOT (dropoff_datetime > pickup_datetime)) AS bad_duration,\n",
        "        COUNT(*) FILTER (WHERE NOT (pickup_location_id BETWEEN {ZONE_MIN} AND {ZONE_MAX} AND dropoff_location_id BETWEEN {ZONE_MIN} AND {ZONE_MAX})) AS bad_zone\n",
        "    FROM {source_std_table}\n",
        "    \"\"\"\n",
        "    stats = con.execute(analysis_query).fetchone()\n",
        "    orig, bad_date, bad_duration, bad_zone = stats\n",
        "    \n",
        "    # 2. Perform actual filtering\n",
        "    con.execute(f\"\"\"\n",
        "    CREATE OR REPLACE VIEW {target_table} AS\n",
        "    SELECT *\n",
        "    FROM {source_std_table}\n",
        "    WHERE \n",
        "        (dropoff_datetime > pickup_datetime AND year(pickup_datetime) BETWEEN {YEAR_MIN} AND {YEAR_MAX})\n",
        "        AND (pickup_location_id BETWEEN {ZONE_MIN} AND {ZONE_MAX}) \n",
        "        AND (dropoff_location_id BETWEEN {ZONE_MIN} AND {ZONE_MAX})\n",
        "        {extra_where};\n",
        "    \"\"\")\n",
        "    \n",
        "    clean = con.execute(f\"SELECT count(*) FROM {target_table}\").fetchone()[0]\n",
        "    return orig, clean, bad_date, bad_duration, bad_zone\n",
        "\n",
        "std_tables = [t[0] for t in con.execute(\"SHOW TABLES\").fetchall() if t[0].endswith(\"_std\")]\n",
        "filter_stats = []\n",
        "total_orig, total_clean = 0, 0\n",
        "\n",
        "for t in std_tables:\n",
        "    orig, clean, b_date, b_dur, b_zone = filter_taxi_rows(t)\n",
        "    filter_stats.append({\n",
        "        \"Table\": t.replace(\"_std\", \"\"), \n",
        "        \"Original\": orig, \n",
        "        \"Cleaned\": clean, \n",
        "        \"Removed\": orig - clean,\n",
        "        \"Bad Date\": b_date,\n",
        "        \"Bad Duration\": b_dur,\n",
        "        \"Bad Zone\": b_zone\n",
        "    })\n",
        "    total_orig += orig\n",
        "    total_clean += clean\n",
        "\n",
        "df_filter = pd.DataFrame(filter_stats)\n",
        "# Formatting numbers for readability\n",
        "numeric_cols = [\"Original\", \"Cleaned\", \"Removed\", \"Bad Date\", \"Bad Duration\", \"Bad Zone\"]\n",
        "df_filter_styled = df_filter.copy()\n",
        "for col in numeric_cols:\n",
        "    df_filter_styled[col] = df_filter_styled[col].apply(lambda x: f\"{x:,}\")\n",
        "\n",
        "display(df_filter_styled)\n",
        "\n",
        "# Visualization: Overall Data Health\n",
        "fig_pie = px.pie(names=['Cleaned Data', 'Removed Data'], \n",
        "                 values=[total_clean, total_orig - total_clean], \n",
        "                 title=f'Overall Data Quality: {total_clean/total_orig*100:.1f}% Retention',\n",
        "                 color_discrete_sequence=['#26DE81', '#EB3B5A'], template='plotly_dark')\n",
        "fig_pie.show()\n",
        "print(f\"Step 1.3.1.2 Complete: {total_orig - total_clean:,} rows filtered out.\")\n"
    ]
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code' and target_header in "".join(cell['source']):
            cell['source'] = new_code
            found = True
            break
            
    if found:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print("Successfully updated filtering table with detailed breakdown.")
    else:
        print("Target cell not found.")

if __name__ == "__main__":
    update_filtering_detailed_stats("Data.ipynb")
