import json

with open('Analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i, cell in enumerate(nb['cells']):
    source = "".join(cell.get('source', []))
    if 'about' in source:
        print(f"Cell {i} ({cell['cell_type']}):")
        lines = cell.get('source', [])
        for j, line in enumerate(lines):
            if 'about' in line:
                print(f"  Line {j}: {line.strip()}")
