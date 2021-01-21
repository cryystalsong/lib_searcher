from selenium_scraper import execute_search

def getSearchURL(library, search_keywords, page=None):
    search_query = search_keywords.replace(" ","+")

    library_search_urls ={
        "VPL": "https://vpl.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart",
        "NWPL": "https://newwestminster.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart",
        "RPL": "https://yourlibrary.bibliocommons.com/v2/search?query="+search_query+"&searchType=keyword",
        "BPL": "https://burnaby.bibliocommons.com/v2/search?query="+search_query+"&searchType=smart"
    }  

    if page: 
        return library_search_urls[library] + "&pagination_page={}".format(page) 
        
    return library_search_urls[library]     

def main(library, search_keywords, page=1):    

    if page == 1: 
        search_url = getSearchURL(library, search_keywords)
    else: 
        search_url = getSearchURL(library, search_keywords, page)
           
    response_object = execute_search(search_url)       
    response_object["current_page"] = page 
    response_object["library"] = library

    return response_object