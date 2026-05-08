import nbformat as nbf
import os

def clean_and_reorder_1_2():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # 1. Categories of cells to keep
    # We will identify cells based on their content
    content_map = {
        'A': {'header': None, 'code': None, 'id_header': '### A. Quy mô', 'id_code': '# 1.2.A'},
        'B': {'header': None, 'code': None, 'id_header': '### B. Tỷ lệ thị phần', 'id_code': '# 1.2.B'},
        'C': {'header': None, 'code': [], 'id_header': '### C. Correlation Analysis', 'id_code': 'Correlation Analysis: Uber & Lyft'}, # C might have multiple code cells (Taxi too)
        'D': {'header': None, 'code': None, 'id_header': '### D. Khu vực cạnh tranh', 'id_code': '# 1.2.D Competition Analysis: Uber vs Lyft Detailed'},
        'E': {'header': None, 'code': None, 'id_header': '### E. Temporal Competition Analysis', 'id_code': '# 1.2.E Temporal Competition Analysis'},
        'F': {'header': None, 'code': None, 'id_header': '### F. Market Share Comparison: Trips vs Revenue', 'id_code': '# 1.2.F Market Share Comparison'}
    }
    
    # 2. Extract and Deduplicate
    # We will iterate through all cells and pick the best version of each
    i = 0
    clean_cells = []
    
    # First, let's find the boundaries of Section 1.2
    idx_start_1_2 = -1
    idx_end_1_2 = -1
    for i, cell in enumerate(nb.cells):
        if '## 1.2. HVFHS Market Analysis' in cell.source:
            idx_start_1_2 = i
        if '## 1.3.' in cell.source:
            idx_end_1_2 = i
            break
            
    if idx_start_1_2 == -1:
        print("Could not find start of 1.2")
        return

    # Extract all cells NOT in 1.2 for now
    before_1_2 = nb.cells[:idx_start_1_2+1]
    after_1_2 = nb.cells[idx_end_1_2:] if idx_end_1_2 != -1 else []
    
    # Inside 1.2, categorize
    section_1_2_cells = nb.cells[idx_start_1_2+1 : idx_end_1_2] if idx_end_1_2 != -1 else nb.cells[idx_start_1_2+1:]
    
    for cell in section_1_2_cells:
        src = cell.source
        if cell.cell_type == 'markdown':
            if '### A. Quy mô' in src: content_map['A']['header'] = cell
            elif '### B. Tỷ lệ thị phần' in src: content_map['B']['header'] = cell
            elif '### C. Correlation Analysis' in src: content_map['C']['header'] = cell
            elif '### D. Khu vực cạnh tranh' in src or '### D. Correlation Analysis' in src: 
                # If D was renamed to Correlation, we fix it
                cell.source = "### D. Competition Analysis: Uber vs Lyft Detailed\nCác bản đồ trực quan hóa chi tiết về khu vực cạnh tranh và danh sách Top 10 Zone."
                content_map['D']['header'] = cell
            elif '### E. Temporal Competition Analysis' in src: content_map['E']['header'] = cell
            elif '### F. Market Share Comparison' in src: content_map['F']['header'] = cell
        elif cell.cell_type == 'code':
            if '# 1.2.A' in src: content_map['A']['code'] = cell
            elif '# 1.2.B' in src: content_map['B']['code'] = cell
            elif 'Correlation Analysis: Uber & Lyft' in src: content_map['C']['code'].append(cell)
            elif 'Correlation Analysis: Yellow & Green' in src: content_map['C']['code'].append(cell)
            elif 'Competition Analysis: Uber vs Lyft Detailed' in src: content_map['D']['code'] = cell
            elif 'Temporal Competition Analysis' in src: content_map['E']['code'] = cell
            elif 'Market Share Comparison: Trip Volume' in src: content_map['F']['code'] = cell

    # 3. Rebuild 1.2
    ordered_1_2 = []
    for key in ['A', 'B', 'C', 'D', 'E', 'F']:
        data = content_map[key]
        if data['header']: 
            # Fix header numbering just in case
            if key == 'C': data['header'].source = "### C. Correlation Analysis"
            if key == 'D': data['header'].source = "### D. Competition Analysis: Uber vs Lyft Detailed"
            if key == 'E': data['header'].source = "### E. Temporal Competition Analysis"
            if key == 'F': data['header'].source = "### F. Market Share Comparison: Trips vs Revenue"
            ordered_1_2.append(data['header'])
        
        if isinstance(data['code'], list):
            for c in data['code']: ordered_1_2.append(c)
        elif data['code']:
            ordered_1_2.append(data['code'])

    # 4. Save
    nb.cells = before_1_2 + ordered_1_2 + after_1_2
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Notebook cleanup complete: Section 1.2 is now perfectly ordered A to F.")

if __name__ == "__main__":
    clean_and_reorder_1_2()
