import pandas as pd
import numpy as np
import random
import datetime
import os

def max_price(df):
    return max(df['close'])

def max_close_date(df):
    return pd.to_datetime(max_price_row(df).date.iloc[0])

def max_price_row(df):
    r, c = df[df['close'] == max_price(df)].shape
    try:
        if r == 1:
            return df[df['close'] == max_price(df)]

    except ValueError:
        print("There are two values for this date")

def delta_days(df1, df2, col=None):
    """
    Input:
    df1 = spac_
    """
    return pd.to_datetime(df1[col].iloc[0]) - max_close_date(df2)

def rename_trade_cols():
    col_names = ['company',
              'symbol',
              'ipo_date',
              'press_release',
              'record_date',
              'vote_date',
              'closing_liquidation_date',
              'closing_year',
              'new_company_ticker',
              'china',
              'current_stock_price',
              'return_val',
              'status',
              'fallon_qs']
    return col_names

def make_df(c1, c2, c3, c4, c5, c6, c7):
    return pd.DataFrame(list(zip(c1,
                           c2,
                           c3,
                           c4,
                           c5,
                           c6,
                           c7)),
                  columns =['symbol',
                            'max_prices',
                            'delta_ipo_max_close_date',
                            'delta_press_max_close_date',
                            'delta_record_max_close_date',
                            'delta_vote_max_close_date',
                            'delta_liquid_max_close_date'])

def delta_df(spac_master, company_dict, spac_list):

    symbol = []
    max_prices = []
    delta_ipo_close_date = []
    delta_press_close_date = []
    delta_record_close_date = []
    delta_vote_close_date = []
    delta_liquid_max_close_date = []


    for marker in spac_list:
        if marker == 'jsyn' or marker == 'algr':
            spac_row = spac_master[spac_master['symbol']== marker.upper()]
            trade_details = company_dict[marker+"_hist"]

            symbol.append(marker)
            max_prices.append(max_price(trade_details))

            #All Dates
            delta_ipo_close_date.append(delta_days(spac_row, trade_details, 'ipo_date'))
            delta_press_close_date.append(delta_days(spac_row, trade_details, 'press_release'))
            delta_record_close_date.append(delta_days(spac_row, trade_details, 'record_date'))
            delta_vote_close_date.append(delta_days(spac_row, trade_details, 'record_date'))
            delta_liquid_max_close_date.append(delta_days(spac_row, trade_details, 'closing_liquidation_date'))

#         print (marker, spac_row.shape, trade_details.shape)
    else:
        pass

    return make_df(symbol,
                   max_prices,
                   delta_ipo_close_date,
                   delta_press_close_date,
                   delta_record_close_date,
                   delta_vote_close_date,
                   delta_liquid_max_close_date)

def make_dictionary(path):

    company_files = os.listdir(path)
    company_files.remove('.DS_Store')
    company_dfs = {} #dictionary
    for name in company_files:
        df = pd.read_csv(path+name)
        file_symbol = name[:-4]+"_hist" #creating a usable name
        company_dfs[file_symbol] = df #adding to the dictionary

    return company_dfs

if __name__ == '__main__':

    #Reading in files (note that path needs to change for implementation)
    spac_master = pd.read_csv("/Users/chaserenick/Desktop/SPAC_Project/company_profiles/spac_master_dataset.csv")
    spac_master.columns = rename_trade_cols()

    #Reading in files from folder containing full trading history of each company
    company_dict = make_dictionary('/Users/chaserenick/Desktop/SPAC_Project/trading_history/')

    #Making a list of the data
    spac_list = list(map(str.lower, list(spac_master.symbol.dropna())))

    df = delta_df(spac_master, company_dict, spac_list)

    print (df)
