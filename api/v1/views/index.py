#!/usr/bin/python3
""" Api index file """

from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """ Api status output """
    return jsonify({"status": "OK"})
