import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_books(self):
        res = self.client().get("/books")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))

    def test_404_sent_when_requesting_beyond_valid_pages(self):
        res = self.client().get("/books?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_books_returned_less_than_or_equal_to_limit(self):
        limit = 5
        res = self.client().get("/books?page=1&limit={}".format(limit))
        data = json.loads(res.data)

        self.assertLessEqual(len(data["books"]), limit)

    def test_update_book_rating(self):
        rating = 2
        bookId = 1

        res = self.client().patch("/books/{}".format(bookId), json={"rating": rating})
        book = Book.query.filter(Book.id == bookId).one_or_none()

        if book:
            self.assertTrue(book.format())
            self.assertEqual(book.format()["rating"], rating)
        else:
            self.fail("No book with id: {} exists.".format(bookId))

    def test_delete_book(self):
        bookId = 2
        existingBook = Book.query.filter(Book.id == bookId).one_or_none()

        if not existingBook:
            self.fail("No book with id: {} exists initially.".format(bookId))

        res = self.client().delete("/books/{}".format(bookId))
        data = json.loads(res.data)

        deleted_book = Book.query.filter(Book.id == bookId).one_or_none()

        self.assertEqual(deleted_book, None)

    def test_create_book(self):
        res = self.client().post("/books", json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])

        created_book = Book.query.filter(
            Book.title == self.new_book["title"],
            Book.rating == self.new_book["rating"],
            Book.author == self.new_book["author"],
        ).one_or_none()

        if not created_book:
            self.fail("New book was not created.")

        self.assertTrue(created_book.format())


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
