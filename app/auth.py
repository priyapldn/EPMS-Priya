from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegistrationForm
from app.models import Employee
from app.database import get_session

auth = Blueprint("auth", __name__)

session = get_session()

@auth.route("/")
@auth.route("/login", methods=["GET", "POST"])
def login():
    """Log user into application"""
    # Check if user is already authenticated
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        employee = session.query(Employee).filter_by(username=username).first()

        # Match password hash and redirect if successful
        if employee and check_password_hash(employee.password, password):
            login_user(employee, remember=remember)
            return redirect(url_for("main.home"))
        else:
            flash("Invalid username or password. Please try again", "danger")

    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    """Add user into application by commiting registration details"""
    form = RegistrationForm()

    if form.validate_on_submit():
        name = form.name.data
        employee_number = form.employee_number.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        # Check for exisiting users
        existing_email = session.query(Employee).filter_by(email=email).first()
        existing_employee = (
            session.query(Employee).filter_by(employee_number=employee_number).first()
        )

        if existing_email:
            flash("Email address already exists.", "danger")
            return redirect(url_for("auth.register"))

        if existing_employee:
            flash(
                "This employee number already exists. Please log in instead.", "danger"
            )
            return redirect(url_for("auth.register"))

        # Create new employee and hash password for security
        new_employee = Employee(
            name=name,
            employee_number=employee_number,
            email=email,
            username=username,
            password=generate_password_hash(password, method="pbkdf2:sha256"),
            is_admin=False,
        )

        session.add(new_employee)
        try:
            session.commit()
            flash("Your account has been created! You can now log in.", "success")
            return redirect(url_for("auth.login"))
        except Exception as e:
            session.rollback()
            flash(f"An error occurred while creating your account: {str(e)}", "danger")
            return redirect(url_for("auth.register"))

    return render_template("register.html", form=form)


@auth.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log user out of application"""
    logout_user()

    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
