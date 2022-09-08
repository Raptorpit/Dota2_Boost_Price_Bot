import csv

import pandas as pd



def grp_data():
    data = pd.read_csv('funpaydotaboost.csv')
    data_grp = data.groupby(['mmr_range']).mean()
    data_grp.to_csv('table_avg_price.csv')
    data_table = pd.read_csv('table_avg_price.csv')
    data_table.rename(columns= {'mmr_range':'Диапазон MMR               ','price':'Средняя цена'},inplace= True)
    for i in range(0,data_table.shape[0]):
       data_table.at[i,'Средняя цена'] =f"{data_table.at[i,'Средняя цена']:.2f} ₽"
    d=data_table.to_string(index=False)
    return d






def average_price():
    data = pd.read_csv('funpaydotaboost.csv')
    data_grp = data.groupby(['mmr_range']).mean()
    d = {}
    for index in range(0,len(data_grp)):
        avg_price = data_grp.iloc[index]['price']

        if index == 0:
            mmr1_range = list(range(1, 2001))
            pair = {avg_price: mmr1_range}
            d.update(pair)
        if index == 1:
            mmr1_range = list(range(2001, 3001))
            pair = {avg_price: mmr1_range}
            d.update(pair)
        elif index > 1:
            mmr1_range = list(range(3001+(index-2)*500, 3501+(index-2)*500))
            pair = {avg_price: mmr1_range}
            d.update(pair)
    return d

def boost_price(price_dict,starting_mmr,ending_mmr):
    price_dict = price_dict
    starting_mmr = starting_mmr
    ending_mmr = ending_mmr
    sum = 0
    while starting_mmr < ending_mmr:
        for k,v in price_dict.items():
            if starting_mmr in v:
                sum += k
        starting_mmr += 100
    return sum

