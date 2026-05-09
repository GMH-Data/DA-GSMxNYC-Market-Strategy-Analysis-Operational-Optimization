
import pandas as pd
import duckdb
import sys

# Set stdout to utf-8
sys.stdout.reconfigure(encoding='utf-8')

# Kết nối database
con = duckdb.connect('src/taxi_data.duckdb', read_only=True)

query_growth = """
WITH monthly_trips AS (
    SELECT 
        date_trunc('month', pickup_datetime) as month,
        CASE 
            WHEN vendor_id = 'HV0003' THEN 'Uber'
            WHEN vendor_id = 'HV0005' THEN 'Lyft'
        END as provider,
        count(*) as trips
    FROM fhvhv_2019_2025_final
    WHERE vendor_id IN ('HV0003', 'HV0005')
    GROUP BY 1, 2
),
growth_calc AS (
    SELECT 
        month,
        extract('year' from month) as year,
        monthname(month) as month_label,
        provider,
        trips,
        (trips * 100.0 / LAG(trips) OVER (PARTITION BY provider ORDER BY month)) - 100 as mom_growth
    FROM monthly_trips
)
SELECT * FROM growth_calc ORDER BY month, provider
"""

df = con.execute(query_growth).df()

# 1. Tìm các tháng bị ảnh hưởng nhiều nhất (Tăng trưởng âm nhất và Dương nhất)
print("--- PHÂN TÍCH BIẾN ĐỘNG CỰC ĐOAN (PEAKS & TROUGHS) ---")
for provider in ['Uber', 'Lyft']:
    df_p = df[df['provider'] == provider]
    max_growth = df_p.loc[df_p['mom_growth'].idxmax()]
    min_growth = df_p.loc[df_p['mom_growth'].idxmin()]
    
    print(f"\n[{provider.upper()}]")
    print(f"- Tăng trưởng mạnh nhất: {max_growth['month_label']} {int(max_growth['year'])} ({max_growth['mom_growth']:.2f}%)")
    print(f"- Sụt giảm sâu nhất: {min_growth['month_label']} {int(min_growth['year'])} ({min_growth['mom_growth']:.2f}%)")

# 2. Phân tích chu kỳ gần nhất (2024 - 2025)
print("\n--- PHÂN TÍCH CHU KỲ GẦN NHẤT (2024 - 2025) ---")
df_recent = df[df['year'] >= 2024]
for provider in ['Uber', 'Lyft']:
    print(f"\n[{provider.upper()}] Recent Cycle:")
    df_p_recent = df_recent[df_recent['provider'] == provider]
    print(df_p_recent[['month_label', 'year', 'mom_growth']].to_string(index=False))

con.close()
