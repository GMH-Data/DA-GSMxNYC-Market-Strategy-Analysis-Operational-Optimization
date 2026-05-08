import json

translations = {
    16: ["### 1. Market Share and Competition\n"],
    17: [
        "#### A. Overall Scale and Peak Month\n",
        "How does the overall scale of the HVFHS market (total trips) change month-over-month from 2019 to 2025 compared to Green and Yellow taxis? Which month is the peak?\n"
    ],
    19: [
        "#### B. Market Share of the 'Big Four'\n",
        "How is the trip market share distributed among the four major providers (Uber, Lyft, Via, Juno) each year?\n"
    ],
    21: [
        "#### C. Correlation Analysis\n",
        "Correlation analysis between market share and operational factors for both ride-hailing and traditional taxis.\n"
    ],
    23: [
        "#### D. Competition Analysis: Uber vs Lyft Detailed\n",
        "Visualizing competition areas and the list of key/high-volume zones.\n"
    ],
    26: [
        "#### E. Temporal Competition Analysis: Time of Day & Year\n",
        "Analyzing competition density by hour and month.\n"
    ],
    30: [
        "#### F. Temporal Competition Analysis: Time of Year\n",
        "Analyzing competition density by month.\n"
    ]
}

with open('Data.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for idx, new_source in translations.items():
    if idx < len(nb['cells']):
        nb['cells'][idx]['source'] = new_source

with open('Data.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
