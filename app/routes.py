from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.forms import RegistrationForm, LoginForm

main = Blueprint('main', __name__)

@main.route("/home")
@login_required
def home():
    return render_template('home.html', name=current_user.name)

@main.route("/create-review")
def create_review():
    return render_template('create_review.html')