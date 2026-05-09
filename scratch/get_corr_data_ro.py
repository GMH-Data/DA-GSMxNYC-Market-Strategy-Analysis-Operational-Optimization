import duckdb
import pandas as pd

try:
    # Try connecting in read-only mode to bypass the lock
    con = duckdb.connect('src/taxi_data.duckdb', read_only=True)
    query = """
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
            m.trips * 100.0 / t.total_hvfhs_trips as market_share
        FROM daily_metrics m
        JOIN market_total t ON m.date = t.date
    )
    SELECT * FROM final_metrics
    """
    df = con.execute(query).df()
    print("DATA_START")
    for vid, name in [('HV0003', 'Uber'), ('HV0005', 'Lyft')]:
        df_p = df[df['vendor_id'] == vid].copy().dropna()
        # Ensure columns exist before corr
        cols = ['market_share', 'avg_fare', 'avg_distance', 'avg_tip', 'avg_total_cost', 'avg_duration_min', 'avg_driver_pay']
        available = [c for c in cols if c in df_p.columns]
        corr = df_p[available].corr()['market_share']
        print(f"PROV:{name}")
        print(corr.to_json())
    print("DATA_END")
except Exception as e:
    print(f"ERROR:{str(e)}")
