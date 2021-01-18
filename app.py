from flask import Flask, request, jsonify
#jsonify take data and automatically convert to JSON

from scraper import main

app = Flask(__name__)

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

