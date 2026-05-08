import json
import re

def update_chart_colors(source):
    # Apply plotly_dark template everywhere
    source = source.replace("template='plotly_white'", "template='plotly_dark'")
    source = source.replace('template="plotly_white"', "template='plotly_dark'")
    
    # Update color discrete sequences (Pink & White/Gray)
    pink_colors = "['#FF1493', '#FFFFFF', '#FF69B4', '#C0C0C0']"
    if 'color_discrete_sequence' in source:
        source = re.sub(r"color_discrete_sequence=\[.*?\]", f"color_discrete_sequence={pink_colors}", source)
    elif 'px.bar' in source or 'px.line' in source or 'px.area' in source:
        # Add color_discrete_sequence if missing but needed (e.g. multi-trace)
        if 'color=' in source and 'color_discrete_sequence' not in source:
             source = source.replace("title=", f"color_discrete_sequence={pink_colors}, title=")

    # Update color continuous scales for maps/heatmaps
    # For growth (Green/Red), maybe keep it or change to a Pink scale? 
    # User said "Black and Pink". Let's use a Pink gradient for heatmaps/shares.
    source = source.replace('color_continuous_scale="RdYlGn"', 'color_continuous_scale="RdPu"')
    source = source.replace('color_continuous_scale="RdBu"', 'color_continuous_scale="RdPu"')
    source = source.replace("color_continuous_scale='RdBu'", "color_continuous_scale='RdPu'")
    source = source.replace("cmap='RdBu'", "cmap='RdPu_r'") # Seaborn heatmaps

    return source

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        new_source = update_chart_colors(source)
        
        # Ensure 'plotly_dark' is the default if not already set per call
        if 'fig.update_layout' in new_source and 'template' not in new_source:
             new_source = new_source.replace('fig.update_layout(', "fig.update_layout(template='plotly_dark', ")

        cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in new_source.splitlines()]

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
