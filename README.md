# Bookshelf



## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad Request."
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /books
- General:
    - Returns a list of book objects, success value, total number of books and a success message.
    - Results are paginated according to the `limit` specified in the request query params. The limit defaults to `8` if it is not specified. Include a `page` argument to choose page number, starting from 1.
    - Results can be filtered by passing a `search` argument. The serach argument filters the books by  title and author. The search argument can be omitted.
    - If no argument is passed, the default values will be used.
- Sample: 
  - `curl http://127.0.0.1:5000/books?page=1&limit=5&search=Novel` 

``` {
"books": [
{
"author": "Stephen King",
"id": 1,
"rating": 5,
"title": "The Outsider: A Novel"
},
{
"author": "Lisa Halliday",
"id": 2,
"rating": 4,
"title": "Asymmetry: A Novel"
},
{
"author": "Jojo Moyes",
"id": 5,
"rating": 5,
"title": "Still Me: A Novel"
},
{
"author": "Gina Apostol",
"id": 9,
"rating": 5,
"title": "Insurrecto: A Novel"
}
],
"message": "Books fetched successfully.",
"success": true,
"total_books": 4
}
```

#### POST /books
- General:
    - Creates a new book using the submitted title, author and rating. Returns the id of the created book, success value, and the created book to be used to update the frontend. 
- `curl http://127.0.0.1:5000/books?page=3 -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}'`
```
{
    "success": True,
    "created": book.id,
    "book": {
      "title":"Neverwhere",
      "author":"Neil Gaiman", 
      "rating":"5"
    }
    "message": "Book created successfully.",
}
```
#### DELETE /books/{book_id}
- General:
    - Deletes the book of the given ID if it exists. Returns the  success value, and a message. 
- `curl -X DELETE http://127.0.0.1:5000/books/16?page=2`
```
{
  {
  "success": True,
  "message": "Book with id: 16 has been deleted successfully."
}
}
```
#### PATCH /books/{book_id}
- General:
    - If provided, updates the rating of the specified book. Returns the success value and id of the modified book. 
- `curl http://127.0.0.1:5000/books/15 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
```
{
  "success": True,
  "message": "Book with id: 15 has been updated successfully."
}
```