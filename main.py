from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import requests
import time

try:
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Navigate to Pinterest page
    search_url = "https://www.pinterest.com/pin/81557443245580480/"
    driver.get(search_url)

    # Explicitly wait for the search input field to be visible
    search_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchBoxContainer"]/div/div/div[2]/input')))

    # Clear any existing text in the search input field
    search_input.clear()

    # Enter the search term and press Enter
    # search_term = "nature wallpaper landscape"
    search_term = str(input("Search :"))
    search_input.send_keys(search_term + "\n")

    # Wait for some time to allow the page to load
    time.sleep(5)

    # Function to scroll down until a certain number of images are loaded
    def scroll_down_until_images_loaded(target_num_images):
        image_urls = set()
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            new_image_urls = {img_tag['src'] for img_tag in soup.find_all('img', {'src': True})}
            image_urls.update(new_image_urls)
            if len(image_urls) >= target_num_images:
                break
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        return list(image_urls)[:target_num_images]

    # Get the image URLs
    image_urls = scroll_down_until_images_loaded(100)

    # Create a folder to store the downloaded images
    folder_name = "downloaded_images"
    os.makedirs(folder_name, exist_ok=True)

    # Download images and save them to the folder
    for idx, img_url in enumerate(image_urls):
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(os.path.join(folder_name, f"image_{idx}.jpg"), 'wb') as f:
                f.write(response.content)
                print(f"Image {idx + 1} downloaded successfully.")
        else:
            print(f"Failed to download image {idx + 1}.")

    driver.quit()

except Exception as e:
    print("An error occurred:", e)
    driver.quit()
