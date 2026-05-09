
import json
import re

def extract_notebook_map(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    code_map = []
    
    for cell in nb['cells']:
        cell_type = cell['cell_type']
        source = cell['source']
        if not source:
            continue
            
        content = "".join(source).strip()
        
        if cell_type == 'markdown':
            # Tìm các tiêu đề #, ##, ###, ####
            match = re.match(r'^(#{1,6})\s+(.*)', content)
            if match:
                level = len(match.group(1))
                title = match.group(2)
                code_map.append({
                    'type': 'markdown',
                    'level': level,
                    'title': title,
                    'id': cell.get('id', 'N/A')
                })
        
        elif cell_type == 'code':
            # Tìm header code cell theo chuẩn # [X.X.X] Title
            first_line = source[0].strip()
            match = re.match(r'^#\s*\[(.*?)\]\s*(.*)', first_line)
            if match:
                tag = match.group(1)
                title = match.group(2)
                code_map.append({
                    'type': 'code',
                    'tag': tag,
                    'title': title,
                    'id': cell.get('id', 'N/A')
                })

    return code_map

def format_as_markdown(code_map):
    md = "# Analysis.ipynb Code Map\n\n"
    md += "This document maps the logical structure of `Analysis.ipynb` for rapid access and navigation.\n\n"
    
    for item in code_map:
        if item['type'] == 'markdown':
            indent = "  " * (item['level'] - 1)
            prefix = "#" * item['level']
            md += f"{indent}- {prefix} {item['title']} (ID: `{item['id']}`)\n"
        elif item['type'] == 'code':
            md += f"    - [CODE] `[{item['tag']}]` {item['title']} (ID: `{item['id']}`)\n"
            
    return md

mapping = extract_notebook_map('Analysis.ipynb')
md_content = format_as_markdown(mapping)

with open('.agents/rules/code-map.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print("Code map generated successfully at .agents/rules/code-map.md")
