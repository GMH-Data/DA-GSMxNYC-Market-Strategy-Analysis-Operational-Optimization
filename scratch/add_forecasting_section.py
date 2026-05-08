import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

new_cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# 1.3 Business Forecasting\n",
            "Predicting the future of the market based on historical trends and saturation velocity."
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 1.3.A Market Saturation Forecast (Zero Growth Projection)\n",
            "import numpy as np\n",
            "import pandas as pd\n",
            "import plotly.express as px\n",
            "from sklearn.linear_model import LinearRegression\n",
            "\n",
            "# 1. Query: Monthly Trip Counts (2021-2025)\n",
            "query_forecast = \"\"\"\n",
            "SELECT \n",
            "    date_trunc('month', pickup_datetime) as month,\n",
            "    count(*) as total_trips\n",
            "FROM fhvhv_2019_2025_cleaned\n",
            "WHERE year(pickup_datetime) BETWEEN 2021 AND 2025\n",
            "GROUP BY 1\n",
            "ORDER BY 1\n",
            "\"\"\"\n",
            "df_f = con.execute(query_forecast).df()\n",
            "\n",
            "# 2. Calculate MoM Growth Rate\n",
            "df_f['mom_growth'] = df_f['total_trips'].pct_change() * 100\n",
            "df_f = df_f.dropna()\n",
            "\n",
            "# 3. Linear Regression on Growth Rate Trend\n",
            "# X: Month index, Y: MoM Growth %\n",
            "df_f['month_idx'] = range(len(df_f))\n",
            "X = df_f[['month_idx']]\n",
            "y = df_f['mom_growth']\n",
            "\n",
            "model = LinearRegression()\n",
            "model.fit(X, y)\n",
            "\n",
            "# Predict when y (growth) hits 0\n",
            "slope = model.coef_[0]\n",
            "intercept = model.intercept_\n",
            "zero_growth_idx = -intercept / slope\n",
            "\n",
            "# Convert index back to date\n",
            "start_date = df_f['month'].min()\n",
            "predicted_date = start_date + pd.DateOffset(months=int(zero_growth_idx))\n",
            "\n",
            "# 4. Visualization\n",
            "df_f['trend_line'] = model.predict(X)\n",
            "\n",
            "fig = px.line(df_f, x='month', y=['mom_growth', 'trend_line'],\n",
            "              title='Market Growth Velocity Trend (MoM %): Projecting Saturation',\n",
            "              labels={'month': 'Date', 'value': 'Growth Rate (%)', 'variable': 'Series'},\n",
            "              color_discrete_sequence=['#FF00BF', 'white'])\n",
            "\n",
            "fig.update_layout(template='plotly_dark')\n",
            "fig.show()\n",
            "\n",
            "print(f\"\\n--- FORECASTING INSIGHT (2021-2025 Trend) ---\")\n",
            "print(f\"Current Growth Slope: {slope:.4f} % per month\")\n",
            "if slope < 0:\n",
            "    print(f\"Projected 'Absolute Saturation' (Zero Growth): {predicted_date.strftime('%B %Y')}\")\n",
            "    print(\"Strategy: Focus on efficiency and revenue-per-trip rather than volume expansion as market hits maturity.\")\n",
            "else:\n",
            "    print(\"The market growth is currently accelerating or stable. Saturation is not yet projected based on the 2021-2025 trend.\")\n"
        ]
    }
]

nb['cells'].extend(new_cells)

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
