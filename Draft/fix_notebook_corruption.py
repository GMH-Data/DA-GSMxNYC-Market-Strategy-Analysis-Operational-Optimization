import json
import os

# Define the mapping of corrupted terms to their correct versions
REPLACEMENTS = {
    "hoaboutrmode": "hovermode",
    "reaboutnue": "revenue",
    "Reaboutnue": "Revenue",
    "Remoaboutd": "Removed",
    "haabout": "have",
    "aboutndor": "vendor",
    "abouthicle": "vehicle",
    "Comprehensiabout": "Comprehensive",
    "aboutndorID": "vendorID",
    "aboutndor_id": "vendor_id",
    "about quy mo": "about scale",
    "remoaboutd": "removed",
    "hoaboutr": "hover"
}

def fix_notebook(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    changed_count = 0
    for cell in nb['cells']:
        if 'source' in cell:
            new_source = []
            for line in cell['source']:
                original_line = line
                for corrupted, fixed in REPLACEMENTS.items():
                    line = line.replace(corrupted, fixed)
                
                if line != original_line:
                    changed_count += 1
                new_source.append(line)
            cell['source'] = new_source

    if changed_count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
        print(f"Successfully fixed {changed_count} occurrences in {file_path}")
    else:
        print("No corruptions found to fix.")

if __name__ == "__main__":
    fix_notebook('Analysis.ipynb')
