#!/usr/bin/python3
"""Route handlers for the City entity"""

from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import abort, request, jsonify
from werkzeug.exceptions import BadRequest

cls = City
IGNORE_LIST = ['id', 'state_id', 'updated_at', 'created_at']


def clean(attr_dict):
    """Just makes sure that keys from IGNORE_LIST are not being set"""
    return {k: v for k,v in attr_dict.items() if k not in IGNORE_LIST}



def state_exists(state_id):
    """
    Checks if state exists
    """
    return storage.get(State, state_id) is not None


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_all_city(state_id):
    """Gets all cities"""
    if not state_exists(state_id):
        return abort(404)
    obj = storage.get(State, state_id)
    return jsonify([v.to_dict() for v in obj.cities]), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city"""
    if not state_exists(state_id):
        return abort(404)
    try:
        body = request.get_json()
        if type(body) is not dict:
            raise BadRequest()
        if 'name' not in body:
            raise KeyError()
        body = clean(body)
        obj = cls(**body)
        obj.state_id = state_id
        obj.save()
        return jsonify(obj.to_dict()), 201
    except BadRequest as e:
        abort(400, 'Not a JSON')
    except KeyError as e:
        abort(400, 'Missing name')


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Get a city by ID"""
    obj = storage.get(cls, city_id)
    if obj is None:
        return abort(404)
    return jsonify(obj.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Delete a city"""
    obj = storage.get(cls, city_id)
    if obj is None:
        return abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city"""
    obj = storage.get(cls, city_id)
    if obj is None:
        return abort(404)
    try:
        body = request.get_json()
        if type(body) is not dict:
            raise BadRequest()
        body = clean(body)
        for key, value in body.items():
            setattr(obj, key, value)
        obj.save()
    except BadRequest as e:
        abort(400, 'Not a JSON')
    return jsonify(obj.to_dict()), 200
