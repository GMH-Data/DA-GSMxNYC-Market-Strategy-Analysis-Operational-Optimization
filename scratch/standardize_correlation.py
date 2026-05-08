import json

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Define the new content for cell 1.2.1.C
new_source_lines = [
    "# 1.2.1.C Correlation Analysis: Uber, Lyft & Taxi\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "# 1. Query for operational factors\n",
    "query_c = \"\"\"\n",
    "SELECT \n",
    "    PULocationID,\n",
    "    count(CASE WHEN hvfhs_license_num = 'HV0003' THEN 1 END) * 1.0 / count(*) as uber_market_share,\n",
    "    count(CASE WHEN hvfhs_license_num = 'HV0005' THEN 1 END) * 1.0 / count(*) as lyft_market_share,\n",
    "    avg(date_diff('second', request_datetime, pickup_datetime)) / 60.0 as avg_wait_time_min,\n",
    "    avg(trip_miles) as avg_miles,\n",
    "    avg(trip_time) / 60.0 as avg_trip_time_min,\n",
    "    avg(base_passenger_fare) as avg_fare,\n",
    "    avg(tips) as avg_tips,\n",
    "    avg(driver_pay) as avg_driver_pay\n",
    "FROM fhvhv_2019_2025_cleaned\n",
    "WHERE year(pickup_datetime) BETWEEN 2019 AND 2025\n",
    "GROUP BY 1 HAVING count(*) > 100\n",
    "\"\"\"\n",
    "df_corr = con.execute(query_c).df()\n",
    "\n",
    "# 2. Standardization & Reordering for \"Standard\" Analysis\n",
    "# Order: Market Factors -> Operations -> Financials\n",
    "ordered_features = [\n",
    "    'uber_market_share', 'lyft_market_share', \n",
    "    'avg_wait_time_min', \n",
    "    'avg_fare', 'avg_tips', 'avg_driver_pay', \n",
    "    'avg_miles', 'avg_trip_time_min'\n",
    "]\n",
    "\n",
    "# User-friendly names\n",
    "name_map = {\n",
    "    'uber_market_share': 'Uber Share',\n",
    "    'lyft_market_share': 'Lyft Share',\n",
    "    'avg_wait_time_min': 'Wait Time',\n",
    "    'avg_fare': 'Avg Fare',\n",
    "    'avg_tips': 'Avg Tips',\n",
    "    'avg_driver_pay': 'Driver Pay',\n",
    "    'avg_miles': 'Trip Miles',\n",
    "    'avg_trip_time_min': 'Trip Time'\n",
    "}\n",
    "\n",
    "df_clean = df_corr[ordered_features].rename(columns=name_map)\n",
    "corr_matrix = df_clean.corr()\n",
    "\n",
    "# 3. Display Correlation Matrix (Market Focus)\n",
    "print(\"\\n--- DETAILED CORRELATION MATRIX (Standardized Order) ---\")\n",
    "display(corr_matrix[['Uber Share', 'Lyft Share']].round(3))\n",
    "\n",
    "# 4. Heatmaps: Market Share Drivers\n",
    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))\n",
    "sns.heatmap(corr_matrix[['Uber Share']].sort_values('Uber Share', ascending=False), annot=True, cmap='RdBu', ax=ax1, center=0)\n",
    "ax1.set_title('Uber Market Share Correlation Factors')\n",
    "sns.heatmap(corr_matrix[['Lyft Share']].sort_values('Lyft Share', ascending=False), annot=True, cmap='RdBu', ax=ax2, center=0)\n",
    "ax2.set_title('Lyft Market Share Correlation Factors')\n",
    "plt.tight_layout()\n",
    "plt.show()\n",
    "\n",
    "# 5. Full Triangular Correlation Heatmap\n",
    "plt.figure(figsize=(12, 10))\n",
    "mask = np.tril(np.ones_like(corr_matrix, dtype=bool)) # Hiding lower half\n",
    "sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdBu', center=0, fmt='.2f')\n",
    "plt.title('Triangular Correlation Matrix: All Business Metrics')\n",
    "plt.show()\n"
]

for cell in nb['cells']:
    if cell['cell_type'] == 'code' and '1.2.1.C Correlation Analysis: Uber, Lyft & Taxi' in ''.join(cell['source']):
        cell['source'] = new_source_lines
        break

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
