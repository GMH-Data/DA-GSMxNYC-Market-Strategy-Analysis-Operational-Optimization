import json

notebook_path = 'Analysis.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

target_index = -1
for i, cell in enumerate(nb['cells']):
    source_str = "".join(cell.get('source', []))
    if "# [2.2.1.4]" in source_str:
        target_index = i
        break

if target_index != -1:
    new_source = [
        "# [2.2.1.4] Bảng tương quan ảnh hưởng tới tốc độ tăng trưởng.\n",
        "# Kiem tra danh sach cot thuc te co trong View de toi uu hoa phan tich\n",
        "actual_cols = con.execute(\"DESCRIBE fhvhv_2019_2025_final\").df()['column_name'].tolist()\n",
        "\n",
        "# Dinh nghia cac chi so tiem nang (bao gom ca cac yeu to ve Tai xe & Dich vu)\n",
        "potential_metrics = {\n",
        "    'avg_fare': 'avg(fare_amount)',\n",
        "    'avg_distance': 'avg(trip_distance)',\n",
        "    'avg_tip': 'avg(tip_amount)',\n",
        "    'avg_total_cost': 'avg(total_amount)',\n",
        "    'avg_duration_min': \"avg(extract('epoch' from (dropoff_datetime - pickup_datetime))) / 60.0\",\n",
        "    'avg_driver_pay': 'avg(driver_pay)',\n",
        "    'avg_wait_time_min': \"avg(extract('epoch' from (pickup_datetime - request_datetime))) / 60.0\",\n",
        "    'shared_req_rate': \"count(CASE WHEN shared_request_flag = 'Y' THEN 1 END) * 100.0 / count(*)\",\n",
        "    'wav_req_rate': \"count(CASE WHEN wav_request_flag = 'Y' THEN 1 END) * 100.0 / count(*)\"\n",
        "}\n",
        "\n",
        "# Chi lay cac chi so ma cot du lieu nguon ton tai\n",
        "available_metrics = {}\n",
        "for name, expr in potential_metrics.items():\n",
        "    # Kiem tra xem cot khoa trong bieu thuc co trong actual_cols khong\n",
        "    needed_cols = [c for c in ['driver_pay', 'request_datetime', 'shared_request_flag', 'wav_request_flag'] if c in expr]\n",
        "    if all(c in actual_cols for c in needed_cols):\n",
        "        available_metrics[name] = expr\n",
        "\n",
        "select_clause = \", \".join([f\"{expr} as {name}\" for name, expr in available_metrics.items()])\n",
        "\n",
        "query_growth_corr = f\"\"\"\n",
        "WITH daily_metrics AS (\n",
        "    SELECT \n",
        "        date_trunc('day', pickup_datetime) as date,\n",
        "        vendor_id,\n",
        "        count(*) as trips,\n",
        "        {select_clause}\n",
        "    FROM fhvhv_2019_2025_final\n",
        "    WHERE vendor_id IN ('HV0003', 'HV0005')\n",
        "    GROUP BY 1, 2\n",
        "),\n",
        "market_total AS (\n",
        "    SELECT date, sum(trips) as total_hvfhs_trips\n",
        "    FROM daily_metrics\n",
        "    GROUP BY 1\n",
        "),\n",
        "final_metrics AS (\n",
        "    SELECT \n",
        "        m.*,\n",
        "        m.trips * 100.0 / t.total_hvfhs_trips as market_share,\n",
        "        (m.trips * 100.0 / LAG(m.trips) OVER (PARTITION BY m.vendor_id ORDER BY m.date)) - 100 as daily_growth\n",
        "    FROM daily_metrics m\n",
        "    JOIN market_total t ON m.date = t.date\n",
        ")\n",
        "SELECT * FROM final_metrics\n",
        "\"\"\"\n",
        "df_growth_corr = con.execute(query_growth_corr).df()\n",
        "\n",
        "# Visualizing Comprehensive Heatmaps\n",
        "print(\"PHÂN TÍCH TƯƠNG QUAN CHI TIẾT (DRIVER & MARKET FACTORS)\")\n",
        "for provider_id, name in [('HV0003', 'Uber'), ('HV0005', 'Lyft')]:\n",
        "    df_p = df_growth_corr[df_growth_corr['vendor_id'] == provider_id].copy()\n",
        "    df_p = df_p.dropna(subset=['daily_growth', 'market_share'])\n",
        "    \n",
        "    # Chi lay cac cot so lieu de tinh tuong quan\n",
        "    cols_to_corr = ['market_share', 'daily_growth'] + list(available_metrics.keys())\n",
        "    corr_matrix = df_p[cols_to_corr].corr()\n",
        "    \n",
        "    fig = px.imshow(corr_matrix, \n",
        "                     text_auto='.2f', \n",
        "                     aspect=\"auto\", \n",
        "                     color_continuous_scale='RdBu_r',\n",
        "                     title=f'{name} - Comprehensive Factor Correlation')\n",
        "\n",
        "    fig.update_layout(template='plotly_dark', plot_bgcolor=THEME['bg'], paper_bgcolor=THEME['bg'])\n",
        "    fig.show()\n",
        "\n",
        "# Detailed Data Tables (Concise view for Market Share influence)\n",
        "print(\"\\n\" + \"=\"*60)\n",
        "print(\"ẢNH HƯỞNG CỦA CÁC YẾU TỐ (BAO GỒM TÀI XẾ) ĐẾN THỊ PHẦN\")\n",
        "print(\"=\"*60)\n",
        "\n",
        "for provider_id, name in [('HV0003', 'Uber'), ('HV0005', 'Lyft')]:\n",
        "    df_p = df_growth_corr[df_growth_corr['vendor_id'] == provider_id].copy()\n",
        "    df_p = df_p.dropna(subset=['daily_growth', 'market_share'])\n",
        "    \n",
        "    cols_to_corr = ['market_share', 'daily_growth'] + list(available_metrics.keys())\n",
        "    corr_matrix = df_p[cols_to_corr].corr()\n",
        "    \n",
        "    # Hien thi rut gon tap trung vao Market Share & Daily Growth\n",
        "    concise_corr = corr_matrix[['market_share', 'daily_growth']]\n",
        "    \n",
        "    print(f\"\\n{name} - Detailed Driver & Market Influence:\")\n",
        "    display(concise_corr.style.format('{:.2f}'))\n"
    ]
    nb['cells'][target_index]['source'] = new_source
    
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
    print("Notebook cell updated with dynamic driver-centric metrics.")
else:
    print("Target cell not found.")
