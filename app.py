from flask import Flask, request, jsonify
#jsonify take data and automatically convert to JSON
from flask_cors import CORS
from scraper import main

app = Flask(__name__)
# CORS(app, origins = ['https://libsearcher.herokuapp.com/'])
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Flask app succeess!"

@app.route('/search/', methods=['GET'])
def get_results():
    library = request.args.get("library")
    search_keywords = request.args.get("search_keywords")

    results = main(library,search_keywords)
    return jsonify(results)

if __name__ == '__main__':
    app.run()

