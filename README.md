# PLP-WK-8-covid19-global-tracker

![Sample Visualization](output/country_comparison_cases_per_million.png)

A comprehensive analysis of worldwide COVID-19 trends including case tracking, death rates, and vaccination progress.

## Features

- Global trends visualization (cases, deaths, vaccinations)
- Country comparison charts
- Automatic data loading (local or online sources)
- Cleaned data export
- Interactive visualizations

## Requirements

- Python 3.8+
- Required packages: `pandas`, `matplotlib`, `seaborn`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/covid19-global-tracker.git
   cd covid19-global-tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the analysis script:
```bash
python covid_analysis.py
```

This will:
1. Download or use local COVID-19 data
2. Clean and process the data
3. Generate visualizations in the `output` folder
4. Save cleaned data as CSV

## Output Files

- `global_trends.png`: Global trends in cases, deaths, and vaccinations
- `country_comparison_*.png`: Country comparisons for key metrics
- `covid_clean_data.csv`: Cleaned dataset ready for further analysis

## Data Sources

Data is sourced from [Our World in Data](https://ourworldindata.org/covid-cases) COVID-19 dataset.

## License

This project is licensed under the MIT License.
```

## Repository Structure

```
covid19-global-tracker/
│
├── covid_analysis.py       # Main analysis script
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── output/                 # Generated output folder
│   ├── global_trends.png
│   ├── country_comparison_cases_per_million.png
│   ├── country_comparison_deaths_per_million.png
│   ├── country_comparison_pct_fully_vaccinated.png
│   └── covid_clean_data.csv
└── sample_data/            # (Optional) Sample data for testing
    └── owid-covid-data.csv
```
