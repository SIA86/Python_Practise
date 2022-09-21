import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
from random import choice
from tkinter import *
import tkinter.ttk as ttk


def get_html(url):
    p = get_proxy()
    proxy = {p['schema']: p['adress']}
    r = requests.get(url, proxies=proxy, timeout=5)
    return r.text

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
    pass


def make_all(url):
    get_data(get_html(url))


def main():
    url = ent1.get()

    #Multiprossesing module 
    with Pool(5) as p:
       p.map(make_all, url)

#GUI commands

def check_time_on():
    ent_time['state'] = NORMAL


def check_multy_on():
    ent_multy['state'] = NORMAL


#Create GUI

root = Tk()
root.title('Yandex Market Parser')
root.resizable(width=False, height=False)

#Create parent frame - Frame 1
frame1 = ttk.Frame(root, borderwidth=5, relief='sunken', padding='0 5 0 5')
frame1.grid(column=0, row=0, sticky=W+E)

#Create child frame - Frame 2
frame2 = ttk.Frame(frame1)
frame2.grid(column=0, row=0)

ent_url = ttk.Entry(frame2, width=80)
lbl_ent_url = ttk.Label(frame2, text='Enter URL:')
ttk.Separator(frame2).grid(row=1, columnspan=2, sticky=E+W, pady=5)

ent_url.grid(column=1, row=0, padx=5)
lbl_ent_url.grid(column=0, row=0, padx=5)

#Create child frame - Frame 3
frame3 = ttk.Frame(frame1)
frame3.grid(column=0, row=1, sticky=W+E)

#First column (filter options: name, price, articul, marka)
name = BooleanVar()
price = BooleanVar()
art = BooleanVar()
mark = BooleanVar()
name.set(0)
price.set(0)
art.set(0)
mark.set(0)

lbl_ch_filter = ttk.Label(frame3, text='Choose filter:')
ch_name = ttk.Checkbutton(frame3, text='Name', variable=name)
ch_price = ttk.Checkbutton(frame3, text='Price', variable=price)
ch_art = ttk.Checkbutton(frame3, text='Art', variable=art)
ch_mark = ttk.Checkbutton(frame3, text='Mark', variable=mark)

lbl_ch_filter.grid(column=0, row=0, sticky=W, padx=5, pady=2)
ch_name.grid(column=0, row=1, sticky=W, padx=5, pady=2)
ch_price.grid(column=0, row=2, sticky=W, padx=5, pady=2)
ch_art.grid(column=0, row=3, sticky=W, padx=5, pady=2)
ch_mark.grid(column=0, row=4, sticky=W, padx=5, pady=2)

#Second column (parser options)
timeout = BooleanVar()
proxy = BooleanVar()
multy = BooleanVar()
timeout.set(0)
proxy.set(0)
multy.set(0)

lbl_parser_options = ttk.Label(frame3, text='Parser options:', padding='50 0 0 0')
ch_proxy = ttk.Checkbutton(frame3, text='Use proxy', variable=proxy, padding='50 0 0 0')
ch_time = ttk.Checkbutton(frame3, text='Timeout', variable=timeout, command=check_time_on, padding='50 0 0 0')
ch_multy = ttk.Checkbutton(frame3, text='Multiprocessing', variable=multy, command=check_multy_on, padding='50 0 0 0')
ent_time = ttk.Entry(frame3, width=5, state=DISABLED)
ent_multy = ttk.Entry(frame3, width=5, state=DISABLED)

lbl_parser_options.grid(column=1, row=0, sticky=W, padx=5, pady=2)
ch_proxy.grid(column=1, row=1, sticky=W,  padx=5, pady=2)
ch_time.grid(column=1, row=2, sticky=W,  padx=5, pady=2)
ch_multy.grid(column=1, row=3, sticky=W,  padx=5, pady=2)
ent_time.grid(column=2, row=2, sticky=W, padx=5, pady=2)
ent_multy.grid(column=2, row=3, sticky=W,  padx=5, pady=2)

#Third column options
format = StringVar()

lbl_output_options = ttk.Label(frame3, text='Output format:')
rad_csv = ttk.Radiobutton(frame3, text='CSV', variable=format, value='csv')
rad_db = ttk.Radiobutton(frame3, text='DATABAse', variable=format, value='DB')
rad_xls = ttk.Radiobutton(frame3, text='XLS', variable=format, value='xls')

lbl_output_options.grid(column=3, row=0, sticky=W, padx=5, pady=2)
rad_csv.grid(column=3, row=1, sticky=W, padx=5, pady=2)
rad_db.grid(column=3, row=2, sticky=W, padx=5, pady=2)
rad_xls.grid(column=3, row=3, sticky=W, padx=5, pady=2)

#Create frame for buttons - Frame 4
frame4 = ttk.Frame(root)
frame4.grid(column=0, row=2, sticky=E)

btn1 = ttk.Button(frame4, text='Start', command=main)
btn2 = ttk.Button(frame4, text='Exit', command=root.quit)

btn1.grid(column=0, row=0, padx=5, sticky=E)
btn2.grid(column=1, row=0, padx=5, sticky=E)

frame4.grid(column=0, row=2, sticky=E)

mainloop()

if __name__ == "__main__":
    main()
