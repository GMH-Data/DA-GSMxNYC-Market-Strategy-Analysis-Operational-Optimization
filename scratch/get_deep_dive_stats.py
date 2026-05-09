import duckdb
import pandas as pd

try:
    con = duckdb.connect('src/taxi_data.duckdb', read_only=True)
    query = """
    SELECT 
        year(pickup_datetime) as year,
        CASE 
            WHEN vendor_id = 'HV0003' THEN 'Uber'
            WHEN vendor_id = 'HV0005' THEN 'Lyft'
        END as provider,
        avg(fare_amount) as avg_fare,
        avg(trip_distance) as avg_dist,
        avg(driver_pay) as avg_pay,
        avg(extract('epoch' from (dropoff_datetime - pickup_datetime))) / 60.0 as avg_dur,
        sum(case when is_shared_requested then 1 else 0 end) * 100.0 / count(*) as shared_rate
    FROM fhvhv_2019_2025_final
    WHERE vendor_id IN ('HV0003', 'HV0005')
    GROUP BY 1, 2
    ORDER BY 1, 2
    """
    df = con.execute(query).df()
    print("HARD_STATS_START")
    print(df.to_json(orient='records'))
    print("HARD_STATS_END")
except Exception as e:
    print(f"ERROR:{str(e)}")
