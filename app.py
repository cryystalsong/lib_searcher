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

    if page is None: 
        results = main(library,search_keywords)
    else: 
        results = main(library,search_keywords,page)

    return jsonify(results)

if __name__ == '__main__':
    app.run()

