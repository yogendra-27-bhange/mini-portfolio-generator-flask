from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80, message="Username must be between 3 and 80 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PortfolioForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[DataRequired()])
    skills = TextAreaField('Skills (one per line)', validators=[DataRequired()])
    education = TextAreaField('Education (one per line)', validators=[DataRequired()])
    projects = TextAreaField('Projects (one per line)', validators=[DataRequired()])
    social_links = TextAreaField('Social Links (one per line)', validators=[DataRequired()])
    submit = SubmitField('Save Portfolio') 