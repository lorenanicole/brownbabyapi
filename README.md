##Brown Baby API
Brown Baby API is a Python 2.7 Flask app using SQLAlchemy ORM.

###Virtualenv
Dependencies defined in requirements.txt. To create a virutalenv with dependencies:

```
$ pip install virtualenv
$ virtualenv bbapi
$ source bbapi/bin/activate #activate virtual environment
(bbapi) $ pip install -r /path/to/requirements.txt
```

 ####Setup Postgres Database Locally
 
 ```
 postgres=# create database brownbabyreads;
 postgres=# /connect brownbabyreads
 ```
 
 ####Create Tables
 In root of project:

 ```
 (bbapi) $ python
 >>> from app import db
 >>> from app.models import Book, User
 >>> db.create_all()
 >>> db.session.commit()
 ```

 To confirm tables made locally:
 
 ```
 brownbabyreads-# \dt
 ```