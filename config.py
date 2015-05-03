import os

class Config(object):
    DEBUG = True
    # TESTING = False
    # CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost/brownbabyreads" #os.environ['DATABASE_URL']
