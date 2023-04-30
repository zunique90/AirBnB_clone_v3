#!/usr/bin/python3
"""Route handlers for the State entity"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, request


@app_views.route('/states')
def get_all_states():
    """get all states"""
    obj = storage.all(State)
    return [v.to_dict() for v in obj.values()]


@app_views.route('/states/<state_id>', methods = ['GET', 'DELETE'])
def get_state_by_id(state_id):
    """
    if request method is DELETE, then deletes the state by state_id
    Else get a state by id
    """
    obj = storage.get(State, state_id)
    if (obj == None):
        return abort(404)
    if request.method == 'DELETE':
        storage.delete(obj)
        storage.save()
        return {}
    return obj.to_dict()
