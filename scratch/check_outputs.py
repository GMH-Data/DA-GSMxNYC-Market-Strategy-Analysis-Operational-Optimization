import json

nb_path = r'e:\Project\Taxi Project (In Process)\Data.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

cell = nb['cells'][10]
if 'outputs' in cell and cell['outputs']:
    for output in cell['outputs']:
        if 'data' in output and 'text/html' in output['data']:
            print("HTML output found. Snippet:")
            html = "".join(output['data']['text/html'])
            print(html[-1000:]) # Look at the end of the table
            break
else:
    print("No outputs found for cell 10.")
