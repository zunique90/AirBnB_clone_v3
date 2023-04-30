#!/usr/bin/python3
"""This files contains all routes definitions"""

from api.v1.views import app_views


@app_views.route('/status')
def status():
    """Returns the status of the API"""
    return {"status": "OK"}
