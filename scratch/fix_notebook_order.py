import nbformat as nbf
import os

def fix_order():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Find the target cells
    d_cell_idx = -1
    h_1_2_idx = -1
    
    for i, cell in enumerate(nb.cells):
        if '### D. Pre-2019 Location Analysis' in cell.source:
            d_cell_idx = i
        if '## 1.2. HVFHS Market Analysis (2019-2025)' in cell.source:
            h_1_2_idx = i

    if d_cell_idx != -1 and h_1_2_idx != -1:
        print(f"Moving cells from {d_cell_idx} to before {h_1_2_idx}")
        
        # Identify how many cells belong to Section D (until the next H2 or H1)
        cells_to_move = []
        # The section D includes the header and the code cells following it
        # Based on previous analysis, there were 2-3 cells (Markdown + 2 Code cells)
        # We stop when we see a "##" header or a significant "#" header
        
        current_idx = d_cell_idx
        while current_idx < len(nb.cells):
            source = nb.cells[current_idx].source
            if current_idx > d_cell_idx and ('## ' in source or '# ' in source.split('\n')[0]):
                break
            cells_to_move.append(nb.cells[current_idx])
            current_idx += 1
            
        # Remove the cells from their old position
        for _ in range(len(cells_to_move)):
            del nb.cells[d_cell_idx]
            
        # Recalculate insertion point (it might have changed if D was before 1.2, but here D is after 1.2)
        # Re-find 1.2 index because deletion might have shifted it
        new_1_2_idx = -1
        for i, cell in enumerate(nb.cells):
            if '## 1.2. HVFHS Market Analysis (2019-2025)' in cell.source:
                new_1_2_idx = i
                break
        
        # Insert before 1.2
        for i, cell in enumerate(cells_to_move):
            nb.cells.insert(new_1_2_idx + i, cell)
            
        # Optional: Rename D to C if it's now back under 1.1
        cells_to_move[0].source = cells_to_move[0].source.replace('### D.', '### C.')

        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Restructure fixed: Pre-2019 analysis moved to 1.1 section.")
    else:
        print(f"Indices not found: D={d_cell_idx}, 1.2={h_1_2_idx}")

if __name__ == "__main__":
    fix_order()
