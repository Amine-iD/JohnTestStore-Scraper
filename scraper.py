from requests_html import HTMLSession 
from bs4 import BeautifulSoup
import csv
session = HTMLSession()
headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
def parser(url):
    try:  
        resp = session.get(url)
        if resp.status_code == 404:
            return 404  # To make the return value of this function 404 to be used in get_all_products ~! NEEDS TO BE MODIFIED  ~!
        soup = BeautifulSoup(resp.text ,'lxml')
        
    except RuntimeWarning as rw:
        print('--'*30)
        print(rw)
        print('--'*30)
        
    except Exception as e:
        print('--'*30)
        print(e)
        print('--'*30)
    
    return soup

def get_all_products():
    """This function gets the products info shown in the page : name / link / price"""
    for page_number in range(1,20):
        url = f'https://gopher1.extrkt.com/?paged={page_number}'
        soup = parser(url)
        if soup == 404:
            return "Page not found!"
        else:
            products = soup.find('ul').find_all('li')
            print('page number:',page_number)
            for product in products:
                url = product.a # This gives the price and the name of the product, but used only to get the link (Best.Practice?)
                yield{    
                    "link" : url['href'],
                    "name" : product.find('h2',{'class' : 'woocommerce-loop-product__title'}).text,
                    "price" : product.find('span',{'class' : 'price'}).text
                    }

def get_product_info():
    products = get_all_products()
    FIELD_NAMES = ['Link','Name','Price','Activity', 'Gender', 'Color', 'Style', 'Pattern', 'Material', 'Strap', 'Size']
    for product in products:
        link  =  product["link"]
        name  =  product["name"]
        price =  product['price']
        resp = session.get(link,headers=headers)
        soup = parser(link)
        data = {
            'link':link ,
            'name' : name ,
            'price':price,
            }
        try:
            category = soup.find('div' ,{'class':'product_meta'}).contents[3].text 
            additional_info = soup.find('table',{'class' : 'woocommerce-product-attributes shop_attributes'}).find_all('tr') 
            for i in range(len(additional_info)):
                key = additional_info[i].contents[1].text.strip()
                value = additional_info[i].contents[3].text.strip()
                data[key] = value
                # field_names.append(key) NOTE : .....
            def write_to_csv():
                with open('test.csv','w') as test_file:
                    csv_writer = csv.DictWriter(test_file , FIELD_NAMES , delimiter='|')
                    csv_writer.writeheader()
                    for j in range(len(FIELD_NAMES)):
                        if data[f'{FIELD_NAMES[j]}'] != True :
                          ...  

        except AttributeError :
            print("NOT FOUND THE PRODUCT :",product) ##tab-additional_information > table > tbody
    #    print(field_names) With this I got all the possible attributes for each product NOTE:~This variable was used just once for non static attributes(which depend on products)~

def cleaned_list(lst:list):
    """This function removes duplacted valus of a given list using casting of type :set object """
    return set(lst)

# start = time.time()
# data = get_product_info()
# print(data)
# lst = ['Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity','Gender', 'Material', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size','Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color','Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color','Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size','Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color','Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Pattern','Material', 'Strap', 'Style', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern','Material', 'Strap', 'Style', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size','Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size','Color', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity','Pattern', 'Material', 'Strap', 'Style', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Activity', 'Gender', 'Material', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Activity', 'Gender', 'Material', 'Size', 'Activity', 'Gender', 'Material', 'Size', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Activity', 'Pattern', 'Material', 'Strap', 'Style', 'Size', 'Color', 'Activity', 'Gender', 'Material', 'Size', 'Color', 'Size', 'Color']

# CSV preparation : 
