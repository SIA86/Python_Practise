"""
Implement a code which parse multy-data from the https://moscow.petrovich.ru/catalog/9575960/ which have several different pages and create 
a CSV file to store the information about name, art, price
"""

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
    with open("samorez.csv", 'a', encoding='cp1251', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Article', 'Name', 'Price'])
        writer.writerow({"Article": data["art"],
                         "Name": data["name"],
                         "Price": data['price']})


def refine(string):
    return string.replace(' ', '').replace('₽', '')

def get_data(string, iter):
    soup = BeautifulSoup(string, 'lxml')
    divs = soup.find('div', class_="product-list").find('div', class_="pt-row pt-v-gutter-xxs-md").find_all('div', class_='fade-in-list page-item-list pt-col-xxs-12 page-{}-item page-item'.format(iter))
    for div in divs:
        try:
            art = div.get('data-item-code')
        except:
            art = ''
        try:
            name = div.find('div', class_="details").find('a').find('span').text.strip()
        except:
            name = ''
        try:
            price = div.find('div', class_="price-details").find_all('p')[2].text
        except:
            price = ''
        price = refine(price)

        data = {"name": name,
                "price": price,
                "art": art}
        
        writer(data)

def main():
    pattern = "https://moscow.petrovich.ru/catalog/9575960/?p={}"
  
    for i in range(0, 3): #Total amount of found elements divided by the number of shown elements at the page.
        url = pattern.format(str(i))
        get_data(get_html(url), i)
    


if __name__ == "__main__":
    main()