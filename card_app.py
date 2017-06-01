from flask import Flask, render_template, request, flash
from forms import ContactForm, SignupForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

# Initialize Flask app
app = Flask(__name__)

app.secret_key = 'key to the heart'

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
    password = db.Column('password', db.String(16))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.set_passwrd(password)
        self.email = email.lower()
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/cards')
def cards():
    return render_template("cards.html")


@app.route('/signin')
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST':
        if form.validate() == False:
            return render_template('signup.html', form=form)
        else:
            return "[1] Create a new user [2] sign in the user [3] redirect to the user's profile"

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            return 'Sorry, not functional at this time'

        return
    elif request.method == 'GET':
        return render_template('contact.html', form=form)
    # request determines if current http method is get or post



