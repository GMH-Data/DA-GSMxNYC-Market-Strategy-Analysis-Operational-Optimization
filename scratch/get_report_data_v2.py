import duckdb
import pandas as pd

try:
    con = duckdb.connect('src/taxi_data.duckdb', read_only=True)
    # Query for [2.2.1.3] Average Growth Rate
    query_growth = """
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
            vendor_id,
            trips,
            (trips * 100.0 / LAG(trips) OVER (PARTITION BY vendor_id ORDER BY month)) - 100 as mo_growth
        FROM monthly_trips
    )
    SELECT vendor_id, avg(mo_growth) as avg_growth
    FROM growth_calc
    GROUP BY 1
    """
    df_growth = con.execute(query_growth).df()
    print("GROWTH_START")
    print(df_growth.to_json())
    print("GROWTH_END")

    # Query for [2.2.1.4] Correlation
    query_corr = """
    WITH daily_metrics AS (
        SELECT 
            date_trunc('day', pickup_datetime) as date,
            vendor_id,
            count(*) as trips,
            avg(fare_amount) as avg_fare,
            avg(trip_distance) as avg_distance,
            avg(tip_amount) as avg_tip,
            avg(total_amount) as avg_total_cost,
            avg(extract('epoch' from (dropoff_datetime - pickup_datetime))) / 60.0 as avg_duration_min,
            avg(driver_pay) as avg_driver_pay
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
    df_corr = con.execute(query_corr).df()
    print("CORR_START")
    for vid, name in [('HV0003', 'Uber'), ('HV0005', 'Lyft')]:
        df_p = df_corr[df_corr['vendor_id'] == vid].copy().dropna()
        cols = ['market_share', 'daily_growth', 'avg_fare', 'avg_distance', 'avg_tip', 'avg_total_cost', 'avg_duration_min', 'avg_driver_pay']
        available = [c for c in cols if c in df_p.columns]
        corr_matrix = df_p[available].corr()
        print(f"PROV:{name}")
        print(corr_matrix[['market_share', 'daily_growth']].to_json())
    print("CORR_END")

except Exception as e:
    print(f"ERROR:{str(e)}")
