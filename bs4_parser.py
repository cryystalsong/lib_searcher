from bs4 import BeautifulSoup as soup 

def parseLibraryPage(html_page):
    pg_soup = soup(html_page, "html.parser")
    result_containers = pg_soup.findAll("div", {"class": "cp-search-result-item-content"})

    response_object = {
        "library": "",
        "current_page": "",
        "current_result_count": "",
        "total_result_count": "",
        "results": []
    }

    if len(result_containers) <= 0:
        response_object["total_result_count"] = 0
        return response_object
 
    total_result_count = pg_soup.find("span", {"class": "pagination-text"}).text.split(' ')[-2]
    response_object["total_result_count"] = total_result_count
    response_object["current_result_count"] = len(result_containers)
    response_object["results"] = parseEachContainer(result_containers)
    
    return response_object

# returns a list of result
def parseEachContainer(contents):    
    results = []

    for content in contents: 
        result = {
            "title": "",
            "author": "",
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

        try:             
            result["availability"] = content.find("div",{"class": "manifestation-item-availability-block-wrap"}).span.text.strip()
        except:
            result["availability"] = "Availability cannot be retrieved"
        
        book_link = content.find("div",{"class": "jacket-cover-wrap hidden-md hidden-lg"}).a["href"]
        result["book_link"] = book_link
        result["book_type_detail"] = content.find("div",{"class": "cp-format-info manifestation-item-format-info"}).contents[0].text

        results.append(result)

    return results