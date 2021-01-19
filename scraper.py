## IMPORTS
from selenium import webdriver
import os
from bs4 import BeautifulSoup as soup 

bibliocommons_domains = {
    "VPL": "vpl",
    "NWPL": "newwestminster",
    "RPL": "yourlibrary",
    "BPL": "burnaby"
}

def generateBibliocommonsDomain(library_domain):
    return "https://{}.bibliocommons.com".format(library_domain)

def set_up_chromedriver(local):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless") # avoids opening browser 
    chrome_options.add_argument("--disable-dev-shm-usage")

    if local: 
        from webdriver_manager.chrome import ChromeDriverManager
        return webdriver.Chrome(ChromeDriverManager(version="87.0.4280.88").install(), chrome_options=chrome_options)

    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    return webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

# returns a list of result
def parseEachContainer(contents, library):    
    library_domain_url = generateBibliocommonsDomain(bibliocommons_domains[library]) 
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

        result["title"] = content.find("div",{"class": "jacket-cover-wrap hidden-md hidden-lg"}).a['title']
        result["img_src"] = content.find('img')['src']
         
        try:             
            result["author"] = content.find("a",{"class": "author-link"}).text
        except:
            result["author"] = None

        book_link = content.find("div",{"class": "jacket-cover-wrap hidden-md hidden-lg"}).a["href"]
        result["book_link"] = library_domain_url + book_link

        result["availability"] = content.find("div",{"class": "manifestation-item-availability-block-wrap"}).span.text
        result["book_type_detail"] = content.find("div",{"class": "cp-format-info manifestation-item-format-info"}).contents[0].text
        result["library_source"] = library

        results.append(result)

    return results

def getSearchURL(library, search_keywords):
    search_query = search_keywords.replace(" ","+")

    library_search_urls ={
        "VPL": "https://vpl.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart",
        "NWPL": "https://newwestminster.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart",
        "RPL": "https://yourlibrary.bibliocommons.com/v2/search?query="+search_query+"&searchType=keyword",
        "BPL": "https://burnaby.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart"
    }  

    return library_search_urls[library]


def main(library, search_keywords):
    driver = set_up_chromedriver(local=False)
    
    search_url = getSearchURL(library, search_keywords)    
    driver.get(search_url)

    page = driver.page_source
    pg_soup = soup(page, "html.parser")
    result_containers = pg_soup.findAll("div", {"class": "cp-search-result-item-content"})

    response_object = {}

    response_object["library"] = library
    response_object["results"] = []  

    if len(result_containers) <= 0:
        response_object["total_result_count"] = 0
        return response_object
 
    total_result_count = pg_soup.find("span", {"class": "pagination-text"}).text.split(' ')[-2]
    response_object["total_result_count"] = total_result_count
    response_object["current_result_count"] = len(result_containers)

    response_object["currentPage"] = 1  
    response_object["totalPages"] = len(pg_soup.find("section", {"class": "bottom-controls"}).div.ul.contents) - 2 #2 of the contents are the forward and backward button
    
    response_object["results"] = parseEachContainer(result_containers, library)
    
    driver.close()

    return response_object