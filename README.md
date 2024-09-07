# Employee Performance Management System

A Python web application to log in and manage employee performance reviews. This application uses Flask, SQLite, SQLAlchemy and Bootstrap.
When running this application, you will have the ability to log in as a general or admin user. Once logged in, you can choose to add, read or update a performance review. Admin users are given the additional ability to delete any obselete performance reviews.

## Setup Instructions

### Clone the repository

Clone the repository to your local machine, running the following commands in your terminal:

Via HTTPS:
```bash
git clone https://github.com/priyapldn/EPMS-SEA-Priya.git
```

OR with an SSH Key:
```bash
git clone git@github.com:priyapldn/EPMS-SEA-Priya.git
cd your-repo
```

### Dependencies

Next, please ensure you have Python3 and `pip` installed. Then install the dependencies in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Configuration

You will need to have a `config.py` file. This will store key environment variables such as 'SECRET_KEY' and 'SQLALCHEMY_DATABASE_URI'. 

Inside the **root** directory (the directory where this README exists), you can use the `config_example.py`, but ensure to rename this to `config.py`. 

The file has the following structure mapped out for you:

```python
import os


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.join(BASEDIR, 'app')

    # This creates an instance folder if it doesn't exist
    instance_dir = os.path.join(APP_DIR, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(APP_DIR, 'instance', 'my_db.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
```

To generate the SECRET_KEY, there is a file in the **root** directory called `generate_secret_key.py`. Execute this file by running:

```bash
python generate_secret_key.py
```

This will print a secret key to your terminal, which you can replace `your_secret_key` for.

You can also change the 'my_db.db' part of `SQLALCHEMY_DATABASE_URI` to any name you like, as long as the file extension remains `.db`. When you run this project, this file will get created in a folder called `instance/`.

### Running the application (EPMS)

Simply run the following to start up the application:

```bash
flask run
```
