from flask_wtf import Form
from wtforms import Form, StringField, TextAreaField, SubmitField


class ContactForm(Form):
    # Basically, this is instead of putting input forms in HTML
    username = StringField("Username")
    email = StringField("Email")
    subject = StringField("Subject")
    message = TextAreaField("Message")
    submit = SubmitField("Send")
