from flask_wtf import Form
from wtforms import Form, StringField, TextAreaField, SubmitField, validators, ValidationError


class ContactForm(Form):
    # Basically, this is instead of putting input forms in HTML
    name = StringField("name",  [validators.Required('Please enter your name.')])
    email = StringField("Email",  [validators.Required('Please enter your email address'), validators.Email('Please enter your email address')])
    subject = StringField("Subject",  [validators.Required('Please enter a subject')])
    message = TextAreaField("Message",  [validators.Required('Please enter a message')])
    submit = SubmitField("Send")
