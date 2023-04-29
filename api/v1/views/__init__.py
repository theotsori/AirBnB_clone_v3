#!/usr/bin/python3
""" The api blueprint """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='api/v1')
