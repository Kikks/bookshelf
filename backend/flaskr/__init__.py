import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

DEFAULT_BOOKS_LIMIT = 8


def paginate_books(page, limit, selection):
    start = (page - 1) * limit
    end = start + limit

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books


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
        limit = request.args.get("limit", DEFAULT_BOOKS_LIMIT, type=int)
        books = Book.query.order_by(Book.id).all()
        paginated_books = paginate_books(page, limit, books)

        if len(paginated_books) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "message": "Books fetched successfully.",
                "books": paginated_books,
                "total_books": len(books),
            }
        )

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if not book:
                abort(404)

            book.delete()

            return jsonify(
                {
                    "success": True,
                    "message": "Book with id: {} deleted successfully.".format(book_id),
                }
            )
        except:
            abort(422)

    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            body = request.get_json()

            rating = body.get("rating", None)

            if not book:
                abort(400)

            if not rating:
                abort(400)

            book.rating = int(rating)
            book.update()

            return jsonify(
                {
                    "success": True,
                    "message": "Book with id: {} updated successfully.".format(book_id),
                }
            )
        except:
            abort(400)

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

            return jsonify(
                {
                    "success": True,
                    "created": book.id,
                    "message": "Book created successfully.",
                }
            )
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found."}), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad Request."}), 400

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Server error."}),
            500,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable."}),
            422,
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405, "message": "Method not allowed."}),
            405,
        )

    return app
