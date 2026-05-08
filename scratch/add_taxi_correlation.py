import nbformat as nbf
import os

def add_yellow_green_correlation_cell():
    notebook_path = 'Data.ipynb'
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    yellow_green_code = """# 1.2.C.2 Correlation Analysis: Yellow & Green Taxi Market Share
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Query aggregated data for Yellow and Green Taxi
# We calculate their share relative to the TOTAL market (Yellow + Green + HVFHS)
query_yg = \"\"\"
WITH TotalByZone AS (
    SELECT PULocationID, count(*) as total_trips FROM (
        SELECT PULocationID FROM yellow_2019_2025_cleaned
        UNION ALL
        SELECT PULocationID FROM green_2019_2025_cleaned
        UNION ALL
        SELECT PULocationID FROM fhvhv_2019_2025_cleaned
    ) GROUP BY 1
),
YellowStats AS (
    SELECT 
        PULocationID,
        count(*) as y_trips,
        avg(trip_distance) as avg_miles,
        avg(fare_amount) as avg_fare,
        avg(tip_amount) as avg_tips,
        avg(total_amount) as avg_total
    FROM yellow_2019_2025_cleaned
    GROUP BY 1
),
GreenStats AS (
    SELECT 
        PULocationID,
        count(*) as g_trips,
        avg(trip_distance) as avg_miles,
        avg(fare_amount) as avg_fare,
        avg(tip_amount) as avg_tips,
        avg(total_amount) as avg_total
    FROM green_2019_2025_cleaned
    GROUP BY 1
)
SELECT 
    t.PULocationID,
    (COALESCE(y.y_trips, 0) * 1.0 / t.total_trips) as yellow_market_share,
    (COALESCE(g.g_trips, 0) * 1.0 / t.total_trips) as green_market_share,
    COALESCE(y.avg_miles, g.avg_miles) as avg_trip_miles,
    COALESCE(y.avg_fare, g.avg_fare) as avg_fare,
    COALESCE(y.avg_tips, g.avg_tips) as avg_tips,
    COALESCE(y.avg_total, g.avg_total) as avg_total_pay
FROM TotalByZone t
LEFT JOIN YellowStats y ON t.PULocationID = y.PULocationID
LEFT JOIN GreenStats g ON t.PULocationID = g.PULocationID
WHERE t.total_trips > 100
\"\"\"
df_yg = con.execute(query_yg).df()

# 2. Calculate Correlation Matrix
corr_matrix_yg = df_yg.drop(columns=['PULocationID']).corr()

# 3. Plot Correlation Heatmaps
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

# Yellow Taxi Heatmap
yellow_corr = corr_matrix_yg[['yellow_market_share']].sort_values(by='yellow_market_share', ascending=False)
sns.heatmap(yellow_corr, annot=True, cmap='YlOrBr', ax=ax1, center=0, fmt=".2f")
ax1.set_title('Correlation: Yellow Taxi Market Share', fontsize=15)

# Green Taxi Heatmap
green_corr = corr_matrix_yg[['green_market_share']].sort_values(by='green_market_share', ascending=False)
sns.heatmap(green_corr, annot=True, cmap='YlGn', ax=ax2, center=0, fmt=".2f")
ax2.set_title('Correlation: Green Taxi Market Share', fontsize=15)

plt.tight_layout()
plt.show()

# 4. Quick Comparison
print("\\n--- TAXI MARKET SHARE CORRELATION SUMMARY ---")
display(corr_matrix_yg[['yellow_market_share', 'green_market_share']].sort_values('yellow_market_share', ascending=False))"""

    new_cell = nbf.v4.new_code_cell(yellow_green_code)
    
    # Find the position of the Uber/Lyft correlation cell to insert after it
    insert_pos = -1
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and ('# 1.2.C Correlation Analysis: Uber & Lyft' in cell.source):
            insert_pos = i + 1
            break
            
    if insert_pos != -1:
        nb.cells.insert(insert_pos, new_cell)
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Yellow and Green taxi correlation cell added successfully.")
    else:
        print("Could not find the Uber/Lyft correlation cell to insert after.")

if __name__ == "__main__":
    add_yellow_green_correlation_cell()
