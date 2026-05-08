import nbformat as nbf
import os

def reorder_1_2_sections():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Identifiers
    header_d = '### D. Correlation Analysis' # Wait, D was Competition Areas in last step
    # Let's use the sources to identify
    
    idx_d_end = -1
    cells_temporal = []
    cells_revenue = []
    
    # 1. Identify and extract cells
    # Part D: Competition Areas (Restructured)
    # Part E (Revenue)
    # Part F (Temporal)
    
    new_cells = []
    other_cells = []
    
    i = 0
    while i < len(nb.cells):
        cell = nb.cells[i]
        source = cell.source
        
        if '### E. Market Share Comparison: Trips vs Revenue' in source or '# 1.2.E Market Share Comparison' in source:
            # This is the Revenue part (currently E, will be F)
            cells_revenue.append(nb.cells[i]) # Header
            cells_revenue.append(nb.cells[i+1]) # Code
            i += 2
            continue
            
        if '### F. Temporal Competition Analysis' in source or '# 1.2.F Temporal Competition Analysis' in source:
            # This is the Temporal part (currently F, will be E)
            cells_temporal.append(nb.cells[i]) # Header
            cells_temporal.append(nb.cells[i+1]) # Code
            i += 2
            continue
            
        new_cells.append(cell)
        i += 1

    # 2. Find insertion point after 1.2.D
    # Section D usually ends after the Top 10 DF code cell
    insert_pos = -1
    for i, cell in enumerate(new_cells):
        if cell.cell_type == 'code' and '# 1.2.D.2 Market Share Summary' in cell.source:
            insert_pos = i + 1
            break
            
    if insert_pos != -1:
        # Update headers
        cells_temporal[0].source = "### E. Temporal Competition Analysis: Time of Day & Year\nPhân tích sự thay đổi của mật độ cạnh tranh theo các khung giờ trong ngày và các tháng trong năm."
        cells_temporal[1].source = cells_temporal[1].source.replace('# 1.2.F', '# 1.2.E')
        
        cells_revenue[0].source = "### F. Market Share Comparison: Trips vs Revenue\nSo sánh sự khác biệt giữa thị phần theo số lượng chuyến đi và thị phần theo doanh thu để đánh giá hiệu quả kinh tế của từng hãng."
        cells_revenue[1].source = cells_revenue[1].source.replace('# 1.2.E', '# 1.2.F')
        
        # Insert Temporal (now E) after D
        for cell in reversed(cells_temporal):
            new_cells.insert(insert_pos, cell)
            
        # Find the end of 1.2 section to put Revenue (now F)
        # Actually we can just append it if nothing else is after 1.2
        # But to be safe, let's find the header for 1.3
        h13_pos = -1
        for i, cell in enumerate(new_cells):
            if '## 1.3.' in cell.source:
                h13_pos = i
                break
        
        if h13_pos != -1:
            for cell in reversed(cells_revenue):
                new_cells.insert(h13_pos, cell)
        else:
            new_cells.extend(cells_revenue)
            
        nb.cells = new_cells
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Notebook reordered: Temporal is 1.2.E, Revenue is 1.2.F.")
    else:
        print("Could not find section 1.2.D end point.")

if __name__ == "__main__":
    reorder_1_2_sections()
