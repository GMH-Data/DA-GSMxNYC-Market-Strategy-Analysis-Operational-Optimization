import json

def update_notebook(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    target_header = "# 1.2. Database Overview: Raw Tables Summary"
    found = False
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_content = "".join(cell['source'])
            if target_header in source_content:
                # Update the filter logic
                new_source = []
                for line in cell['source']:
                    if 'not t.endswith("_cleaned")' in line:
                        line = line.replace('not t.endswith("_cleaned")', 'not t.endswith(("_cleaned", "_std"))')
                    if 'exclude \'_cleaned\'' in line:
                        line = line.replace('exclude \'_cleaned\'', "exclude '_cleaned', '_std'")
                    new_source.append(line)
                cell['source'] = new_source
                found = True
                break
    
    if found:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print("Successfully updated cell 1.2 in Data.ipynb")
    else:
        print("Could not find the target cell in Data.ipynb")

if __name__ == "__main__":
    update_notebook("Data.ipynb")
