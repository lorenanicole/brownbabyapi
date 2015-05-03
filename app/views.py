from app import app
from app.models import Book


@app.route('/')
@app.route('/index')
def index():
    return "you are here"

@app.route('/books/<int:id>')
def book(id):
    book = Book.query.filter_by(id=1)
    if book:
        return book.to_dict()
    else:
        return {}

@app.route('/books')
def books():
    return "you asked for all the books"

@app.route('/users')
def users():
    return "you got all the users!"

