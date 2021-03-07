import pandas as pd
import numpy as np
import scipy
import scipy.stats
from scipy.spatial.distance import euclidean
from multiprocessing import Pool
threads = 22

df = pd.read_csv('../../data/financial_data/data2000_2020_edited.csv')

WEIGHTS = [1/3, 1/3, 1/3]
# calculate rank of each firm for each year

def calculate_distmat(year):
    df_year = df[df['fyear'] == year]
    # select dropping criteria
    df_year = df_year[df_year['ebit_margin'].notna()]
    df_year = df_year[df_year['div_ebit'].notna()]
    df_year = df_year[~df_year['ebit_margin'].isin([np.inf, -np.inf])]
    df_year = df_year[df_year['leverage'].notna()]
    df_year = df_year[~df_year['div_ebit'].isin([np.inf, -np.inf])]

    df_year['ebit_margin_rank'] = df_year['ebit_margin'].rank()
    df_year['leverage_rank'] = df_year['leverage'].rank()

    # calculate std and mean of kpi's
    std_ebit = np.std(df_year['ebit_margin'])
    std_leverage = np.std(df_year['leverage'])
    mean_ebit = np.mean(df_year['ebit_margin'])
    mean_leverage = np.mean(df_year['leverage'])
    mean_div = np.mean(df_year['div_ebit'])
    std_div = np.std(df_year['div_ebit'])

    # normalize the kpi's
    df_year['norm_ebit_margin'] = scipy.stats.norm.cdf(
        df_year['ebit_margin'], loc=mean_ebit, scale=std_ebit)
    df_year['norm_leverage'] = scipy.stats.norm.cdf(
        df_year['leverage'], loc=mean_leverage, scale=std_leverage)
    df_year['norm_div_ebit'] = scipy.stats.norm.cdf(
        df_year['leverage'], loc=mean_div, scale=std_div)

    rows_and_cols = df_year.tic.unique()

    # set the ticker as index to search more efficient
    df_year = df_year.set_index('tic')

    distance_matrix = pd.DataFrame(index=rows_and_cols, columns=rows_and_cols)
    for column in rows_and_cols:
        company_1_ebit = df_year.loc[column, :]['norm_ebit_margin']
        company_1_leverage = df_year.loc[column, :]['norm_leverage']
        company_1_div_ebit = df_year.loc[column, :]['norm_div_ebit']
        for row in rows_and_cols:
            company_2_ebit = df_year.loc[row, :]['norm_ebit_margin']
            company_2_leverage = df_year.loc[row, :]['norm_leverage']
            company_2_div_ebit = df_year.loc[row, :]['norm_div_ebit']
            #distance_matrix.loc[row, column] = np.round(np.absolute(company_1_leverage-company_2_leverage), decimals=4)
            distance_matrix.loc[row, column] = np.round(np.absolute(euclidean(
                [company_1_ebit, company_1_leverage, company_1_div_ebit], [company_2_ebit, company_2_leverage, company_2_div_ebit], w=WEIGHTS)), decimals=4)  # company_1_leverage - company_2_leverage)
    return distance_matrix


years = [y for y in range(2000, 2021)]
with Pool(threads) as pool:
    distance_matrices = pool.map(calculate_distmat, years)

for year, distance_matrix in zip(years, distance_matrices):
    distance_matrix.to_csv(
        'distance_matrices_combined3/cluster_{}.csv'.format(year))
