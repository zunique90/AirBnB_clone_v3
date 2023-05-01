#!/usr/bin/python3
"""Route handlers for the City entity"""

from api.v1.views import app_views
from models.city import City
from models import storage
from flask import abort, request
from werkzeug.exceptions import BadRequest

cls = City


@app_views.route('/cities', methods=['GET'])
def get_all_city():
    """Gets all cities"""
    obj = storage.all(cls)
    return [v.to_dict() for v in obj.values()]


@app_views.route('/cities', methods=['POST'])
def create_city():
    """create a new city"""
    try:
        body = request.get_json()
        if 'name' not in body:
            raise KeyError()
        obj = cls(**body)
        obj.save()
        return obj.to_dict(), 201
    except BadRequest as e:
        abort(400, 'Not a JSON')
    except KeyError as e:
        abort(400, 'Missing name')


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Get a city by ID"""
    obj = storage.get(cls, city_id)
    if obj is None:
        return abort(404)
    return obj.to_dict()


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a city"""
    obj = storage.get(cls, city_id)
    if obj is None:
        return abort(404)
    storage.delete(obj)
    storage.save()
    return {}


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a city"""
    obj = storage.get(cls, city_id)
    if obj is None:
        return abort(404)
    try:
        IGNORE_LIST = ['id', 'updated_at', 'created_at']
        body = request.get_json()
        for key, value in body.items():
            if key in IGNORE_LIST:
                continue
            setattr(obj, key, value)
        obj.save()
    except BadRequest as e:
        abort(400, 'Not a JSON')
    return obj.to_dict()
