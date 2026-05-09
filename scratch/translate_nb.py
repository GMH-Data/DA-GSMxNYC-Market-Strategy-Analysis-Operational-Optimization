import json
import re

def translate_text(text):
    if not isinstance(text, str):
        return text
    
    # Mapping of full phrases (prioritize longer phrases)
    phrases = {
        "Chung ta using": "We use",
        "de tu dong quet": "to automatically scan",
        "The file Parquet trong thu muc": "Parquet files in the directory",
        "and tao The View tuong ung cho tung period": "and create corresponding Views for each period",
        "TONG QUAN Data GOC BAN DAU (RAW DATA):": "INITIAL RAW DATA OVERVIEW:",
        "TONG conG Data GOC:": "TOTAL RAW DATA:",
        "Tu dong reload The module tu": "Automatically reload modules from",
        "Bo loc chat che: Chi lay The using has cau truc": "Strict filter: Only take tables with structure",
        "and not chua The tu khoa cua Model": "and not containing Model keywords",
        "Rules: Phai has The tu khoa ve Time and not has tu khoa ve model": "Rules: Must have Time keywords and not have model keywords",
        "STARTING XAY DUNG _FINAL VIEWS TU RAW DATA...": "STARTING TO BUILD _FINAL VIEWS FROM RAW DATA...",
        "Data Pipeline: Chuan hoa, Lam sach & Imputation (All-in-one View)": "Data Pipeline: Standardization, Cleaning & Imputation (All-in-one View)",
        "Lay danh sach using goc": "Get raw table list",
        "Xoa The view trung gian cu neu ton tai de don dep Database": "Delete old intermediate views if they exist to clean up the Database",
        "Tao using statistics truc quan": "Create visual statistics table",
        "RESULTS DATA PIPELINE (Da Removed": "DATA PIPELINE RESULTS (Removed",
        "DA KHOI TAO XONG The using DIMENSIONS (ZONES, SERVICE_TYPES, CALENDAR).": "DIMENSIONS INITIALIZED (ZONES, SERVICE_TYPES, CALENDAR).",
        "Phan loai hang xe": "Vehicle category classification",
        "using lich": "calendar table",
        "Phan nay perform The phan tich khai pha Data de hieu ro more about thi truong taxi NYC, bao gom toc do growth (Market Growth), Market Share (Market Share), and xu huong tai chinh (Financial Trends).": "This section performs exploratory data analysis to better understand the NYC taxi market, including growth rate (Market Growth), Market Share, and financial trends (Financial Trends).",
        "Setup cho EDA": "Setup for EDA",
        "Theme colors by chuan": "Standard theme colors",
        "Phan tich period tien Uber/Lyft dominated (2015-2018), tap trung vao su Shift tu Taxi truyen tmoreg sang FHV.": "Analyze the pre-Uber/Lyft dominance period (2015-2018), focusing on the shift from traditional Taxi to FHV.",
        "Danh gia quy mo thi truong hang thang and su change ty trong between The loai hinh Service before and after hast moc quan trọng nam 2017.": "Evaluate monthly market scale and changes in share between service types before and after the 2017 milestone.",
        "So sanh gia thanh moi dam (Fare per Mile)": "Fare per Mile Comparison",
        "Phân tích Tốc độ tăng trưởng MoM của Uber và Lyft": "MoM Growth Rate Analysis of Uber and Lyft",
        "Toc do tang truong trung binh cua Uber va Lyft": "Average Growth Rate of Uber and Lyft",
        "Bảng tương quan ảnh hưởng tới tốc độ tăng trưởng.": "Correlation table affecting growth rate.",
        "Phân tích Ma trận tương quan (Drivers of Market Share & Growth)": "Correlation Matrix Analysis (Drivers of Market Share & Growth)",
    }

    for vn, en in phrases.items():
        text = text.replace(vn, en)

    # Word-based replacements to avoid "Yeare" (Name -> Year-e)
    # Mapping for words that should be replaced only as words or in specific contexts
    word_mapping = {
        "dong": "rows",
        "thanh cong": "successfully",
        "SUCCESS": "SUCCESS", # Keep
        "Ket noi": "Connect",
        "Lay danh sach": "Get list",
        "Bo loc": "Filter",
        "Xay dung": "Build",
        "Chuan hoa": "Standardize",
        "Lam sach": "Clean",
        "Khoi tao": "Initialize",
        "Phan loai": "Classify",
        "Bieu do": "Chart/Plot",
        "Tuong quan": "Correlation",
        "Anh huong": "Influence/Affect",
        "Tang truong": "Growth",
        "Giam": "Decline",
        "Trung binh": "Average",
        "thang": "month",
        "nam": "year",
        "giua": "between",
        "truoc": "before",
        "sau": "after",
    }

    # Use regex with word boundaries for word-based mapping
    for vn, en in word_mapping.items():
        # Match word if it's not part of another word (e.g. "Name" contains "nam")
        # We also need to handle the case where "nam" might be part of "Vietnam" (keep)
        # But here most "nam" are "year" or in "Name" (if already processed incorrectly)
        
        # If we see "Yeare", fix it back to "Name"
        text = text.replace("Yeare", "Name")
        
        # Replace only if it's a stand-alone word (with case sensitivity options)
        pattern = r'\b' + re.escape(vn) + r'\b'
        text = re.compile(pattern, re.IGNORECASE).sub(lambda m: en if m.group().islower() else en.capitalize(), text)

    # Specific fix for "dong" in number contexts like "1,000 dong"
    text = re.sub(r'(\d[\d,]*)\s+dong', r'\1 rows', text)

    return text

def process_notebook(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if 'source' in cell:
            cell['source'] = [translate_text(line) for line in cell['source']]
        
        if 'outputs' in cell:
            for output in cell['outputs']:
                if 'text' in output:
                    if isinstance(output['text'], list):
                        output['text'] = [translate_text(line) for line in output['text']]
                    else:
                        output['text'] = translate_text(output['text'])
                if 'data' in output:
                    for mime, content in output['data'].items():
                        if mime in ['text/plain', 'text/html']:
                            if isinstance(content, list):
                                output['data'][mime] = [translate_text(line) for line in content]
                            else:
                                output['data'][mime] = translate_text(content)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    process_notebook('Analysis.ipynb', 'Analysis.ipynb')
