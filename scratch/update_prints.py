import json

file_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
output_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Update the print statement in Section 1.3.1.1
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and "# 1.3.1.1 Column Standardization" in "".join(cell['source']):
        new_source = cell['source']
        # Find the last print statement or append to the end
        if new_source[-1].startswith('print("Step 1.3.1.1 Complete'):
            new_source[-1] = 'print("Step 1.3.1.1 Complete: Unified schema mapping applied.")\n'
            new_source.append('print(f"Standardized Columns: [\'pickup_datetime\', \'dropoff_datetime\', \'pickup_location_id\', \'dropoff_location_id\', \'service_type\']")\n')
            new_source.append('# Show sample from one standardized view\n')
            new_source.append('display(con.execute("SELECT * FROM yellow_Pre_2019_std LIMIT 1").df())\n')
        cell['source'] = new_source

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Updated print statements in 1.3.1.1 to show standardized columns.")
