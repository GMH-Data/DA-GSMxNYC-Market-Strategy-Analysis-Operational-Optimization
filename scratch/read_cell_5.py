import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find cell 5 (which has execution_count: 5)
for i, cell in enumerate(nb['cells']):
    if cell.get('execution_count') == 5:
        print(f"Cell {i} source:")
        print("".join(cell['source']))
        break
