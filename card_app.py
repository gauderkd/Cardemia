from flask import Flask, render_template, request, flash, session, url_for, redirect

from forms import ContactForm, SignupForm


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

from models import db, Users


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
            newuser = Users(form.username.data, form.password.data, form.email.data)
            db.session.add(newuser)
            db.session.commit()

            session['email'] = newuser.email
            return redirect(url_for('profile'))

    elif request.method == 'GET':
        return render_template('signup.html', form=form)


@app.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('signin'))

    user = Users.query.filter_by(email=session['email']).first()

    if user is None:
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



