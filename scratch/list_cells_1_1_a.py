import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# List all cells from 9 to 12
for i in range(9, 13):
    cell = nb['cells'][i]
    print(f"Cell {i} ({cell['cell_type']}):")
    print("".join(cell['source'])[:200])
    print("-" * 20)
