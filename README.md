# Big Data Analytics Final Project

## Your First Week at Owl Analytics

This repository contains the final project brief and starter folder structure.

Start here:

1. [Welcome](01_Welcome.md)
2. [Team 1: Data Collection](02_Team1_Data_Collection.md)
3. [Team 2: Data Quality](03_Team2_Data_Quality.md)
4. [Team 3: Analytics](04_Team3_Analytics.md)
5. [Report and Reflection](05_Report_and_Reflection.md)
6. [Submission Guidelines](06_Submission_Guidelines.md)
7. [Rubric](07_Rubric.md)

## Starter Structure

The repository includes folders for the files you will generate:

```txt
data/clean/
data/messy/
results/
reports/
```

Your datasets, logs, notebooks, reports, and result files should be created by your own code during the project. Do not commit a `.venv/` folder.

### Provided Scripts

The `scripts/` folder already contains small helper scripts:

- `get_one_record.py`: tests the Binance API by downloading one `BTCUSDT` record.
- `save_dictionary_to_csv.py`: shows how to save one Python dictionary as a CSV row.
- `mess_my_data.py`: creates the messy dataset for Team 2 after you complete Team 1.
- Script part1_build_dataset.py is placed within the scripts folder. It uses multithreading and serial threading to get through api request candlestick market data for 10 crypto symbols at 1h intervals for a limit of 1000 records of clean data per crypto symbol.

Run the first two scripts before building `part1_build_dataset.py`. Run `mess_my_data.py` only after you have created `data/clean/clean_market_data.csv`.

## Author

**Markos Toufexis**

Repository: [https://github.com/MarkosTouf/BDA---Final-Project](https://github.com/MarkosTouf/BDA---Final-Project)

## Project Overview

Specific project simulates work in a small analytics team ("Owl Analytics") working with real historical cryptocurrency market data taken via downloader using the Binance public API. 
For Team 1 collecting the data and updating in csv while of 10000 records for 1000 records download for each of the 10 crypto currencies analysed. Run is also captured log file. Team 1 uses multithreading and and manages concurrency.
For team 2 performing data cleaning for datatypes, incorrect numeric or timestamp values, impossible trades and volumes as well as impossible price ranges and and adding quality-checks in it, as well as checking a dataset sample of 50 recods.
For Team 3 running full-dataset analytics in Spark via both spark data pipeline logical transformations and embedded sql queries. And then producing aggregated summary reports and aggregated final market summary report with addition of volatility and activity rankings for dataset symbols analysed.

## How to Run

### Team 1 (VS Code)

From the project root, with the virtual environment activated:

```bash
python scripts/part1_build_dataset.py
```

This downloads market data for 10 crypto symbols and creates `data/clean/clean_market_data.csv`, `results/api_download.log`, and `results/runtime_comparison.csv`.

### Team 2 (VS Code)

Requires the same virtual environment as Team 1, plus the Jupyter extension for VS Code.

1. First, generate the messy dataset (requires `clean_market_data.csv` from Team 1):

```bash
python scripts/mess_my_data.py --input data/clean/clean_market_data.csv --output data/messy/messy_market_data.csv
```

2. Open `scripts/part2_clean_with_pandas.ipynb` in VS Code and run all cells (Run All).

This produces `data/clean/cleaned_market_data.csv`, `results/pandas_sample_results.csv`, and the data-quality report (printed inside the notebook).

### Team 3 (Google Colab)

The Spark analytics notebook was developed and run in Google Colab, then saved into this repository:

[scripts/part3_spark_analytics.ipynb](scripts/part3_spark_analytics.ipynb)

Google collab is linked in the repo as well.

To re-run it, upload `data/clean/cleaned_market_data.csv` and `results/pandas_sample_results.csv` directly into the Colab file panel, then run all cells. This produces `results/spark_market_summary.csv`.

## Reports

The final written report explains how the project was built, whether the data is reliable, and what the analytics showed — written for Stelios, without line-by-line code explanation.

- [Report to Stelios](reports/report_to_stelios.md)

The reflection covers the hardest technical challenges faced, whether multithreading helped, and what pandas and Spark each made easier.

- [Reflection](reports/reflection.md)

## Submitted Files

**Scripts:**
- `part1_build_dataset.py`
- `scripts/part2_clean_with_pandas.ipynb`
- `scripts/part3_spark_analytics.ipynb`
- `scripts/get_one_record.py`
- `scripts/save_dictionary_to_csv.py`
- `scripts/mess_my_data.py`

**Data:**
- `data/clean/clean_market_data.csv` (10,000 records from Team 1)
- `data/messy/messy_market_data.csv` (Team 2 input)
- `data/clean/cleaned_market_data.csv` (Team 2 output)

**Results:**
- `results/api_download.log`
- `results/runtime_comparison.csv`
- `results/pandas_sample_results.csv`
- `results/spark_market_summary.csv`

**Reports:**
- `reports/report_to_stelios.md`
- `reports/reflection.md`
