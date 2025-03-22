from urllib.parse import urljoin, urlparse
from flask import Blueprint, flash, render_template, redirect, url_for, request, abort
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegistrationForm
from app.models import Employee
import re


class AuthHandler:
    def __init__(self, session):
        # Initialize with session, create blueprint for auth
        self.session = session

        # Create blueprint for auth routes
        self.auth_bp = Blueprint("auth", __name__)

        # Register auth routes
        self.auth_bp.add_url_rule("/", view_func=self.login, methods=["GET", "POST"])
        self.auth_bp.add_url_rule(
            "/login", view_func=self.login, methods=["GET", "POST"]
        )
        self.auth_bp.add_url_rule(
            "/register", view_func=self.register, methods=["GET", "POST"]
        )
        self.auth_bp.add_url_rule("/logout", view_func=self.logout, methods=["POST"])

    def is_safe_url(self, target):
        """Validate URL to prevent open redirect vulnerability"""
        # Extract current host URL and the target URL
        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, target))

        # Ensure target URL has the same network location as the referrer to prevent open redirects
        return test_url.netloc == ref_url.netloc

    def sanitize_input(self, value):
        """Sanitize input to prevent SQL Injection and unsafe characters"""
        # Use regex to allow only alphanumeric characters, underscore, @, and period
        if not re.match(r"^[a-zA-Z0-9_@.]+$", value):
            # Abort if input contains unsafe characters
            abort(400, description="Invalid input detected")
        return value

    def login(self):
        """Log user into application"""
        # If the user is already logged in, redirect to home page
        if current_user.is_authenticated:
            return redirect(url_for("main.home"))

        form = LoginForm()
        if form.validate_on_submit():
            # Sanitize user input
            username = self.sanitize_input(form.username.data)
            password = form.password.data
            remember = form.remember.data

            # Check if the employee exists in the database with the provided username
            employee = self.session.query(Employee).filter_by(username=username).first()

            # If employee found and password matches, log them in
            if employee and check_password_hash(employee.password, password):
                login_user(employee, remember=remember)

                next_url = request.args.get("next")
                if next_url and self.is_safe_url(next_url):
                    return redirect(next_url)
                return redirect(url_for("main.home"))
            else:
                flash("Invalid username or password. Please try again", "danger")

        # If form is not submitted or invalid, render login page
        return render_template("login.html", form=form)

    def register(self):
        """Register a new user"""
        form = RegistrationForm()

        if form.validate_on_submit():
            # Sanitize inputs for registration
            name = self.sanitize_input(form.name.data)
            employee_number = self.sanitize_input(form.employee_number.data)
            email = self.sanitize_input(form.email.data)
            username = self.sanitize_input(form.username.data)
            password = form.password.data

            # Check if email or employee number already exists in the database
            existing_email = self.session.query(Employee).filter_by(email=email).first()
            existing_employee = (
                self.session.query(Employee)
                .filter_by(employee_number=employee_number)
                .first()
            )

            # Display error message if the email or employee number is already taken
            if existing_email:
                flash("Email address already exists.", "danger")
                return redirect(url_for("auth.register"))

            if existing_employee:
                flash(
                    "This employee number already exists. Please log in instead.",
                    "danger",
                )
                return redirect(url_for("auth.register"))

            # Create a new employee and add to database
            new_employee = Employee(
                name=name,
                employee_number=employee_number,
                email=email,
                username=username,
                # Secure password hashing
                password=generate_password_hash(password, method="pbkdf2:sha256"),
                is_admin=False,
            )

            # Attempt to commit the new employee to the database
            self.session.add(new_employee)
            try:
                self.session.commit()
                flash("Your account has been created! You can now log in.", "success")
                return redirect(url_for("auth.login"))
            except Exception as e:
                # If there's an error, roll back and show an error message
                self.session.rollback()
                flash(
                    f"An error occurred while creating your account: {str(e)}", "danger"
                )
                return redirect(url_for("auth.register"))

        # If form is not submitted or invalid, render registration page
        return render_template("register.html", form=form)

    @login_required
    def logout(self):
        """Log user out of application"""
        # Get the next URL from request, or redirect to login page
        next_url = request.args.get("next")
        if not self.is_safe_url(next_url):
            next_url = url_for("auth.login")

        logout_user()
        flash("You have been logged out.", "info")
        return redirect(next_url or url_for("auth.login"))
