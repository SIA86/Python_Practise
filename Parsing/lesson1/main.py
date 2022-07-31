"""
Using Request, BeautifulSoup and Lxml modules parse the https://www.python.org/ and 
catch the string: "Python is a programming language that lets you work quickly
and integrate systems more effectively."
"""

import requests
from bs4 import BeautifulSoup as BS

def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(text):
    soup = BS(text, 'lxml')
    p = soup.find('div', class_="introduction").find('p').text
    return p
    


def main():
    url = "https://www.python.org/"
    print(get_data(get_html(url)))


if __name__ == "__main__":
    main()
