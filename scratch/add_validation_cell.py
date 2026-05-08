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
        "# Testing our Linear Saturation Model against the '2026_Plus' synthetic/test dataset.\n",
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
        "# 2. Calculate Actual Growth in 2026\n",
        "# We combine with the last month of 2025 to get the first MoM of 2026\n",
        "last_2025 = df_f.tail(1)[['month', 'total_trips']]\n",
        "df_val = pd.concat([last_2025, df_2026]).sort_values('month')\n",
        "df_val['actual_growth'] = df_val['total_trips'].pct_change() * 100\n",
        "df_val = df_val.dropna() # Remove the last 2025 row\n",
        "\n",
        "# 3. Predict Growth for 2026 using the model from 1.3.A\n",
        "# The index continues from where df_f left off\n",
        "start_idx = len(df_f)\n",
        "df_val['month_idx'] = range(start_idx, start_idx + len(df_val))\n",
        "df_val['predicted_growth'] = model.predict(df_val[['month_idx']])\n",
        "\n",
        "# 4. Visualization: Actual vs Predicted\n",
        "fig_val = px.line(df_val, x='month', y=['actual_growth', 'predicted_growth'],\n",
        "                  title='Forecast Validation: Predicted vs Actual MoM Growth (2026 Test Set)',\n",
        "                  labels={'month': 'Month (2026)', 'value': 'Growth Rate (%)', 'variable': 'Type'},\n",
        "                  color_discrete_sequence=['white', '#FF00BF'],\n",
        "                  markers=True)\n",
        "\n",
        "fig_val.update_layout(template='plotly_dark')\n",
        "fig_val.show()\n",
        "\n",
        "# 5. Error Analysis\n",
        "mae = np.mean(np.abs(df_val['actual_growth'] - df_val['predicted_growth']))\n",
        "print(f\"\\n--- VALIDATION RESULTS (2026 TEST SET) ---\")\n",
        "print(f\"Mean Absolute Error (MAE): {mae:.2f}%\")\n",
        "if mae < 1:\n",
        "    print(\"SUCCESS: The model is highly accurate. Market saturation is following the predicted linear trend.\")\n",
        "else:\n",
        "    print(\"NOTICE: There is a deviation. The market might be recovering or saturating faster than expected.\")\n"
    ]
}

nb['cells'].append(new_cell)

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
