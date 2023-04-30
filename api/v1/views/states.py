#!/usr/bin/python3
"""Route handlers for the State entity"""

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import abort, request
from werkzeug.exceptions import BadRequest


@app_views.route('/states', methods=['GET', 'POST'])
def get_all_states():
    """
    if request method is POST, create a new state object
    else get all states
    """
    obj = storage.all(State)
    if request.method == 'POST':
        try:
            body = request.get_json()
            if 'name' not in body:
                raise KeyError()
            state = State(**body)
            state.save()
            return state.to_dict()
        except BadRequest as e:
            abort(400, 'Not a JSON')
        except KeyError as e:
            abort(400, 'Missing name')
    return [v.to_dict() for v in obj.values()]


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def get_state_by_id(state_id):
    """
    if request method is DELETE, then deletes the state by state_id
    Else get a state by id
    """
    obj = storage.get(State, state_id)
    if obj is None:
        return abort(404)
    if request.method == 'DELETE':
        storage.delete(obj)
        storage.save()
        return {}
    return obj.to_dict()
