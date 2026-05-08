import shutil
import duckdb
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

try:
    shutil.copy2('src/taxi_data.duckdb', 'src/taxi_data_temp.duckdb')
    con = duckdb.connect('src/taxi_data_temp.duckdb')
    
    query_c = """
    SELECT 
        PULocationID,
        count(CASE WHEN hvfhs_license_num = 'HV0003' THEN 1 END) * 1.0 / count(*) as uber_market_share,
        count(CASE WHEN hvfhs_license_num = 'HV0005' THEN 1 END) * 1.0 / count(*) as lyft_market_share,
        avg(date_diff('second', request_datetime, pickup_datetime)) / 60.0 as avg_wait_time_min,
        avg(trip_miles) as avg_miles,
        avg(trip_time) / 60.0 as avg_trip_time_min,
        avg(base_passenger_fare) as avg_fare,
        avg(tips) as avg_tips,
        avg(driver_pay) as avg_driver_pay
    FROM fhvhv_2019_2025_cleaned
    WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
    GROUP BY 1 HAVING count(*) > 100
    """
    
    df_corr = con.execute(query_c).df()
    corr_matrix = df_corr.drop(columns=['PULocationID']).corr()
    print('--- CORRELATION MATRIX ---')
    print(corr_matrix[['uber_market_share', 'lyft_market_share']].round(3))
except Exception as e:
    print('Error:', e)
