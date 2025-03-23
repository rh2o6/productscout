
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium_stealth import stealth
import time
import random
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

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

# Suppress logs from Chrome
options.add_argument("--log-level=3")  # 0 = INFO, 1 = WARNING, 2 = ERROR, 3 = FATAL

stores = {
    "amazon": {
        'searchbar': 'field-keywords',
        'name': 'Amazon',
        'results': [],
        'Link': 'https://www.amazon.ca/',
        'Captcha': 'captchacharacters'
    },
    "walmart": {
        'searchbar': 'q',
        'name': 'Walmart',
        'identifier': 'Online Shopping Canada: Everyday Low Prices at Walmart.ca!',
        'imageselector': '',
        'linkselector': '',
        'Link': 'https://www.walmart.ca/en',
        'results': []
    },
    "gamestop": {
        'searchbar': 'q',
        'name': 'Gamestop',
        'Link': 'https://www.gamestop.ca/',
        'Captcha': 'True',
        'results': []
    },
    "bestbuy": {
        'searchbar': 'search',
        'name': 'Best Buy',
        'Link': 'https://www.bestbuy.ca/en-ca',
        'results': []
    },
    "target": {
        'searchbar': 'searchTerm',
        'name': 'Target',
        'Link': 'https://www.target.com/',
        'results': []
    },
    "ebay": {
        'searchbar': '_nkw',
        'name': 'Ebay',
        'Link': 'https://www.ebay.ca/',
        'results': []
    },
    "homedepot": {
        'searchbar': '#id110',
        'name': 'Sams Club',
        'Link': 'https://www.homedepot.ca/en/home.html',
        'results': []
    }
}

headers = {"apikey":"CpRFLFxf9zEqQQ8m8ET3nOtGojDSRMyj"}

def passhashing(password):
    import bcrypt
    password_bytes = password.encode('utf-8')
    hashedpw = bcrypt.hashpw(password=password_bytes,salt=bcrypt.gensalt())
    
    return hashedpw


