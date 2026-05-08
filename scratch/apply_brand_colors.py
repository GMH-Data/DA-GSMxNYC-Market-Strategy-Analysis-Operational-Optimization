import json
import re

def update_brand_colors(source):
    # Mapping for brand colors
    # Uber: White/Silver (for dark mode), Lyft: Pink
    brand_map = "{'Uber': '#FFFFFF', 'Lyft': '#FF00BF', 'HV0003': '#FFFFFF', 'HV0005': '#FF00BF'}"
    
    # 1. Update px charts that use color='provider' or color='yr' (if applicable)
    # If the chart is comparing providers, use the brand map
    if 'provider' in source or 'hvfhs_license_num' in source:
        if 'color=' in source and 'color_discrete_map' not in source:
            source = source.replace("color='provider'", f"color='provider', color_discrete_map={brand_map}")
            source = source.replace("color='hvfhs_license_num'", f"color='hvfhs_license_num', color_discrete_map={brand_map}")
        elif 'color_discrete_map' in source:
            # Update existing map
            source = re.sub(r"color_discrete_map=\{.*?\}", f"color_discrete_map={brand_map}", source)

    # 2. Specific fixes for sections
    # Area chart in 1.2.E.3 (facet_col='provider')
    if 'facet_col=\'provider\'' in source:
        # For faceted charts, the color is often by 'yr'. 
        # But if we want to show Uber as White and Lyft as Pink traces...
        pass # px.area usually colors by the 'color' argument

    # 3. Market Share Correlation Heatmaps (Section 1.2.1.C)
    # Uber Heatmap -> Silver/Gray, Lyft Heatmap -> Pink
    if 'sns.heatmap' in source:
        if 'Uber Market Share' in source or 'Uber Share' in source:
             source = source.replace("cmap='RdPu_r'", "cmap='Greys'") # Silver/Black for Uber
        if 'Lyft Market Share' in source or 'Lyft Share' in source:
             source = source.replace("cmap='RdPu_r'", "cmap='PuRd'") # Pink for Lyft

    return source

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        new_source = update_brand_colors(source)
        cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in new_source.splitlines()]

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
