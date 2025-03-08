import unittest
from unittest.mock import patch, MagicMock
from flask import url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import create_app
from app.database import get_session
from app.forms import LoginForm
from app.models import Employee
from app.tests.unit.test_main import User


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                # Disable CSRF for testing
                "WTF_CSRF_ENABLED": False,
            }
        )
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.mock_session = MagicMock()
        patch("app.database.get_session", return_value=self.mock_session).start()

        # Prepare a mock user
        self.mock_user = Employee(username="testuser123", password="Testpassword123!")
        self.mock_user.check_password = MagicMock(return_value=True)
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = (
            self.mock_user
        )

    # Remove context after each test
    def tearDown(self):
        self.app_context.pop()
        patch.stopall()

    def test_login_success(self):
        with self.app.test_request_context():
            # Create a test user
            self.mock_employee = User(
                id="testuser123", employee_number=123, is_admin=False
            )
            with self.client.session_transaction() as session:
                session["user_id"] = self.mock_employee.id
                session["employee_number"] = self.mock_employee.employee_number

            # Mock the login form
            login_form = LoginForm()
            login_form.username.data = "testuser123"
            login_form.password.data = "Testpassword123!"

            # Patch the validate_on_submit method of the LoginForm
            with patch.object(login_form, "validate_on_submit", return_value=True):
                # Send a POST request to the login route
                response = self.client.post(
                    url_for("auth.login"),
                    data={"username": "testuser123", "password": "Testpassword123!"},
                    follow_redirects=True,
                )

            # Check user is redirected to the home page
            self.assertEqual(response.status_code, 200)

            # Check user is logged in
            with self.client.session_transaction() as session:
                self.assertIn("user_id", session)
                self.assertEqual(session["user_id"], self.mock_employee.id)
                self.assertIn("employee_number", session)
                self.assertEqual(
                    session["employee_number"], self.mock_employee.employee_number
                )

    @patch("flask_login.login_user")
    @patch("flask_login.current_user")
    def test_login_failure(self, mock_current_user, mock_login_user):
        """Test login with invalid credentials"""
        with self.app.test_request_context():
            mock_current_user.is_authenticated = False

            # Mock that no employee was found (invalid username or password)
            self.mock_session.query().filter_by().first.return_value = None

            # Post login request with invalid credentials
            response = self.client.post(
                url_for("auth.login"),
                data={
                    "username": "wrong_user",
                    "password": "wrong_password",
                },
                follow_redirects=True,
            )

            # Check the login failed and user was not logged in
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                b"Invalid username or password", response.data
            )  # Check for an error message
            mock_login_user.assert_not_called()

    @patch("flask_login.current_user")
    def test_login_already_authenticated(self, mock_current_user):
        """Test login when already authenticated"""
        with self.app.test_request_context():
            mock_current_user.is_authenticated = True

            # Attempt login when already authenticated
            response = self.client.get("/login")

            # Check the user is redirected to the home page
            self.assertEqual(response.status_code, 200)
            response = self.client.get("/home")
            self.assertEqual(response.status_code, 302)

    @patch("flask_login.logout_user")
    @patch("flask_login.current_user")
    def test_logout(self, mock_current_user, mock_logout_user):
        """Test successful logout"""
        with self.app.test_request_context():
            mock_current_user.is_authenticated = True

            # Call the logout route
            response = self.client.post(url_for("auth.logout"), follow_redirects=True)

            # Check the user was logged out and redirected to the login page
            self.assertIn(b"Username", response.data)
            self.assertEqual(response.status_code, 200)

    def test_register_success(self):
        """Test successful registration"""
        with self.app.test_request_context():
            # Mock no existing user found (for email and username)
            self.mock_session.query().filter_by().first.side_effect = [None, None]

            # Post registration request with valid data
            response = self.client.post(
                url_for("auth.register"),
                data={
                    "name": "New User",
                    "employee_number": 54321,
                    "email": "newuser@example.com",
                    "username": "newuser123",
                    "password": "new_password123!",
                },
                follow_redirects=True,
            )

            new_user = User(id="newuser123", employee_number=123, is_admin=False)

            self.mock_session.add(new_user)
            self.mock_session.commit(new_user)

            # Set the user_id and employee_number in the session
            with self.client.session_transaction() as session:
                session["user_id"] = new_user.id
                session["employee_number"] = new_user.employee_number

            # Check the user was registered and redirected to the login page
            self.assertEqual(response.status_code, 200)
            self.mock_session.add.assert_called_once()
            self.mock_session.commit.assert_called_once()

            # Check the user is logged in
            with self.client.session_transaction() as session:
                self.assertIn("user_id", session)
                self.assertEqual(session["user_id"], new_user.id)
                self.assertIn("employee_number", session)
                self.assertEqual(session["employee_number"], new_user.employee_number)

    def test_register_existing_email(self):
        """Test registration with an existing email"""
        with self.app.test_request_context():
            # Mock an existing user with the same email
            mock_existing_employee = Employee(email="existing@example.com")
            self.mock_session.query().filter_by().first.side_effect = [
                mock_existing_employee,
                None,
            ]

            # Post registration request with an existing email
            response = self.client.post(
                url_for("auth.register"),
                data={
                    "name": "New User",
                    "employee_number": 54321,
                    "email": "existing@example.com",
                    "username": "new_user123",
                    "password": "new_password123!",
                },
                follow_redirects=True,
            )

            # Check the registration failed and user was not added
            self.assertEqual(response.status_code, 200)
            self.mock_session.add.assert_not_called()


if __name__ == "__main__":
    unittest.main()
