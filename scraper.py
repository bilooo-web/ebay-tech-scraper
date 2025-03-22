from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
from datetime import datetime

# Set up the webdriver (use ChromeDriver)
service = Service(ChromeDriverManager().install())  # Automatically manage ChromeDriver
driver = webdriver.Chrome(service=service)

# Open the eBay tech deals page
driver.get("https://www.ebay.com/globaldeals/tech")

# Function to scroll and load all products on the page
def scroll_and_load():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Wait for new items to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# Scroll to load all products
scroll_and_load()

# Wait for products to load (timeout after 10 seconds if not found)
wait = WebDriverWait(driver, 10)
products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'dne-itemtile')))

product_data = []

for product in products:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        title = product.find_element(By.CLASS_NAME, 'dne-itemtile-title').text
    except:
        title = 'N/A'
    try:
        price = product.find_element(By.CLASS_NAME, 'dne-itemtile-price').text.strip('US $')
    except:
        price = 'N/A'
    try:
        original_price = product.find_element(By.CLASS_NAME, 'dne-itemtile-price').find_element(By.TAG_NAME, 'span').text.strip('US $')
    except:
        original_price = 'N/A'
    try:
        shipping = product.find_element(By.CLASS_NAME, 'dne-itemtile-shipping').text
    except:
        shipping = 'Shipping info unavailable'
    
    item_url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
    
    product_data.append([timestamp, title, price, original_price, shipping, item_url])

# Save the data into a CSV file
filename = 'ebay_tech_deals.csv'

# Check if the file already exists to append data
try:
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # If the file is empty, write headers
            writer.writerow(['timestamp', 'title', 'price', 'original_price', 'shipping', 'item_url'])
        writer.writerows(product_data)
except Exception as e:
    print(f"Error writing to file: {e}")

# Close the browser
driver.quit()
