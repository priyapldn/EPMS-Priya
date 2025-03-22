# import tempfile
# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException, NoSuchElementException

# @pytest.fixture
# def driver():
#     """Create a unique temporary directory for each test session"""
#     user_data_dir = tempfile.mkdtemp()

#     chrome_options = Options()
#     # Ensure unique user-data-dir
#     chrome_options.add_argument(f"user-data-dir={user_data_dir}") 
#     chrome_options.add_argument("--headless")

#     # Create a new WebDriver instance with the unique user data directory
#     driver = webdriver.Chrome(options=chrome_options)

#     yield driver
#     driver.quit()

# def wait_for_element(driver, by, value, timeout=10):
#     """Waits for an element to be visible."""
#     try:
#         return WebDriverWait(driver, timeout).until(
#             EC.visibility_of_element_located((by, value))
#         )
#     except TimeoutException:
#         return None


# def fill_registration_form(driver, name, emp_number, email, username, password):
#     """Fills the registration form with given data."""
#     driver.find_element(By.NAME, "name").send_keys(name)
#     driver.find_element(By.NAME, "employee_number").send_keys(emp_number)
#     driver.find_element(By.NAME, "email").send_keys(email)
#     driver.find_element(By.NAME, "username").send_keys(username)
#     driver.find_element(By.NAME, "password").send_keys(password)
#     driver.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]").click()

# def test_successful_registration(driver):
#     """Test successful registration with valid data."""
#     driver.get("http://127.0.0.1:5000/register")

#     fill_registration_form(
#         driver,
#         name="Alice Johnson",
#         emp_number="123456",
#         email="alice.johnson@example.com",
#         username="alicejohnson001",
#         password="SecurePass123!"
#     )

#     # Wait for the flash message or success indication
#     success_message = wait_for_element(driver, By.CLASS_NAME, "alert-success")
    
#     assert success_message is not None, "Success message not displayed!"
#     assert "Registration successful" in success_message.text


# def test_registration_existing_email(driver):
#     """Test registration with an already registered email."""
#     driver.get("http://127.0.0.1:5000/register")

#     fill_registration_form(
#         driver,
#         name="Bob Smith",
#         emp_number="654321",
#         email="alice.johnson@example.com",
#         username="bobsmith002",
#         password="Password123!"
#     )

#     # Check for error message
#     error_message = wait_for_element(driver, By.CLASS_NAME, "alert-danger")
    
#     assert error_message is not None, "Error message not displayed!"
#     assert "Email already registered" in error_message.text


# def test_registration_invalid_input(driver):
#     """Test form validation with invalid inputs."""
#     driver.get("http://127.0.0.1:5000/register")

#     # Fill form with invalid data
#     fill_registration_form(
#         driver,
#         name="",
#         emp_number="",
#         email="invalid-email",
#         username="short",
#         password="123"
#     )

#     # Check for individual validation errors
#     name_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'This field is required')]")
#     email_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'Invalid email format')]")
#     username_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'Username too short')]")
#     password_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'Password too weak')]")

#     assert name_error is not None, "Name validation error not displayed!"
#     assert email_error is not None, "Email validation error not displayed!"
#     assert username_error is not None, "Username validation error not displayed!"
#     assert password_error is not None, "Password validation error not displayed!"


# def test_registration_empty_fields(driver):
#     """Test form submission with empty fields."""
#     driver.get("http://127.0.0.1:5000/register")

#     # Try submitting empty form
#     driver.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]").click()

#     # Check for validation errors
#     name_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'This field is required')]")
#     emp_number_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'This field is required')]")
#     email_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'This field is required')]")
#     username_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'This field is required')]")
#     password_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'This field is required')]")

#     assert name_error is not None, "Name field validation failed!"
#     assert emp_number_error is not None, "Employee number field validation failed!"
#     assert email_error is not None, "Email field validation failed!"
#     assert username_error is not None, "Username field validation failed!"
#     assert password_error is not None, "Password field validation failed!"


# def test_registration_invalid_password(driver):
#     """Test form with invalid password format."""
#     driver.get("http://127.0.0.1:5000/register")

#     fill_registration_form(
#         driver,
#         name="Tom Cruise",
#         emp_number="789456",
#         email="tom.cruise@example.com",
#         username="tomcruise001",
#         password="weak"
#     )

#     # Check for weak password error
#     password_error = wait_for_element(driver, By.XPATH, "//div[contains(text(),'Password too weak')]")

#     assert password_error is not None, "Weak password error message not displayed!"

