#!/usr/bin/python3
"""
This module contains the views for the Review model.

"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


def get_reviews(place_id):
    """
    Retrieve all reviews for a given place.

    Args:
        place_id: The ID of the place to retrieve reviews for.

    Returns:
        A list of reviews, or an empty list if no reviews are found.

    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


def get_review(review_id):
    """
    Retrieve a single review by ID.

    Args:
        review_id: The ID of the review to retrieve.

    Returns:
        The review, or None if the review is not found.

    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


def delete_review(review_id):
    """
    Delete a review by ID.

    Args:
        review_id: The ID of the review to delete.

    Returns:
        An empty dictionary.

    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({})


def create_review(place_id):
    """
    Create a new review for a given place.

    Args:
        place_id: The ID of the place to create the review for.

    Returns:
        The newly created review, or None if the review could not be created.

    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    user = storage.get('User', request.json['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.json:
        abort(400, 'Missing text')
    review = Review(**request.json)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


def update_review(review_id):
    """
    Update a review by ID.

    Args:
        review_id: The ID of the review to update.

    Returns:
        The updated review, or None if the review could not be updated.

    """
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
