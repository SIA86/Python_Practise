import requests, time
from bs4 import BeautifulSoup
from multiprocessing import Pool
from random import choice



def get_html(url):
    if S_proxy.get() == 0:
        p = get_proxy()
        proxy = {p['schema']: p['adress']}
        r = requests.get(url, proxies=proxy, timeout=5)
    else:
        r = requests.get(url)

    return r.html.

#Parsing free proxy list and choose random one

def get_proxy():
    html = requests.get("https://free-proxy-list.net/").text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', class_="table table-striped table-bordered").find_all('tr')[1:11]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'

        proxy = {'schema':schema, 'adress': ip + ':' + port}
        proxies.append(proxy)

    return choice(proxies)

#This function will be done for current web site
def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    #divs = soup.find('section', _class="pfgfjrg_plp").find('div', _class="pr7cfcb_plp largeCard").find_all('div')
    print(soup.prettify())
    


def make_all(url):
    get_data(get_html(url))


def main():
    url = "https://leroymerlin.ru/search/?q=топор"
    #url = ent_url.get()
    if S_multy.get() == 1:
        #Multiprossesing module 
        with Pool(int(ent_multy.get())) as p:
            p.map(make_all, url)
    else:
        get_data(get_html(url))


