import json

def has_vietnamese(text):
    return any(ord(c) > 127 for c in text)

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

missed = []
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell['source'])
    if has_vietnamese(source):
        cell_info = {
            "index": i,
            "type": cell["cell_type"],
            "vietnamese_lines": [line.strip() for line in cell['source'] if has_vietnamese(line)]
        }
        missed.append(cell_info)

if not missed:
    print("SUCCESS: No Vietnamese found.")
else:
    print(f"FOUND {len(missed)} CELLS WITH VIETNAMESE:")
    for m in missed:
        print(f"Cell {m['index']} ({m['type']}):")
        for line in m['vietnamese_lines']:
            print(f"  - {line}")
