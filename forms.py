from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError, PasswordField

from models import db, Users


class ContactForm(Form):
    # Basically, this is instead of putting input forms in HTML
    name = StringField("name",  [validators.DataRequired('Please enter your name.')])
    email = StringField("Email",  [validators.DataRequired('Please enter your email address'), validators.Email('Please enter your email address')])
    subject = StringField("Subject",  [validators.DataRequired('Please enter a subject')])
    message = TextAreaField("Message",  [validators.DataRequired('Please enter a message')])
    submit = SubmitField("Send")


class SignupForm(Form):
    username = StringField("Username", [validators.DataRequired("Please enter your username.")])
    email = StringField("Email", [validators.DataRequired("Please enter your email address."),
                                validators.Email("Please enter a valid email address.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
    submit = SubmitField("Create account")


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired("Please enter your username.")])
    password = PasswordField('Password', [validators.DataRequired("Please enter your password.")])
    submit = SubmitField("Sign In")


class CardCreateForm(Form):
    title = StringField('Title', [validators.DataRequired("Please enter the title.")])
    year = StringField('Year', [validators.DataRequired("Please enter the publish year.")])
    authors = StringField('Authors', [validators.DataRequired("Please enter at least one author.")])
    submit = SubmitField("Create")


class ViewEditCard(Form):
    text = TextAreaField('Text')
    submit = SubmitField("Save")
