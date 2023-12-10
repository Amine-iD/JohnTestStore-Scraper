from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
resp = session.get('https://gopher1.extrkt.com/')
resp.html.render(sleep = 1 , keep_page = True , scrolldown = 1)
soup = BeautifulSoup(resp.html.raw_html,'lxml')

def get_product_info(soup ,lst:list):
    """This function gets the products info shown in the page : name / link / price"""
    products = soup.find('ul').find_all('li')
    for product in products:
        url = product.a # This gives the price and the name of the product, but used only to get the link (B.P?)
        link = url['href']
        name = product.find('h2',{'class' : 'woocommerce-loop-product__title'}).text  
        price = product.find('span',{'class' : 'price'}).text
        products_list = {'link' :link , 'product-name' : name , 'product-price' : price}
        lst.append(products_list)
    return lst
lst = []
output = get_product_info(soup,lst)
print(output[0])