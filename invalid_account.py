import pandas as pd


def invalid_account(df):
    df_invalid_account = df[df['date'] > df['account_valid_to']]

    return df_invalid_account
