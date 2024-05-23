# Stock-Price-Prediction

## Overview
This project focuses on predicting how stock prices will change at the closing auction in the last ten minutes of the Nasdaq trading day. It is based on the Optiver Trading at the Close Kaggle challenge. The aim is to analyze and model the given data to make accurate predictions about stock price movements.

## Dataset
The dataset contains records with various features related to stock trading activity. Key fields include:

- `row_id`: Unique identifier for each record.
- `time_id`: Sequential indicator for time buckets.
- `stock_id`: Unique identifier for each stock.
- `date_id`: Unique identifier for each date.
- `imbalance_size`, `imbalance_buy_sell_flag`: Indicators of auction imbalance.
- `reference_price`, `matched_size`, `far_price`, `near_price`: Prices and matched sizes at different auction stages.
- `bid_price`, `ask_price`, `bid_size`, `ask_size`: Most competitive buy/sell levels.
- `wap`: Weighted average price in the non-auction book.
- `seconds_in_bucket`: Number of seconds elapsed since the beginning of the day's closing auction.
- `target`: The 60-second future move in the WAP of the stock, less the 60-second future move of the synthetic index (training set only).

## Tasks
1. Data Cleaning and Anomaly Detection:
- Inspect and clean the data to handle any anomalies that could affect analysis.

2. Pairwise Correlation Analysis:
- Construct a pairwise correlation table of the given variables using Pearson correlation.
- Explain the reasons for high absolute correlations between certain pairs of variables.

3. Stock-Day Distance and Autocorrelation Analysis:
- Define an average record for each stock on a particular day.
- Measure the autocorrelation of the average distance between day i and day i+k.
- Determine if there is a statistically significant degree of autocorrelation in the market.

4. Stock Similarity Analysis:
- Measure the distance between pairs of stocks for each day.
- Identify pairs of stocks that are unusually similar consistently.

5. Clustering and Visualization:
- Create consensus records for each stock.
- Cluster the stocks using an algorithm like k-means.
- Visualize the clusters using a TSNE plot and assess the coherence of the clusters.

6. Market Trend Analysis:
- Determine if the closing trajectory of stocks is highly correlated or random.
- Create plots to support the conclusion and perform a statistical test if applicable.

7. Permutation Test:
- Perform a permutation test to determine statistical confidence in the conclusion.
- Run enough permutations to establish a p-value.

8. Prediction Model Building:
- Build and evaluate various models to solve the Kaggle task.
- Report the average absolute error using 5-fold cross-validation for each model.

## Usage
To run the project, open the `stock_price_prediction.ipynb` notebook and execute the cells in order. Ensure you have all the necessary libraries installed.

## Requirements
- Python 3.x
- Jupyter Notebook
- Libraries: Pandas, Scikit-learn, NumPy, Matplotlib, Seaborn
