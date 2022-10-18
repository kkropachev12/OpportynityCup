import json
import re

import pandas as pd


from df_to_sql import df_to_sql
from df_from_sql import df_from_sql
from json_to_dict import json_to_dict
from send_error import send_error
from too_many_accounts import too_many_accounts
from invalid_passport import invalid_passport
from invalid_account import invalid_account
from too_many_transactions import too_many_transactions
from list_to_txt import list_to_txt
from validate_df import validate
from df_to_gsheet import df_to_gsheet

def main():
    # Создаем из полученного словаря ДатаФрейм
    df = pd.DataFrame(json_to_dict('transactions_final'))

    # Отправляем полученный df в sql
    df_to_sql(df, 'all_transactions')

    # Выгружаем df из sql
    df = df_from_sql('all_transactions')

    # Валидация данных
    df = validate(df)

    list_of_re = [r'\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2}', r'\d{20}', r'\d{10}', r'\d{4}-\d{2}-\d{2}', r'\d{1}-\d{5}', r'\D+', r'\D+', r'\D+', r'\d{4}-\d{2}-\d{2}', r'\d{10}', r'\d{4}-\d{2}-\d{2}', r'\+\d{11}', r'\D+', r'\d+\.\d+', r'\D+', r'\D{3}\d{5}', r'\D{3}', r'\D+', r'\D.+', r'\d+']
    # Проверка на соответствие регулярному выражению значения в данных и удаление таковых
    i = 0
    errors = ''
    list_errors = []
    import time
    for title in df.columns:

        for data in df[title]:
            if re.match(list_of_re[i], str(data)) == None:

                df_error = df.loc[df[title] == data]
                for error in df_error['transaction_id']:

                    if error in errors:
                        continue
                    else:
                        errors += error + ', '
                        list_errors.append(error)
        i += 1

    # Отправка номеров транзакций, в которых найдена ошибка
    send_error(errors[:-2])


    # Удаление строчек с ошибками
    df = df.loc[~df['transaction_id'].isin(list_errors)]

    # 4 паттерна:
    # Слишком много аккаунтов, оформленных на одного человека (>= 8)
    df_too_many_accounts = too_many_accounts(df)

    # Транзакции совершены с аккаунта с просроченым паспортом
    df_invalid_passport = invalid_passport(df)

    # Транзакции совершены с недейтсвительного аккаунта
    df_invalid_account = invalid_account(df)

    # Много транзакций за короткий промежуток времени
    df_too_many_transactions = too_many_transactions(df)

    # Запишем список транзакций в txt файл для каждого паттерна
    list_to_txt(df_too_many_accounts['transaction_id'].to_list(), 'too_many_accounts')

    list_to_txt(df_invalid_passport['transaction_id'].to_list(), 'invalid_passport')

    list_to_txt(df_invalid_account['transaction_id'].to_list(), 'invalid_account')

    list_to_txt(df_too_many_transactions['transaction_id'].to_list(), 'too_many_transactions')

    # Переведем дату в удобный вид перед загрузкой в google sheet и sql
    df_too_many_accounts['date'] = pd.to_datetime(df_too_many_accounts['date']).astype(str)
    df_too_many_accounts.index = range(len(df_too_many_accounts.index))

    df_invalid_passport['date'] = pd.to_datetime(df_invalid_passport['date']).astype(str)
    df_invalid_passport.index = range(len(df_invalid_passport.index))

    df_invalid_account['date'] = pd.to_datetime(df_invalid_account['date']).astype(str)
    df_invalid_account.index = range(len(df_invalid_account.index))

    df_too_many_transactions['date'] = pd.to_datetime(df_too_many_transactions['date']).astype(str)
    df_too_many_transactions.index = range(len(df_too_many_transactions.index))

    # Отправляем полученные данные в sql
    df_to_sql(df_too_many_accounts, 'too_many_accounts')

    df_to_sql(df_invalid_passport, 'invalid_passport')

    df_to_sql(df_invalid_account, 'invalid_account')

    df_to_sql(df_too_many_transactions, 'too_many_transactions')


    df_to_gsheet(df_too_many_accounts, '1f8_yoLRu7snGtIyXX6p64RZZLoDv55rFYwoNfDi0H9c')

    df_to_gsheet(df_invalid_passport, '1ju50NM-ZhmKT2OLAs1O6sVEkibO5BRtyQuPAn7_hzFM')

    df_to_gsheet(df_invalid_account, '1NLvfMXXK_fF8XPMPA9j8D8HsilyCSy07eKRpFs0besA')

    df_to_gsheet(df_too_many_transactions, '1nucg6x2fKZsaQBDDGiQhhUul0bD1pWrqRAANzcwxAUo')


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        send_error(ex)
