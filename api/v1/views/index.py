#!/usr/bin/python3
""" Api index file """

from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """ Api status output """
    return jsonify({"status": "OK"})
