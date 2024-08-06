#!/usr/bin/python3
"""Handle for crud operations for place_amenity"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User

@app_views.get("/places/<place_id>/amenities")
def amenitiesOfPlace(place_id):
    """All amenities of a place."""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    amenitiesOfPlace = []
    amenities = storage.all(Amenity)
    for amenity in amenities:
        if amenity.place_id == place_id:
            amenitiesOfPlace.append(amenity)
    return jsonify(amenitiesOfPlace)

@app_views.delete("/places/<place_id>/amenities/<amenity_id>")
def deleteAmenityOfPlace(place_id, amenity_id):
    """delete amenity of a place if exist"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity.place_id != place_id:
        abort(404)
    if storage_t == "db":
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({})

@app_views.post("/places/<place_id>/amenities/<amenity_id>")
def createAmenityOfPlace(place_id, amenity_id):
    """create amenity and link it to a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity.place_id == place_id:
        return jsonify(amenity.to_dict())
    setattr(amenity, "place_id", place_id)
    storage.save()
    return jsonify(amenity.to_dict(), 201)
