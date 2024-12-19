
# Section 8 Investment Analyzer

## Overview
The Section 8 Investment Analyzer is a Python-based tool designed to assist real estate investors in identifying profitable investment opportunities in the Section 8 housing program. By analyzing data from Zillow.com and HUD (Department of Housing and Urban Development), this tool evaluates listings in five investor-friendly cities to recommend properties with significant potential for passive income.

### Key Features:
- Data collection from Zillow and HUD for housing listings and fair market rent values.
- Data cleaning to handle outliers, missing values, and inconsistencies.
- Cashflow analysis based on rental income, mortgage payments, and operational expenses.
- Interactive visualizations for property prices, area distribution, and geographic mapping.
- Final recommendation list of properties with at least $500 in monthly positive cash flow.

---

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Fall24-DSCI-510/final-project-rafayelmirijanyan1997.git
   cd section8-investment-analyzer
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download Data**:
   - Place raw data files in the `data/raw` directory.
   - If files exceed GitHub limits, download from the provided Google Drive link mentioned in the `README.md` file.

---

## Repository Structure
```
.
├── .gitignore
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── images/
│   ├── visualizations/
│   └── final_report.pdf
├── src/
│   ├── get_data.py
│   ├── clean_data.py
│   ├── analyze_data.py
│   ├── visualize_results.py
│   └── utils/
└── proposal.pdf
```

### Key Files:
- **`src/get_data.py`**: Script for scraping or downloading data.
- **`src/clean_data.py`**: Functions for cleaning and preprocessing data.
- **`src/analyze_data.py`**: Analysis scripts for evaluating investment properties.
- **`src/visualize_results.py`**: Visualization generation for analysis results.
- **`results/`**: Directory for final outputs, including plots, interactive visualizations, and the project report.

---

## How to Run the Project

1. **Fetch Data**:
   ```bash
   python src/get_data.py
   ```

2. **Clean Data**:
   ```bash
   python src/clean_data.py
   ```

3. **Analyze Data**:
   ```bash
   python src/analyze_data.py
   ```

4. **Generate Visualizations**:
   ```bash
   python src/visualize_results.py
   ```

5. **View Results**:
   - Open the `results/visualizations` directory for generated plots.
   - Review the interactive map in `results/visualizations/map.html`.
   - Check `results/final_report.pdf` for a detailed project summary.

---

## Data Sources
1. **Zillow.com**:
   - Provides property listings including price, area, and number of bedrooms.
2. **HUD (huduser.gov)**:
   - Supplies fair market rent data based on zip code and property specifications.

---

## Analysis and Visualizations

- **Data Cleaning**:
  - Outliers identified using IQR-based methods.
  - Null values removed and inconsistent formats standardized.
- **Key Visualizations**:
  - Price vs. Area scatter plots.
  - Distribution histograms of property prices.
  - Interactive maps showcasing property locations and details.

---

## Results

- Positive cash-flow properties identified in Detroit, Indianapolis, Memphis, Cleveland, and Birmingham.
- A total of 82 properties met the criteria of at least $500 in monthly passive income.
- Final recommendations saved in `results/passive_income_properties.csv`.

---

## Future Work
- Expand analysis to additional cities and states.
- Integrate crime rates and renovation costs into the evaluation model.
- Explore advanced visualization techniques for more engaging insights.

---

## Contributors
- **Rafayel Mirijanyan**
  - USC ID: 3487192016
  - GitHub: [rafayelmirijanyan1997](https://github.com/rafayelmirijanyan1997)

---

## Acknowledgements
- DSCI 510: Principles of Programming for Data Science, Viterbi School of Engineering, USC.
- Zillow.com and HUD for providing data resources.
