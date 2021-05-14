import pyppdf.patch_pyppeteer
from requests_html import HTMLSession
import pandas as pd

urls = ['https://www.amazon.com/adidas-Womens-Grand-Court-Tennis/dp/B08CZGHT8F/ref=sxin_7_slsr_d_i_fs4star_fa_0?cv_ct_cx=shoes&dchild=1&keywords=shoes&pd_rd_i=B08CZGHT8F&pd_rd_r=dca7dcfd-7bf5-4515-b0a4-3695e4ea5254&pd_rd_w=OHcTl&pd_rd_wg=knCgq&pf_rd_p=696b97f2-fff3-48c5-874b-e5bf2fda9d69&pf_rd_r=B7W7BYY4WASRTVJBEFMM&psc=1&qid=1619983164&sr=1-1-1157f02f-9108-4e24-9b1c-597d53863e82']

"""
amazon_getPrice(url)
Input: an url of a Amazon product page. 
Funtion: Retrieve product name and price from the iput url. 
Return value: a list with two strings: [product_name, price] 
"""
def amazon_getInfo(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)

    # product name
    try: 
        product_name = r.html.xpath('//*[@id="productTitle"]', first=True).text
    except: 
        product_name = 'No name for display'
    
    # product price
    try: 
        product_price = r.html.xpath('//*[@id="priceblock_ourprice"]', first=True).text
    except: 
        product_price = 'No Price for display.'

    # product rating
    try: 
        product_rating = r.html.xpath('//*[@id="acrCustomerReviewText"]', first=True).text.replace(' ratings', '')
    except: 
        product_rating = 'Rating is not available.'

    print([product_name, product_price, product_rating])
    return [product_name, product_price, product_rating]

tvprices = []
for url in urls:
    tvprices.append(amazon_getInfo(url))

print(len(tvprices))

pricesdf = pd.DataFrame(tvprices)
pricesdf.to_excel('tvprices.xlsx', index=False)