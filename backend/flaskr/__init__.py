import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/books")
    def get_books():
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * BOOKS_PER_SHELF
        end = start + BOOKS_PER_SHELF

        books = [book.format() for book in Book.query.order_by(Book.id.desc()).all()]

        return jsonify(
            {"success": True, "books": books[start:end], "total_books": len(books)}
        )

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        book = Book.query.filter(Book.id == book_id).one_or_none()

        if not book:
            abort(400)

        book.delete()

        return jsonify({"success": True})

    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            body = request.get_json()

            rating = body.get("rating", None)

            if not book:
                abort(400)

            if rating:
                book.rating = rating
                book.update()

            return jsonify({"success": True})
        except:
            abort(500)

    @app.route("/books", methods=["POST"])
    def create_book():
        body = request.get_json()

        title = body.get("title", None)
        author = body.get("author", None)
        rating = body.get("rating", None)

        try:
            book = Book(
                title=title,
                author=author,
                rating=rating,
            )

            book.insert()

            return jsonify({"success": True, "created": book.id})
        except:
            abort(422)

    return app