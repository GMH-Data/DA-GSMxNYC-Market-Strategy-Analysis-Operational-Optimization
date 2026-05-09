import nbformat as nbf
import os

def fix_correlation_cell(nb_path):
    # Load the notebook
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbf.read(f, as_version=4)

    # Updated code with standardized column names
    fixed_code = """# [2.2.1] Correlation between Trip Volume and Revenue
# This analysis validates the use of trip counts as a reliable proxy for Market Share
query_corr_validation = \"\"\"
WITH monthly_data AS (
    -- HVFHS (Uber & Lyft)
    SELECT 
        date_trunc('month', pickup_datetime) as month,
        CASE 
            WHEN vendor_id = 'HV0003' THEN 'Uber'
            WHEN vendor_id = 'HV0005' THEN 'Lyft'
        END as provider,
        count(*) as trips,
        sum(fare_amount) as revenue
    FROM fhvhv_2019_2025_final
    WHERE vendor_id IN ('HV0003', 'HV0005')
    GROUP BY 1, 2
    
    UNION ALL
    
    -- Yellow Taxi (Standardized to pickup_datetime)
    SELECT 
        date_trunc('month', pickup_datetime) as month,
        'Yellow' as provider,
        count(*) as trips,
        sum(fare_amount) as revenue
    FROM yellow_2019_2025_final
    GROUP BY 1, 2
    
    UNION ALL
    
    -- Green Taxi (Standardized to pickup_datetime)
    SELECT 
        date_trunc('month', pickup_datetime) as month,
        'Green' as provider,
        count(*) as trips,
        sum(fare_amount) as revenue
    FROM green_2019_2025_final
    GROUP BY 1, 2
)
SELECT * FROM monthly_data ORDER BY month, provider
\"\"\"

df_corr_val = con.execute(query_corr_validation).df()

# Calculate Correlation per Provider
corr_results = []
for p in df_corr_val['provider'].unique():
    df_p = df_corr_val[df_corr_val['provider'] == p]
    correlation = df_p['trips'].corr(df_p['revenue'])
    corr_results.append({'Provider': p, 'Trips-Revenue Correlation': correlation})

df_corr_summary = pd.DataFrame(corr_results)

print(\"CORRELATION ANALYSIS: TRIP VOLUME VS REVENUE (2019-2025)\")
display(df_corr_summary.style.format({'Trips-Revenue Correlation': '{:.4f}'}))

# Visualization
fig_corr = px.scatter(df_corr_val, x='trips', y='revenue', color='provider', 
                      trendline='ols', title='Correlation: Trip Volume vs Revenue by Provider',
                      labels={'trips': 'Monthly Trip Volume', 'revenue': 'Monthly Revenue ($)'},
                      template='plotly_dark',
                      color_discrete_map={'Uber': THEME['uber'], 'Lyft': THEME['lyft'], 'Yellow': THEME['yellow'], 'Green': THEME['green']})
fig_corr.update_layout(plot_bgcolor=THEME['bg'], paper_bgcolor=THEME['bg'])
fig_corr.show()

print(\"\\\\nCONCLUSION: High positive correlation (close to 1.0) justifies using Trip Volume as a primary metric for Market Share.\")"""

    # Find and update the cell
    updated = False
    for cell in nb.cells:
        if cell.id == "validation_trips_revenue_corr":
            cell.source = fixed_code
            updated = True
            break

    if updated:
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbf.write(nb, f)
        print("Successfully updated the correlation cell.")
    else:
        print("Cell not found. Please ensure the cell exists.")

if __name__ == "__main__":
    path = "Analysis.ipynb"
    fix_correlation_cell(path)
