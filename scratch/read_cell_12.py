import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell = nb['cells'][12]
print("".join(cell['source']))
