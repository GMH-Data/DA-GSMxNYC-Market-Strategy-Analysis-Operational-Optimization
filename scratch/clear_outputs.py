import json

file_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
output_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'

with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the specific cell and clear outputs
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and "# 1.3.1.1 Column Standardization" in "".join(cell['source']):
        cell['outputs'] = []
        cell['execution_count'] = None

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Cleared outputs for 1.3.1.1.")
