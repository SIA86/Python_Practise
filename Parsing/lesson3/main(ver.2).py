"""
Implement a code which parse multy-data from the https://www.finam.ru/infinity/quotes/stocks/usa/ which have several different pages and create 
a CSV file to store the information about name, last_price, price_change and volume. Assume that we don't know how many pages is it and parse them using "next" button.
"""

import re
import requests
import csv
from bs4 import BeautifulSoup 

def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    else:
        print(r.status_code)



def writer(data):
    with open("currency.csv", 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Name', 'Last Price', 'Price Change', 'Volume'])
        writer.writerow({"Name": data["Name"],
                         "Last Price": data["Last_price"],
                         "Price Change": data['Price_change'],
                         "Volume": data['Volume']})


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id="finfin-local-plugin-quote-table-table-table").find('tbody').find_all('tr')
    
    for tr in trs:
        try:
            name = tr.find('td').find('a').text.strip().splitlines()[0]
        except:
            name = ''
        try:
            last_price = tr.find_all('td')[1].find_all('span')[1].text.strip()
        except:
            last_price = ''
        try:
            change = tr.find_all('td')[2].text.strip()
        except:
            change = ''
        try:
            volume = tr.find_all('td')[7].text.strip()
        except:
            volume = ''
        
        data = {"Name": name,
                "Last_price": last_price,
                "Price_change": change,
                "Volume": volume}
        
        writer(data)

def main():
    url = "https://www.finam.ru/infinity/quotes/stocks/usa/"
    
    
    while True:
        get_data(get_html(url))
        soup = BeautifulSoup(get_html(url), 'lxml')
        
        try:
            pattern = 'Далее'
            url = "https://www.finam.ru/infinity/quotes/stocks/usa/" + soup.find('a', text=re.compile(pattern)).get('href')
        except:
            break



if __name__ == "__main__":
    main()