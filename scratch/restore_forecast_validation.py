import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 1.3.B Forecast Validation (2026 Testing)\n",
        "# Testing our Smoothed Saturation Model against the '2026_Plus' dataset.\n",
        "\n",
        "# 1. Query: Actual 2026 Data\n",
        "query_2026 = \"\"\"\n",
        "SELECT \n",
        "    date_trunc('month', pickup_datetime) as month,\n",
        "    count(*) as total_trips\n",
        "FROM fhvhv_2026_plus_cleaned\n",
        "WHERE year(pickup_datetime) = 2026\n",
        "GROUP BY 1\n",
        "ORDER BY 1\n",
        "\"\"\"\n",
        "df_2026 = con.execute(query_2026).df()\n",
        "\n",
        "# 2. Calculate Smoothed Growth for 2026\n",
        "# We need the previous 11 months from df_f to calculate the 12-month rolling average for early 2026\n",
        "query_2025 = \"\"\"\n",
        "SELECT \n",
        "    date_trunc('month', pickup_datetime) as month,\n",
        "    count(*) as total_trips\n",
        "FROM fhvhv_2019_2025_cleaned\n",
        "WHERE year(pickup_datetime) = 2025\n",
        "GROUP BY 1\n",
        "ORDER BY 1\n",
        "\"\"\"\n",
        "df_2025_full = con.execute(query_2025).df()\n",
        "\n",
        "df_val = pd.concat([df_2025_full, df_2026]).sort_values('month')\n",
        "df_val['mom_growth_raw'] = df_val['total_trips'].pct_change() * 100\n",
        "df_val['actual_smoothed_growth'] = df_val['mom_growth_raw'].rolling(window=12, min_periods=12).mean()\n",
        "\n",
        "# Keep only 2026 for validation\n",
        "df_val_2026 = df_val[df_val['month'].dt.year == 2026].copy()\n",
        "\n",
        "# 3. Predict Growth for 2026 using the model from 1.3.A\n",
        "# The index continues from where df_f left off\n",
        "start_idx = len(df_f)\n",
        "df_val_2026['month_idx'] = range(start_idx, start_idx + len(df_val_2026))\n",
        "df_val_2026['predicted_growth'] = model.predict(df_val_2026[['month_idx']])\n",
        "\n",
        "# 4. Visualization: Actual vs Predicted (Smoothed)\n",
        "import plotly.express as px\n",
        "fig_val = px.line(df_val_2026, x='month', y=['actual_smoothed_growth', 'predicted_growth'],\n",
        "                  title='Forecast Validation: Predicted vs Actual Smoothed MoM Growth (2026 Test Set)',\n",
        "                  labels={'month': 'Month (2026)', 'value': 'Smoothed Growth Rate (%)', 'variable': 'Type'},\n",
        "                  color_discrete_map={'actual_smoothed_growth': 'white', 'predicted_growth': '#FF00BF'},\n",
        "                  markers=True)\n",
        "\n",
        "fig_val.update_layout(template='plotly_dark')\n",
        "fig_val.show()\n",
        "\n",
        "# 5. Error Analysis\n",
        "mae = np.mean(np.abs(df_val_2026['actual_smoothed_growth'] - df_val_2026['predicted_growth']))\n",
        "print(f\"\\n--- VALIDATION RESULTS (2026 TEST SET) ---\")\n",
        "print(f\"Mean Absolute Error (MAE): {mae:.3f}%\")\n",
        "print(f\"Actual 2026 Average Smoothed Growth: {df_val_2026['actual_smoothed_growth'].mean():.3f}%\")\n",
        "if mae < 1.0:\n",
        "    print(\"SUCCESS: The model is highly accurate. The smoothed saturation trend held true in 2026.\")\n",
        "else:\n",
        "    print(\"NOTICE: There is a deviation. The market might be recovering or saturating at a different rate than predicted.\")\n"
    ]
}

# Append the new cell to the notebook
nb['cells'].append(new_cell)

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
