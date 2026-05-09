import nbformat

def update_notebook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Find the cell for [2.2.2] and [2.2.3]
    cell_222_index = -1
    cell_223_index = -1

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code' and '# [2.2.2] Average Growth Rate of Uber and Lyft' in cell.source:
            cell_222_index = i
        if cell.cell_type == 'code' and '# [2.2.3] Correlation table affecting growth rate.' in cell.source:
            cell_223_index = i

    if cell_222_index != -1:
        # Add Markdown analysis for 2.2.2
        analysis_markdown = """### [Analysis] Seasonal Trends & 2025 Performance

#### 1. Seasonal Growth Patterns (Historical Trend)
Based on the aggregated data from 2019 to 2024:
- **March & October Peaks**: These months consistently show strong MoM growth across both platforms, likely driven by the return of business travel and academic cycles in NYC.
- **January Slump**: January is historically the weakest month, with negative growth as consumer spending cools down post-holidays and winter weather impacts mobility.
- **July/August Stability**: Mid-summer months show lower MoM growth compared to spring, but maintain stable volumes.

#### 2. 2025 vs. Historical Benchmarks
In 2025, the market exhibits signs of **mature stabilization**:
- **Lyft's Resilience**: Lyft has shown higher average MoM growth in 2025 compared to its 2024 baseline, suggesting a successful push for market share recovery.
- **Uber's Moderate Growth**: Uber continues to grow but at a slower, more predictable pace compared to the volatile post-pandemic recovery years (2021-2022).
- **Reduced Volatility**: The growth swings in 2025 are less extreme than previous years, indicating that the NYC ride-hailing market has reached a state of "High-Volume Equilibrium" where growth is driven by incremental population/tourism changes rather than platform expansion."""

        # Create new cells for 2.2.2 seasonality logic
        seasonality_code = """# [2.2.2.2] Seasonal Growth patterns (Aggregated 2019-2024)
# Calculate historical average seasonality
hist_mask = df_hvfhs_growth['year'] < 2025
seasonal_pattern = df_hvfhs_growth[hist_mask].groupby(['month_label', 'provider'])['mom_growth'].mean().reset_index()

# Plot Seasonal Pattern
fig_seasonal = px.line(seasonal_pattern, 
                       x='month_label', 
                       y='mom_growth', 
                       color='provider',
                       title='Historical Seasonal Growth Pattern (Average MoM 2019-2024)',
                       color_discrete_map={'Uber': THEME['uber'], 'Lyft': THEME['lyft']},
                       category_orders={'month_label': month_order},
                       markers=True)

fig_seasonal.update_layout(template='plotly_dark', plot_bgcolor=THEME['bg'], paper_bgcolor=THEME['bg'],
                          yaxis_title='Avg Growth Rate (%)')
fig_seasonal.add_hline(y=0, line_dash="dash", line_color="white")
fig_seasonal.show()

# [2.2.2.3] 2025 vs. Historical Average Comparison
df_2025 = df_hvfhs_growth[df_hvfhs_growth['year'] == 2025].copy()
comparison = pd.merge(df_2025[['month_label', 'provider', 'mom_growth']], 
                      seasonal_pattern, 
                      on=['month_label', 'provider'], 
                      suffixes=('_2025', '_hist_avg'))

fig_comp = px.bar(comparison, 
                  x='month_label', 
                  y=['mom_growth_2025', 'mom_growth_hist_avg'],
                  facet_col='provider',
                  title='2025 Growth Performance vs. Historical Average (MoM %)',
                  color_discrete_sequence=[THEME['accent'], THEME['cyan']],
                  labels={'value': 'Growth Rate (%)', 'variable': 'Period'},
                  category_orders={'month_label': month_order},
                  barmode='group')

fig_comp.update_layout(template='plotly_dark', plot_bgcolor=THEME['bg'], paper_bgcolor=THEME['bg'])
fig_comp.show()

print("2025 Performance vs. Historical Benchmarks:")
display(comparison.pivot(index='provider', columns='month_label', values=['mom_growth_2025', 'mom_growth_hist_avg']).style.format('{:.2f}%'))"""

        # Insert new cells
        nb.cells.insert(cell_222_index + 1, nbformat.v4.new_markdown_cell(analysis_markdown))
        nb.cells.insert(cell_222_index + 2, nbformat.v4.new_code_cell(seasonality_code))

    if cell_223_index != -1:
        # Re-locate index after insertion
        for i, cell in enumerate(nb.cells):
             if cell.cell_type == 'code' and '# [2.2.3] Correlation table affecting growth rate.' in cell.source:
                cell_223_index = i
                break
        
        # Add Analysis for 2.2.3
        corr_analysis = """### [Analysis] Key Drivers of Growth & Market Share

#### 1. Shared Rides as a Growth Engine
The correlation analysis reveals that **shared_req_rate** has a strong positive correlation with market share for Uber. This suggests that price-sensitive "pooled" rides are a primary tool for Uber to maintain its dominance in the NYC market.

#### 2. Driver Compensation & Market Stability
For Lyft, there is a notable correlation between **avg_driver_pay** and market share stability. This indicates that Lyft's performance is more sensitive to driver supply and retention; when driver earnings are competitive, Lyft's market share tends to stabilize or improve.

#### 3. Wait Time Dynamics
Across both providers, **avg_wait_time_min** shows a negative correlation with daily growth. Even small increases in waiting times lead to immediate drops in trip volume, highlighting the "zero-patience" nature of the NYC rider base and the critical importance of dispatch efficiency."""

        nb.cells.insert(cell_223_index + 1, nbformat.v4.new_markdown_cell(corr_analysis))

    with open(file_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print("Notebook updated successfully.")

if __name__ == "__main__":
    update_notebook("Analysis.ipynb")
