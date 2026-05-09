import json
import re

def repair_text(text):
    if not isinstance(text, str):
        return text
    
    # Very specific repairs first
    repairs = {
        "monthyeare": "monthname",
        "dayyeare": "dayname",
        "yeare = t[0]": "name = t[0]",
        "possible_yeares": "possible_names",
        "service_type_yeare": "service_type_name",
        "day_yeare": "day_name",
        "index_yeare": "index_name",
        "column_yeare": "column_name",
        "Table Yeare": "Table Name",
    }
    for bad, good in repairs.items():
        text = text.replace(bad, good)

    # Use regex for more general but safe variable/key replacements
    # Replace 'yeare' with 'name' when it's a stand-alone variable or dict key
    # Cases like: [yeare], {yeare}, as yeare, f"...{yeare}..."
    text = re.sub(r'(\W)yeare(\W)', r'\1name\2', text)
    
    return text

def process_notebook(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if 'source' in cell:
            cell['source'] = [repair_text(line) for line in cell['source']]
        
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'text' in output:
                    if isinstance(output['text'], list):
                        output['text'] = [repair_text(line) for line in output['text']]
                    else:
                        output['text'] = repair_text(output['text'])
                if 'data' in output:
                    for mime, content in output['data'].items():
                        if mime in ['text/plain', 'text/html']:
                            if isinstance(content, list):
                                output['data'][mime] = [repair_text(line) for line in content]
                            else:
                                output['data'][mime] = repair_text(content)
                if 'traceback' in output:
                    output['traceback'] = [repair_text(line) for line in output['traceback']]
                if 'evalue' in output:
                    output['evalue'] = repair_text(output['evalue'])

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    process_notebook('Analysis.ipynb', 'Analysis.ipynb')
