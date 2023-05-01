#!/usr/bin/python3
"""Route handlers for the State entity"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, request, jsonify
from werkzeug.exceptions import BadRequest

cls = State
IGNORE_LIST = ['id', 'updated_at', 'created_at']


def clean(attr_dict, obj):
    """Just makes sure that keys from IGNORE_LIST are not being set"""
    return {k: v for k, v in attr_dict.items() if k not in IGNORE_LIST}


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    """Get all states"""
    obj = storage.all(cls)
    parsed = [v.to_dict() for v in obj.values()]
    return jsonify(parsed), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """create a new state"""
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


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get(state_id):
    """Get a state by ID"""
    obj = storage.get(cls, state_id)
    if obj is None:
        return abort(404)
    return jsonify(obj.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Delete a state"""
    obj = storage.get(cls, state_id)
    if obj is None:
        return abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """Update a state"""
    obj = storage.get(cls, state_id)
    if obj is None:
        return abort(404)
    try:
        body = request.get_json()
        body = clean(body)
        for key, value in body.items():
            print(key in IGNORE_LIST)
            if key in IGNORE_LIST:
                continue
            setattr(obj, key, value)
        obj.save()
    except BadRequest as e:
        abort(400, 'Not a JSON')
    return jsonify(obj.to_dict()), 200
