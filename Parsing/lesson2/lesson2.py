"""
Implement a code which will parse multy-data from the https://www.finam.ru/quotes/stocks/europe/ and create 
a CSV file to store the information about stocks (name, last price, volumes)
"""

import requests
import csv
from bs4 import BeautifulSoup 


def get_html(url):
    r = requests.get(url)
    return r.text


def normalize(str):
    return str.split()[0]


def normalize2(str):
    return str.replace('\xa0', '')


def make_CSV(data):
    with open("stocks.csv", 'a', newline='') as f:
        writer = csv.writer(f)

        writer.writerow((data["name"],
                         data["last_price"],
                         data["volume"]))


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    stocks = soup.find("tbody", class_="QuoteTable__tableBody--dHw").find_all("tr")

    for stock in stocks:
        name = stock.find('td', class_="QuoteTable__tableCell--151 QuoteTable__left--3jl").find('a').text
        last_price = stock.find_all('td')[2].find('span').text
        last_price = normalize(last_price)
        volume = stock.find_all('td')[8].find('span').text
        volume = normalize2(volume)
            
        data = {"name": name,
                "last_price": last_price,
                "volume": volume}

        make_CSV(data)
        

def main():
    url = "https://www.finam.ru/quotes/stocks/europe/"
    get_data(get_html(url))


if __name__ == '__main__':
    main()