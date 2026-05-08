import nbformat as nbf
import os

def fix_crs_in_1_2_d():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    for cell in nb.cells:
        if cell.cell_type == 'code' and '# 1.2.D' in cell.source:
            # Add to_crs(epsg=4326) right after reading the shapefile
            old_code = "gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp')"
            new_code = "gdf = gpd.read_file('Dataset/taxi_zones/taxi_zones.shp').to_crs(epsg=4326)"
            cell.source = cell.source.replace(old_code, new_code)
            break
            
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print("Fixed CRS projection issue in section 1.2.D.")

if __name__ == "__main__":
    fix_crs_in_1_2_d()
