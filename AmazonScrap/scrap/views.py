from django.shortcuts import render
from django.http import HttpResponse

#Amazon Scrapping Function
from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/601.36', 
            'Accept-Language': 'en-US, en;q=0.5'})

##########################################################
# Main Page ##############################################
##########################################################
def interface(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        #try: 
        product_list = amazon_getSearchResult(product_name)
        if not product_list:
            print("\nWARNING: The user agent might have been temporarily banned. Please replace the HEADERS with a valid one, or try again later.\n")
            product_list = [["https://developers.whatismybrowser.com", "Empty", "Empty", "Empty"]]
        return render(request, 'products.html', {'product_list':product_list})
        #except: 
            #return HttpResponse("Sorry, something went wrong. ")
    else:
        return render(request, 'products.html')

# Main Function 
def amazon_getSearchResult(product_name):
    url = 'https://www.amazon.com/s?k=' + product_name.replace(' ', '+')
    webpage = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    product_list = []
    count = 10
    for link in links: 
        link = "https://www.amazon.com" + link.get('href')
        product_list.append(amazon_product(link))
        if (count <= 0):
            break
        else: 
            count -= 1
    return product_list

# Helper Function 
def amazon_product(url):
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    title = get_title(soup)
    price = get_price(soup)
    rating = get_rating(soup)
    return [str(url), title, price, rating]

def get_title(soup):
    try: 
        title = soup.find("span", attrs={"id":'productTitle'}).text.replace('\n', '').replace('\'', '')
    except: 
        try: 
            title = soup.find("span", attrs={"class": 'a-size-large qa-title-text'}).text.replace('\n', '').replace('\'', '')
        except: 
            title = ""
    return title

def get_price(soup):
    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
    except:
        try: 
            price = soup.find("span", attrs={'class': 'a-size-large a-color-price'}).string
        except: 
            price = ""
    return price

def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    except:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

