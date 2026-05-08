import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'px.imshow' in source and 'color_discrete_sequence' in source:
            # More direct replacement
            bad_string = "color_discrete_sequence=['#FF1493', '#FFFFFF', '#FF69B4', '#C0C0C0'], "
            source = source.replace(bad_string, "")
            # Also try without the space or with a newline
            source = source.replace("\n                color_discrete_sequence=['#FF1493', '#FFFFFF', '#FF69B4', '#C0C0C0'],", "")
            source = source.replace(", color_discrete_sequence=['#FF1493', '#FFFFFF', '#FF69B4', '#C0C0C0']", "")
            
            lines = [line + '\n' if not line.endswith('\n') else line for line in source.splitlines()]
            cell['source'] = lines

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
