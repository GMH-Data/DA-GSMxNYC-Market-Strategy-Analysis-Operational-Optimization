import json
import re

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'px.imshow' in source and 'color_discrete_sequence' in source:
            # Remove color_discrete_sequence from px.imshow
            # It might be in different formats, let's be careful
            source = re.sub(r",\s*color_discrete_sequence=\[.*?\]", "", source)
            
            lines = [line + '\n' if not line.endswith('\n') else line for line in source.splitlines()]
            cell['source'] = lines

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
