import requests
from bs4 import BeautifulSoup as BS

def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(text):
    soup = BS(text, 'lxml')
    return soup.find('div', id='touchnav-wrapper').find('header').find('div').find("p").text


def main():
    url = "https://www.python.org/"
    print(get_data(get_html(url)))


if __name__ == "__main__":
    main()
