#!/usr/bin/python3
"""The start up script for our API server"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up(exception):
    """Closes the database connection before teardown"""
    storage.close()

@app.errorhandler(404)
def notFound(error):
    """returns a JSON-formatted 404 status code response"""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, debug=True, threaded=True)
