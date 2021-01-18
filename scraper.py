## IMPORTS
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# returns a list of result
def parseEachContainer(contents, library):
    results = []

    for content in contents: 
        result = {
            "title": "",
            "author": "",
            "library_source": "",
            "book_link": "",
            "availability": "",
            "img_src": ""
        }

        result["title"] = content.find_element_by_class_name('title-content').text
        result["img_src"] = content.find_element_by_tag_name('img').get_attribute("src")
         
        try:             
            result["author"] = content.find_element_by_class_name('author-link').text
        except:
            result["author"] = None

        result["book_link"] = content.find_element_by_class_name('cp-title').find_element_by_tag_name('a').get_attribute("href")
        result["availability"] = content.find_element_by_class_name('manifestation-item-availability-block-wrap').find_element_by_tag_name('span').text
        result["book_type_detail"] = content.find_element_by_class_name('format-info-main-content').text
        result["library_source"] = library

        results.append(result)

    return results


def main(library, search_keywords):
    search_query = search_keywords.replace(" ","+")

    library_search_urls ={
        "VPL": "https://vpl.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart",
        "NWPL": "https://newwestminster.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart",
        "RPL": "https://yourlibrary.bibliocommons.com/v2/search?query="+search_query+"&searchType=keyword",
        "BPL": "https://burnaby.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart"
    }    
    
    driver.get(library_search_urls[library])

    response_object = {}

    response_object["library"] = library

    contents = driver.find_element_by_class_name('results').find_elements_by_tag_name('li')
    response_object["result_count"] = len(contents)  
    response_object["results"] = []  

    if response_object["result_count"] <= 0:
        return response_object
    
    response_object["results"] = parseEachContainer(contents, library)

    return response_object