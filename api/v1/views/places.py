#!/usr/bin/python3
"""Places Routes"""

from flask import abort, jsonify
from api.v1.views import app_views
from models import storage

from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City


@app_views.route(
    '/cities/<city_id>/places', strict_slashes=False, methods=['GET'])
def get_places_in_city(city_id):
    """ retrieves all places in a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = []
    for place in storage.all('Place').values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places)


@ app_views.route('/places/<place_id>', methods=['GET'])
def place(place_id):
    """returns place of id given"""

    from models import storage
    from models.place import Place

    place_found = storage.get(Place, place_id)
    if place_found is None:
        abort(404)

    return jsonify(place_found.to_dict()), 201


@ app_views.route('/cities/<city_id>/places', methods=['POST'])
def post_place(city_id):
    """create a place and link to city"""
    from flask import request
    from models.place import Place
    from models.user import User
    from models.city import City

    http_request = request.get_json(silent=True)
    if http_request is None:
        return 'Not a JSON', 400
    elif 'name' not in http_request.keys():
        return 'Missing name', 400
    elif 'user_id' not in http_request.keys():
        return 'Missing user_id', 400

    if storage.get(User, http_request.user_id) is None or\
            storage.get(City, city_id) is None:
        abort(404)

    new_place = Place(**http_request)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()

    return jsonify(new_place.to_dict()), 201


@ app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """updates given place"""

    from flask import request
    from models.place import Place

    found_place = storage.get(Place, place_id)

    if found_place is None:
        return '', 404

    http_request = request.get_json(silent=True)
    if http_request is None:
        return 'Not a JSON', 400

    for key, values in http_request.items():
        if key not in ['id', 'user_id', 'city_id' 'created_at', 'updated_at']:
            setattr(found_place, key, values)

    storage.save()
    return jsonify(found_place.to_dict()), 201


@ app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """DELETE place if id is found"""

    from models import storage
    from models.place import Place

    place_found = storage.get(Place, place_id)
    if place_found is None:
        return '{}', 404

    storage.delete(place_found)
    storage.save()
    return jsonify({}), 200
