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
    with open("NineForNews.csv", 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Article', 'Comments', 'Views'])
        writer.writerow({"Article": data["Article"],
                         "Comments": data["Comments"],
                         "Views": data['Views']})



def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    lis = soup.find('div', id='tie-block_2154').find('ul').find_all('li')

    for li in lis:
        try:
            Article = li.find('h2').find('a').text.strip()
        except:
            Article = ''
        try:
            Comments = li.find('div', class_='tie-alignright').find_all('span')[0].text.strip()
        except:
            Comments = ''
        try:
            Views = li.find('div', class_='tie-alignright').find_all('span')[1].text.strip()
        except:
            Views = ''
        

        data = {"Article": Article,
                "Comments": Comments,
                "Views": Views}
        
        writer(data)

def main():
    pattern = "https://www.ninefornews.nl/page/{}/"
  
    for i in range(2, 203):
        url = pattern.format(str(i))
        get_data(get_html(url))
    


if __name__ == "__main__":
    main()