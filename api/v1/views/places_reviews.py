#!/usr/bin/python3
"""Places reviews restful"""
from api.v1.views import app_views
from flask import jsonify, abort, request, Blueprint
from models.place import Place
from models.review import Review
from models.user import User


reviews = Blueprint('reviews', __name__, url_prefix='/places')

@reviews.route('/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Get reviees from user"""
    place = Place.get(place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@reviews.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Retrieve single review """
    review = Review.get(review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@reviews.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """ Delete single revies """
    review = Review.get(review_id)
    if not review:
        abort(404)
    review.delete()
    return jsonify({})

@reviews.route('/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """ Create a single review """
    place = Place.get(place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if not user_id:
        abort(400, 'Missing user_id')
    user = User.get(user_id)
    if not user:
        abort(404)
    text = data.get('text')
    if not text:
        abort(400, 'Missing text')
    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201

@reviews.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update a single review """
    review = Review.get(review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
