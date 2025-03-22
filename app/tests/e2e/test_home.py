import tempfile
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    # Create a unique temporary directory for each test session
    user_data_dir = tempfile.mkdtemp()

    chrome_options = Options()
    # Ensure unique user-data-dir
    chrome_options.add_argument(f"user-data-dir={user_data_dir}") 
    chrome_options.add_argument("--headless")

    # Create a new WebDriver instance with the unique user data directory
    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()
    
# Test for authenticated user with admin privileges
def test_authenticated_admin(driver):
    # Login as an admin user
    driver.get("http://127.0.0.1:5000/login")

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys("johndoe1234")
    password_input.send_keys("Password123!")
    password_input.send_keys(Keys.RETURN)

    # Wait for the home page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Welcome')]")))

    # Check if admin sees their name, employee number, and admin privileges
    welcome_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Welcome')]").text
    employee_number = driver.find_element(By.XPATH, "//h5[contains(text(), 'Employee Number')]").text
    admin_privileges = driver.find_element(By.XPATH, "//h6[contains(text(), 'You have admin privileges')]").text

    assert "Welcome, John Doe" in welcome_text
    assert "Employee Number:" in employee_number
    assert "You have admin privileges" in admin_privileges

    # Ensure admin buttons are visible
    view_reviews_button = driver.find_element(By.XPATH, "//a[contains(text(), 'View All Reviews')]")
    assert view_reviews_button.is_displayed()

# Test for authenticated user with regular privileges
def test_authenticated_user(driver):
    # Login as a regular user
    driver.get("http://127.0.0.1:5000/login")

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys("lucyhayes006")
    password_input.send_keys("Password123!")
    password_input.send_keys(Keys.RETURN)

    # Wait for the home page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Welcome')]")))

    # Check if regular user sees their name, employee number, and regular privileges
    welcome_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Welcome')]").text
    employee_number = driver.find_element(By.XPATH, "//h5[contains(text(), 'Employee Number')]").text
    regular_privileges = driver.find_element(By.XPATH, "//h6[contains(text(), 'You have regular user privileges')]").text

    assert "Welcome, Lucy H" in welcome_text
    assert "Employee Number:" in employee_number
    assert "You have regular user privileges" in regular_privileges

    # Ensure regular user doesn't see admin buttons
    try:
        view_reviews_button = driver.find_element(By.XPATH, "//a[contains(text(), 'View All Reviews')]")
        assert False, "Admin button should not be visible"
    except:
        pass

# Test for unauthenticated user
def test_unauthenticated_user(driver):
    # Visit the home page without logging in
    driver.get("http://127.0.0.1:5000/home")

    # Wait for the warning message to appear
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "flash-message")))

    # Check if the unauthenticated user sees the warning message
    warning_message = driver.find_element(By.ID, "flash-message").text
    assert "Please log in to access this page" in warning_message
