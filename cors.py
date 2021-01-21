from flask_cors import CORS
import os

def setup(app):
    env_mode = os.environ.get("FLASK_ENV")

    if env_mode == 'development': 
        api_origin_cors_config = {"origins": ['*']}
    else: 
        api_origin_cors_config = {
            "origins": [
                'https://libsearcher.herokuapp.com'
            ]
        }
        

    CORS(app, resources={
            r"/search/*": api_origin_cors_config
        }
    )