#!/usr/bin/python3
"""
Flask API app
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(exception):
    from models import storage
    """ Close Storage api """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Error handler """
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
