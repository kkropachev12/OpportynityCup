import json


def json_to_dict(file_name: str)->dict:
    '''открываем файл с транзакциями и преобразовываем его в словарь'''

    with open(f'{file_name}.json') as f:
        transactions = json.load(f)

    list_trans_id = []

    dict_transactions = {}

    for key, transaction in transactions['transactions'].items():
        list_trans_id.append(key)
        for k, v in transaction.items():
            if not dict_transactions.get(k):
                dict_transactions[k] = []
                dict_transactions[k].append(v)
            else:
                dict_transactions[k].append(v)

    dict_transactions['transaction_id'] = list_trans_id

    return dict_transactions
