from flask import Flask, render_template
from flask.ext.login import login_user , logout_user , current_user , login_required
from flask.ext.sqlalchemy import SQLAlchemy

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
    title = db.Column(db.String(60))
    text = db.Column(db.String(500))
    pub_date = db.Column(db.DateTime)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    password = db.Column('password', db.String(10))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

