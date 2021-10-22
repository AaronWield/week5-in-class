from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import validators
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email

class UserLogInForm(FlaskForm):
    #email, pw, submit attributes
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()