import nbformat as nbf
import os

def add_section_1_2_d():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    header_d = nbf.v4.new_markdown_cell("### D. Correlation Analysis\nPhân tích mối tương quan giữa thị phần của Uber và các yếu tố vận hành như giá cước, quãng đường, tiền tip và thu nhập tài xế.")
    
    code_d = nbf.v4.new_code_cell("""# 1.2.D Correlation Analysis: Market Share vs Other Factors
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Query aggregated data by Zone
query_corr = \"\"\"
SELECT 
    PULocationID,
    count(CASE WHEN hvfhs_license_num = 'HV0003' THEN 1 END) * 1.0 / count(*) as uber_market_share,
    avg(trip_miles) as avg_trip_miles,
    avg(trip_time) / 60.0 as avg_trip_time_min,
    avg(base_passenger_fare) as avg_fare,
    avg(tips) as avg_tips,
    avg(driver_pay) as avg_driver_pay,
    avg(congestion_surcharge) as avg_congestion,
    avg(airport_fee) as avg_airport_fee
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1
HAVING count(*) > 100
\"\"\"
df_corr = con.execute(query_corr).df()

# 2. Calculate Correlation Matrix
# We exclude PULocationID as it's just an identifier
corr_matrix = df_corr.drop(columns=['PULocationID']).corr()

# 3. Plot Correlation Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', center=0, fmt=".2f", linewidths=0.5)
plt.title('Correlation Heatmap: Uber Market Share vs Operational Factors', fontsize=15)
plt.show()

# 4. Quick Insights
print("\\n--- KEY CORRELATIONS WITH UBER MARKET SHARE ---")
print(corr_matrix['uber_market_share'].sort_values(ascending=False))""")

    # Find the position of 1.2.C to insert after it
    insert_pos = -1
    for i, cell in enumerate(nb.cells):
        if '### C. Competition Areas' in cell.source or '### C. Khu vực cạnh tranh' in cell.source:
            # We want to find the code cell after this markdown cell
            for j in range(i+1, len(nb.cells)):
                if nb.cells[j].cell_type == 'code':
                    insert_pos = j + 1
                    break
            if insert_pos != -1: break

    if insert_pos != -1:
        nb.cells.insert(insert_pos, header_d)
        nb.cells.insert(insert_pos + 1, code_d)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Section 1.2.D added successfully.")
    else:
        print("Could not find section 1.2.C to insert after.")

if __name__ == "__main__":
    add_section_1_2_d()
