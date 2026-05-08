import json

file_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
output_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# --- Update Cell 6 (Markdown) ---
cell_6 = nb['cells'][6]
cell_6['source'] = [
    "### 1.3.1.1. Column Standardization\n",
    "\n",
    "Unified schema mapping to ensure consistency across all datasets:\n",
    "- **DateTime**: `pickup_datetime`, `dropoff_datetime` (Standardized from vendor-specific names).\n",
    "- **Location**: `pickup_location_id`, `dropoff_location_id` (Renamed from `PULocationID`/`DOLocationID`).\n",
    "- **Service Metadata**: Added `service_type` (`yellow`, `green`, `fhv`, `hvfhs`) for cross-dataset analysis.\n",
    "- **Null Handling**: Missing Location IDs are defaulted to `264` (Unknown)."
]

# --- Update Cell 7 (Code) ---
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and "# 1.3.1.1 Column Standardization" in "".join(cell['source']):
        new_source = [
            "# 1.3.1.1 Column Standardization: Unified Schema Mapping\n",
            "def standardize_taxi_columns(taxi_type, source_table, pickup_col, dropoff_col, pu_col='PULocationID', do_col='DOLocationID', extra_select=\"\", exclude_cols=None):\n",
            "    target_table = f\"{source_table}_std\"\n",
            "    actual_cols = [row[0] for row in con.execute(f\"DESCRIBE {source_table}\").fetchall()]\n",
            "    \n",
            "    mapping_select = []\n",
            "    mapping_select.append(f\"COALESCE({pu_col}, 264) AS pickup_location_id\") if pu_col in actual_cols else mapping_select.append(\"264 AS pickup_location_id\")\n",
            "    mapping_select.append(f\"COALESCE({do_col}, 264) AS dropoff_location_id\") if do_col in actual_cols else mapping_select.append(\"264 AS dropoff_location_id\")\n",
            "    mapping_select.append(f\"{pickup_col} AS pickup_datetime\") if pickup_col in actual_cols else mapping_select.append(\"CAST(NULL AS TIMESTAMP) AS pickup_datetime\")\n",
            "    mapping_select.append(f\"{dropoff_col} AS dropoff_datetime\") if dropoff_col in actual_cols else mapping_select.append(\"CAST(NULL AS TIMESTAMP) AS dropoff_datetime\")\n",
            "    mapping_select.append(f\"'{taxi_type}' AS service_type\")\n",
            "    \n",
            "    mapping_str = \", \".join(mapping_select)\n",
            "    to_exclude = [pu_col, do_col, pickup_col, dropoff_col]\n",
            "    if exclude_cols: to_exclude.extend(exclude_cols)\n",
            "    existing_exclude = [c for c in to_exclude if c in actual_cols]\n",
            "    exclude_clause = f\"EXCLUDE ({', '.join(set(existing_exclude))})\" if existing_exclude else \"\"\n",
            "    select_extra = f\"{extra_select},\" if extra_select else \"\"\n",
            "    \n",
            "    con.execute(f\"\"\"\n",
            "    CREATE OR REPLACE VIEW {target_table} AS\n",
            "    SELECT {mapping_str}, {select_extra} * {exclude_clause}\n",
            "    FROM {source_table};\n",
            "    \"\"\")\n",
            "\n",
            "all_tables = [t[0] for t in con.execute(\"SHOW TABLES\").fetchall()]\n",
            "raw_tables = [t for t in all_tables if \"_20\" in t and not t.endswith(\"_cleaned\") and not t.endswith(\"_std\")]\n",
            "\n",
            "for t in raw_tables:\n",
            "    if \"yellow_\" in t: standardize_taxi_columns('yellow', t, 'tpep_pickup_datetime', 'tpep_dropoff_datetime')\n",
            "    elif \"green_\" in t: standardize_taxi_columns('green', t, 'lpep_pickup_datetime', 'lpep_dropoff_datetime')\n",
            "    elif \"fhvhv_\" in t: \n",
            "        standardize_taxi_columns('hvfhs', t, 'pickup_datetime', 'dropoff_datetime', \n",
            "                                extra_select=\"UPPER(CAST(hvfhs_license_num AS VARCHAR)) AS hvfhs_license_num\",\n",
            "                                exclude_cols=['hvfhs_license_num'])\n",
            "    elif \"fhv_\" in t: \n",
            "        standardize_taxi_columns('fhv', t, 'pickup_datetime', 'dropOff_datetime', pu_col='PUlocationID', do_col='DOlocationID')\n",
            "\n",
            "print(\"Step 1.3.1.1 Complete: All tables standardized into _std views.\")"
        ]
        cell['source'] = new_source

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Removed dashboard from 1.3.1.1 and added descriptive notes to the markdown cell.")
