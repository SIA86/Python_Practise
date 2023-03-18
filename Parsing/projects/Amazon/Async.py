import asyncio
import time, csv, sys
from requests_html import AsyncHTMLSession


async def get_html(url):
    #print(url)
    asession = AsyncHTMLSession()
    headers = {'User_Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    tries = 1    
    while(True):       
        try:
            r = await asession.get(url, headers = headers)
            
        except Exception:
            print('Failed')
            pass
        else:
            print('Success')
            if r.status_code == 200:
                await r.html.arender(sleep=0.5, timeout= 15)
                return r
            else:
                print(f'Connection problems {r}')
                print(f'{5-tries} tries left')
                if tries <= 5:
                    time.sleep(5)
                    tries += 1
                    pass
                else:
                    sys.exit(2)

async def get_data(r):
        
    products = r.html.find('[data-component-type="s-search-result"]')  
    
    print("Collecting product's data")
 
    for product in products:
        asin = product.attrs['data-asin']
        link = 'https://www.amazon.com' + product.find('span.rush-component a', first=True).attrs['href']
                   
        name = product.find('span[class="a-size-base-plus a-color-base a-text-normal"]', first=True).text
        
        try: 
            integer = product.find('span.a-price-whole', first=True).text 
            decimal = product.find('span.a-price-fraction', first=True).text
            price = integer +  decimal
        except:
            price = None
        
        data = {"Asin": asin,
                "Name": name,
                "Price": price,
                "Link": link}
        
        #ADD try block if
        csv_writer(data)
    print('Done')    


def csv_writer(data):
    print('Writing data to file')
    with open("Amazon2.csv", 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Asin', 'Name', 'Price', 'Link'])
        writer.writerow({"Asin": data["Asin"],
                         "Name": data["Name"],
                         "Price": data['Price'],
                         "Link": data['Link']})
        


async def get_next(response):    
    try:
        next = response.html.find('a.s-pagination-next', first=True).attrs['href']
        url ='https://www.amazon.com' + next   
        response = await get_html(url)
        task1 = asyncio.create_task(get_data(response))
        task2 = asyncio.create_task(get_next(response))
        await asyncio.gather(task1, task2 )
    except AttributeError:
        pass
    

async def main():
    url = "https://www.amazon.com/s?k=sucsess&dc&qid=1671548156&rnid=2941120011&ref=sr_pg_1"
    t0 = time.time()
    response = await get_html(url)
    task1 = asyncio.create_task(get_data(response))
    task2 = asyncio.create_task(get_next(response))
    await asyncio.gather(task1, task2 )
    
    print(time.time() - t0)



if __name__ == '__main__':
    asyncio.run(main())
                