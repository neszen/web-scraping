from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import time
# Function to create a database and a table to store product data
def create_database():
    conn = sqlite3.connect('flipkart_products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT,
                  price TEXT,
                  rating TEXT,
                  desc TEXT,
                  img_url)''')
    conn.commit()
    conn.close()

# Function to insert product data into the database
def insert_product(products):
    conn = sqlite3.connect('flipkart_products.db')
    c = conn.cursor()
    data_to_insert = [
        (product['title'], product['price'], product['rating'], product['desc'], product['img_url']) 
        for product in products
    ]
    print(f"Inserting {len(data_to_insert)} products:")
    print(data_to_insert)
   
    try:
        c.executemany('''
            INSERT INTO products (title, price, rating, desc, img_url) 
            VALUES (?, ?, ?, ?, ?)
        ''', data_to_insert)
        conn.commit()
    except sqlite3.ProgrammingError as e:
        print(f"Error during insertion: {e}") 
    finally:
        conn.close()


def scrape_flipkart(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)
   

    products = driver.find_elements(By.CLASS_NAME, 'CGtC98')#replace with actual class name
    data=[]
    try:
        for product in products:
            # Extracting product title
            title = product.find_element(By.CLASS_NAME, 'KzDlHZ').text #replace with actual class name 
            price = product.find_element(By.CLASS_NAME, 'hl05eU').text #replace with actual class name
            rating = product.find_element(By.CLASS_NAME, 'XQDdHH').text #replace with actual class name
            desc =  product.find_element(By.CLASS_NAME, '_6NESgJ').text #replace with actual class name
            img_url =  product.find_element(By.CLASS_NAME, 'DByuf4').text#replace with actual class name
            _d = {
                'title': title,
                'price': price,
                'rating': rating,
                'desc': desc,
                'img_url': img_url
            }
            data.append(_d)
        
    except Exception as e:
        print(f"Error extracting product data: {e}")

    insert_product(data)
    # Close the driver
    driver.close()
    driver.quit()

# Main execution
if __name__ == "__main__":
    create_database()
    # Example Flipkart URL to scrape (replace with a valid URL)
    flipkart_url = 'https://www.flipkart.com/search?q=laptop'
    scrape_flipkart(flipkart_url)
    print("Data scraping completed!")
