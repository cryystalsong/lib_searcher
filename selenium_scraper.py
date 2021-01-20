from selenium import webdriver
import os

from bs4_parser import parseLibraryPage 

def set_up_chromedriver(dev_mode):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless") # avoids opening browser 
    chrome_options.add_argument("--disable-dev-shm-usage")

    if dev_mode: 
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(ChromeDriverManager(version="87.0.4280.88").install(), chrome_options=chrome_options)

    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

def execute_search(search_url, dev_mode=True):
    driver = set_up_chromedriver(dev_mode) 
    driver.get(search_url)
    html_page = driver.page_source
    driver.close()

    response_object = parseLibraryPage(html_page)

    return response_object