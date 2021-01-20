from selenium_scraper import execute_search

def getSearchURL(library, search_keywords):
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

def main(library, search_keywords):    
    search_url = getSearchURL(library, search_keywords)

    response_object = execute_search(search_url, dev_mode=False)       
    
    response_object["library"] = library
    return response_object