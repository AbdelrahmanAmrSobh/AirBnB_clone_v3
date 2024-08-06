#!/usr/bin/python3
"""Handle for crud operations for state"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.get("/states")
def states():
    """All states"""
    return jsonify([storage.all(State).values()])


@app_views.get("/states/<state_id>")
def getState(state_id):
    """get state by id if exist"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.delete("/states/<state_id>")
def deleteState(state_id):
    """delete state by id if exist"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.post("/states")
def createState():
    """create new state."""
    state = request.get_json(force=True, silent=True)
    if type(state) is not dict:
        abort(400, "Not a JSON")
    if "name" in state.keys():
        newState = State(state)
        storage.new(newState)
        storage.save()
        return jsonify(newState.to_dict(), 201)
    abort(400, "Missing name")


@app_views.put("/states/<state_id>")
def updateState(state_id):
    """update existing state."""
    updatedObj = request.get_json(force=True, silent=True)
    obj = storage.get(State, state_id)
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
