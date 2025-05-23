# COVID-19 Global Tracker

![Sample Visualization](output/global_trends.png)

A data-driven project analyzing global COVID-19 trends, including case tracking, death rates, and vaccination progress through dynamic visualizations.

## ✅ Features

* Visualize global COVID-19 trends (cases, deaths, vaccinations) using data analysis and visualization libraries.
* Compare key metrics across multiple countries.
* Automatic data acquisition from local or online sources.
* Export cleaned datasets for further analysis.
* Generate interactive visualizations for comprehensive data interpretation.

## 🛠️ Requirements

* **Python 3.8+**
* Python libraries: `pandas`, `matplotlib`, `seaborn`

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/JuniorCarti/PLP-WK-8-covid19-global-tracker.git
   cd PLP-WK-8-covid19-global-tracker
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

Run the analysis script to generate visualizations and export cleaned data:

```bash
python covid_analysis.py
```

This command will:

1. Download or use existing COVID-19 data.
2. Clean and process the dataset.
3. Generate visualizations in the `output` folder.
4. Save the cleaned dataset as a CSV file.

## 📂 Output Files

* `global_trends.png`: Global trends for cases, deaths, and vaccinations.
* `country_comparison_*.png`: Visual comparisons of COVID-19 metrics across countries.
* `covid_clean_data.csv`: Processed and cleaned dataset for further analysis.

Here’s the updated repository structure with the correct order:

## 📦 Repository Structure

```
PLP-WK-8-covid19-global-tracker/
│
├── output/                 # Output visualizations and data
│   ├── global_trends.png
│   ├── country_comparison_cases_per_million.png
│   ├── country_comparison_deaths_per_million.png
│   ├── country_comparison_pct_fully_vaccinated.png
│   └── covid_clean_data.csv
├── sample_data/            # (Optional) Sample dataset
│   └── owid-covid-data.csv
├── README.md               # Project documentation
├── covid_analysis.py       # Main analysis script
└── requirements.txt        # Dependencies
```
## 📊 Data Source


Due to file size limitations on GitHub, the `owid-covid-data.csv` file is not included in the repository.
To run the analysis, download the latest COVID-19 dataset from [Our World in Data](https://ourworldindata.org/covid-cases) and place it in the `sample_data/` directory as:
sample_data/owid-covid-data.csv
```

## 📝 License

This project is licensed under the MIT License.
