import json

notebook_path = 'Analysis.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find positions for 2.2.1.3 and 2.2.1.4
idx_2_2_1_3 = -1
idx_2_2_1_4 = -1

for i, cell in enumerate(nb['cells']):
    source_str = "".join(cell.get('source', []))
    if "# [2.2.1.3]" in source_str:
        idx_2_2_1_3 = i
    if "# [2.2.1.4]" in source_str:
        idx_2_2_1_4 = i

# Insert description for 2.2.1.3
if idx_2_2_1_3 != -1:
    desc_2_2_1_3 = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2.2.1.3. Phân tích Tốc độ tăng trưởng MoM của Uber và Lyft\n",
            "Phần này đánh giá khả năng phục hồi và độ ổn định của hai nền tảng gọi xe lớn nhất NYC. \n",
            "- **Uber**: Thể hiện sự ổn định cao với mạng lưới tài xế rộng.\n",
            "- **Lyft**: Có độ biến động (Volatility) cao hơn, thường nhạy cảm hơn với các thay đổi chính sách giá."
        ]
    }
    nb['cells'].insert(idx_2_2_1_3, desc_2_2_1_3)
    idx_2_2_1_4 += 1 # Adjust index after insertion

# Insert description for 2.2.1.4
if idx_2_2_1_4 != -1:
    desc_2_2_1_4 = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### 2.2.1.4. Phân tích Ma trận tương quan (Drivers of Market Share & Growth)\n",
            "Ma trận này giúp xác định các yếu tố vận hành tác động mạnh nhất đến kết quả kinh doanh. Các nhóm đặc trưng bao gồm:\n",
            "1. **Yếu tố Tài xế**: Thu nhập tài xế (`avg_driver_pay`) và Thời gian chờ (`avg_wait_time_min`).\n",
            "2. **Yếu tố Kinh tế**: Giá vé (`avg_fare`) và Tổng chi phí khách trả (`avg_total_cost`).\n",
            "3. **Hiệu suất vận hành**: Quãng đường (`avg_distance`) và Thời gian chuyến đi (`avg_duration_min`).\n",
            "4. **Đặc trưng Dịch vụ**: Tỷ lệ đi chung (`shared_req_rate`) và xe đặc thù (`wav_req_rate`)."
        ]
    }
    nb['cells'].insert(idx_2_2_1_4, desc_2_2_1_4)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook updated with markdown descriptions for sections 2.2.1.3 and 2.2.1.4.")
