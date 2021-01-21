# lib_searcher

## The "Why"

My local libraries, in the greater Vancouver area of Canada, doesn't have APIs available to the public, so I decided to web scrape the library sites of the four municipalities that I frequently visit, to create an API for my website, where I can search content across all the specified libraries and see their availability accordingly.

The libraries I chose all use Bibliocommons, so the content was pretty consistent across all of them, for an effective template. I scraped them using Selenium, as the contents on the sites are dynamically generated, and parsed the html page using BeautifulSoup as I found it to be slighter faster and more effective than using Selenium's `get_element_by_xx` methods.

See website: https://libsearcher.herokuapp.com/


## How to run this project locally

### Set your flask environment variable to development

`$env:FLASK_ENV = "development"` powershell (windows)

`set FLASK_ENV=development` cmd

`export FLASK_ENV=development` bash

See here for more help: https://flask.palletsprojects.com/en/master/server/

### Run!

`flask run`

You should see something like this in your console, make sure the environment is set to development as shown below, 
and simply visit the link that's generated for your flask app, in this case it's `http://126.1.0.2:5000/`

```
 * Environment: development
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 235-511-312
 * Running on http://126.1.0.2:5000/ (Press CTRL+C to quit)
 ```

## How to test the API endpoints

 I recommend using something like Postman or Insomnia to test this api

 Currently, I have only 1 endpoint being: `GET /search/`

 There are 3 supported parameter: 
 `library`(mandatory), 
 `search_keywords`(mandatory) and
 `page`(optional)
 
  `search_keywords` contains keywords where words are separated by `+` 
  i.e. `harry potter` should be `harry+potter`
  
  Reponses are returned in JSON format
 
## Other notes
This app is currently being hosted on Heroku: https://libsearcherapi.herokuapp.com/
 
Using something like Postman or Insomnia will allow you to play with the API and get familiarized

You can also see this API being used live on my website: https://libsearcher.herokuapp.com/
 
 ## Example calls
 
 `https://libsearcherapi.herokuapp.com/search/?library=VPL&search_keywords=cracking+the+coding+interview`
 
 would yield the following result
 
 ```{
    "current_page": 1,
    "current_result_count": 4,
    "library": "VPL",
    "results": [
        {
            "author": "McDowell, Gayle Laakmann",
            "availability": "All copies in use",
            "book_link": "/item/show/4543686038",
            "book_type_detail": "Book - 2015 | 6th edition",
            "img_src": "https://secure.syndetics.com/index.aspx?isbn=9780984782857/MC.GIF&client=vancp&type=xw12&oclc=",
            "title": "Cracking the Coding Interview"
        },
        {
            "author": "Pellett, Evan",
            "availability": "Available ",
            "book_link": "/item/show/5272104038",
            "book_type_detail": "Audiobook CD - 2016 | Unabridged",
            "img_src": "https://secure.syndetics.com/index.aspx?isbn=9781504760881/MC.GIF&client=vancp&type=xw12&oclc=",
            "title": "Cracking the Code to A Successful Interview"
        },
        {
            "author": null,
            "availability": "All copies in use",
            "book_link": "/item/show/3900718038",
            "book_type_detail": "Book - 2015",
            "img_src": "https://secure.syndetics.com/index.aspx?isbn=9781608463954/MC.GIF&client=vancp&type=xw12&oclc=",
            "title": "The Breakbeat Poets"
        },
        {
            "author": "Horner, James",
            "availability": "Available ",
            "book_link": "/item/show/975713038",
            "book_type_detail": "Music CD - 2001",
            "img_src": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJsAAADZCAIAAAC4k9W8AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAADFxJREFUeNrsnWlPIk0bhV0HBQQVUVFBRTHOksz//w9+mEwy6rijKCCK4oKgou95uZ...",
            "title": "A Beautiful Mind"
        }
    ],
    "total_result_count": "4"
}