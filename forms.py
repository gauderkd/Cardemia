from flask_wtf import Form
from wtforms import Form, StringField, TextAreaField, SubmitField, validators, ValidationError


class ContactForm(Form):
    # Basically, this is instead of putting input forms in HTML
    username = StringField("Username",  [validators.Required()])
    email = StringField("Email",  [validators.Required(), validators.Email()])
    subject = StringField("Subject",  [validators.Required()])
    message = TextAreaField("Message",  [validators.Required()])
    submit = SubmitField("Send")
