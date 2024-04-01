#!/usr/bin/python3
""" Blueprint for the views """

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """"
    Endpoint that retrieves the number of each objects by type
    """
    from models import storage
    from models.state import State
    from models.city import City
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review
    from models.user import User
    from models.base_model import BaseModel

    return jsonify({
        "states": storage.count(State),
        "cities": storage.count(City),
        "amenities": storage.count(Amenity),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "users": storage.count(User)
    })
