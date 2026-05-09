import duckdb
import pandas as pd

con = duckdb.connect('src/taxi_data.duckdb')

query = """
WITH monthly_trips AS (
    SELECT 
        date_trunc('month', pickup_datetime) as month,
        vendor_id,
        count(*) as trips
    FROM fhvhv_2019_2025_final
    WHERE vendor_id IN ('HV0003', 'HV0005')
    GROUP BY 1, 2
),
growth_calc AS (
    SELECT 
        month,
        extract('year' from month) as year,
        extract('month' from month) as month_num,
        CASE WHEN vendor_id = 'HV0003' THEN 'Uber' ELSE 'Lyft' END as provider,
        trips,
        (trips * 100.0 / LAG(trips) OVER (PARTITION BY vendor_id ORDER BY month)) - 100 as mom_growth
    FROM monthly_trips
)
SELECT * FROM growth_calc
"""

df = con.execute(query).df()

# 1. Historical Benchmarks
periods = [
    (2019, 2020),
    (2021, 2022),
    (2023, 2024),
    (2025, 2025)
]

print("=== III. DIỄN BIẾN TĂNG TRƯỞNG LỊCH SỬ (MoM Growth) ===")
for start, end in periods:
    period_df = df[(df['year'] >= start) & (df['year'] <= end)]
    summary = period_df.groupby('provider')['mom_growth'].mean()
    print(f"Giai đoạn {start}-{end}:")
    print(summary)

# 2. Strategic Gap (2025 vs 2019-2024 Baseline)
print("\n=== II. STRATEGIC GAP ANALYSIS (2025 vs 2019-2024 Mean) ===")
baseline = df[df['year'] < 2025].groupby(['provider', 'month_num'])['mom_growth'].mean()
current_2025 = df[df['year'] == 2025].set_index(['provider', 'month_num'])['mom_growth']

deviation = current_2025 - baseline
print(deviation.unstack().round(2))

con.close()
