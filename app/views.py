from flask import request
from app import app, db
from app.models import Book, Curricula, Keyword, Author, Article
from flask.ext.jsonpify import jsonify
import requests
import json


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

@app.route('/books/create', methods=['POST'])
def create_book():

    book = Book.query.filter_by(title=request.form.get('title'))
    if book:
        return jsonify({'data': 'Error, already exists'})

    book = Book(request.form)
    keywords = request.form.get('keywords')
    if keywords:
        for keyword in keywords.split(','):
            k = Keyword.query.filter_by(keyword=keyword)
            if not k:
                k = Keyword(keyword.strip())
            book.keywords.append(k)
    authors = request.form.get('authors')
    if authors:
        for author in authors.split(','):
            a = Author.query.filter_by(name=author)
            if not a:
                a = Author(author.strip())
            book.authors.append(a)
    curriculum = request.form.get('curriculum')
    if curriculum:
        for curricula in curriculum.split(','):
            c = Curricula.query.filter_by(link=curricula)
            if not c:
                c = Curricula(curricula.strip())
            book.curriculum.append(c)
    try:
        db.session.add(book)
        db.session.commit()
        return jsonify({'data': 'Success'})
    except Exception as e:
            return jsonify({'data': 'Error'})


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

@app.route('/books/<int:book_id>/authors')
def book_authors(book_id):
    book = Book.query.filter_by(id=book_id).first()
    authors = [authors.to_dict() for authors in book.authors]

    if authors:
        return jsonify({'data': authors})
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

@app.route('/articles')
def articles():
    articles = Article.query.all()
    articles = [article.to_dict() for article in articles]

    if articles:
        return jsonify({'data': articles})
    else:
        return jsonify({'data': None })

@app.route('/articles/<int:article_id>')
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()

    if article:
        return jsonify({'data': article.to_dict()})
    else:
        return jsonify({'data': None })

@app.route('/articles/create', methods=['POST'])
def create_article():
    article = Article.query.filter_by(title=request.form.get('title'))
    if article:
        return jsonify({'data': 'Error, already exists'})

    article = Article(request.form)

    try:
        db.session.add(article)
        db.session.commit()
        return jsonify({'data': 'Success'})
    except Exception as e:
            return jsonify({'data': 'Error'})
            
@app.route('/constant_contact/create', methods=['POST'])
def create_constant_contact():
    email_address_to_add = request.form.get("email")
    url = "https://api.constantcontact.com/v2/contacts?email=%s&api_key=vw6uf3x79ww5txvgffrfss8f&access_token=28bca3b8-4991-45d5-8ea6-ff28960f873c" % email_address_to_add
    constant_contact_response = requests.get(url)
    response_dict = json.loads(constant_contact_response.content)

    if response_dict.get('results'):
        response = constant_contact_response
        print "The user already exists"
    else:
        print "Creating a new user"
        print request.form
        parameters_dict = request.form
        create_contact_url = "https://api.constantcontact.com/vetr2/contacts?api_key=vw6uf3x79ww5txvgffrfss8f&access_token=28bca3b8-4991-45d5-8ea6-ff28960f873c"
        response = requests.post(create_contact_url, data=parameters_dict)

    return jsonify(response)
