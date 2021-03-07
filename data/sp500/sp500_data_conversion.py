#! /bin/env python3

import pandas as pd
import numpy as np

input_filename = 'compustat_sp500_since2000_2.csv'
ticker_filename = '../sp500_constituents_wikipedia.csv'

prices_output_filename = 'sp500_since2000_prices.csv'
dividends_output_filename = 'sp500_since2000_dividends.csv'
log_returns_output_filename = 'sp500_since2000_logreturns.csv'
company_data_output_filename = 'sp500_since2000_companies.csv'


"""
Read in data and prepare
"""
input_file = pd.read_csv(input_filename)

# Get the relevant tickers and only select data for those tickers
ticker_input = pd.read_csv(ticker_filename, header = None)
ticker_input[0] = ticker_input[0].apply(lambda s: s.strip()) # remove whitespces
input_file = input_file.loc[input_file['tic'].isin(ticker_input[0])]

# Convert date types
input_file['datadate'] = pd.to_datetime(input_file['datadate'], format = '%Y%m%d')
#input_file['paydateind'] = pd.to_datetime(input_file['paydateind'], format = '%Y%m%d')
input_file['divdpaydate'] = pd.to_datetime(input_file['divdpaydate'], format = '%Y%m%d')
input_file['divsppaydate'] = pd.to_datetime(input_file['divsppaydate'], format = '%Y%m%d')
input_file['paydate'] = pd.to_datetime(input_file['paydate'], format = '%Y%m%d')
input_file['recorddate'] = pd.to_datetime(input_file['recorddate'], format = '%Y%m%d')

# Get dates
dates = input_file['datadate'].unique()
dates.sort()

"""
Get unique companies
"""
companies = input_file[['tic', 'gvkey', 'cusip', 'conm', 'ggroup', 'gind', 'gsector', 'gsubind', 'naics', 'sic', 'spcindcd', 'spcseccd', 'busdesc']].drop_duplicates('tic', keep='last')
companies.index = companies['tic']
companies.sort_index(inplace=True)
companies = companies.drop('tic', axis='columns')
companies.to_csv(company_data_output_filename)


"""
Construct price dataframe
"""
price_df = pd.DataFrame(index = dates, columns = companies.index)
for tic in companies.index:
    this_tic_prices = input_file.loc[input_file['tic'] == tic]
    this_tic_prices.index = this_tic_prices['datadate']
    price_df[tic] = this_tic_prices['prccd'] / this_tic_prices['ajexdi'] # divided by stock split adjustment factor
price_df.to_csv(prices_output_filename)

"""
Construct dividend dataframe
"""
dividend_df = pd.DataFrame(index = dates, columns = companies.index)
for tic in companies.index:
    this_tic_dividends = input_file.loc[input_file['tic'] == tic]
    this_tic_dividends = this_tic_dividends[this_tic_dividends['recorddate'].notna()]
    this_tic_dividends.index = this_tic_dividends['datadate']
    dividend_df[tic] = this_tic_dividends['div']
dividend_df.index.name = 'exdate'
dividend_df.to_csv(dividends_output_filename)


"""
Calculate dividend adjusted daily log returns
"""
price_plus_div_df = price_df + dividend_df.fillna(0) # Stock prices with the dividend added on the ex date

log_return_df = pd.DataFrame(index = dates, columns = companies.index)
for tic in price_df.columns:
    log_return_df[tic] = np.log(price_plus_div_df[tic] / price_df[tic].shift(1))
log_return_df.to_csv(log_returns_output_filename)