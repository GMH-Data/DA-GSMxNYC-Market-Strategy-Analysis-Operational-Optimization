import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '1.3.B Final Model Validation' in ''.join(cell['source']):
        source_str = ''.join(cell['source'])
        
        # Replace the problematic lines
        old_lines = [
            "test_start_date = pd.Timestamp('2026-01-01')",
            "fig_val.add_vline(x=test_start_date, line_dash=\"dot\", line_color=\"yellow\", annotation_text=\"Test Set Start (2026)\")"
        ]
        
        new_lines = [
            "# Fix: Use millisecond timestamp to bypass Plotly/Pandas annotation bugs",
            "test_start_date_ms = pd.Timestamp('2026-01-01').timestamp() * 1000",
            "fig_val.add_vline(x=test_start_date_ms, line_dash=\"dot\", line_color=\"yellow\", annotation_text=\"Test Set Start (2026)\")"
        ]
        
        if old_lines[0] in source_str:
            source_str = source_str.replace(old_lines[0], new_lines[0] + "\n" + new_lines[1])
            source_str = source_str.replace(old_lines[1], new_lines[2])
            
            # Put back as list of lines with newlines
            cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in source_str.split('\n')]
            # Clean up empty lines created by split
            if cell['source'][-1] == '\n':
                cell['source'].pop()
        break

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
