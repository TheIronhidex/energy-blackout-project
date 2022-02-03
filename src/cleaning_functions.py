from dotenv import load_dotenv
import pandas as pd


def load_csv(csv):
    '''Just like that, imports a .csv. It looks better like this'''
    return pd.read_csv(csv)

def df_no_nulls_and_unique(df):
    '''In a dataframe, removes the rows with all its values NaN, removes the duplicated rows, and sort
    the values according to the index'''
    df.dropna(how="all", inplace=True)
    df.drop_duplicates()
    df.sort_index(axis=1, ascending=True, inplace=True, na_position='last')
    return df

def filter_dataframe(df,category):
    '''Allows the creation of a new df based on a previous filtered one'''
    new_df = df['category'].copy()
    return new_df