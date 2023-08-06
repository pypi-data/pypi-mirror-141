# some data processing function #

import pandas as pd
from datetime import datetime

def create_date_df(startDate = '20200101', endDate = '20210101'):
  date_list = [datetime.strftime(x, '%Y-%m-%d') for x in list(pd.date_range(start = startDate, end= endDate))]
  date_pd = pd.DataFrame(date_list)
  date_pd.rename(columns={0:'DATE'}, inplace= True)
  return date_pd

def sg_holiday_feature(holiday_df, startDate = '20200101', endDate = '20210101'):
  date_pd = create_date_df(startDate = startDate, endDate = endDate)
  holiday_df.rename(columns = {'Date':'DATE'}, inplace = True)
  df = date_pd.merge(holiday_df, on='DATE', how = 'left')
  df['Holiday'] = df['Holiday'].fillna('Non-Holiday')
  df = df[['DATE', 'Holiday']]
  df_dummy = pd.get_dummies(df, columns = ['Holiday'])
  return df_dummy

def get_dummy_value(df, dummy_columns):
  df_dummy = pd.get_dummies(df, columns = dummy_columns)
  return df_dummy

