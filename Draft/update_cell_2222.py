import nbformat

def update_notebook_cell(notebook_path, cell_id_prefix, new_source):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    found = False
    for cell in nb.cells:
        if cell.cell_type == 'code' and any(cell_id_prefix in line for line in cell.source.splitlines()):
            cell.source = new_source
            found = True
            break
    
    if found:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Successfully updated cell with prefix: {cell_id_prefix}")
    else:
        print(f"Cell with prefix {cell_id_prefix} not found.")

new_code = """# [2.2.2.2] Seasonal Growth patterns (Aggregated 2019-2024)
if 'df_hvfhs_growth' in locals() and not df_hvfhs_growth.empty:
    # --- 1. Calculate Historical Baseline (2019-2024) ---
    seasonal_pattern = (
        df_hvfhs_growth[df_hvfhs_growth['year'] < 2025]
        .groupby(['month_label', 'provider'])['mom_growth']
        .mean()
        .reset_index()
    )
    
    # Sort by month_label using month_order to prevent "spaghetti" lines
    seasonal_pattern['month_label'] = pd.Categorical(seasonal_pattern['month_label'], categories=month_order, ordered=True)
    seasonal_pattern = seasonal_pattern.sort_values(['provider', 'month_label'])

    # --- 2. Visualization: Historical Seasonal Pattern ---
    fig_seasonal = px.line(
        seasonal_pattern, 
        x='month_label', y='mom_growth', color='provider',
        title='<span style="color:#FF007F">HISTORICAL SEASONAL GROWTH</span> (Avg MoM 2019-2024)',
        color_discrete_map={'Uber': THEME['uber'], 'Lyft': THEME['lyft']},
        category_orders={'month_label': month_order},
        markers=True
    )
    fig_seasonal.update_layout(
        template='plotly_dark', 
        plot_bgcolor=THEME['bg'], 
        paper_bgcolor=THEME['bg'],
        yaxis_title='Avg Growth Rate (%)',
        hovermode='x unified'
    )
    fig_seasonal.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
    fig_seasonal.show()

    # --- 3. 2025 Performance vs. Benchmark ---
    df_2025 = df_hvfhs_growth[df_hvfhs_growth['year'] == 2025].copy()
    if not df_2025.empty:
        # Merge actuals with historical averages
        comparison = pd.merge(
            df_2025[['month_label', 'provider', 'mom_growth']], 
            seasonal_pattern, 
            on=['month_label', 'provider'], 
            suffixes=('_2025', '_hist_avg')
        )
        
        # Calculate Deviation (Alpha)
        comparison['deviation'] = comparison['mom_growth_2025'] - comparison['mom_growth_hist_avg']

        # Visualization: Benchmark Comparison
        fig_comp = px.bar(
            comparison, 
            x='month_label', y=['mom_growth_2025', 'mom_growth_hist_avg'],
            facet_col='provider',
            title='<span style="color:#00F2FF">2025 PERFORMANCE</span> vs. HISTORICAL BENCHMARKS',
            color_discrete_sequence=[THEME['accent'], THEME['cyan']],
            labels={'value': 'Growth Rate (%)', 'variable': 'Period'},
            category_orders={'month_label': month_order},
            barmode='group'
        )
        fig_comp.update_layout(template='plotly_dark', plot_bgcolor=THEME['bg'], paper_bgcolor=THEME['bg'])
        fig_comp.show()

        # --- 4. Strategic Summary Table ---
        print("\\nSTRATEGIC GAP ANALYSIS: 2025 vs. HISTORICAL AVERAGES")
        summary_pivot = comparison.pivot(index='provider', columns='month_label', values='deviation')
        display(summary_pivot.style.background_gradient(cmap='RdYlGn', axis=None).format('{:+.2f}%'))
else:
    print("Warning: df_hvfhs_growth not found. Please ensure EDA Phase 2.2.1 is executed.")"""

update_notebook_cell('Analysis.ipynb', '# [2.2.2.2]', new_code)
