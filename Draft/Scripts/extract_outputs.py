import json
import os

notebook_path = 'e:/Project/Taxi Project (In Process)/Analysis.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

extracted_text = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and 'outputs' in cell:
        header = f"Cell {i}"
        source_header = "".join(cell['source'][:1]) if cell['source'] else "Empty"
        for output in cell['outputs']:
            if 'text' in output:
                extracted_text.append(f"--- {header} ({source_header.strip()}) stdout ---\n" + "".join(output['text']))
            if 'data' in output and 'text/plain' in output['data']:
                extracted_text.append(f"--- {header} ({source_header.strip()}) data ---\n" + "".join(output['data']['text/plain']))

output_file = 'e:/Project/Taxi Project (In Process)/Draft/extracted_outputs.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n\n".join(extracted_text))
