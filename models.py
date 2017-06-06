from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from passlib.hash import argon2
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(100), unique=True, index=True)
    password = db.Column('password', db.String(100))
    email = db.Column('email', db.String(255), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    cards = db.relationship('cards', backref='owner', lazy='dynamic')

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


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    title = db.Column(db.String(300))
    year = db.Column(db.String(10))
    authors = db.Column(db.String(300))

    keywords = db.Column(db.String(50))

    card_text = db.Column(db.Text)

    registered_on = db.Column(db.DateTime)
    last_edited = db.Column(db.DateTime)

    def __init__(self, title, year, authors, keywords="", card_text=""):
        self.title = title
        self.year = year
        self.authors = authors
        self.keywords = keywords
        self.card_text = card_text
        self.registered_on = datetime.utcnow()
        self.last_edited = datetime.utcnow()
