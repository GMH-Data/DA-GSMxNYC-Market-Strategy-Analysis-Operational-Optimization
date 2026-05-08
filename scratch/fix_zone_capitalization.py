import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '1.2.1.E Key Zone Analysis' in ''.join(cell['source']):
        source = ''.join(cell['source'])
        
        # Fix the capitalization issues
        source = source.replace("x='zone'", "x='Zone'")
        source = source.replace("'zone': 'Taxi Zone'", "'Zone': 'Taxi Zone'")
        source = source.replace("df_key_zones['zone']", "df_key_zones['Zone']")
        source = source.replace(", 'zone']", ", 'Zone']")
        
        lines = [line + '\n' if not line.endswith('\n') else line for line in source.splitlines()]
        cell['source'] = lines
        break

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
