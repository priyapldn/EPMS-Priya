# Employee Performance Management System

A Python web application to log in and manage employee performance reviews. This application uses Flask, SQLite, SQLAlchemy and Bootstrap.
When running this application, you will have the ability to log in as a general or admin user. Once logged in, you can choose to add, read or update a performance review. Admin users (please note these are NOT Reviewers, they are HR Administrators) are given the additional ability to delete any obselete performance reviews. Please see the bottom of this README for admin login details.

This application has been built and deployed on Render, with the hosted links as follows: 

- Development: https://epms-sedo-dev.onrender.com
- Staging: https://epms-sedo-staging.onrender.com
- Production: https://epms-sedo-prod.onrender.com

NOTE: Please allow up to 60 seconds to load the webpage, as the server loads (usually takes around 15 seconds but 60 seconds maximum)

To log in as admin, the credentials are at the bottom of this README.

Uptime Robot has been used to keep this site running, and is monitored regularly.
Please visit https://uptimerobot.com/ for more information.

The following badges review the workflows that are present in GitHub Actions:

### Test and Linting Pipeline

[![Test & Linting](https://github.com/priyapldn/EPMS-Priya/actions/workflows/ci-cd-test.yaml/badge.svg)](https://github.com/priyapldn/EPMS-Priya/actions/workflows/ci-cd-test.yaml)

### Deploy Application Pipeline

[![Deploy Application](https://github.com/priyapldn/EPMS-Priya/actions/workflows/ci-cd-deploy.yaml/badge.svg)](https://github.com/priyapldn/EPMS-Priya/actions/workflows/ci-cd-deploy.yaml)

## Setup Instructions

### Clone the repository

Clone the repository to your local machine, running the following command(s) in your terminal:

Via HTTPS:
```bash
git clone https://github.com/priyapldn/EPMS-SEA-Priya.git
```

OR with an SSH Key:
```bash
git clone git@github.com:priyapldn/EPMS-SEA-Priya.git
```

### Virtual Environment/Dependencies

Next, please ensure you have Python3 and `pip` installed. Ensure you have a python virtual environment set up in the **root** directory. If not, please follow these steps to do so:

```bash
# Install virtualenv
pip install virtualenv

# Create environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate
```

Then install the dependencies in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Want to run this locally?

Follow these steps to run this project locally, rather than accessing the hosted URL.

### 1. Configuration

Inside the root directory, there is a `config.py` file. This will store key environment variables such as the 'SECRET_KEY' and 'SQLALCHEMY_DATABASE_URI'. 

The file has the following structure mapped out:

```python
import os

class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.join(BASEDIR, 'app')

    # Create instance folder if it doesn't exist
    instance_dir = os.path.join(APP_DIR, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{os.path.join(APP_DIR, 'instance', 'epmstore.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    # Use the environment variable for SECRET_KEY, fallback to None if not set
    SECRET_KEY = os.getenv('SECRET_KEY')
```

To run this locally, you will need to generate the SECRET_KEY. There is a file in the **root** directory called `generate_secret_key.py`. Execute this file by running:

```bash
# Ensure you are in the root directory first, otherwise your terminal will not find this file... e.g. cd EPMS-Priya
python3 generate_secret_key.py
```

This will print a secret key to your terminal, which you can replace the last line with `SECRET_KEY = os.getenv('SECRET_KEY', 'your_generated_key_goes_here')`.

### 2. Running the application (EPMS)

Simply run the following to start up the application:

```bash
flask run
```

If you would like to clean the database, you can delete the `epmstore.db` file. Run `flask run` again to initialise the database. The admin user will be created for you.

## Logging in

Logging into the application is simple. The first user that is generated automatically is the only admin user for this application. They have control over all employees and can perform all operations on Performance Reviews. 

The credentials to log in as admin are:

| Username       | Password        |
| -------------- | --------------- |
| johndoe1234    | Password123!    |

Once logged in, you can see all the reviews for John, and other employees.

## Testing

To run the tests, ensure you have setup a virtual environment in your IDE. 
Then simply run:

```bash
pytest
```
