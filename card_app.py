from flask import Flask, render_template, request, flash, session, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from forms import *
from config import *

from models import db, Users, Card
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


@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/cards')
def cards():
    if current_user.is_authenticated:
        user_cards = Card.query.filter(Card.owner == current_user)
        return render_template("cards.html", cards=user_cards)
    else:
        flash('Please sign in to make cards')
        return redirect(url_for('signin'))


@app.route('/signin', methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        flash('You are already logged in!')
        return redirect(url_for('main'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None:
            flash('username doesnt exist')
        elif user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('profile'))
        else:
            flash('password incorrect')
    return render_template("signin.html", form=form)


@app.route('/signout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('main'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        mail_check = Users.query.filter_by(email=form.email.data.lower()).first()
        user_check = Users.query.filter_by(username=form.username.data).first()

        if mail_check is None and user_check is None:
            newuser = Users(username=form.username.data, password=form.password.data, email=form.email.data)
            db.session.add(newuser)
            db.session.commit()
            login_user(newuser)
            return redirect(url_for('profile'))

        elif user_check is not None:
            flash('Username is taken!')
        elif mail_check is not None:
            flash('Email is already registered!')
        else:
            flash('Sorry, an error has occurred')
    return render_template('signup.html', form=form)


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        user_cards = Card.query.filter(Card.owner == current_user)
        card_count = 0
        for i in user_cards:
            card_count += 1
        return render_template('profile.html', cards=user_cards, card_num=card_count)
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

@app.route('/createcard', methods=["GET", "POST"])
def createcard():
    form = CardCreateForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            newcard = Card(owner=current_user, title=form.title.data, year=form.year.data, authors=form.authors.data)
            db.session.add(newcard)
            db.session.commit()
            flash('card successfully created!')
            return redirect(url_for('createcard'))
    else:
        flash('Sorry, you have to make an account first.')

    return render_template("createcard.html", form=form)

@app.route('/viewcard/<path:variable>', methods=['GET', "POST"])
def viewcard(variable):
    if current_user.is_authenticated:
        form = ViewEditCard()
        try:
            this_card = Card.query.filter(Card.id == variable, Card.owner == current_user).first()
            if request.method == 'POST':
                this_card.edit_text(form.text.data)
                db.session.commit()
            form.text.data = this_card.card_text
            flash('Text Saved!')
            return render_template("viewcard.html", card=this_card, form=form)
        except:
            flash('Sorry, something went wrong')
            return redirect(url_for('main'))
    else:
        flash('Please sign in to make and view cards')
        return redirect(url_for('signin'))
