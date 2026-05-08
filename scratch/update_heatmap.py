import json
import numpy as np

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '1.2.1.C Correlation Analysis: Uber, Lyft & Taxi' in ''.join(cell['source']):
        source = ''.join(cell['source'])
        
        # Add import numpy if not present
        if 'import numpy as np' not in source:
            source = 'import numpy as np\n' + source
            
        addition = """
# 4. Full Triangular Correlation Heatmap
plt.figure(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdBu', center=0, fmt='.2f')
plt.title('Triangular Correlation Matrix: All Features')
plt.show()
"""
        if 'Full Triangular Correlation Heatmap' not in source:
            new_source = source + addition
        else:
            new_source = source
            
        lines = []
        for line in new_source.splitlines(True):
            lines.append(line)
        cell['source'] = lines
        break

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
