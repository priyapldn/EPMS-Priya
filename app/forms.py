import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.models import Employee

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_password(self, password):
        # Check if the password is at least 8 characters long
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        # Check if the password contains at least one uppercase letter
        if not re.search(r'[A-Z]', password.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        # Check if the password contains at least one lowercase letter
        if not re.search(r'[a-z]', password.data):
            raise ValidationError('Password must contain at least one lowercase letter.')
        
        # Check if the password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password.data):
            raise ValidationError('Password must contain at least one special character.')

    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There is already an account with this email. Please login.')