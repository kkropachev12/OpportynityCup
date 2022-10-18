import pandas as pd


def validate(df):

    # приведем дату в удобный вид
    df['account_valid_to'] = pd.to_datetime(df['account_valid_to']).astype(str)
    df['passport_valid_to'] = pd.to_datetime(df['passport_valid_to']).astype(str)
    df['date_of_birth'] = pd.to_datetime(df['date_of_birth']).astype(str)
    df.index = range(len(df.index))

    return df
