from bs4 import BeautifulSoup
import requests

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def ebay_getSearchResult(product_name):
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570&_nkw=' + product_name.replace(' ', '+') + '&_sacat=0'
    webpage = requests.get(url, headers = HEADERS)
    soup = BeautifulSoup(webpage.content, "lxml")
    links = soup.find_all("a", attrs={'class':'s-item__link'})
    product_list = []
    count = 12
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
    return [title, price, condition]

def ebay_get_title(soup):
    try: 
        title = soup.title.string.replace('  | eBay', '')
    except:
        title = "N/A"
    return title

def ebay_get_price(soup):
    try:
        price = soup.find("span", attrs={'id':'prcIsum'}).string
        price = price.replace('US ', '').replace('/ea', '')
    except:
        try: 
            price = soup.find("span", attrs={'id':'prcIsum', 'itemprop': 'price'})
        except: 
            price = "N/A"
    return price

def ebay_get_condition(soup):
    try:
        condition = soup.find("div", attrs={'id':'vi-itm-cond'}).string
    except:
        condition = "N/A"
    return condition

url ='https://www.ebay.com/itm/133239982629?_trkparms=ispr%3D1&hash=item1f05b8ca25:g:dJMAAOSwsMZfWBJU&amdata=enc%3AAQAFAAACcBaobrjLl8XobRIiIML1V4Imu%252Fn%252BzU5L90Z278x5ickkBUIiHwYv5YgVss0WaiENzzVt8rDF%252BdLTzcnLEKHY3SsjRUNkmXYBWUVpMLRtGKjII57f%252B5pyfIFgCtvkVaRtpX737NmfRPkW2W1bbY5y1dG0tMNR72aWG74U1gahVaseYt8%252BWQipMiHq4cjyZ97Agl9Q8CGO8ew2YtOFeVycRjef3E7YMGJnUNumeNIvWVGTupNqTAsYQulsCCQdA061DcgMtj2a1rPyf%252FFruWPEReF7Y%252Bxf5zQl7xopbj%252BynHGj7f4GQuImyRAae5PrMEOC6WBn53zDtG%252Bz4KjL2dl%252FEd2Seyo8DIMvjuS2xe%252FeHFN46I7aYZYgN%252FuRIcFW3bdo1F1j7GYaTzzFMhWpUeFMSDV1%252BCtPg8Mg5%252FJW73k8RGVnXRjhCdV%252FL%252BNOQGMZAJ8QeGPjqlwo8nhaDQ8kg64e5aAqowf12SivxCs1dEmnAgNRjbdg82deI1y3HC3bMxSviDL%252FlFTlrxPXjTtoeFa8kRLpAgFWVT7rNatl%252BaXcPY1b0nvFgkCLrXMCXGwVvp%252F7x%252BaNK5ITQn9eaRyeSZeX2j20KQ26KYRa6FeKAWNPemNJcYN0YU7S1UaNG2q28DJ2Zc6HNGujryRy%252FvKMDWjj0anB6sDm3gqCbYGI%252BG0VrA5YeY1EePMHUs9sZGRkeSfJnz0WtoyR7t3WIN3HP941B4OcsPQEa8EIvfLLInunrjNW0rRNRwht3reu97kV4ErXHWnrjrbX9eQI1oZhT1dLRbtzRgvcloYAGZFIspBqsRpMArDjMxRYLR8MtYWDo0Gm9w%253D%253D%7Ccksum%3A1332399826299c61119fa40844a7b85ef843f8a67e69%7Campid%3APL_CLK%7Cclp%3A2334524'
print(ebay_product(url))