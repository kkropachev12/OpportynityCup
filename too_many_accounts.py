import pandas as pd

def too_many_accounts(df):

    df_grouped = df.groupby(['passport']).count()

    df_many_accounts = df_grouped.loc[df_grouped['account'] >= 8]

    list_passports = df_many_accounts.index.to_list()
    df_too_many_accounts = df.loc[df['passport'].isin(list_passports)]

    return df_too_many_accounts
