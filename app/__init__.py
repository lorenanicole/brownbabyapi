from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config.from_object('config')
app.secret_key = 'this-really-should-be-changed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/brownbabyreads'
db = SQLAlchemy(app)

from app import views, models
