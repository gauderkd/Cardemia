from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, current_user

from forms import ContactForm, SignupForm, loginForm


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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Users
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

@login_manager.user_loader
def load_user(userid):
    return Users.query.filter(Users.id == userid).first()



@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/cards')
def cards():
    return render_template("cards.html")


@app.route('signin', methods=["GET", "POST"])
def signin():
    form = loginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first_or_404()
        if user.check_passowrd(form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            return redirect(url_for('signin'))

    return render_template("signin.html", form=form)


@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('signup'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
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
        return redirect(url_for('signin'))
    else:
        return render_template('profile.html')


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



