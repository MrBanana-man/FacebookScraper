import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import pyautogui
import time


def login_and_scroll(username, password, url):
    # Set up Chrome options
    options = Options()
    options.add_argument("--start-maximized")  # Open browser in maximized mode
    options.add_argument("--disable-notifications")  # Disable notifications

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Open the provided URL (Facebook Marketplace or any URL)
        driver.get(url)

        # Allow some time for the page to load
        time.sleep(2)

        # Use pyautogui to click on specific coordinates (adjust as per your screen resolution)
        pyautogui.moveTo(1127, 848)
        time.sleep(0.5)
        pyautogui.click()

        # Find the email and password fields and enter credentials
        wait = WebDriverWait(driver, 20)
        email_xpath = "//input[@name='email' or @id='email']"
        password_xpath = "//input[@name='pass' or @id='pass']"

        username_field = wait.until(EC.presence_of_element_located((By.XPATH, email_xpath)))
        username_field.send_keys(username)

        password_field = wait.until(EC.presence_of_element_located((By.XPATH, password_xpath)))
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        # Wait for the page to load after login
        time.sleep(8)  # Adjust as needed
        
        # Function to check if element is present
        def is_element_present(locator):
            try:
                driver.find_element(*locator)
                return True
            except:
                return False

        # Scroll down until the specified element is found
        while not is_element_present((By.XPATH, '//span[contains(@class, "x193iq5w") and text()="Fler resultat utanför ditt område"]')):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Adjust sleep time as needed

        # Once element is found, you can perform further actions if needed
        element = driver.find_element(By.XPATH, '//span[contains(@class, "x193iq5w") and text()="Fler resultat utanför ditt område"]')
        #print("Element found:", element.text)

        # Optionally, you can perform additional actions after scrolling

        # Return the page source
        return driver.page_source.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)

    finally:
        driver.quit()

def filer_data():
    # Create a BeautifulSoup object
    soup = BeautifulSoup(login_and_scroll(username, password, marketplace_url), 'html.parser')
    
    ItemPrice = soup.find_all('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u')
    ItemLocation = soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')
    ItemLink = soup.find_all('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv')
    ItemTitle = soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
    
    # List to store the data
    data = []
    
    for price, title, location, link in zip(ItemPrice, ItemTitle, ItemLocation, ItemLink):
        price_text = price.text.replace('\xa0', ' ').strip()
        locations = location.text
        links = baseurl + link.get('href')
        titles = title.text
        
        # Append a dictionary with the extracted data to the list
        data.append({
            'Title': titles,
            'Price': price_text,
            'Location': locations,
            'Link': links
        })
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    
    # Write the DataFrame to a CSV file
    df.to_csv('facebook_data.csv', index=False)


marketplace_url = "https://www.facebook.com/marketplace/"
baseurl = "https://www.facebook.com"

# Your Facebook credentials
username = "gmail@to.login"
password = "password_to_account"

filer_data()
