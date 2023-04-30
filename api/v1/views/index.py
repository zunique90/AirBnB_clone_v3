#!/usr/bin/python3
"""This files contains all routes definitions"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity

@app_views.route('/status')
def status():
    """Returns the status of the API"""
    return {"status": "OK"}


@app_views.route('/stats')
def stats():
    """Return number of each objects in storage"""
    objs = storage.all()
    print(objs)
    obj = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return obj
