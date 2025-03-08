import unittest
from flask import Flask
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from app.forms import LoginForm, RegistrationForm, CreateReviewForm
from app.models import Employee
from unittest.mock import patch, MagicMock
from datetime import date


class TestLoginForm(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["SECRET_KEY"] = "test_secret_key"

    # Check login details are valid
    def test_valid_login_form(self):
        with self.app.test_request_context():
            form = LoginForm(username="validusername", password="Validpassword123!")
            self.assertTrue(form.validate())

    # Check for username length
    def test_invalid_login_form_username_length(self):
        with self.app.test_request_context():
            form = LoginForm(username="short", password="validpassword")
            self.assertFalse(form.validate())
            self.assertIn(
                "Field must be at least 10 characters long.", form.username.errors
            )

    # Check password length
    def test_invalid_login_form_password_length(self):
        with self.app.test_request_context():
            form = LoginForm(username="validusername", password="short")
            self.assertFalse(form.validate())
            self.assertIn(
                "Field must be at least 8 characters long.", form.password.errors
            )


class TestRegistrationForm(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["SECRET_KEY"] = "test_secret_key"
        self.session = MagicMock()

    def rollback(self):
        self.session.rollback() 
        self.session.remove()

    @patch("app.forms.get_session")
    def test_valid_registration_form(self, mock_get_session):
        # Mock the session to simulate that the username and email are not already taken
        mock_session = mock_get_session.return_value
        # No employee found
        mock_session.query(Employee).filter_by.return_value.first.return_value = None

        with self.app.test_request_context():
            form = RegistrationForm(
                name="Valid Name",
                employee_number=1234,
                email="valid@example.com",
                username="validusername",
                password="ValidPassword1!",
            )

            self.assertTrue(form.validate())

    # Check if username already exists
    @patch("app.forms.get_session")
    def test_username_already_taken(self, mock_get_session):
        mock_session = mock_get_session.return_value
        mock_session.query(Employee).filter_by.return_value.first.return_value = True

        with self.app.test_request_context():
            form = RegistrationForm(
                name="Valid Name",
                employee_number=1234,
                email="valid@example.com",
                username="takenusername",
                password="ValidPassword1!",
            )
            with self.assertRaises(ValidationError):
                form.validate_username(form.username)

    # Check password is invalid
    def test_invalid_password_complexity(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                name="Valid Name",
                employee_number=1234,
                email="valid@example.com",
                username="validusername",
                password="weakpass",
            )
            with self.assertRaises(ValidationError):
                form.validate_password(form.password)

    # Check for existing email
    @patch("app.forms.get_session")
    def test_email_already_in_use(self, mock_get_session):
        mock_session = mock_get_session.return_value
        mock_session.query(Employee).filter_by.return_value.first.return_value = True

        with self.app.test_request_context():
            form = RegistrationForm(
                name="Valid Name",
                employee_number=1234,
                email="existing@example.com",
                username="validusername",
                password="ValidPassword1!",
            )
            with self.assertRaises(ValidationError):
                form.validate_email(form.email)


class TestCreateReviewForm(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["SECRET_KEY"] = "test_secret_key"

    # Check create review details are valid
    def test_valid_create_review_form(self):
        with self.app.test_request_context():
            form = CreateReviewForm(
                review_date=date.today(),
                reviewer_id=1,
                overall_performance_rating="Good",
                goals="Achieve 100% target",
                reviewer_comments="Good performance.",
            )
            self.assertTrue(form.validate())

    # Check reviewer id is not negative
    def test_invalid_reviewer_id(self):
        with self.app.test_request_context():
            form = CreateReviewForm(
                review_date=date.today(),
                reviewer_id=-1,
                overall_performance_rating="Good",
                goals="Achieve 100% target",
                reviewer_comments="Good performance.",
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Reviewer ID must be a positive integer", form.reviewer_id.errors
            )

    # Check goals are of certain length
    def test_invalid_goals_length(self):
        with self.app.test_request_context():
            form = CreateReviewForm(
                review_date=date.today(),
                reviewer_id=1,
                overall_performance_rating="Good",
                goals="Short",
                reviewer_comments="Good performance.",
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Field must be at least 10 characters long.", form.goals.errors
            )

    # Check comments length
    def test_invalid_reviewer_comments_length(self):
        with self.app.test_request_context():
            form = CreateReviewForm(
                review_date=date.today(),
                reviewer_id=1,
                overall_performance_rating="Good",
                goals="Achieve 100% target",
                reviewer_comments="x" * 600,
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Comments cannot exceed 500 characters", form.reviewer_comments.errors
            )


if __name__ == "__main__":
    unittest.main()
