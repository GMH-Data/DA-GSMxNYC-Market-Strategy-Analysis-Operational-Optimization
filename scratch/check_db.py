import duckdb
import pandas as pd

con = duckdb.connect('src/taxi_data.duckdb', read_only=True)
try:
    print("Market Overview Stats:")
    df = con.execute("SELECT service_type, count(*), count(total_amount), avg(total_amount) FROM v_MARKET_OVERVIEW GROUP BY 1").df()
    print(df)
    
    print("\nFHVHV Final Check:")
    df_fhvhv = con.execute("SELECT count(*), count(fare_amount), count(driver_pay), count(total_amount) FROM fhvhv_2019_2025_final").df()
    print(df_fhvhv)
except Exception as e:
    print(f"Error: {e}")
finally:
    con.close()
