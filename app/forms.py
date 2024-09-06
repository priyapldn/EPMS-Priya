import re
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from app.database import get_session
from app.models import Employee

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Name')
    employee_number = IntegerField('Employee Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=10)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def __init__(self, session=None, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.session = get_session()

    def validate_username(self, username):
        employee_exists = self.session.query(Employee).filter_by(username=username.data).first()
        if employee_exists:
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
        employee_exists = self.session.query(Employee).filter_by(email=email.data).first()
        if employee_exists:
            raise ValidationError('There is already an account with this email. Please login.')