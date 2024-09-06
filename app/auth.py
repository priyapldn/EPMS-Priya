from flask import Blueprint, flash, render_template, redirect, url_for, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Employee
from app.database import get_session

auth = Blueprint('auth', __name__)

@auth.route("/")
@auth.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    session = get_session()

    name = request.form.get('name')
    employee_number = request.form.get('employee_number')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    existing_employee = session.query(Employee).filter_by(email=email).first()

    if existing_employee:
        flash('Email address already exists.')
        return redirect(url_for('auth.register'))

    new_employee = Employee(name=name, employee_number=employee_number,email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'), is_admin=False)
    
    session.add(new_employee)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    return 'Logout'