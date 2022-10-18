import pandas as pd

def invalid_passport(df):
    df_invalid_passport = df[df['date'] > df['passport_valid_to']]

    return df_invalid_passport
