import nbformat as nbf
import os

def fix_outliers():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    modified = False
    for cell in nb.cells:
        # 1. Fix Cleaning Logic (Line 315 area)
        if 'year(pickup_datetime) BETWEEN 2010 AND 2026' in cell.source:
            print("Updating Cleaning Logic: 2010 -> 2016")
            cell.source = cell.source.replace('year(pickup_datetime) BETWEEN 2010 AND 2026', 
                                            'year(pickup_datetime) BETWEEN 2016 AND 2026')
            modified = True
        
        # 2. Fix Section 1.2.A Query (HVFHS 2019-2025)
        if 'FROM fhvhv_2019_2025_cleaned' in cell.source and 'WHERE' not in cell.source:
            print("Updating 1.2.A Query to include date filtering")
            # We need to insert WHERE clause into the UNION blocks
            new_source = cell.source.replace("FROM fhvhv_2019_2025_cleaned", "FROM fhvhv_2019_2025_cleaned\\nWHERE year(pickup_datetime) BETWEEN 2019 AND 2025")
            new_source = new_source.replace("FROM yellow_2019_2025_cleaned", "FROM yellow_2019_2025_cleaned\\nWHERE year(pickup_datetime) BETWEEN 2019 AND 2025")
            new_source = new_source.replace("FROM green_2019_2025_cleaned", "FROM green_2019_2025_cleaned\\nWHERE year(pickup_datetime) BETWEEN 2019 AND 2025")
            cell.source = new_source
            modified = True

    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Outlier filtering fixed successfully.")
    else:
        print("No outlier filtering patterns found to update.")

if __name__ == "__main__":
    fix_outliers()
