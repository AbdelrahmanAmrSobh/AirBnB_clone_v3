#!/usr/bin/python3
"""Handle for crud operations for user"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.get("/users")
def users():
    """All users"""
    return jsonify([storage.all(User).values()])


@app_views.get("/users/<user_id>")
def getUser(user_id):
    """get user by id if exist"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.delete("/users/<user_id>")
def deleteUser(user_id):
    """delete user by id if exist"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({})


@app_views.post("/users")
def createUser():
    """create new user."""
    user = request.get_json(force=True, silent=True)
    if type(user) is not dict:
        abort(400, "Not a JSON")
    if "email" in user.keys() and "password" in user.keys():
        newUser = User(user)
        storage.new(newUser)
        storage.save()
        return jsonify(newUser.to_dict(), 201)
    if "email" not in user.keys():
        abort(400, "Missing email")
    abort(400, "Missing password")


@app_views.put("/users/<user_id>")
def updateUser(user_id):
    """update existing user."""
    updatedObj = request.get_json(force=True, silent=True)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    if type(updatedObj) is not dict:
        abort(400, "Not a JSON")
    for key, value in updatedObj.items():
        if key in ["id", "email", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
