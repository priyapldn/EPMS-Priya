import unittest
from flask_login import UserMixin
from app import create_app
from app.database import get_session


# Set users to differentiate by
class User(UserMixin):
    def __init__(self, id, employee_number, is_admin=False):
        self.id = id
        self.is_admin = is_admin
        self.employee_number = employee_number


class ReviewRoutesTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "WTF_CSRF_ENABLED": False,
            }
        )
        self.client = self.app.test_client()

        # Create a test user
        self.test_user = User(id="test_user123", employee_number=123, is_admin=False)

        # Create an admin user
        self.admin_user = User(id="admin_user123", employee_number=123, is_admin=True)

        # Set up the database session
        self.session = get_session()
        self.session.query = lambda x: self.session
        self.session.commit = lambda: None
        self.session.rollback = lambda: None

        # Push application context
        self.app.app_context().push()

        # Register the test user in the session
        self.client.post(
            "/login", data={"username": "testuser123", "password": "Testpassword123!"}
        )

    def login(self, user):
        with self.client:
            self.client.post(
                "/login", data={"username": user.id, "password": "Testpassword123!"}
            )

    # Check URL contains parameter for admin
    def test_home_with_admin(self):
        self.login(self.admin_user)
        response = self.client.get("/home?all_reviews=true")
        self.assertEqual(response.status_code, 302)

    # Check URL is standard for regular users
    def test_home_with_regular_user(self):
        self.login(self.test_user)
        response = self.client.get("/home")
        self.assertEqual(response.status_code, 302)

    # Check user can create review on authentication
    def test_create_review_authenticated(self):
        self.login(self.test_user)
        response = self.client.post(
            "/create-review",
            data={
                "review_date": "20-09-2024",
                "reviewer_id": 12,
                "overall_performance_rating": "Outstanding",
                "goals": "Goals for the review",
                "reviewer_comments": "Great job!",
            },
        )
        # Redirect after successful post
        self.assertEqual(response.status_code, 302)

    # Check user is redirected if not authenticated
    def test_create_review_not_authenticated(self):
        response = self.client.post("/create-review")
        # Redirect to login
        self.assertEqual(response.status_code, 302)

    # Check authenticated user can update review
    def test_update_review(self):
        self.login(self.test_user)
        # Assume a review with ID 1 exists
        response = self.client.post(
            "/edit-review/1",
            data={
                "review_date": "21-09-2024",
                "reviewer_id": 12,
                "overall_performance_rating": "Outstanding",
                "goals": "Updated goals",
                "reviewer_comments": "Updated comments",
            },
        )
        # Redirect after successful update
        self.assertEqual(response.status_code, 302)

    def test_delete_review_as_owner(self):
        self.login(self.test_user)
        # Assume a review with ID 1 exists and belongs to the test user
        response = self.client.post("/delete-review/1")
        # Redirect after deletion
        self.assertEqual(response.status_code, 302)

    def test_delete_review_as_admin(self):
        self.login(self.admin_user)
        # Assume a review with ID 1 exists
        response = self.client.post("/delete-review/1")
        # Redirect after deletion
        self.assertEqual(response.status_code, 302)

    def test_delete_review_no_permission(self):
        self.login(self.test_user)
        # Assume a review with ID 2 does not belong to the test user
        response = self.client.post("/delete-review/2")
        # Redirect to home with flash message
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
