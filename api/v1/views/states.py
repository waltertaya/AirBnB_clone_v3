#!/usr/bin/python3
""" Create a new view for State objects that
 handles all default RestFul API actions """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request
from flask import jsonify


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Retrieves the list of all State objects """
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)
    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ Creates a State """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}, 400)
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}, 400)
    new_state = State(**request.get_json())
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ Updates a State object """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}, 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
