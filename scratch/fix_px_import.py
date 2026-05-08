import json

def fix_imports(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # 1. Add to Environment Setup (Cell 1.1)
    setup_header = "## 1.1. Environment Setup & DB Initialization"
    found_setup = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown' and any(setup_header in line for line in cell['source']):
            found_setup = True
            continue
        if found_setup and cell['cell_type'] == 'code':
            if not any("import plotly.express as px" in line for line in cell['source']):
                # Insert after standard imports
                new_source = []
                for line in cell['source']:
                    new_source.append(line)
                    if "import seaborn as sns" in line:
                        new_source.append("import plotly.express as px\n")
                cell['source'] = new_source
            found_setup = False # Done with setup cell
    
    # 2. Also check the specific failing cell (1.3.2) and add it there just in case for independence
    target_header = "# 1.3.1.2 Row Filtering: Cleaning Invalid Records"
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_content = "".join(cell['source'])
            if target_header in source_content:
                if not any("import plotly.express as px" in line for line in cell['source']):
                    cell['source'].insert(1, "import plotly.express as px\n")
                break

    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Successfully added plotly.express imports to Data.ipynb")

if __name__ == "__main__":
    fix_imports("Data.ipynb")
