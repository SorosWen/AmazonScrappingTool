import pyppdf.patch_pyppeteer
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd


s = HTMLSession()
product_name = 'shoes'
url = 'https://www.amazon.com/s?k=' + product_name

def getdata(url):
    r = s.get(url)
    r.html.render()
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup

def getNextSearchPage(soup):
    # this will return the next page URL
    pages = soup.find('ul', {'class': 'a-pagination'})
    if not pages.find('li', {'class': 'a-disabled a-last'}):
        #url = 'https://www.amazon.com' + str(pages.find('li', {'class': 'a-last'}).find('a')['href'])
        links_list = getAllProductPage(soup)
        #return url
        return links_list
    else:
        return

def getAllProductPage(soup):
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})
    links_list = []
    for link in links:
        links_list.append("https://www.amazon.com" + link.get('href'))
    return links_list

output_limit = 1

while output_limit > 0:
    data = getdata(url)
    links_list = getAllProductPage(data)
    if not links_list:
        break
    print(links_list)
    output_limit = output_limit - 1