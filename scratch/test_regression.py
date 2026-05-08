import duckdb
import pandas as pd
from sklearn.linear_model import LinearRegression

try:
    con = duckdb.connect('src/taxi_data.duckdb', read_only=True)
except Exception:
    import shutil
    shutil.copy2('src/taxi_data.duckdb', 'src/taxi_data_test.duckdb')
    con = duckdb.connect('src/taxi_data_test.duckdb')

query = """
SELECT 
    date_trunc('month', pickup_datetime) as month,
    count(*) as total_trips
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2021 AND 2025
GROUP BY 1
ORDER BY 1
"""
df = con.execute(query).df()
df['mom_growth'] = df['total_trips'].pct_change() * 100
df = df.dropna()

# Smooth with 12-month rolling average
df['smoothed'] = df['mom_growth'].rolling(window=12).mean()
df_fit = df.dropna().copy()
df_fit['month_idx'] = range(len(df_fit))

X = df_fit[['month_idx']]
y = df_fit['smoothed']
model = LinearRegression()
model.fit(X, y)
print(f'Smoothed Slope: {model.coef_[0]}')
print(f'Smoothed Intercept: {model.intercept_}')
if model.coef_[0] < 0:
    zero_idx = -model.intercept_ / model.coef_[0]
    print(f'Zero crossing at index: {zero_idx}')
else:
    print('Slope is positive, no zero crossing.')

# What if we just fit on raw mom_growth?
df['idx'] = range(len(df))
model2 = LinearRegression()
model2.fit(df[['idx']], df['mom_growth'])
print(f'Raw Slope: {model2.coef_[0]}')
print(f'Raw Intercept: {model2.intercept_}')

