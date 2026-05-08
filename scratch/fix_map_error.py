import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '1.2.1.D Competition Analysis: Uber vs Lyft Detailed Visualizations' in ''.join(cell['source']):
        source = ''.join(cell['source'])
        
        # Remove the problematic fixedrange=True
        source = source.replace(', fixedrange=True', '')
        
        # Update show() calls to disable scroll zoom via config
        source = source.replace('fig_uber.show()', "fig_uber.show(config={'scrollZoom': False})")
        source = source.replace('fig_lyft.show()', "fig_lyft.show(config={'scrollZoom': False})")
        source = source.replace('fig_comp.show()', "fig_comp.show(config={'scrollZoom': False})")
        
        lines = [line + '\n' if not line.endswith('\n') else line for line in source.splitlines()]
        cell['source'] = lines
        break

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
