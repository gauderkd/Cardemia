from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class Card(db.Model):
    __tablename__ = 'cards'
    id = db.Column('card_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String(500))
    pub_date = db.Column(db.DateTime)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(16))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.set_password(password)
        self.email = email.lower()
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


