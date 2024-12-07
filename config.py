from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import time
import random
# Path to the chromedriver executable
driverpath = r"C:\Users\roblo\OneDrive\Desktop\Python Projects\Seleniumstuff\Selenium.Project\chromedriver.exe"
# Path to the log file
log_path = r"C:\Users\roblo\OneDrive\Desktop\Python Projects\Seleniumstuff\Selenium.Project\chromedriver.exe"
# Set Chrome options if needed
options = Options()

user_agents = [
    # Add your list of user agents here
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
]

useragent = random.choice(user_agents)

#options.add_argument('--headless')
options.add_argument('--disable-gpu')  # May improve stability in headless mode
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-web-security')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--no-sandbox')  # Sometimes helps with stability
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument(f'user-agent={useragent}')
# Create the service with logging
service = Service(executable_path=driverpath, log_path=log_path)




amazon = {'searchbar':'field-keywords',
          'name':'Amazon',
          'identifier':'Amazon.ca: Low Prices – Fast Shipping – Millions of Items',
          'titleselector':'h2 a span',
          'priceselector':'[data-cy="price-recipe"] span',
          'imageselector':'.s-image',
          'linkselector':"h2 a",
          'cardselect':'[data-component-type="s-search-result"]',
          'results':[],
          'Link':'https://www.amazon.ca/',
          'Captcha':'captchacharacters',
          'CaptchaImg':'body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-row.a-spacing-large > div > div > div.a-row.a-text-center > img',
          'CaptchaSubmit':'field-keywords',
          'CaptchaButton':'a-button-text'}
walmart = {'searchbar':'q',
           'name':'Walmart',
           'identifier':'Online Shopping Canada: Everyday Low Prices at Walmart.ca!',
           'imageselector':'',
           'linkselector':'',
           'Link':'https://www.walmart.ca/en',
           'results':[]}

gamestop  = {'searchbar':'q',
           'name':'Gamestop',
           'identifier':'GameStop |',
           'imageselector':'div .searchProductImage > a > img',
           'linkselector':'div .desktopSearchProductTitle a',
           'titleselector':'div .desktopSearchProductTitle',
           'priceselector':'div .searchTilePriceDesktop div',
           'cardselect':'#productsList > div > div',
           'results':[],
           'Link':'https://www.gamestop.ca/',
           'Captcha':'None'}

bestbuy  = {'searchbar':'search',
           'name':'Best Buy',
           'identifier':'Best Buy:',
           'imageselector':'div .searchProductImage > a > img',
           'linkselector':'div .desktopSearchProductTitle a',
           'titleselector':'div .desktopSearchProductTitle',
           'priceselector':'div .searchTilePriceDesktop div',
           'cardselect':'class*=style-module_col > class*=productItemName',
           'results':[],
           'Link':'https://www.bestbuy.ca/en-ca'}

target = {'searchbar':'searchTerm',
           'name':'Target',
           'identifier':'Best Buy:',
           'imageselector':'.sc-f82024d1-0.rLjwS h3 div a div.sc-d091612e-0.dqtsAv picture source:first-child',
           'linkselector':'div.sc-f82024d1-0.rLjwS a',
           'titleselector':'div.sc-f82024d1-0.rLjwS a',
           'priceselector':'.sc-f82024d1-0.rLjwS div.sc-25636ef2-0.hjjUok span > span',
           'cardselect':'.sc-f82024d1-0.rLjwS',
           'results':[],
           'Link':'https://www.target.com/'}

ebay = {'searchbar':'_nkw',
           'name':'Ebay',
           'identifier':'Best Buy:',
           'imageselector':'.s-item.s-item__pl-on-bottom > div > div.s-item__image-section > div > a > div > img',
           'linkselector':'div > div.s-item__info.clearfix > a',
           'titleselector':'.s-item.s-item__pl-on-bottom > div > div.s-item__info.clearfix > a > div > span',
           'priceselector':'.s-item.s-item__pl-on-bottom > div > div.s-item__info.clearfix > div.s-item__details.clearfix > div.s-item__details-section--primary > div:nth-child(1) > span > span',#item52df3aeca1 > div > div.s-item__info.clearfix > div.s-item__details.clearfix > div.s-item__details-section--primary > div:nth-child(1) > span
           'cardselect':'.s-item.s-item__pl-on-bottom',
           'results':[],
           'Link':'https://www.ebay.ca/'}

homedepot = {'searchbar':'#id110',
           'name':'Sams Club',
           'identifier':'Best Buy:',
           'imageselector':'.s-item.s-item__pl-on-bottom > div > div.s-item__image-section > div > a > div > img',
           'linkselector':'div > div.s-item__info.clearfix > a',
           'titleselector':'.s-item.s-item__pl-on-bottom > div > div.s-item__info.clearfix > a > div > span',
           'priceselector':'.s-item.s-item__pl-on-bottom > div > div.s-item__info.clearfix > div.s-item__details.clearfix > div.s-item__details-section--primary > div:nth-child(1) > span > span',#item52df3aeca1 > div > div.s-item__info.clearfix > div.s-item__details.clearfix > div.s-item__details-section--primary > div:nth-child(1) > span
           'cardselect':'.sc-pc-medium-desktop-card-canary.sc-plp-cards-card',
           'results':[],
           'Link':'https://www.homedepot.ca/en/home.html'}



stores = [gamestop,amazon,ebay]
headers = {"apikey":"CpRFLFxf9zEqQQ8m8ET3nOtGojDSRMyj"}

def passhashing(password):
    import bcrypt
    password_bytes = password.encode('utf-8')
    hashedpw = bcrypt.hashpw(password=password_bytes,salt=bcrypt.gensalt())
    
    return hashedpw


