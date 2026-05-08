import json
import re

def translate_text(text):
    # Dictionary for common translations based on previous context
    translations = {
        "Phân tích hoạt động kinh doanh": "Business Operation Analysis",
        "Dự báo tình hình kinh doanh": "Business Forecasting",
        "Hệ thống cảnh báo bất thường": "Anomaly Warning System",
        "Thành phần dữ liệu": "Data Components",
        "Chi tiết từ điển dữ liệu": "Data Dictionary Details",
        "Hoạt động kinh doanh của taxi": "Taxi business operations",
        "mức độ tăng trưởng qua các năm": "growth rate over the years",
        "tình hình kinh doanh trong tương lai": "future business conditions",
        "dựa trên dữ liệu lịch sử": "based on historical data",
        "thiết lập các chỉ số": "set indicators",
        "đưa ra cảnh báo kịp thời": "provide timely warnings",
        "đối với xe ấy": "for those vehicles",
        "trọng điểm": "key/high-volume",
        "thời gian chờ trung bình": "average wait time",
        "tỷ lệ ghép đôi": "shared match rate",
        "vùng trọng điểm": "key zones",
        "thị phần": "market share",
        "chỉ số vận hành": "operational metrics",
        "tài chính": "financial",
        "mô hình cảnh báo": "warning model",
        "vùng": "zone",
        "thời gian kết nối": "connection time",
        "nhanh nhất": "fastest",
        "chậm nhất": "slowest",
        "quãng đường trung bình": "average distance",
        "tỷ lệ ghép nối thành công": "successful shared match rate",
        "được lấy": "retrieved",
        "dữ liệu mới nhất": "latest data",
        "năm": "year",
        "tháng": "month",
        "chuyến đi": "trips",
        "tăng trưởng": "growth",
        "mật độ cạnh tranh": "competition density",
        "đối thủ": "competitors",
        "so sánh": "comparison",
        "tương quan": "correlation",
        "biểu đồ nhiệt": "heatmap",
        "ma trận": "matrix",
        "biến": "variables",
        "đặc trưng": "features",
        "dòng": "row",
        "cột": "column",
        "giá trị": "value",
        "trung bình": "average",
        "trung vị": "median",
        "lỗi": "error",
        "sửa lại": "fixed",
        "cập nhật": "updated",
        "phần": "section",
        "bản đồ": "map",
        "tĩnh": "static",
        "thông tin": "information",
        "chi tiết": "detailed",
        "tổng quan": "overview",
        "làm sạch dữ liệu": "data cleaning",
        "chuẩn hóa": "standardization",
        "xử lý": "processing",
        "hiệu quả": "efficient",
        "kết quả": "results",
        "thông báo": "notification",
        "ghi nhận": "recorded",
        "yêu cầu": "request",
        "khách hàng": "customer",
        "tài xế": "driver",
        "đón": "pickup",
        "trả": "dropoff",
        "giá cước": "fare",
        "tiền tip": "tips",
        "thu nhập": "income/pay",
        "khoảng cách": "distance",
        "thời gian": "time",
        "phút": "minutes",
        "giây": "seconds",
        "ngày": "day",
        "giờ": "hour"
    }
    
    # Simple replacement loop
    new_text = text
    for vn, en in translations.items():
        # Case insensitive replacement for whole words would be better but simple replace for now
        new_text = re.sub(rf'(?i){vn}', en, new_text)
    
    # Also handle some specific long sentences or patterns if needed
    new_text = new_text.replace("hãy đổi cho tôi thành biểu đồ biểu đồ area để dễ nhìn hơn nhé", "changed to area chart for better visibility")
    new_text = new_text.replace("sao chúng ta không dùng thời gian chờ để tìm xem thử tương quan với thị phần nhỉ", "why don't we use wait time to check correlation with market share?")
    new_text = new_text.replace("hãy cho tôi biểu đồ tương quan hình tam giác nhé để tôi muốn biết các feature có tương quan gì với nhau không", "give me a triangular correlation heatmap so I can see how features relate to each other")
    
    return new_text

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb['cells']:
    # Translate Markdown cells
    if cell['cell_type'] == 'markdown':
        source = ''.join(cell['source'])
        translated = translate_text(source)
        cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in translated.splitlines()]
    
    # Translate strings/comments in Code cells
    elif cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        # Translate comments (lines starting with #)
        new_lines = []
        for line in source.splitlines():
            if line.strip().startswith('#'):
                new_lines.append(translate_text(line))
            elif 'print(' in line or 'title=' in line or 'labels=' in line:
                # Attempt to translate strings within print or title
                new_lines.append(translate_text(line))
            else:
                new_lines.append(line)
        cell['source'] = [line + '\n' if not line.endswith('\n') else line for line in new_lines]

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
