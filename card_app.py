from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.bcrypt import Bcrypt
from flask_login import UserMixin
from passlib.hash import argon2

from forms import ContactForm, SignupForm, LoginForm


# Initialize Flask app
app = Flask(__name__)
bcrypt = Bcrypt(app)

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Users
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"


@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return Users.query.get(user_id)


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
@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/cards')
def cards():
    return render_template("cards.html")


@app.route('/signin', methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        return 'You are already logged in'

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            return 'user doesnt exist'
        elif user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('profile'))
        else:
            return 'password incorrect'

    return render_template("signin.html", form=form)


@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit() and (form.validate() is True):
        newuser = Users(username=form.username.data, password=form.password.data, email=form.email.data)
        db.session.add(newuser)
        db.session.commit()
        login_user(newuser)

        return redirect(url_for('profile'))

    else:
        return render_template('signup.html', form=form)


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html')
    else:
        return redirect(url_for('signin'))


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
