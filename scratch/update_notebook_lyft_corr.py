import nbformat as nbf
import os

def update_1_2_c_with_lyft_correlation():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    lyft_corr_code = """# 1.2.C Correlation Analysis: Uber & Lyft Market Share vs Operational Factors
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Query aggregated data for both Uber and Lyft
query_corr = \"\"\"
SELECT 
    PULocationID,
    count(CASE WHEN hvfhs_license_num = 'HV0003' THEN 1 END) * 1.0 / count(*) as uber_market_share,
    count(CASE WHEN hvfhs_license_num = 'HV0005' THEN 1 END) * 1.0 / count(*) as lyft_market_share,
    avg(trip_miles) as avg_trip_miles,
    avg(trip_time) / 60.0 as avg_trip_time_min,
    avg(base_passenger_fare) as avg_fare,
    avg(tips) as avg_tips,
    avg(driver_pay) as avg_driver_pay,
    avg(congestion_surcharge) as avg_congestion,
    avg(airport_fee) as avg_airport_fee
FROM fhvhv_2019_2025_cleaned
WHERE year(pickup_datetime) BETWEEN 2019 AND 2025
GROUP BY 1
HAVING count(*) > 100
\"\"\"
df_corr = con.execute(query_corr).df()

# 2. Calculate Correlation Matrix
corr_matrix = df_corr.drop(columns=['PULocationID']).corr()

# 3. Plot Correlation Heatmaps (Side by Side for Uber and Lyft)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Uber Heatmap (Correlation of all factors with Uber Share)
uber_corr = corr_matrix[['uber_market_share']].sort_values(by='uber_market_share', ascending=False)
sns.heatmap(uber_corr, annot=True, cmap='RdBu', ax=ax1, center=0, fmt=".2f")
ax1.set_title('Correlation: Uber Market Share', fontsize=15)

# Lyft Heatmap (Correlation of all factors with Lyft Share)
lyft_corr = corr_matrix[['lyft_market_share']].sort_values(by='lyft_market_share', ascending=False)
sns.heatmap(lyft_corr, annot=True, cmap='RdBu', ax=ax2, center=0, fmt=".2f")
ax2.set_title('Correlation: Lyft Market Share', fontsize=15)

plt.tight_layout()
plt.show()

# 4. Comparative Insights
print("\\n--- TOP CORRELATIONS COMPARISON ---")
comparison = pd.DataFrame({
    'Uber Correlation': corr_matrix['uber_market_share'],
    'Lyft Correlation': corr_matrix['lyft_market_share']
}).drop(['uber_market_share', 'lyft_market_share'])
display(comparison.sort_values('Uber Correlation', ascending=False))"""

    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and ('# 1.2.C' in cell.source or 'Correlation Analysis: Market Share vs Other Factors' in cell.source):
            cell.source = lyft_corr_code
            found = True
            break
            
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Updated section 1.2.C with Lyft correlation analysis.")
    else:
        print("Target cell for 1.2.C not found.")

if __name__ == "__main__":
    update_1_2_c_with_lyft_correlation()
