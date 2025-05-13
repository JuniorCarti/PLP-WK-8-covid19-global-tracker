# COVID-19 GLOBAL DATA TRACKER
# ===========================
# A comprehensive analysis of worldwide COVID-19 trends
# Includes case tracking, death rates, and vaccination progress

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configure visualization settings
plt.style.use('ggplot')
sns.set_theme(style="whitegrid", palette="viridis")
pd.set_option('display.max_columns', 50)
pd.set_option('display.float_format', '{:.2f}'.format)

# 1. DATA LOADING WITH MULTIPLE SOURCES
# ------------------------------------
def load_covid_data():
    """Load COVID-19 data from multiple potential sources"""
    data_sources = [
        "sample_data/owid-covid-data.csv",  # Local file
        "https://covid.ourworldindata.org/data/owid-covid-data.csv",  # Primary source
        "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv"  # GitHub mirror
    ]
    
    for source in data_sources:
        try:
            if source.startswith('http'):
                print(f"Attempting to download from {source}")
                df = pd.read_csv(source, parse_dates=['date'], low_memory=False)
            else:
                if os.path.exists(source):
                    print(f"Loading local file: {source}")
                    df = pd.read_csv(source, parse_dates=['date'], low_memory=False)
                else:
                    continue
            
            print(f"✅ Successfully loaded data with {len(df)} records")
            return df
        
        except Exception as e:
            print(f"⚠️ Failed to load from {source}: {str(e)}")
    
    print("❌ All data sources failed. Please check your internet connection or download the data manually.")
    exit()

# 2. DATA CLEANING AND PREPARATION
# --------------------------------
def clean_covid_data(raw_df):
    """Clean and prepare COVID-19 data for analysis"""
    # Essential columns with fallbacks
    essential_cols = [
        'date', 'location', 'iso_code', 'continent', 'population',
        'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
        'total_cases_per_million', 'new_cases_per_million',
        'total_deaths_per_million', 'new_deaths_per_million'
    ]
    
    # Vaccination data (optional)
    vaccination_cols = [
        'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
        'new_vaccinations', 'total_boosters'
    ]
    
    # Select available columns only
    available_cols = [col for col in essential_cols if col in raw_df.columns]
    available_cols += [col for col in vaccination_cols if col in raw_df.columns]
    
    # Create cleaned dataframe
    clean_df = raw_df[available_cols].copy()
    
    # Remove aggregate regions
    non_countries = [
        'World', 'Europe', 'Asia', 'Africa', 'North America', 'South America',
        'European Union', 'International', 'High income', 'Low income',
        'Lower middle income', 'Upper middle income', 'Oceania'
    ]
    clean_df = clean_df[~clean_df['location'].isin(non_countries)]
    
    # Handle missing values
    numeric_cols = clean_df.select_dtypes(include=[np.number]).columns
    clean_df[numeric_cols] = clean_df.groupby('location')[numeric_cols].transform(
        lambda x: x.ffill().fillna(0)
    )
    
    # Calculate derived metrics
    clean_df['case_fatality_rate'] = (clean_df['total_deaths'] / clean_df['total_cases']) * 100
    clean_df['weekly_case_growth'] = clean_df.groupby('location')['new_cases'].transform(
        lambda x: x.rolling(7).sum().pct_change()
    )
    
    if 'people_vaccinated' in clean_df.columns:
        clean_df['pct_vaccinated'] = (clean_df['people_vaccinated'] / clean_df['population']) * 100
    
    if 'people_fully_vaccinated' in clean_df.columns:
        clean_df['pct_fully_vaccinated'] = (clean_df['people_fully_vaccinated'] / clean_df['population']) * 100
    
    # Add time features
    clean_df['year'] = clean_df['date'].dt.year
    clean_df['month'] = clean_df['date'].dt.month
    
    return clean_df

# 3. VISUALIZATION FUNCTIONS
# --------------------------
def plot_global_trends(data):
    """Visualize global COVID-19 trends"""
    try:
        # Aggregate global data
        global_data = data.groupby('date').agg({
            'new_cases': 'sum',
            'new_deaths': 'sum',
            'new_vaccinations': 'sum' if 'new_vaccinations' in data.columns else None
        }).reset_index()
        
        # Create figure
        fig, axes = plt.subplots(3, 1, figsize=(14, 15))
        
        # Plot cases
        axes[0].plot(global_data['date'], global_data['new_cases'].rolling(7).mean(),
                    color='#1f77b4', linewidth=2)
        axes[0].set_title('Global Daily New Cases (7-day average)', fontsize=12)
        axes[0].set_ylabel('Cases')
        axes[0].grid(True, alpha=0.3)
        
        # Plot deaths
        axes[1].plot(global_data['date'], global_data['new_deaths'].rolling(7).mean(),
                    color='#d62728', linewidth=2)
        axes[1].set_title('Global Daily New Deaths (7-day average)', fontsize=12)
        axes[1].set_ylabel('Deaths')
        axes[1].grid(True, alpha=0.3)
        
        # Plot vaccinations if available
        if 'new_vaccinations' in global_data.columns:
            axes[2].plot(global_data['date'], global_data['new_vaccinations'].rolling(7).mean(),
                        color='#2ca02c', linewidth=2)
            axes[2].set_title('Global Daily Vaccinations (7-day average)', fontsize=12)
            axes[2].set_ylabel('Vaccinations')
            axes[2].grid(True, alpha=0.3)
        else:
            fig.delaxes(axes[2])
        
        plt.tight_layout()
        plt.savefig('output/global_trends.png')
        plt.close()
        print("✅ Saved global trends visualization")
        
    except Exception as e:
        print(f"Error plotting global trends: {e}")

def plot_country_comparison(data, metric='total_cases_per_million', top_n=15):
    """Compare countries on key COVID-19 metrics"""
    try:
        # Get latest data
        latest = data[data['date'] == data['date'].max()]
        sorted_data = latest.dropna(subset=[metric]).sort_values(metric, ascending=False).head(top_n)
        
        if len(sorted_data) == 0:
            print(f"No data available for {metric}")
            return
        
        # Create plot
        plt.figure(figsize=(12, 8))
        ax = sns.barplot(x=metric, y='location', data=sorted_data, 
                        palette='viridis', edgecolor='black')
        
        # Add value labels
        for i, value in enumerate(sorted_data[metric]):
            ax.text(value/2, i, f"{value:,.1f}", 
                   va='center', ha='center', color='white', fontweight='bold')
        
        # Formatting
        if 'per_million' in metric:
            unit = "per million"
        elif 'pct' in metric:
            unit = "%"
        else:
            unit = "count"
        
        plt.title(f"Top {top_n} Countries by {metric.replace('_', ' ').title()}", pad=20)
        plt.xlabel(f"{metric.replace('_', ' ').title()} ({unit})")
        plt.ylabel("Country")
        plt.tight_layout()
        
        # Save plot
        filename = f"output/country_comparison_{metric}.png"
        plt.savefig(filename)
        plt.close()
        print(f"✅ Saved {filename}")
        
    except Exception as e:
        print(f"Error plotting country comparison: {e}")

# MAIN EXECUTION
# --------------
if __name__ == "__main__":
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Load and clean data
    print("🔄 Loading COVID-19 data...")
    raw_df = load_covid_data()
    clean_df = clean_covid_data(raw_df)
    
    print(f"\n📊 Cleaned data covers {clean_df['location'].nunique()} countries")
    print(f"📅 Time period: {clean_df['date'].min().date()} to {clean_df['date'].max().date()}")
    
    # Generate visualizations
    print("\n📈 Generating visualizations...")
    plot_global_trends(clean_df)
    plot_country_comparison(clean_df, 'cases_per_million')
    plot_country_comparison(clean_df, 'deaths_per_million')
    plot_country_comparison(clean_df, 'case_fatality_rate')
    
    if 'pct_fully_vaccinated' in clean_df.columns:
        plot_country_comparison(clean_df, 'pct_fully_vaccinated')
    
    # Save cleaned data
    clean_df.to_csv('output/covid_clean_data.csv', index=False)
    print("\n🎉 Analysis complete! Check the 'output' folder for results.")