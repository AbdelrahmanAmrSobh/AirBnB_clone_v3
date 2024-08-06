#!/usr/bin/python3
"""Handle for crud operations for amenity"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.get("/amenities")
def amenities():
    """All amenities"""
    return jsonify([storage.all(Amenity).values()])


@app_views.get("/amenities/<amenity_id>")
def getAmenity(amenity_id):
    """get amenity by id if exist"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.delete("/amenities/<amenity_id>")
def deleteAmenity(amenity_id):
    """delete amenity by id if exist"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.post("/amenities")
def createAmenity():
    """create new amenity."""
    amenity = request.get_json(force=True, silent=True)
    if type(amenity) is not dict:
        abort(400, "Not a JSON")
    if "name" in amenity.keys():
        newAmenity = Amenity(amenity)
        storage.new(newAmenity)
        storage.save()
        return jsonify(newAmenity.to_dict(), 201)
    abort(400, "Missing name")


@app_views.put("/amenities/<amenity_id>")
def updateAmenity(amenity_id):
    """update existing amenity."""
    updatedObj = request.get_json(force=True, silent=True)
    obj = storage.get(Amenity, amenity_id)
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
