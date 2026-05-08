import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find index of 1.3.A
target_idx = -1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code' and '1.3.A Market Saturation Forecast' in ''.join(cell['source']):
        target_idx = i
        break

if target_idx != -1:
    explanation_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "### Methodology: Market Saturation Forecasting Logic\n",
            "\n",
            "To provide a highly accurate projection, the model follows a 3-step scientific process:\n",
            "\n",
            "1. **Mature Market Filtering (2023-2025)**:\n",
            "   - We exclude 2021-2022 data (Post-COVID rebound phase) to eliminate extreme outliers.\n",
            "   - Focusing on the **2023-2025 period** captures the current \"Mature\" state of the NYC market.\n",
            "\n",
            "2. **Seasonality Smoothing (Rolling 6-Month Average)**:\n",
            "   - Raw MoM growth is highly volatile due to weather and holidays. We apply a **6-month rolling average**:\n",
            "     $$\\text{Smoothed Growth}_t = \\frac{\\sum_{i=0}^{5} \\text{Growth}_{t-i}}{6}$$\n",
            "   - This reveals the underlying \"Market Velocity\" by removing short-term noise.\n",
            "\n",
            "3. **Linear Regression & Confidence Intervals**:\n",
            "   - We fit a linear trend line: $$y = ax + b$$\n",
            "   - **Slope ($a$)**: Represents the rate of deceleration. When $y=0$, the market hits absolute saturation.\n",
            "   - **95% Confidence Interval**: Calculated using the **Standard Error of the Estimate (RMSE)**. The shaded band represents the margin of error ($y \\pm 1.96 \\cdot \\sigma$)."
        ]
    }
    nb['cells'].insert(target_idx, explanation_cell)

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
