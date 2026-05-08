import nbformat as nbf
import os

def fix_borough_casing_in_1_2_d():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # The issue is 'Borough' should be 'borough' based on the error message
    for cell in nb.cells:
        if cell.cell_type == 'code' and '# 1.2.D' in cell.source:
            # Replace 'Borough' with 'borough' in hover_data and color arguments
            cell.source = cell.source.replace("'Borough'", "'borough'").replace("color='Borough'", "color='borough'")
            break
            
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Fixed casing for 'borough' column in section 1.2.D.")

if __name__ == "__main__":
    fix_borough_casing_in_1_2_d()
