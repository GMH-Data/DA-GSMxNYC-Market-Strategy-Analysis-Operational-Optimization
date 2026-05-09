import duckdb
import pandas as pd

con = duckdb.connect('src/taxi_data.duckdb')

query = """
WITH daily_data AS (
    SELECT 
        date_trunc('day', pickup_datetime) as date,
        vendor_id,
        count(*) as trips,
        avg(tip_amount) as avg_tip,
        avg(fare_amount) as avg_fare
    FROM fhvhv_2019_2025_final
    WHERE vendor_id = 'HV0005'
    GROUP BY 1, 2
),
growth_calc AS (
    SELECT 
        *,
        (trips * 100.0 / LAG(trips) OVER (ORDER BY date)) - 100 as growth
    FROM daily_data
)
SELECT * FROM growth_calc
"""

df = con.execute(query).df()
print("Lyft Correlation (Daily):")
print(df[['avg_tip', 'trips', 'growth']].corr())

# Monthly aggregation
query_monthly = """
WITH monthly_data AS (
    SELECT 
        date_trunc('month', pickup_datetime) as month,
        vendor_id,
        count(*) as trips,
        avg(tip_amount) as avg_tip,
        avg(fare_amount) as avg_fare
    FROM fhvhv_2019_2025_final
    WHERE vendor_id = 'HV0005'
    GROUP BY 1, 2
),
growth_calc AS (
    SELECT 
        *,
        (trips * 100.0 / LAG(trips) OVER (ORDER BY month)) - 100 as growth
    FROM monthly_data
)
SELECT * FROM growth_calc
"""
df_m = con.execute(query_monthly).df()
print("\nLyft Correlation (Monthly):")
print(df_m[['avg_tip', 'trips', 'growth']].corr())

con.close()
