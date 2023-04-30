#!/usr/bin/python3
"""
Object thats handles all default RESTFul API actions for states
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
"""from flasgger.utils import swag_from"""


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """
    Retrieve the list of all State objects
    """
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State """
    if not request.get__json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get__json():
        abort(400, description="Missing name")

    data = request.get__json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Update a State """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.__json():
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'created_at', 'updated_at']

    data = request.json()
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
