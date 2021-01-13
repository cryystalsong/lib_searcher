## IMPORTS
from bs4 import BeautifulSoup as soup 
from urllib.request import urlopen as uReq
from PIL import Image

bibliocommons_domains = {
    "VPL": "vpl",
    "NWPL": "newwestminster",
    "RPL": "yourlibrary",
    "BPL": "burnaby"
}

def generateBibliocommonsDomain(library_domain):
    return "https://{}.bibliocommons.com".format(library_domain)

def readURLtoSoup(url):
    # opens the connection and downloads html page from url
    uClient = uReq(url)

    # parses html into a soup data structure to traverse html
    # as if it were a json data type.
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    return page_soup

def getBookImg(url):
    page_soup = readURLtoSoup(url)
    img_src = page_soup.find("img",{"class": "jacketCover bib_detail"})['src']

    try: 
        uClient = uReq(img_src)    
    except: 
        img_src = "https:" + img_src
        uClient = uReq(img_src)
    finally:
        im = Image.open(uClient)
        uClient.close()
        return img_src
        # display(im)

# returns a list of result
def parseEachContainer(containers, library, library_domain_url):
    results = []

    for container in containers: 
        result = {
            "title": "",
            "author": "",
            "library_source": "",
            "book_link": "",
            "availability": "",
            "img_src": ""
        }

        title = container.find("div",{"class": "jacket-cover-wrap hidden-md hidden-lg"}).a['title']
        result["title"] = title
         
        try: 
            author = container.find("a",{"class": "author-link"}).text #sometimes unavailabile
            result["author"] = author
        except:
            author = None

        book_link = container.find("div",{"class": "jacket-cover-wrap hidden-md hidden-lg"}).a["href"]
        book_link = library_domain_url + book_link

        availability = container.find("div",{"class": "manifestation-item-availability-block-wrap"}).span.text

        result["library_source"] = library
        result["book_link"] = book_link
        result["availability"] = availability
        result["book_type_detail"] = container.find("div",{"class": "cp-format-info manifestation-item-format-info"}).contents[0].text
        result["img_src"] = getBookImg(book_link) #TODO: fetch from lazy loading

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
        
    page_soup = readURLtoSoup(library_search_urls[library])

    response_object = {}

    response_object["library"] = library

    containers = page_soup.findAll("div", {"class": "cp-search-result-item-content"})
    response_object["result_count"] = len(containers)  
    response_object["results"] = []  

    if response_object["result_count"] <= 0:
        return response_object
    
    library_domain_url = generateBibliocommonsDomain(bibliocommons_domains[library])  
    response_object["results"] = parseEachContainer(containers, library, library_domain_url)

    return response_object