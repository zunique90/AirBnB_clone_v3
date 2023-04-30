#!/usr/bin/python3
"""Route handlers for the State entity"""

from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states')
def get_all_states():
    obj = storage.all(State)
    return [v.to_dict() for v in obj.values()]
