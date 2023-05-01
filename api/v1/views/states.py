#!/usr/bin/python3
"""Route handlers for the State entity"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, request, jsonify
from werkzeug.exceptions import BadRequest

cls = State
IGNORE_LIST = ['id', 'updated_at', 'created_at']


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    """Get all states"""
    obj = storage.all(cls)
    parsed = [v.to_dict() for v in obj.values()]
    return jsonify(parsed)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """create a new state"""
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if body.get("name") is None:
        abort(400 "Missing name")
    obj = cls(**body)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get(state_id):
    """Get a state by ID"""
    obj = storage.get(cls, state_id)
    if obj is None:
        abort(404, "Not found")
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(state_id):
    """Delete a state"""
    obj = storage.get(cls, state_id)
    if obj is None:
        abort(404, "Not found")
    obj.delete()
    del obj
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update(state_id):
    """Update a state"""
    obj = storage.get(cls, state_id)
    if obj is None:
        abort(404, "Not found")
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    return jsonify(obj.to_dict()), 200
