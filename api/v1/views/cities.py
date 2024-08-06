#!/usr/bin/python3
"""Handle for crud operations for city"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.get("/states/<state_id>/cities")
def getCitiesOfState(state_id):
    """get cities by state_id if exist"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    citiesOfState = []
    cities = storage.all(cities).values()
    for city in cities:
        if city.state_id == state_id:
            citiesOfState.append(city)
    return jsonify(citiesOfState)

@app_views.get("/cities/<city_id>")
def getCity(city_id):
    """get city by id if exist"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj)

@app_views.delete("/cities/<city_id>")
def deleteCity(city_id):
    """delete city if exist"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})

@app_views.post("/states/<state_id>/cities")
def createCityOfState(state_id):
    """create a new city of a state."""
    city = request.get_json(force=True, silent=True)
    exist = storage.get(State, state_id)
    if exist is None:
        abort(404)
    if type(city) is not dict:
        abort(400, "Not a JSON")
    if "name" in city.keys():
        newCity = State(city)
        storage.new(newCity)
        storage.save()
        return jsonify(newCity.to_dict(), 201)
    abort(400, "Missing name")

@app_views.put("/cities/<city_id>")
def updateCity(city_id):
    """update existing city."""
    updatedObj = request.get_json(force=True, silent=True)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    if type(updatedObj) is not dict:
        abort(400, "Not a JSON")
    for key, value in updatedObj.items():
        if key == "id" or key == "created_at" or key == "updated_at":
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
