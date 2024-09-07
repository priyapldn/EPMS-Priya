from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Employee, Review

# Set engine and session for DB
engine = None
Session = sessionmaker()

def init_engine(database_uri):
    """Initialize the database engine and create tables."""
    global engine
    engine = create_engine(database_uri, echo=True)
    Base.metadata.create_all(engine)

def get_session():
    """Retrieve a session to utilize operations."""
    if engine is None:
        raise RuntimeError("Engine is not initialized")
    return Session(bind=engine)

def add_employee(session, name, employee_number, username, email, password, is_admin=False):
    """Add a new employee to the database if the Employee table is empty."""
    if session.query(Employee).count() == 0:
        new_employee = Employee(
            employee_number=employee_number,
            name=name,
            username=username,
            email=email,
            password=password,
            is_admin=is_admin
        )
        session.add(new_employee)
        session.commit()
        print("Employee added.")
    else:
        print("Employee table is not empty. No new employee added.")

def add_review(session, employee_number, review_date, reviewer_id, overall_performance_rating, goals, reviewer_comments):
    """Add a review for an employee if the Review table is empty."""
    if session.query(Review).count() == 0:
        new_review = Review(
            employee_number=employee_number,
            review_date=review_date,
            reviewer_id=reviewer_id,
            overall_performance_rating=overall_performance_rating,
            goals=goals,
            reviewer_comments=reviewer_comments
        )
        session.add(new_review)
        session.commit()
        print("Review added.")
    else:
        print("Review table is not empty. No new review added.")
