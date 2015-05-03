import datetime
from flask import jsonify, request
from sqlalchemy import cast, DATE, extract, and_
from app import app, db
from app.models import Book, Curricula, Keyword, Author


@app.route('/')
@app.route('/index')
def index():
    return "you are here"

@app.route('/books/<int:book_id>')
def book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        return jsonify({'data': book.to_dict()})
    else:
        return jsonify({'data': None })

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book:
        try:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'data': 'Success'})
        except Exception as e:
            return jsonify({'data': 'Error'})
    else:
        return jsonify({'data': None })

@app.route('/books/<int:book_id>', methods=['POST'])
def edit_book(book_id):
    book = db.session.query(Book).filter_by(id=book_id)
    if book:
        print request.form
        try:
            book.update(request.form)
            db.session.commit()
            return jsonify({'data': 'Success'})
        except Exception as e:
            return jsonify({'data': 'Error'})
    else:
        return jsonify({'data': None })

@app.route('/books')
def books():
    page = int(request.args.get('page'))
    if page:
        page_size = int(request.args.get('page_size', 48))
        query = db.session.query(Book)
        result = query.order_by(Book.id).limit(page_size).offset(page * page_size)
        result = [book.to_dict() for book in result]
        return jsonify({'data': result})

    books = Book.query.all()
    books = [book.to_dict() for book in books]

    return jsonify({'data': books})

@app.route('/users')
def users():
    return "you got all the users!"

@app.route('/curriculum')
def curriculum():
    curriculum = Curricula.query.all()
    curriculum = [curricula.to_dict() for curricula in curriculum if curricula.link]
    return jsonify({'data': curriculum})

@app.route('/curriculum/<int:curricula_id>')
def curricula(curricula_id):
    curricula = Curricula.query.filter_by(id=curricula_id).first()
    if curricula:
        return jsonify({'data': curricula.to_dict()})
    else:
        return jsonify({'data': None })

@app.route('/curriculum/<int:curricula_id>/books')
def curricula_books(curricula_id):
    curricula = Curricula.query.filter_by(id=curricula_id).first()
    books = [book.to_dict() for book in curricula.books]
    if books:
        return jsonify({'data': books})
    else:
        return jsonify({'data': None })

@app.route('/keywords')
def keywords():
    keywords = Keyword.query.all()
    keywords = [keyword.to_dict() for keyword in keywords if keyword.keyword]

    if keywords:
        return jsonify({'data': keywords})
    else:
        return jsonify({'data': None })

@app.route('/keywords/<int:keyword_id>')
def keyword(keyword_id):
    keyword = Keyword.query.filter_by(id=keyword_id).first()
    return jsonify({'data': keyword.to_dict()})

@app.route('/books/<int:book_id>/keywords')
def book_keyword(book_id):
    book = Book.query.filter_by(id=book_id).first()
    keywords = [keyword.to_dict() for keyword in book.keywords]

    if keywords:
        return jsonify({'data': keywords})
    else:
        return jsonify({'data': None })

@app.route('/keywords/<int:keyword_id>/books')
def keyword_book(keyword_id):
    keyword = Keyword.query.filter_by(id=keyword_id).first()
    books = [book.to_dict() for book in keyword.books]

    if books:
        return jsonify({'data': books})
    else:
        return jsonify({'data': None })

@app.route('/search', methods=['POST'])
def books_search():
    book_titles = []
    book_illustrators = []
    book_lexile = []
    book_type = []
    book_age_group = []
    book_series = []
    book_authors = []
    book_keywords = []
    query_params = request.form
    if query_params.get('title') in query_params.values():
        book_titles = Book.query.filter_by(title=query_params.get('title')).all()
    if query_params.get('author') in query_params.values():
        author = Author.query.filter_by(name=query_params.get('author')).first()
        book_authors = author.books
    if query_params.get('illustrator') in query_params.values():
        book_illustrators = Book.query.filter_by(illustrator=query_params.get('illustrator')).all()
    if query_params.get('keyword') in query_params.values():
        keyword = Keyword.query.filter_by(keyword=query_params.get('keyword')).first()
        book_keywords = keyword.books
    if query_params.get('lexile') in query_params.values():
        book_lexile = Book.query.filter_by(lexile=query_params.get('lexile')).all()
    if query_params.get('type') in query_params.values():
        book_type = Book.query.filter_by(type=query_params.get('type')).all()
    if query_params.get('age_group') in query_params.values():
        book_age_group = Book.query.filter_by(age_group=query_params.get('age_group')).all()
    if query_params.get('series') in query_params.values():
        book_series = Book.query.filter_by(series=query_params.get('series')).all()
    # if query_params.get('year_published') in query_params:
        # year = datetime.datetime.strptime(query_params.get('year_published'),"%m/%d/%Y").date().year()
        # book_keywords = db.session.query(Book).filter(and_(Book.publish_date <= '%s-12-31' % year, Book.publish_date >= '%s-01-01' % year))

    all_results = book_titles + book_authors + book_illustrators + book_keywords + book_lexile + book_type + book_age_group + book_series
    all_results = set(all_results)

    results = []
    for item in all_results:
        results.append(item.to_dict())

    if len(results) >= 48:
        results = results[0:48]

    return jsonify({'data':results})

@app.route('/books/<int:book_id>/curriculum')
def book_curriculm(book_id):
    book = Book.query.filter_by(id=book_id).first()
    curriculum = [curricula.to_dict() for curricula in book.curriculum]

    if curriculum:
        return jsonify({'data': curriculum})
    else:
        return jsonify({'data': None })


