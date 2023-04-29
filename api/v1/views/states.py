#!/usr/bin/python3
""" State module """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Return the list of all State objects """
    states_list = []
    for state in storage.all(State).values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id=None):
    """ Return a state object """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """ Delete a state object """
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    state = State(**request.json)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """ Update a State object """
    state = storage.get(State, state_id)
    if state:
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        for key, value in body.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
