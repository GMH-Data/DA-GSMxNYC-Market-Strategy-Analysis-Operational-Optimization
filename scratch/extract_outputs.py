import json
import sys

# Set stdout to utf-8
sys.stdout.reconfigure(encoding='utf-8')

def extract_plotly_growth_data(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if '# [2.2.1.3]' in source:
                print("--- EXTRACTING PLOTLY DATA FOR 2.2.1.3 ---")
                for output in cell.get('outputs', []):
                    if output['output_type'] == 'display_data' and 'application/vnd.plotly.v1+json' in output['data']:
                        data = output['data']['application/vnd.plotly.v1+json']
                        title = data['layout'].get('title', {}).get('text', 'No Title')
                        print(f"\nChart: {title}")
                        for trace in data['data']:
                            provider = trace.get('name', 'Unknown')
                            x = trace.get('x', [])
                            y_data = trace.get('y', [])
                            
                            y = []
                            if isinstance(y_data, dict) and 'bdata' in y_data:
                                import base64
                                import numpy as np
                                decoded = base64.b64decode(y_data['bdata'])
                                y = np.frombuffer(decoded, dtype=np.float64).tolist()
                            else:
                                y = y_data
                                
                            print(f"[{provider}]")
                            for m, val in zip(x, y):
                                print(f"  {m}: {float(val):.2f}%")

extract_plotly_growth_data('Analysis.ipynb')
