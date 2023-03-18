from requests_html import HTMLSession
import time

def get_html(url):
    session = HTMLSession()
    r = session.get(url='https://www.beerwulf.com/en-gb/c/beer-kegs/sub-kegs')
    print(r)
    r.html.render(sleep=1, timeout=10)
    return r


def get_data(response):
    print('collecting')
    products = response.html.find('a[data-saletype="Regular"]')
        
    for product in products:
        print()
        name = product.find('h4.product-name', first = True).text
        link = 'https://www.beerwulf.com/' + product.attrs['href']
        price = product.find('span.price', first=True).text
        print(name, price, link, sep='|')


def main():
    url='https://www.beerwulf.com/en-gb/c/beer-kegs/sub-kegs'
    start=time.perf_counter()
    get_data(get_html(url))
    fin = time.perf_counter() - start
    print(fin)

if __name__ == "__main__":
    main()
   
