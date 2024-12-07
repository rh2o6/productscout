from config import *
def run_search(itemtofind):
    import requests
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    import time
    import random
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    # Store Item Class
    class Item():
        def __init__(self, price: str, title: str, img: str, link: str):
            self.price = price
            self.title = title
            self.img = img
            self.link = link

        def __str__(self):
            return f"Price: {self.price}, Item Name: {self.title}, Source Image: {self.img}, Link: {self.link}"
        

        def to_dict(self):
            return {
            'title': self.title,
            'price': self.price,
            'link': self.link,
            'img': self.img
            }


    def solvecaptcha(store,headers):

        currlink = driver.current_url
        print(currlink)
        img = driver.find_element(By.CSS_SELECTOR,store['CaptchaImg'])
        imgurl = "https://api.apilayer.com/image_to_text/url?url="+img.get_attribute('src')
        print("URL:",imgurl)
        payload = {}

        response = requests.request("GET",imgurl,headers=headers,data=payload)

        print(response.status_code)

        result = response.json()

        if 'all_text' in result:
            print("Extracted Text:", result['all_text'])
            captchakey = result['all_text']

        captchasubmitfield = driver.find_element(By.NAME,store['CaptchaSubmit'])
        captchasubmitfield.click()
        captchasubmitfield.send_keys(captchakey)
        captchasubmitbutton = driver.find_element(By.CLASS_NAME,store['CaptchaButton'])
        captchasubmitbutton.click()
        



    def searchstore(itemtofind: str, store: dict):
        driver.get(store['Link'])

        #Finds the search bar and searches for item
        search = driver.find_element(By.NAME,store['searchbar'])
        search.click()
        search.send_keys(itemtofind)
        search.send_keys(Keys.RETURN)
        try:
            #time.sleep(2)
            captcha = driver.find_element(By.ID, store['Captcha'])
            if captcha != None:
               #solveCaptcha()
               print('There is a captcha')
               solvecaptcha(store=store,headers=headers)


        except:
            print('There is not a captcha!')



        

        try:
            driver.implicitly_wait(1)
            cards = driver.find_elements(By.CSS_SELECTOR, store['cardselect'])
        except:
            driver.implicitly_wait(1)
            cards = driver.find_elements(By.CLASS_NAME, store['cardselect'])

        results = []

        if cards:
            print("FOUND ELEMENTS")
            print(len(cards))
            for card in cards:
                if card.get_attribute("data-product") is None and store == gamestop:
                    continue
                try:
                    title = card.find_element(By.CSS_SELECTOR, store["titleselector"])
                except:
                    title = card.find_element(By.CLASS_NAME, store["titleselector"])


                try:
                    price = card.find_element(By.CSS_SELECTOR, store["priceselector"])
                    pricedisplay = price_formatting(price.text)
                except:
                    price = ""
                    pricedisplay = price 

                

                image = card.find_element(By.CSS_SELECTOR, store['imageselector'])
                driver.execute_script("arguments[0].scrollIntoView(true);", image)
                link = card.find_element(By.CSS_SELECTOR, store['linkselector'])
                title = title_trunc(title.text)

                #Some cards not selecting price, come back and permafix later. For now just dont include entries without price
                if pricedisplay!= "" or price!= "":
                    results.append(Item(pricedisplay, title, image.get_attribute('src'), link.get_attribute('href')))
                #print(f"\nTitle: {title},\nPrice: {pricedisplay}\nImage: {image.get_attribute('src')},\nLink: {link.get_attribute('href')}")
        else:
            print(f"{store['name']}   NOTHING FOUND")
        return results

    findings = {}

    for store in stores:
        store_name = store['name']
        #searchstore(store)
        findings[store_name] = {}
        findings[store_name]['name'] = store_name
        findings[store_name]['Results'] = searchstore(itemtofind, store)
    return findings

    # Ensure the browser closes properly
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting and closing the browser.")
        driver.quit()


def price_formatting(price: str) -> str:
    import re
    """
    Returns the price of the item, removing extra characters that may have been included.

    Args:
        price (str): Price string obtained from innerHTML or any other source.

    Returns:
        str: Exact price filtered out from extra characters.
    """
    # Step 1: Clean the string of unwanted characters like currency symbols, letters, etc.
    price = re.sub(r'[^\d.\n]', '', price)  # Remove everything that's not a digit, period, or newline

    # Step 2: Normalize newline characters to periods (for cases like "45\n56")
    price = price.replace('\n', '.')

    # Step 3: Split the price by spaces or newline (if they exist) and filter for valid numbers
    potential_prices = price.split()
    
    # Step 4: Build the 'after' string from valid segments (handling multiple numbers correctly)
    after = ""
    for substr in potential_prices:
        if re.match(r'^\d*\.?\d+$', substr):  # This checks for valid number format (e.g., "45.56")
            after = substr  # This overwrites to get the last valid price
    
    return "$"+after
        

def title_trunc(title:str):


    before = title
    after= ""
    mylist = title.split(" ")
    length = len(mylist)
    if length < 10:
        return before

    while length >=10:
      length = len(mylist)
      print("List Length",length)
      mylist.pop(length-1)
    
    after = (" ").join(mylist)
    


    return after

def resultsorting(store:str,findings:dict,sorttype:str):
    
    presorted = findings[store]['Results']

    if sorttype == "price-low":
        presorted.sort(key=lambda x: float(x['price'][1:]))

    elif sorttype == "price-high":
            presorted.sort(key=lambda x: float(x['price'][1:]),reverse = True)

    elif sorttype == "alpha":
        presorted.sort(key = lambda x:x['title'])

    elif sorttype == "alphar":
        presorted.sort(key = lambda x:x['title'],reverse = True)

    else:
        pass


    findings[store]['Results'] = presorted
    

    print("SORTED")

    return findings

def convert_items_to_dict(items):
    return [item.to_dict() for item in items]





