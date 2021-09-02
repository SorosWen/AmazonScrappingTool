# Amazona and eBay Scraper using BeautifulSoup
This is a personal project as an extension of the 411 project. 
The purpose of this project is to explore functionalities of BeautifulSoup and its integration with Python, not for any commercial use. 

**What this Application does:**
- The application takes a product name and fetch related product information from Amazon and eBay. 

There are two scraper in this project: 
1. Amazon/eBay product search page scraper: scrape all urls containing product urls. 
2. Amazon/eBay product information scraper: scrape product name, price, rating, review from a product page. 

**Sample Image:**

![GitHub Logo](/images/demo.png)

**Performance:**
- Each product page takes roughly 1.5 sec to scrap. A total of around 24 pages are being scrapped during each search. 
- The total wait time of each search is around 25 sec. 

# See this App on Google Cloud 
~~https://django-project-313903.uc.r.appspot.com~~ (This App is currently offline due to a payment issue). However, feel free to download and run this app locally. 

Note that the deployed application was configured for production environment. The configuration detail is not published on this repository for account security. 

# Tools Involved

- Language and Tools: Python, HTML, CSS.  
- Framework: Django. 
- Package: BeautifulSoup, SoupStainer. 
- Publisher: Google Cloud. 
