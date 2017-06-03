from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, SubmitField, validators, ValidationError, PasswordField

from models import db, Users

class ContactForm(Form):
    # Basically, this is instead of putting input forms in HTML
    name = StringField("name",  [validators.Required('Please enter your name.')])
    email = StringField("Email",  [validators.Required('Please enter your email address'), validators.Email('Please enter your email address')])
    subject = StringField("Subject",  [validators.Required('Please enter a subject')])
    message = TextAreaField("Message",  [validators.Required('Please enter a message')])
    submit = SubmitField("Send")


class SignupForm(Form):
    username = StringField("Username", [validators.Required("Please enter your username.")])
    email = StringField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    submit = SubmitField("Create account")

    def validate(self):
        if not Form.validate(self):
            return False

        user_mail = Users.query.filter_by(email=self.email.data.lower()).first()
        user_name = Users.query.filter_by(username=self.email.data.lower()).first()
        if user_name:
            self.email.errors.append("That username is already taken")
            return False
        if user_mail:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True


class LoginForm(Form):
    username = StringField('Username', [validators.Required("Please enter your username.")])
    password = PasswordField('Password', [validators.Required("Please enter your password.")])
    submit = SubmitField("Sign In")