#!/usr/bin/python3
"""Route handlers for the Amenity entity"""

from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import abort, request, jsonify
from werkzeug.exceptions import BadRequest

cls = Amenity
IGNORE_LIST = ['id', 'updated_at', 'created_at']


def clean(attr_dict):
    """Just makes sure that keys from IGNORE_LIST are not being set"""
    return {k: v for k, v in attr_dict.items() if k not in IGNORE_LIST}


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenity():
    """Get all amenities"""
    obj = storage.all(cls)
    return jsonify([v.to_dict() for v in obj.values()]), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a new amenity"""
    try:
        body = request.get_json()
        body = clean(body)
        if type(body) is not dict:
            raise BadRequest()
        if 'name' not in body:
            raise KeyError()
        obj = cls(**body)
        obj.save()
        return jsonify(obj.to_dict()), 201
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
    return jsonify(obj.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity"""
    obj = storage.get(cls, amenity_id)
    if obj is None:
        return abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


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
        body = clean(body)
        if type(body) is not dict:
            raise BadRequest()
        for key, value in body.items():
            setattr(obj, key, value)
        obj.save()
    except BadRequest as e:
        abort(400, 'Not a JSON')
    return jsonify(obj.to_dict()), 200
