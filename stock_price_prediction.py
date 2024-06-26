# -*- coding: utf-8 -*-
"""cse519_hw3_segireddy_rutwik_115936140.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PsPElqThWZrjhvITqLEg-K1Bt1tT35ai

#### TOC
1. Anomalies in Data, and cleaning action & explaination. 15 pts
2. Pairwise Corralation Table and explaition. 10 pts
3. Average records stockID vs Day, 25 pts
    - a. autocorrelation, 10 pts
    - b. measure the distance, 5 pts
    - c. clustering algorithm, 10 pts
4. Closing trajectory of stocks on each day highly correlated, 25 pts
   - a. Make three plots, 10 pts
   - b. permutation test to determine the statistical confidence, 15 pts
      p-value
5. Best prediction model, any approaches, 25 pts
6. submit model on Kaggle, 0 pts

#### Start
- Copy this notebook.
  In Google Colab use `File -> Save a Copy in Drive`.
- Use the "Text" blocks to provide explanations wherever you find them necessary.
- Highlight your answers inside these text fields to ensure that we don't miss it
while grading your HW.

#### Setup

- Code to download the data directly from the colab notebook.
- If you find it easier to download the data from the kaggle website (and
uploading it to your drive), you can skip this section.
"""

# Commented out IPython magic to ensure Python compatibility.
## First mount your drive before running analysis code
from google.colab import drive
drive.mount('/content/drive')

## Create a folder for the this HW and change to that dir
# %cd drive/MyDrive/cse519

## packages
# !pip install -q kaggle
# !pip install -q pandas
# !pip install -q scikit-learn
# !pip install -q numpy
# !pip install -q Matplotlib
# !pip install -q seaborn

## Upload the file by clicking on the browse
from google.colab import files
files.upload()

## Create a new API token under "Account" in the kaggle webpage and download the json file

# !mkdir ~/.kaggle
# !cp kaggle.json ~/.kaggle/
# !kaggle competitions download -c optiver-trading-at-the-close
# !unzip optiver-trading-at-the-close.zip

"""#### Q1: Anomalies and Cleaning, 15 pts

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

col_names = [
  "stock_id",
  "date_id",
  "seconds_in_bucket",
  "imbalance_size",
  "imbalance_buy_sell_flag",
  "reference_price",
  "matched_size",
  "far_price",
  "near_price",
  "bid_price",
  "bid_size",
  "ask_price",
  "ask_size",
  "wap",
  "target",
  "time_id",
  "row_id"
]
dtypes = {
  "stock_id": np.int,
  "date_id":np.int,
  "seconds_in_bucket":np.int,
  "imbalance_size":np.float64,
  "imbalance_buy_sell_flag":np.int,
  "reference_price":np.float64,
  "matched_size":np.float64,
  "far_price":np.float64,
  "near_price":np.float64,
  "bid_price":np.float64,
  "bid_size":np.float64,
  "ask_price":np.float64,
  "ask_size":np.float64,
  "wap":np.float64,
  "target":np.float64,
  "time_id":np.int,
  "row_id": "string",
}
csv = pd.read_csv("train.csv")

"""## Dataset Analysis
- 200 unique stocks
- [0, 480] is the range of dates
- Closing Auction Time Range is divided into buckets of 10 seconds from 0 to 540
- 55% of the far price and near price values are NULL
- 88 values in the target column are NULL

"""

print("------------Metrics-----------\n")
print(f"Stocks Count: {len(csv['stock_id'].unique())}")
print(f"Date ID Range: {csv['date_id'].min()}, {csv['date_id'].max()}")
print(f"Closing Auction Time Range: {csv['seconds_in_bucket'].min()}, {csv['seconds_in_bucket'].max()} \n\tList of values {csv['seconds_in_bucket'].unique()}")
# print(f"Stocks Count: {csv['imbalance_buy_sell_flag'].unique()}")
print(f"Percentage of null values in Far Price: {csv['far_price'].isna().sum() * 100 / len(csv['far_price'])}")
print(f"Percentage of null values in Near Price: {csv['near_price'].isna().sum() * 100 / len(csv['near_price'])}")
print(f"Number of null values in Target Price: {csv['target'].isna().sum()} out of {len(csv['target'])}")
csv

print("-------------Data after pre-processing---------------\n")
cleaned_csv = csv.dropna(subset=['target'])
print(f"Number of null values in Target Price: {csv['target'].isna().sum()} out of {len(csv['target'])}")
cleaned_csv

"""## Results:
- Removed the rows having NULL values in the target column since these rows are meant to be predicted, it doesn't make sense to have them in the dataset.
- About 50% of the Far and Near Price values are NULL because NASDAQ releases the data for these values at 3:55 pm. This leaves a 5-minute time interval where there is no information available for these values.

#### Q2: Pairwise Corralation Table and Explaition. 10 pts
"""

correlation_table = cleaned_csv.corr(method='pearson', numeric_only=True)
ax = sns.heatmap(correlation_table, vmin=-1, vmax=1, center=0,
                 cmap=sns.diverging_palette(10, 125, n=10), linewidths=0.5,
                 linecolor='black')
plt.show()

"""## Results
- I have constructed a correlation table that takes values from -1 to 1 using Pearson correlation.
- Following is the list of features that are highly correlated (correlation>0.8)
  - date_id and time_id
  - reference_price and bid_price
  - reference_price and ask_price
  - reference_price and wap
  - bid_price and ask_price
  - bid_price and wap
  - ask_price and wap
- This effectiveley means that (date_id, time_id) and (reference_price, bid_price, ask_price, wap) are strongly correlated.
- We find out that time_id = (date_id * 55) + (seconds_in_bucket / 10) which naturally means that date_id and time_id are highly correlated.
- The line plot for (reference_price, bid_price, ask_price, wap) is generated to provide evidence for the high correlation. Given that each of these values is directly or indirectly connected in the stock market realm, it is expected that they would exhibit a strong correlation.
"""

# Correlation betwreen date_id and time_id

# Scatter plot between date_id and time_id
plt.scatter(cleaned_csv['date_id'], cleaned_csv['time_id'], s=0.1)
plt.xlabel('date_id')
plt.ylabel('time_id')
plt.title('Correlation between date_id and time_id')
plt.show()

# Find out the relationship between date_id and time_id
# time_id = (date_id * 55) + (seconds_in_bucket / 10)
stock0 = cleaned_csv[cleaned_csv['stock_id'] == 0]
stock0_date0_480 = stock0[stock0['date_id'].isin([0, 480])]
stock0_date0_480[['date_id', 'seconds_in_bucket', 'time_id']]

# Correlation between reference_price, bid_price, ask_price and wap

cols=['seconds_in_bucket', 'reference_price', 'bid_price','ask_price', 'wap']
stock_id = 5
date_id = 5

# Line Plot showing the high correlation between these values
stock_day_cols = cleaned_csv[(cleaned_csv['stock_id'] == stock_id) & (cleaned_csv['date_id'] == date_id)][cols]
stock_day_cols.set_index('seconds_in_bucket').plot(title=f"Stock {stock_id}, Day {date_id}", figsize=(12, 5), grid=True, style='.-')
plt.show()

"""#### Q3: Average records stockID vs Day, 25 pts
distance function between entries
- a. autocorrelation, 10 pts
- b. measure the distance, 5 pts
- c. clustering algorithm, 10 pts

## Observations and Action Performed:
- I'm Defining a consensus record for each stock id s on a particular day d by taking the average of the reference price values.
- I considered taking the the most recent value of the reference price for each day d as a hypothesis could be that the stock prices should have correlation with its immediate values instead of values 2-5 min ago.
- Since the above hypothesis is quite extremely, a good middle ground would be to use a weighted average since the recent values would contribute more to the current stock price than the older values.
"""

consensus_csv = cleaned_csv.groupby(['stock_id', 'date_id'])['reference_price'].mean()
consensus_csv[481: 483]

for k in range(11):
  for i in range(200):
    s = consensus_csv[481 * i: 481 * (i + 1)].autocorr(lag=k)
    # print(s)
    plt.scatter(i, s, c='C0')
    plt.title(f"Lag = {k}")
  plt.show()

"""## Observations and Actions Taken:
- Distance function between prices used is Euclidiean distance.
- Other possible distance functions are mean absolute error.
- One point to note is that I have scaled the distances by 1000 since the prices are in the 1/1000.
- There is almost no difference for Euclidean and Mean Absolute Error.

- Computed the pairwise distances
"""

# from scipy.spatial.distance import pdist
from sklearn.metrics import pairwise_distances

def custom_calc(x,y):
    return 1000 * (y-x) ** 2

a = consensus_csv[consensus_csv.index.get_level_values('date_id') == 0]
matrix = pairwise_distances(a.values.reshape(-1,1), metric=custom_calc)

# matrix
# plt.imshow(matrix)
# plt.show()
sns.heatmap(matrix)
plt.title('Pairwise distance of stocks on day i ')
plt.show()

# a = consensus_csv[consensus_csv.index.get_level_values('date_id') == 1]
# matrix = pairwise_distances(a.values.reshape(-1,1), metric=custom_calc)
# sns.heatmap(matrix)
# plt.show()
# pdist(consensus_csv[consensus_csv.index.get_level_values('date_id') == 0], 'euclidean')

# Computing the Mean of Reference Price and WAP for each stock_id
consensus_csv2 = cleaned_csv.groupby(['stock_id'])[['reference_price', 'wap']].mean()
consensus_csv2

X = cleaned_csv.groupby(['stock_id'])[['reference_price', 'wap']].mean()
# X.values

"""## Observations and Actions Taken:
- Average is used to define the consensus for each stock.
- Initial cluster means are sampled randomly and is tested for 2 to 5 stocks.
- TSNE plot is given below whereby each cluster is colored differently.
- The clusters are visually coherent to some extent but won't be able to have high confidence.

"""

from sklearn.cluster import KMeans

X = cleaned_csv.groupby(['stock_id'])[['reference_price', 'target']].mean().values

num_clusters = range(2, 5)

for c in num_clusters:
  kmeans = KMeans(n_clusters=c, n_init=10, init ='k-means++', max_iter=300, random_state=0)

  y_kmeans = kmeans.fit_predict(X)

  # X_embedded = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=3).fit_transform(X)

  plt.scatter(X[y_kmeans==0, 0], X[y_kmeans==0, 1], s=10, c='red', label ='Cluster 1')
  plt.scatter(X[y_kmeans==1, 0], X[y_kmeans==1, 1], s=10, c='blue', label ='Cluster 2')
  plt.scatter(X[y_kmeans==2, 0], X[y_kmeans==2, 1], s=10, c='green', label ='Cluster 3')
  plt.scatter(X[y_kmeans==3, 0], X[y_kmeans==3, 1], s=10, c='cyan', label ='Cluster 4')
  plt.scatter(X[y_kmeans==4, 0], X[y_kmeans==4, 1], s=10, c='magenta', label ='Cluster 5')

  plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=30, c='yellow', label = 'Centroids')
  plt.title('Clusters of Customers')
  plt.xlabel('Reference Price')
  plt.ylabel('Target')
  plt.show()

"""#### Q4: Closing trajectory of stocks on each day highly correlated, 25 pts


- a. Make three plots, 10 pts
- b. permutation test for statistical confidence, p-value, 15 pts

## Observations and Actions Taken:-
---
- 3 plots are listed below that
- 1st Plot shows that in the initial seconds in bucket, the imbalance size has higher values and then lower towards the end of the day. This is an important indication showing that markets tend to have more fluctuations in the morning and tend to get stable towards the day's close.
- 2nd Plot shows the distribution of the reference_price which has an average of around 1. There is no correlation between positive and negative changes.
"""

def scatter_plot(df, x_colname, y_colname, figscale=1, alpha=.8):
  from matplotlib import pyplot as plt
  plt.figure(figsize=(6 * figscale, 6 * figscale))
  df.plot(kind='scatter', x=x_colname, y=y_colname, s=(32 * figscale), alpha=alpha)
  plt.gca().spines[['top', 'right',]].set_visible(False)
  plt.tight_layout()
  return autoviz.MplChart.from_current_mpl_state()

chart = scatter_plot(cleaned_csv, *['seconds_in_bucket', 'imbalance_size'], **{})
chart

# Function to calculate number of bins in a histrogram
def calc_num_bins(x):
  q25, q75 = np.percentile(x, [25, 75])
  bin_width = 2 * (q75 - q25) * len(x) ** (-1/3)
  bins = round((x.max() - x.min()) / bin_width)
  print("Freedman–Diaconis number of bins:", bins)
  return bins

import numpy as np
from google.colab import autoviz

def histogram(df, colname, num_bins=50, figscale=1):
  from matplotlib import pyplot as plt
  df[colname].plot(kind='hist', bins=num_bins, title=colname, figsize=(8*figscale, 4*figscale))
  plt.gca().spines[['top', 'right',]].set_visible(False)
  plt.tight_layout()
  return autoviz.MplChart.from_current_mpl_state()

chart1 = histogram(cleaned_csv, *['reference_price'], **{})
chart1

"""## Observations and Actions Taken:-
-
"""

from scipy.stats import permutation_test
import random
import copy

def statistic(x, y, axis):
  return np.mean(x, axis=axis) - np.mean(y, axis=axis)

for s in range(0, 5):
  con_csv_stock_0 = consensus_csv[consensus_csv.index.get_level_values('stock_id') == s].to_numpy()
  plt.figure(figsize=(15,4))
  plt.plot(range(481), con_csv_stock_0)
  con_csv_random_stock_0 = copy.copy(con_csv_stock_0)
  random.shuffle(con_csv_random_stock_0)
  plt.plot(range(481), con_csv_random_stock_0)

  res = permutation_test((con_csv_stock_0, con_csv_random_stock_0), statistic)

  plt.xlabel('Date ID')
  plt.ylabel('Average Reference Price')
  plt.title(f'P-Value = {res.pvalue} for Stock {s}')
  plt.show()

  # print(res.pvalue)

"""#### Q5: Best prediction model, any approaches, 25 pts

- I know linear regression is not a great model for predicting values but still I wanted to test it out for this dataset.
- Then I tried out LightGBMR and the XGBMR models that performed better than linear regression as stated above.
- I believe LightGBMR would be better since there are sudden changes of direction in the dataset that would not be modeled correctly using linear regression.
- One reason for choosing XGMR over LightGBMR would be parallelization that can concurrently process data.
"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold


# Linear Regression
min_max_scaler = preprocessing.MinMaxScaler()
cleaned_null_csv = cleaned_csv.dropna()
X = min_max_scaler.fit_transform(cleaned_null_csv[cols])

models = []

X_train, X_test, y_train, y_test = train_test_split(X, cleaned_null_csv['target'], test_size=0.2)

# cleaned_csv

LR_model = LinearRegression()
LR_model.fit(X_train, y_train)

y_pred_content = LR_model.predict(X_test)

models.append(LR_model)

folds = KFold(n_splits = 5, shuffle = True, random_state = 100)
scores = cross_val_score(LR_model, X_train, y_train, scoring='neg_mean_absolute_error', cv=folds)
scores
# metrics.get_scorer_names()

from lightgbm import log_evaluation, early_stopping, LGBMRegressor as LGBMR;
from xgboost import XGBRegressor as XGBR;
from sklearn.metrics import mean_absolute_error

LGB_model = LGBMR()

LGB_model.fit(X_train, y_train, eval_set=(X_test, y_test))

models.append(LGB_model)
# score = mean_absolute_error(y_test, LGB_model.predict(X_test));
# score

folds = KFold(n_splits = 5, shuffle = True, random_state = 100)
scores = cross_val_score(LGB_model, X_train, y_train, scoring='neg_mean_absolute_error', cv=folds)
scores

XGB_model = XGBR()

XGB_model.fit(X_train, y_train)

models.append(XGB_model)

folds = KFold(n_splits = 5, shuffle = True, random_state = 100)

scores = cross_val_score(XGB_model, X_train, y_train, scoring='neg_mean_absolute_error', cv=folds)
scores

models

"""#### Q6: submit model on Kaggle, 0 pts
Public Score: 18.7628 \\
Private Score: \\
Kaggle profile link: https://www.kaggle.com/rutwik99  
Screenshot(s): ![image.png](data:image/png;base64,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)

"""



