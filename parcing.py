import requests
from bs4 import BeautifulSoup


def parsing():
    url = "https://funpay.com/lots/82/"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    accounts = soup.find_all('a', class_='tc-item')
    return accounts
