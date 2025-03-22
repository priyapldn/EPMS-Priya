import re
from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    IntegerField,
    SelectField,
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError,
    NumberRange,
    Regexp,
)
from app.database import get_session
from app.models import Employee


class LoginForm(FlaskForm):
    """Form to validate user login credentials"""

    username = StringField("Username", validators=[DataRequired(), Length(min=10)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """Form to validate user registration data"""

    # Name field with regex to ensure it contains only letters, spaces, or hyphens
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Regexp(r"^[a-zA-Z\s\-]+$", message="Name must contain only letters."),
        ],
    )
    # Employee number field must be an integer
    employee_number = IntegerField("Employee Number", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    # Username field with a minimum length of 10 characters
    username = StringField("Username", validators=[DataRequired(), Length(min=10)])
    # Password field with no predefined validators, will be validated separately
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def __init__(self, session=None, *args, **kwargs):
        """Initialize form with optional session parameter for database access"""
        super().__init__(*args, **kwargs)
        self.session = get_session()

    def validate_username(self, username):
        """Custom validator to check if the username already exists"""
        # Query the database to check if the username already exists
        employee_exists = (
            self.session.query(Employee).filter_by(username=username.data).first()
        )
        if employee_exists:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_password(self, password):
        """Custom validator to ensure password meets complexity requirements"""
        if len(password.data) < 8:
            raise ValidationError("Password must be at least 8 characters long.")

        if not re.search(r"[A-Z]", password.data):
            raise ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", password.data):
            raise ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password.data):
            raise ValidationError(
                "Password must contain at least one special character."
            )

    def validate_email(self, email):
        """Custom validator to check if the email is already associated with an existing account"""
        # Query the database to check if the email already exists
        employee_exists = (
            self.session.query(Employee).filter_by(email=email.data).first()
        )
        # Raise a validation error if the email is already in use
        if employee_exists:
            raise ValidationError(
                "There is already an account with this email. Please login."
            )


class CreateReviewForm(FlaskForm):
    """Form to validate review creation data"""

    # Review date field, required to enter a date
    review_date = DateField("Date", validators=[DataRequired()])
    # Reviewer ID field, must be a positive integer
    reviewer_id = IntegerField(
        "Reviewer ID",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Reviewer ID must be a positive integer"),
        ],
    )
    # Dropdown to select the overall performance rating
    overall_performance_rating = SelectField(
        "Overall Performance Rating",
        choices=[
            # Default placeholder
            ("", "Select Value"),
            ("Excellent", "Excellent"),
            ("Good", "Good"),
            ("Satisfactory", "Satisfactory"),
            ("Needs Improvement", "Needs Improvement"),
            ("Unsatisfactory", "Unsatisfactory"),
        ],
        validators=[DataRequired()],
    )
    # Goals field, required and with a minimum length of 10 characters
    goals = TextAreaField("Goals", validators=[DataRequired(), Length(min=10)])
    reviewer_comments = TextAreaField(
        "Reviewer Comments",
        validators=[
            DataRequired(),
            Length(max=500, message="Comments cannot exceed 500 characters"),
        ],
    )
