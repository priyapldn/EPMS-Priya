from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/login")
def login():
    return render_template('login.html')

@main.route("/register")
def register():
    return render_template('register.html')

@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/create-review")
def create_review():
    return render_template('create_review.html')