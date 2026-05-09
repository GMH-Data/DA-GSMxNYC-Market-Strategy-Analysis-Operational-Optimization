import duckdb
import pandas as pd

con = duckdb.connect('src/taxi_data.duckdb')

# Define metrics
potential_metrics = {
    'avg_fare': 'avg(fare_amount)',
    'avg_distance': 'avg(trip_distance)',
    'avg_tip': 'avg(tip_amount)',
    'avg_duration_min': "avg(extract('epoch' from (dropoff_datetime - pickup_datetime))) / 60.0",
    'avg_driver_pay': 'avg(driver_pay)',
    'avg_wait_time_min': "avg(extract('epoch' from (pickup_datetime - request_datetime))) / 60.0",
    'shared_req_rate': "count(CASE WHEN shared_request_flag = 'Y' THEN 1 END) * 100.0 / count(*)"
}

select_clause = ", ".join([f"{expr} as {name}" for name, expr in potential_metrics.items()])

query = f"""
WITH daily_metrics AS (
    SELECT 
        date_trunc('day', pickup_datetime) as date,
        vendor_id,
        count(*) as trips,
        {select_clause}
    FROM fhvhv_2019_2025_final
    WHERE vendor_id IN ('HV0003', 'HV0005')
    GROUP BY 1, 2
),
market_total AS (
    SELECT date, sum(trips) as total_hvfhs_trips
    FROM daily_metrics
    GROUP BY 1
),
final_metrics AS (
    SELECT 
        m.*,
        m.trips * 100.0 / t.total_hvfhs_trips as market_share,
        (m.trips * 100.0 / LAG(m.trips) OVER (PARTITION BY m.vendor_id ORDER BY m.date)) - 100 as daily_growth
    FROM daily_metrics m
    JOIN market_total t ON m.date = t.date
)
SELECT * FROM final_metrics
"""

df = con.execute(query).df()

for pid, name in [('HV0003', 'Uber'), ('HV0005', 'Lyft')]:
    print(f"\n--- {name} Correlation Matrix ---")
    df_p = df[df['vendor_id'] == pid].dropna(subset=['market_share', 'daily_growth'])
    cols = ['market_share', 'daily_growth'] + list(potential_metrics.keys())
    print(df_p[cols].corr()[['market_share', 'daily_growth']])

con.close()
