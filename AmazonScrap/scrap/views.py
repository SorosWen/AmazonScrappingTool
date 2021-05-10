from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/679.36', 
            'Accept-Language': 'en-US, en;q=0.5'})
product_number = 12

def interface(request):
    if request.method == 'POST':
        product_name = request.POST['product_name']
        amazon_list = amazon_getSearchResult(product_name)
        ebay_list = ebay_getSearchResult(product_name)
        #recommend_list = getRecommendation(amazon_list + ebay_list)
        return render(request, 'products.html', {'product_name': product_name, 'amazon_list':amazon_list, 'ebay_list': ebay_list})
    else:
        return render(request, 'products.html')


##########################################################
# Recommend Result #######################################
##########################################################

##########################################################
# Amazon Product Result #################################
##########################################################
def amazon_getSearchResult(product_name):
    url = 'https://www.amazon.com/s?k=' + product_name.replace(' ', '+')
    webpage = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    product_list = []
    count = product_number
    for link in links: 
        link = "https://www.amazon.com" + link.get('href')
        product_list.append(amazon_product(link))
        if (count <= 0):
            break
        else: 
            count -= 1
    if not product_list:
        print("\nWARNING: The user agent might have been temporarily banned. Please replace the HEADERS with a valid one, or try again later.\n")
        product_list = [["https://developers.whatismybrowser.com", "Empty", "Empty", "Empty"]]
    return product_list
 
def amazon_product(url):
    webpage = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    title = get_title(soup)
    price = get_price(soup)
    rating = get_rating(soup)
    review = get_reviewNum(soup)
    return [str(url), title, price, rating, review]

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

def get_reviewNum(soup): 
    try:
        review = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
    except:
        review = ""
    return review

##########################################################
# eBay Product Result ###################################
##########################################################
def ebay_getSearchResult(product_name):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570&_nkw=' + product_name.replace(' ', '+') + '&_sacat=0'
    webpage = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    links = soup.find_all("a", attrs={'class':'s-item__link'})
    product_list = []
    count = product_number
    for link in links: 
        link = link.get('href')
        product_list.append(ebay_product(link))
        if count <= 0:
            break
        else:
            count -= 1
    return product_list

def ebay_product(url):
    webpage = requests.get(url)
    soup = BeautifulSoup(webpage.text, "html.parser")
    title = ebay_get_title(soup)
    price = ebay_get_price(soup)
    condition = ebay_get_condition(soup)
    return [str(url), title, price, condition]

def ebay_get_title(soup):
    try: 
        title = soup.title.string.replace('  | eBay', '')
    except:
        title = "N/A"
    return title

def ebay_get_price(soup):
    try:
        price = soup.find("span", attrs={'id':'prcIsum'}).string.replace('US ', '').replace('/ea', '').strip()
    except:
        price = "N/A"
    return price

def ebay_get_condition(soup):
    try:
        condition = soup.find("div", attrs={'id':'vi-itm-cond'}).string
    except:
        condition = "N/A"
    return condition
