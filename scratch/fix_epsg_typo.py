import nbformat as nbf
import os

def fix_epsg_in_notebook():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'epsg=4321' in cell.source:
            cell.source = cell.source.replace('epsg=4321', 'epsg=4326')
            found = True
            break
    
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Fixed EPSG code from 4321 to 4326.")
    else:
        print("Could not find the erroneous EPSG code.")

if __name__ == "__main__":
    fix_epsg_in_notebook()
