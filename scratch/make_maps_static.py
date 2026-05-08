import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '1.2.1.D Competition Analysis: Uber vs Lyft Detailed Visualizations' in ''.join(cell['source']):
        source = ''.join(cell['source'])
        
        # Update fig_uber
        source = source.replace(
            'fig_uber.update_geos(fitbounds="locations", visible=False)',
            'fig_uber.update_geos(fitbounds="locations", visible=False, fixedrange=True)'
        )
        source = source.replace(
            'fig_uber.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template=\'plotly_white\')',
            'fig_uber.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template=\'plotly_white\', dragmode=False)'
        )
        
        # Update fig_lyft
        source = source.replace(
            'fig_lyft.update_geos(fitbounds="locations", visible=False)',
            'fig_lyft.update_geos(fitbounds="locations", visible=False, fixedrange=True)'
        )
        source = source.replace(
            'fig_lyft.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template=\'plotly_white\')',
            'fig_lyft.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, template=\'plotly_white\', dragmode=False)'
        )
        
        # Also updating fig_comp to be consistent if desired, but user only asked for growth maps.
        # Let's just do growth maps as requested.
        
        lines = [line + '\n' if not line.endswith('\n') else line for line in source.splitlines()]
        cell['source'] = lines
        break

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
