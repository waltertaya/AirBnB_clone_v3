#!/usr/bin/python3
""" Create a new view for City objects that
 handles all default RestFul API actions """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import request
from flask import jsonify


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)
    cities = state.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}, 404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}, 404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """ Creates a City """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}, 404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}, 400)
    if 'name' not in request.get_json():
        return jsonify({"error": "Missing name"}, 400)
    new_city = City(**request.get_json())
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}, 404)
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}, 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
