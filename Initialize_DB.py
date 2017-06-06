from flask import Flask, render_template
from flask.ext.login import login_user , logout_user , current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from passlib.hash import argon2
from datetime import datetime


# Initialize Flask app
app = Flask(__name__)
app.config["DEBUG"] = True

# Connect to database 'carddb'
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="dragnerz",
    password="cardemia_db",
    hostname="dragnerz.mysql.pythonanywhere-services.com",
    databasename="dragnerz$carddb",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)

class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column('card_id', db.Integer, primary_key=True)

    owner = db.Column(db.String)

    title = db.Column(db.String(300))
    year = db.Column(db.String(10))
    authors = db.Column(db.String(300))

    keywords = db.Column(db.String(50))

    card_text = db.Column(db.Text)

    registered_on = db.Column(db.DateTime)
    last_edited = db.Column(db.DateTime)

    def __init__(self, owner, title, year, authors, keywords="", card_text=""):
        self.owner = owner
        self.title = title
        self.year = year
        self.authors = authors
        self.keywords = keywords
        self.card_text = card_text
        self.registered_on = datetime.utcnow()
        self.last_edited = datetime.utcnow()

    def check_owner(self):
        return self.owner




class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String, unique=True, index=True)
    password = db.Column('password', db.String)
    email = db.Column('email', db.String, unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email.lower()
        self.registered_on = datetime.utcnow()

    def set_password(self, plaintext):
        self.password = argon2.using(rounds=4).hash(plaintext)

    def check_password(self, plaintext):
        if argon2.verify(plaintext, self.password):
            return True
        return False

@app.route('/')
def hello_world():
    return render_template("main.html")
