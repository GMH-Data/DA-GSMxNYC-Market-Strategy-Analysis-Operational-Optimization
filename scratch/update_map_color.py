import nbformat as nbf
import os

def update_color_scale():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'color_continuous_scale="RdBu"' in cell.source:
            # Changing to Viridis for better readability and a professional look
            cell.source = cell.source.replace('color_continuous_scale="RdBu"', 'color_continuous_scale="Viridis"')
            found = True
            break
    
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Updated color scale to Viridis.")
    else:
        print("Could not find the previous color scale setting.")

if __name__ == "__main__":
    update_color_scale()
