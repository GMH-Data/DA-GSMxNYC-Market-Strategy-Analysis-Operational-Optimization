import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# HVFHS section is likely later
for i in range(13, len(nb['cells'])):
    cell = nb['cells'][i]
    if cell['cell_type'] == 'code':
        print(f"Cell {i} source:")
        print("".join(cell['source'])[:300])
        print("-" * 20)
