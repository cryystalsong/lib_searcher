from flask import Flask, request, jsonify
#jsonify take data and automatically convert to JSON
from scraper import main
import cors

app = Flask(__name__)
cors.setup(app)

@app.route('/')
def home():
    return "Flask app succeess!"

@app.route('/search/', methods=['GET'])
def get_results():
    library = request.args.get("library")
    search_keywords = request.args.get("search_keywords")
    page = request.args.get("page")

    if library == "" or library is None:
        results = {
            "error": "cannot execute search without library input"
        } 
        return jsonify(results)
    
    if search_keywords == "" or search_keywords is None:
        results = {
            "error": "cannot execute search without search keywords"
        } 
        return jsonify(results)

    try:
        if page is None: 
            results = main(library,search_keywords)
        else: 
            results = main(library,search_keywords,page)
    
    except Exception as e:
        results = {
            "error": str(e)
        } 

    return jsonify(results)
if __name__ == '__main__':
    app.run()

