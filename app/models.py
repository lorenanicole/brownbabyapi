from sqlalchemy import PrimaryKeyConstraint
import time
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % self.username

books_curriculum = db.Table('books_curriculum',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('curricula_id', db.Integer, db.ForeignKey('curriculum.id')),
    PrimaryKeyConstraint('book_id', 'curricula_id')
)

books_keywords = db.Table('books_keywords',
                         db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                         db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id')),
                         PrimaryKeyConstraint('book_id', 'keyword_id')
                         )

class Keyword(db.Model):
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(255), unique=True)

    def __init__(self, keyword):
        self.keyword = keyword

    def to_dict(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            if key == 'publish_date' or key == 'date_entered':
                print str(getattr(self, key))
                result[key] = str(getattr(self, key))
            result[key] = getattr(self, key)

        return result



books_authors = db.Table('books_authors',
                         db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
                         db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),
                         PrimaryKeyConstraint('book_id', 'author_id'))

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            if key == 'publish_date' or key == 'date_entered':
                print str(getattr(self, key))
                result[key] = str(getattr(self, key))
            result[key] = getattr(self, key)

        return result

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    booklists = db.Column(db.String(255), index=True)
    title= db.Column(db.String(255), index=True)
    lexile= db.Column(db.String(255), index=True)
    reading_room= db.Column(db.Boolean)
    dra= db.Column(db.String(255))
    google_book_preview= db.Column(db.String(255))
    age_group= db.Column(db.String(255))
    picture= db.Column(db.String(255))
    date_entered= db.Column(db.Date)
    description= db.Column(db.Text)
    type= db.Column(db.String(255), index=True)
    interest_level = db.Column(db.String(255))
    pages= db.Column(db.String)
    illustrator= db.Column(db.String(255))
    biography_person= db.Column(db.String(255), index=True)
    guided_reading_level= db.Column(db.String(255))
    out_of_print= db.Column(db.Boolean)
    bbr_estore_link= db.Column(db.String(255))
    reading_grade_level= db.Column(db.String(255))
    series= db.Column(db.String(255), index=True)
    publish_date = db.Column(db.Date, index=True) #combo of month, publish_year
    publisher = db.Column(db.String(255), index=True)
    parent_publisher = db.Column(db.String(255), index=True)
    curriculum = db.relationship('Curricula', secondary=books_curriculum, backref=db.backref('books'))
    keywords = db.relationship('Keyword', secondary=books_keywords, backref=db.backref('books'))
    authors = db.relationship('Author', secondary=books_authors, backref=db.backref('books'))

    def __init__(self, data):
        self.booklists = data.get('booklists')
        self.title= data.get('title')
        self.lexile= data.get('lexile')
        self.reading_room = data.get('reading_room', False)
        self.dra= data.get('dra')
        self.google_book_preview= data.get('google_book_preview')
        self.age_group= data.get('age_group')
        self.picture= data.get('picture')
        self.date_entered= data.get('date_entered')
        self.description= data.get('description')
        self.type= data.get('type')
        self.interest_level = data.get('interest_level')
        self.pages= data.get('pages',0)
        self.illustrator= data.get('illustrator')
        self.biography_person= data.get('biography_person')
        self.guided_reading_level= data.get('guided_reading_level')
        self.out_of_print= data.get('out_of_print', False)
        self.bbr_estore_link= data.get('bbr_estore_link')
        self.reading_grade_level= data.get('reading_grade_level')
        self.series= data.get('series')
        self.publish_date = data.get('publish_date') #combo of month, publish_year
        self.parent_publisher = data.get('parent_publisher')
        self.publisher = data.get('publisher')

    def to_dict(self):
        return {'id': self.id,
                'booklists': self.booklists,
                'title': self.title,
                'lexile': self.lexile,
                'reading_room' : self.reading_room,
                'dra': self.dra,
                'google_book_preview':self.google_book_preview,
                'age_group': self.age_group,
                'picture': self.picture,
                'date_entered': str(self.date_entered),
                'description': self.description,
                'type': self.type,
                'interest_level' : self.interest_level,
                'pages': self.pages,
                'illustrator': self.illustrator,
                'biography_person': self.biography_person,
                'guided_reading_level': self.guided_reading_level,
                'out_of_print': self.out_of_print,
                'bbr_estore_link': self.bbr_estore_link,
                'reading_grade_level': self.reading_grade_level,
                'series': self.series,
                'publish_date' : str(self.publish_date), #combo of month, publish_year
                'parent_publisher' : self.parent_publisher,
                'publisher' : self.publisher }


class Curricula(db.Model):
    __tablename__ = 'curriculum'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(255), unique=True) #books.csv.cirriclumn_links, 1, 2, 3

    def __init__(self, link):
        self.link = link

    def to_dict(self):
        result = dict()
        for key in self.__mapper__.c.keys():
            if key == 'publish_date' or key == 'date_entered':
                print str(getattr(self, key))
                result[key] = str(getattr(self, key))
            result[key] = getattr(self, key)

        return result