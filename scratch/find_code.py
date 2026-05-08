import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        source = "".join(cell['source'])
        if 'AMG' in source or 'YOY' in source or 'Growth Rate' in source:
            print(f"Found match in cell {i}:")
            print(source[:500] + "...")
            print("-" * 40)
