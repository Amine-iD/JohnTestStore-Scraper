from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
resp = session.get('https://gopher1.extrkt.com/')
resp.html.render(sleep = 1 , keep_page = True , scrolldown = 1)
soup = BeautifulSoup(resp.html.raw_html,'lxml')

def get_product_info(soup):
    
    products = soup.find('ul').find_all('li')
    for product in products:
        url = product.a # This gives the price and the name of the product, but used only to get the link (B.P?)
        link = url['href']
        name = product.find('h2',{'class' : 'woocommerce-loop-product__title'}).text  
        price = link 
        products_list = {'link' :link , 'product-name' : name , 'product-price' : price}
        print(products_list)
# get the product info using requests_html Parser
# def get_product_info(resp):
#     all_products = resp.html.find('ul',first = True)
#     products = all_products.find('li')
#     for product in products:
#         name = product.find('.woocommerce-loop-product__title')
#         price_span = product.find('.price')
#         price = price_span[0].find('bdi') # to print these results out ,try to print price[0]
#         link = product.find('a')[0].absolute_links # try to print list(link)[0]

output = get_product_info(soup)
