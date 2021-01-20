from flask import Flask, request, jsonify
#jsonify take data and automatically convert to JSON
from flask_cors import CORS
from scraper import main

app = Flask(__name__)

api_origin_cors_config = {
    "origins": [
        'https://libsearcher.herokuapp.com'
    ]
}

CORS(app, resources={
        r"/search/*": api_origin_cors_config
    }
)

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

