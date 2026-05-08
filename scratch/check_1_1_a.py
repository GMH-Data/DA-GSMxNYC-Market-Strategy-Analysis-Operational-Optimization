import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find header 1.1.A
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown' and '### A. Overall and trip-based growth' in "".join(cell['source']):
        print(f"Header at index {i}")
        if i+1 < len(nb['cells']):
            print(f"Next cell ({i+1}) source:")
            print("".join(nb['cells'][i+1]['source']))
        break
