import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

notebook_path = 'Analysis.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("--- START EXTRACT ---")
for i, cell in enumerate(nb['cells']):
    source_str = "".join(cell.get('source', []))
    if "# [2.2.1.3]" in source_str or "# [2.2.1.4]" in source_str:
        print(f"CELL {i}")
        for output in cell.get('outputs', []):
            if 'text' in output:
                print("STDOUT:")
                print("".join(output['text']))
            if 'data' in output:
                if 'text/html' in output['data']:
                    print("HTML_TABLE_START")
                    print("".join(output['data']['text/html']))
                    print("HTML_TABLE_END")
print("--- END EXTRACT ---")
