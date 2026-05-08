import json

def add_investigation_cell(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    investigation_header = "#### 1.3.2.B - Detailed query"
    found_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown' and investigation_header in "".join(cell['source']):
            found_idx = i
            break
    
    if found_idx != -1:
        new_code_cell = {
            "cell_type": "code",
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1.3.2.B - Deep Dive Investigation: fhv_Pre_2019 Data Loss\n",
                "table_to_investigate = 'fhv_Pre_2019_std'\n",
                "\n",
                "print(f\"--- Analyzing Data Loss for {table_to_investigate} ---\")\n",
                "query_analysis = f\"\"\"\n",
                "SELECT \n",
                "    COUNT(*) AS total_rows,\n",
                "    COUNT(*) FILTER (WHERE year(pickup_datetime) < 2016) AS rows_before_2016,\n",
                "    COUNT(*) FILTER (WHERE year(pickup_datetime) > 2026) AS rows_after_2026,\n",
                "    COUNT(*) FILTER (WHERE dropoff_datetime <= pickup_datetime) AS invalid_duration,\n",
                "    COUNT(*) FILTER (WHERE pickup_location_id NOT BETWEEN 1 AND 265 OR dropoff_location_id NOT BETWEEN 1 AND 265) AS invalid_zones,\n",
                "    COUNT(*) FILTER (WHERE pickup_location_id = 264 OR dropoff_location_id = 264) AS unknown_zones_264\n",
                "FROM {table_to_investigate}\n",
                "\"\"\"\n",
                "\n",
                "analysis_results = con.execute(query_analysis).df()\n",
                "display(analysis_results)\n",
                "\n",
                "print(\"\\n--- Breakdown of Rows by Year (Top 10 earliest) ---\")\n",
                "query_years = f\"\"\"\n",
                "SELECT year(pickup_datetime) as year, COUNT(*) as count\n",
                "FROM {table_to_investigate}\n",
                "GROUP BY 1 ORDER BY 1 LIMIT 10\n",
                "\"\"\"\n",
                "display(con.execute(query_years).df())\n"
            ]
        }
        
        # Check if the next cell is already a code cell or if we should insert
        if found_idx + 1 < len(nb['cells']) and nb['cells'][found_idx+1]['cell_type'] == 'code' and not nb['cells'][found_idx+1]['source']:
            # Replace empty code cell
            nb['cells'][found_idx+1] = new_code_cell
        else:
            # Insert new code cell
            nb['cells'].insert(found_idx + 1, new_code_cell)
            
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print("Successfully added investigation logic to 1.3.2.B.")
    else:
        print("Could not find header 1.3.2.B.")

if __name__ == "__main__":
    add_investigation_cell("Data.ipynb")
