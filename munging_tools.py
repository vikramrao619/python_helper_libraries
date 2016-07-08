import pandas as pd
from pandas import Series, DataFrame
import numpy as np

def winsorizer(frame, columns, percentile):
    
    '''This function takes in a dataframe, a list of columns, and a percentile.
       It winsorizes each of the columns in the frame based on the proportion.
       It then returns the frame. This function deals with na values appropriately.'''
  
    if type(columns) == list:

        for variable in columns:

            pXX = frame[variable].dropna().quantile(percentile)
            mask = frame[variable] > pXX
            frame.loc[mask, variable] = pXX

        return frame
    
    elif type(columns) == str:
        
        pXX = frame[columns].dropna().quantile(percentile)
        mask = frame[columns] > pXX
        frame.loc[mask, columns] = pXX
        
    return frame
    
def breakdown(frame, column):
    
    '''This function takes in a dataframe and column. It does a more comprehensive
       description.'''
    
    index_list = [
        'count',
        'null_count',
        'total_count',
        'min',
        '10%',
        '25%',
        '50%',
        '75%',
        '90%',
        '95%',
        '99%',
        'max',
        'mean',
        'stddev',
        'variance'        
    ]
    
    
    cleaned = frame[column].dropna()
    description_series = cleaned.describe()
    description_series['null_count'] = sum(frame[column].isnull())
    description_series['total_count'] = len(data[column])
    description_series['10%'] = cleaned.quantile(.1)
    description_series['90%'] = cleaned.quantile(.9)
    description_series['95%'] = cleaned.quantile(.95)
    description_series['99%'] = cleaned.quantile(.99)
    description_series['stddev'] = cleaned.std()
    description_series['variance'] = cleaned.var()
    description_series.rename({'count': 'non_null_count'})
    final = description_series.reindex(index_list).round(2)
    return final
    
def column_filterer(frame, col_whitelist_dict):
    
    '''This function takes a dataframe and a column whitelist dict.
       The keys of this dict are column names (strings) and the values
       are lists of whitelisted values. The function returns a frame that
       contains only rows for which '''
    
    master_mask = Series([True] * len(frame.index))
    
    for column in col_whitelist_dict:
        
        this_mask = frame[column].isin(col_whitelist_dict[column])
        master_mask = master_mask & this_mask
    
    final_frame = frame[master_mask]
    return final_frame.reset_index(drop = True)

