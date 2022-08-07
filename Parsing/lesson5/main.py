
#The implementation of code which parse the AJAX web resourses usign multyprocess module
#url: https://www.liveinternet.ru/rating/ru/literature/#geo=ru;group=literature;page=1;


import csv
from multiprocessing import Pool
import requests

def get_html(url):
    r = requests.get(url)
    return r.text


def writer(data):
    with open('live.csv', 'a', encoding= 'utf-8', newline='') as f:
        order = ['name', 'url', 'description', 'rating']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def make_all(url):
    get_data(get_html(url))


def get_data(html):
    response = html.strip().split('\n')[1:]

    for row in response:
        column = row.strip().split('\t')
        name = column[0]
        url = column[1]
        description = column[2]
        rating = column[3]

        data = {'name': name,
                'url': url,
                'description': description,
                'rating': rating}

        writer(data)

    
def main():
    url = 'https://www.liveinternet.ru/rating/ru/literature/today.tsv?page={}'
    urls = [url.format(str(i)) for i in range(1, 64)]
    #for i in range(1, 64):
    #    urls = url.format(str(i)) 
    
    with Pool(5) as p:
       p.map(make_all, urls)

    #    get_data(get_html(urls))


if __name__ == "__main__":
    main()