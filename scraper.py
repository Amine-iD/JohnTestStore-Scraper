from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
session = HTMLSession()

def parser(page_number:int):
    try:
        url = f'https://gopher1.extrkt.com/?paged={page_number}' # Some iteration 
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        resp = session.get(url,headers=headers)
        # resp.html.render(sleep = 2 , keep_page = True , scrolldown = 1)
        if resp.status_code == 404:
            return 404
        soup = BeautifulSoup(resp.html.raw_html,'lxml')
        print('page number: ',page_number )
    except RuntimeWarning as rw:
        print('--'*30)
        print(rw)
        print('--'*30)
        
    except Exception as e:
        print('--'*30)
        print(e)
        print('--'*30)
    
    return soup

def get_all_products(lst:list):
    """This function gets the products info shown in the page : name / link / price"""
    for page_number in range(1,20):
        soup = parser(page_number)
        if soup == 404:
            return "Page not found!"
        else:
            products = soup.find('ul').find_all('li')
            for product in products:
                url = product.a # This gives the price and the name of the product, but used only to get the link (Best.Practice?)
                link = url['href']
                name = product.find('h2',{'class' : 'woocommerce-loop-product__title'}).text  
                price = product.find('span',{'class' : 'price'}).text
                products_list = {'link' :link , 'product-name' : name , 'product-price' : price}
                lst.append(products_list)
            print(lst)
            lst = [] # to get a new independent list for each page 
            
lst = []
print(get_all_products(lst))
