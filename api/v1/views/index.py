#!/usr/bin/python3
""" Api index file """

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    """ Api status output """
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats', methods=['GET'])
def stats():
    """ Retrieves the number of each object by type """
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("Cities"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
