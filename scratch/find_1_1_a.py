import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and '### A. Overall and trip-based growth' in "".join(cell['source']):
        print(f"Found header at cell {i}")
        # The code cell should be the next one
        if i+1 < len(nb['cells']):
            next_cell = nb['cells'][i+1]
            print(f"Next cell ({i+1}) source:")
            print("".join(next_cell['source']))
        break
