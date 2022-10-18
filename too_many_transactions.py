import json
import datetime, time


import pandas as pd


def too_many_transactions(df):
    # Собираем все паспорта
    passports = df['passport'].to_list()

    # Собираем все транзакции для каждого пасспорта
    trans_np = {}
    for passport in passports:
        tran = df.loc[df['passport'] == passport]
        if not(trans_np.get(passport)):
            trans_np[passport] = [tran]
        else:
            trans_np[passport].append(tran)

    # Находим кол-во транзакций и их время
    ans = [0 for i in range(22)]
    date_passport = {}
    date_passport_ids = {}
    for passort in trans_np.keys():

        a = trans_np[passort][0]
        a = pd.DataFrame(a)
        date_passport[passort] = a['date'].tolist()
        date_passport_ids[passort] = a['transaction_id'].tolist()
        count_trans = len(date_passport[passort])

        # ans[count_trans] += 1

    # Из полученных данных выше можно сделать вывод о том, что обычные люди совершают от 1 до 3 транзакций,
    # 4 и 5 транзакций никто не соверашл,
    # а вот мошенники совершают от 6 до 20
    # но нужно вычислить время, за которое были совершены эти транзакции
    import datetime, time
    def f(s): # переводим дату в секунды
        t = datetime.datetime(int(s[0:4]), int(s[5:7]), int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:]))
        return time.mktime(t.timetuple())

    count_minutes = 8 # задаём кол-во минут, за которые были произведены транзакции оп новому паттерну
    total_fraud_trans = 0
    fraud_trans_ids = []

    for i in date_passport.keys():
        date_fio_tran = date_passport[i]
        if len(date_fio_tran) >= 6:
            if ((f(date_passport[i][-1]) - f(date_passport[i][0]))) <= count_minutes * 60:
                total_fraud_trans += len(date_fio_tran)
                fraud_trans_ids += date_passport_ids[i]

            else: # Ищем максимальное кол-во транзакций, которые были произведены за count_minutes,
                # Если все транзакции этого фио не "поместились" в указанное кол-во минут

                max_trans = 0
                indexes = []
                seconds = list(map(f,date_passport[i]))

                for ind1 in range(len(date_passport[i])):
                    for ind2 in range(ind1, len(date_passport[i])):
                        if ind1 != ind2 and ((f(date_passport[i][ind2]) - f(date_passport[i][ind1]))) <= count_minutes * 60:
                            if ind2 - ind1 + 1 > max_trans:
                                max_trans =  ind2 - ind1 + 1
                                indexes = [ind1,ind2]
                if len(indexes) > 0 and max_trans > 0:

                    total_fraud_trans += len(date_fio_tran[indexes[0]:indexes[1]+1])
                    fraud_trans_ids += date_passport_ids[i][indexes[0]:indexes[1]+1]

    df_too_many_transactions = df.loc[df['transaction_id'].isin(fraud_trans_ids)]

    return df_too_many_transactions
