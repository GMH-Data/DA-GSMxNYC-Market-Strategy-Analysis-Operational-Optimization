import duckdb
con = duckdb.connect('src/taxi_data.duckdb')
df = con.execute("DESCRIBE yellow_2019_2025_final").df()
print("Columns in yellow_2019_2025_final:")
print(df['column_name'].tolist())
con.close()
