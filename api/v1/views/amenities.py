#!/usr/bin/python3
"""Route handlers for the Amenity entity"""

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, request
from werkzeug.exceptions import BadRequest

cls = Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenity():
    """Get all amenities"""
    obj = storage.all(cls)
    return [v.to_dict() for v in obj.values()]


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a new amenity"""
    try:
        body = request.get_json()
        if type(body) is not dict:
            raise BadRequest()
        if 'name' not in body:
            raise KeyError()
        obj = cls(**body)
        obj.save()
        return obj.to_dict(), 201
    except BadRequest as e:
        abort(400, 'Not a JSON')
    except KeyError as e:
        abort(400, 'Missing name')


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Get an amenity by ID"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        return abort(404)
    return obj.to_dict()


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        return abort(404)
    storage.delete(obj)
    storage.save()
    return {}


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an amenity"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        return abort(404)
    try:
        IGNORE_LIST = ['id', 'updated_at', 'created_at']
        body = request.get_json()
        if type(body) is not dict:
            raise BadRequest()
        for key, value in body.items():
            if key in IGNORE_LIST:
                continue
            setattr(obj, key, value)
        obj.save()
    except BadRequest as e:
        abort(400, 'Not a JSON')
    return obj.to_dict()
