import csv

def record_html(acc):
    file_list = [['mmr_range', 'price', 'link']]
    accounts = acc
    for account in accounts:
        boost_price = account.find('div', attrs={'tc-price'})
        mm_range = account['data-f-range']
        if mm_range == "1-2000 (цена за 100 mmr)" and float(boost_price['data-s']) > 300:
            continue
        elif mm_range == "6500+ (цена за 100 mmr)":
            continue
        else:
            file_list.append([mm_range,
                        boost_price['data-s'],
                        account['href']
                        ])
    return file_list

def record_in_file(list):
    myFile = open('funpaydotaboost.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(list)


