#!/usr/bin/python3
"""Handle for crud operations for place"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.get("/cities/<city_id>/places")
def places(city_id):
    """All places"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify([storage.all(Place).values()])

@app_views.get("/places/<place_id>")
def getPlace(place_id):
    """get place by id if exist"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())

@app_views.delete("/places/<place_id>")
def deletePlace(place_id):
    """delete place by id if exist"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}) # 200 is a default status code

@app_views.post("/cities/<city_id>/places")
def createPlace(city_id):
    """create new place."""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    place = request.get_json(force=True, silent=True)
    if type(place) is not dict:
        abort(400, "Not a JSON")
    if "user_id" not in place.keys():
        abort(400, "Missing user_id")
    if storage.get(User, place.get('user_id')) == None:
        abort(404)
    if "name" in place.keys():
        newPlace = Place(place)
        storage.new(newPlace)
        storage.save()
        return jsonify(newPlace.to_dict(), 201)
    abort(400, "Missing name")

@app_views.put("/places/<place_id>")
def updatePlace(place_id):
    """update existing place."""
    updatedObj = request.get_json(force=True, silent=True)
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if type(updatedObj) is not dict:
        abort(400, "Not a JSON")
    for key, value in updatedObj.items():
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
