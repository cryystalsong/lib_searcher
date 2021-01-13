from flask import Flask, jsonify
#jsonify take data and automatically convert to JSON

from flask_cors import CORS

from scraper import main

app = Flask(__name__)
CORS(app)

@app.route('/search/<string:library>/<string:search_keywords>', methods=['GET'])
def get_results(library,search_keywords):    
    results = main(library,search_keywords)
    return jsonify(results)

app.run(host='0.0.0.0', port=5000)


