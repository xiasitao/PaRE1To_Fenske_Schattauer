import pandas as pd
import numpy as np

df = pd.read_csv('data2000_2020.csv')

##Drop all ticker symbols which are not in sp500_constituents_wikipedia.csv
ticker_list = pd.read_csv('../../sp500_constituents_wikipedia.csv', header=None)

for index, row in df[:5].iterrows():
    if row['tic'] not in ticker_list[0].tolist():
        df.drop(index=index, inplace=True)
##=> All tickers are correct, no drops

#analyze empty cells
relevant_columns = ['at', 'ebit', 'lt', 'sale', 'act', 'dltt', 'dv']
for column in relevant_columns:
    print(column, 'has', df[column].isnull().sum(), 'empty cells of', len(df), 'cells in total')

##calculate financial ratios
df['ebit_margin'] = df['ebit'] / df['sale']
df['leverage'] = df['lt'] / df['at']
df['div_ebit'] = df['dv'] / df['ebit']

#save data
df.to_csv('data2000_2020_edited.csv')