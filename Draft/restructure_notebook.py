import nbformat
import re

def translate_text(text):
    # Mapping of common Vietnamese phrases to English
    mapping = {
        "ẢNH HƯỞNG CỦA CÁC YẾU TỐ (BAO GỒM TÀI XẾ) ĐẾN THỊ PHẦN": "INFLUENCE OF FACTORS (INCLUDING DRIVERS) ON MARKET SHARE",
        "PHÂN TÍCH TƯƠNG QUAN CHI TIẾT (DRIVER & MARKET FACTORS)": "DETAILED CORRELATION ANALYSIS (DRIVER & MARKET FACTORS)",
        "Kiem tra danh sach columns thuc te co trong View de toi uu hoa phan tich": "Check actual column list in View to optimize analysis",
        "Dinh nghia potential metrics (bao gom ca Driver & Service factors)": "Define potential metrics (including Driver & Service factors)",
        "Chi lay metrics ma columns du lieu nguon ton tai": "Only include metrics where source columns exist",
        "Kiem tra xem columns khoa trong bieu thuc co trong actual_cols khong": "Check if required columns exist in actual_cols",
        "Chi lay numeric columns so lieu de tinh Correlation": "Only take numeric columns for Correlation calculation",
        "Hien thi rut gon tap trung vao Market Share & Daily Growth": "Display concise view focusing on Market Share & Daily Growth",
        "Tong quan Data goc": "Raw Data Overview",
        "Data goc": "Raw Data",
        "Tong quan": "Overview",
        "Da Removed": "Removed",
        "Ket qua": "Results",
        "thanh cong": "successfully",
        "Loi": "Error",
        "truy van": "query",
        "mo ta": "description",
        "cot": "column",
        "dong": "row",
        "bang": "table",
        "Kiem tra": "Check",
        "Dinh nghia": "Define",
    }
    
    # Word-based mapping for short words to avoid corruption (like ve -> about inside words)
    word_mapping = {
        "ve": "about",
        "Neu": "If",
        "thi": "then",
        "hoac": "or",
        "mac dinh": "default",
        "du lieu": "data",
        "nguon": "source",
        "khoa": "key",
        "thiet lap": "setup",
        "khoi tao": "initialize",
        "truy cap": "access",
        "hang month": "monthly",
        "hang year": "yearly",
        "quy mo market": "market scale",
        "su phan chia": "division",
        "So sanh": "Compare",
        "luong chuyen xe": "trip volume",
        "tung": "each",
        "duoc": "get",
        "thanh": "to",
        "canh tranh": "competition",
        "nha cung cap": "provider",
        "tuyet doi": "absolute",
        "danh dau": "mark",
        "giai doan": "period",
        "The Service": "the service",
        "goi xe cong nghe": "ride-hailing",
        "chung ta se": "we will",
        "thong ke": "statistics",
        "hien thi": "display",
        "bieu do": "chart",
        "The diem": "point",
        "nhieu": "many",
        "cuc doan": "extreme",
        "dau": "early",
        "Tai using": "Using",
        "tu cell before": "from previous cell",
        "moi segment": "each segment",
        "phan chia": "split",
        "giua": "between",
        "Peak Month": "Peak Month",
    }
    
    new_text = text
    # Apply long mapping first
    for vn, en in mapping.items():
        new_text = re.sub(re.escape(vn), en, new_text, flags=re.IGNORECASE)
    
    # Apply word-based mapping using word boundaries
    for vn, en in word_mapping.items():
        # Match as whole word or with specific boundaries
        pattern = r'\b' + re.escape(vn) + r'\b'
        new_text = re.sub(pattern, en, new_text, flags=re.IGNORECASE)
    
    # Cleanup accidental corruptions if any were already made (e.g., Noaboutmber -> November)
    # Since I'm running this on the ALREADY corrupted file, I should fix them.
    cleanup = {
        "Noaboutmber": "November",
        "aboabout": "above",
        "Driaboutrs": "Drivers",
        "Oaboutrall": "Overall",
        "competitiabout": "competitive",
        "hasmpetitiabout": "competitive",
        "Dyyearics": "Dynamics",
    }
    for bad, good in cleanup.items():
        new_text = new_text.replace(bad, good)
        
    return new_text

def process_notebook(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    for cell in nb.cells:
        if 'source' in cell:
            cell['source'] = translate_text(cell['source'])
        if 'outputs' in cell:
            for output in cell['outputs']:
                if output.output_type == 'stream' and 'text' in output:
                    output['text'] = translate_text(output['text'])
                elif output.output_type == 'display_data' and 'data' in output:
                    if 'text/plain' in output['data']:
                        output['data']['text/plain'] = translate_text(output['data']['text/plain'])
                    if 'text/html' in output['data']:
                        output['data']['text/html'] = translate_text(output['data']['text/html'])
    
    with open(output_file, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    process_notebook('Analysis.ipynb', 'Analysis.ipynb')
    print("Notebook restructured, translated and corruption fixed.")
