import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import add_employee, add_review, get_session, init_engine
from app.models import Base, Employee, Review


class TestDatabaseInitialization(unittest.TestCase):

    @patch("app.database.create_engine")
    @patch(
        "app.database.Base.metadata.create_all"
    )
    def test_init_engine(self, mock_create_all, mock_create_engine):
        """Test that the engine is initialized and tables are created."""

        # Call the init_engine function with test database URI
        test_db_uri = "sqlite:///:memory:"
        init_engine(test_db_uri)

        # Check create_engine was called with the correct database URI
        mock_create_engine.assert_called_once_with(test_db_uri, echo=True)

        # Check the create_all method was called with the correct engine
        mock_create_all.assert_called_once_with(mock_create_engine.return_value)

        from app.database import engine

        self.assertEqual(engine, mock_create_engine.return_value)

    @patch("app.database.Session")
    def test_get_session_success(self, mock_session):
        """Test that a session is retrieved successfully when engine is initialized."""

        # Mock the engine to be initialized
        mock_engine = MagicMock()
        with patch("app.database.engine", new=mock_engine):
            # Call get_session
            session_instance = get_session()

            # Check session was created and bound to the mock engine
            mock_session.assert_called_once_with(bind=mock_engine)
            self.assertEqual(session_instance, mock_session.return_value)

    def test_get_session_no_engine(self):
        """Test that get_session raises a RuntimeError when engine is not initialized."""

        # Ensure that engine is None
        with patch("app.database.engine", new=None):
            # Check RuntimeError is raised when engine is not initialized
            with self.assertRaises(RuntimeError) as context:
                get_session()

            # Check if the correct error message is raised
            self.assertEqual(str(context.exception), "Engine is not initialized")

    @patch("app.database.Session")
    def test_add_employee(self, mock_session):
        """Test adding a new employee when the Employee table is empty."""

        # Create a mock session instance
        session = mock_session.return_value

        # Mock the count to return 0 (table is empty)
        session.query.return_value.count.return_value = 0

        add_employee(
            session,
            "John Doe",
            12345,
            "johndoe1234",
            "john@example.com",
            "hashed_password",
            is_admin=False,
        )

        # Check that the new employee was added and session committed
        self.assertEqual(session.add.call_count, 1)
        self.assertEqual(session.commit.call_count, 1)

        # Verify the correct employee was added
        new_employee = session.add.call_args[0][0]
        self.assertIsInstance(
            new_employee, Employee
        )
        self.assertEqual(new_employee.name, "John Doe")
        self.assertEqual(new_employee.employee_number, 12345)
        self.assertEqual(new_employee.username, "johndoe1234")
        self.assertEqual(new_employee.email, "john@example.com")
        self.assertEqual(new_employee.password, "hashed_password")

    @patch("app.database.Session")
    def test_add_review(self, mock_session):
        """Test adding a new review when the Review table is empty."""

        session = mock_session.return_value

        # Mock the count to return 0 (table is empty)
        session.query.return_value.count.return_value = 0

        add_review(
            session,
            12345,
            "20-09-2024",
            1,
            "Good",
            "Achieved all goals",
            "Great performance!",
        )

        self.assertEqual(session.add.call_count, 1)
        self.assertEqual(session.commit.call_count, 1) 

        # Verify the correct review was added
        new_review = session.add.call_args[0][0]
        self.assertIsInstance(new_review, Review)
        self.assertEqual(new_review.employee_number, 12345)
        self.assertEqual(new_review.review_date, "20-09-2024")
        self.assertEqual(new_review.reviewer_id, 1)
        self.assertEqual(new_review.overall_performance_rating, "Good")
        self.assertEqual(new_review.goals, "Achieved all goals")
        self.assertEqual(new_review.reviewer_comments, "Great performance!")


if __name__ == "__main__":
    unittest.main()
