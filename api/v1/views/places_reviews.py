#!/usr/bin/python3
"""Handle for crud operations for place_review"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

@app_views.get("/places/<place_id>/reviews")
def reviewsOfPlace(place_id):
    """All reviews of a place"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    reviews = storage.all(Review)
    placeReviews = []
    for review in reviews:
        if review.place_id == place_id:
            placeReviews.append(review)
    return jsonify(placeReviews)

@app_views.get("/reviews/<review_id>")
def getReview(review_id):
    """get review by id if exist"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())

@app_views.delete("/reviews/<review_id>")
def deleteReview(review_id):
    """delete review by id if exist"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}) # 200 is a default status code

@app_views.post("/places/<place_id>/reviews")
def createReview(place_id):
    """create new review."""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    review = request.get_json(force=True, silent=True)
    if type(review) is not dict:
        abort(400, "Not a JSON")
    if "user_id" not in review.keys():
        abort(400, "Missing user_id")
    if storage.get(User, review.get('user_id')) == None:
        abort(404)
    if "text" in review.keys():
        newReview = Review(review)
        storage.new(newReview)
        storage.save()
        return jsonify(newReview.to_dict(), 201)
    abort(400, "Missing text")

@app_views.put("/reviews/<review_id>")
def updateReview(review_id):
    """update existing review."""
    updatedObj = request.get_json(force=True, silent=True)
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    if type(updatedObj) is not dict:
        abort(400, "Not a JSON")
    for key, value in updatedObj.items():
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
