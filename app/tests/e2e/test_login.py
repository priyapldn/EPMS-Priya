import tempfile
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException


@pytest.fixture
def driver():
    """Create a unique temporary directory for each test session."""
    user_data_dir = tempfile.mkdtemp()

    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()


def test_authenticated_admin(driver):
    """Login as an admin and verify access."""
    driver.get("http://127.0.0.1:5000/login")

    # Enter admin credentials
    driver.find_element(By.NAME, "username").send_keys("johndoe1234")
    driver.find_element(By.NAME, "password").send_keys("Password123!")
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Wait until the admin page loads
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Welcome')]"))
    )

    # Validate admin info
    assert "Welcome, John Doe" in driver.page_source
    assert "You have admin privileges" in driver.page_source

    # Ensure admin buttons are visible
    try:
        view_reviews_button = driver.find_element(By.XPATH, "//a[contains(text(), 'View All Reviews')]")
        assert view_reviews_button.is_displayed()
    except NoSuchElementException:
        pytest.fail("Admin button not found")


def test_authenticated_user(driver):
    """Login as a regular user and verify access."""
    driver.get("http://127.0.0.1:5000/login")

    # Enter regular user credentials
    driver.find_element(By.NAME, "username").send_keys("lucyhayes006")
    driver.find_element(By.NAME, "password").send_keys("Password123!")
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Wait until the user page loads
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Welcome')]"))
    )

    # Validate regular user info
    assert "Welcome, Lucy H" in driver.page_source
    assert "You have regular user privileges" in driver.page_source

    # Ensure regular user cannot see admin buttons
    with pytest.raises(NoSuchElementException):
        driver.find_element(By.XPATH, "//a[contains(text(), 'View All Reviews')]")


def test_unauthenticated_user(driver):
    """Access a protected route without logging in."""
    driver.get("http://127.0.0.1:5000/home")

    # Wait for the flash message
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "flash-message"))
    )

    # Verify the warning message is displayed
    warning_message = driver.find_element(By.ID, "flash-message").text
    assert "Please log in to access this page" in warning_message


def test_invalid_login(driver):
    """Test login with invalid credentials."""
    driver.get("http://127.0.0.1:5000/login")

    # Enter incorrect credentials
    driver.find_element(By.NAME, "username").send_keys("wronguser12")
    driver.find_element(By.NAME, "password").send_keys("wrongpassword")
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    # Increase wait time to ensure flash message appears
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert')]"))
    )

    # Verify flash message
    flash_message = driver.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text
    assert "Invalid username or password. Please try again" in flash_message


# def test_csrf_protection(driver):
#     """Test that CSRF protection is enforced."""
#     driver.get("http://127.0.0.1:5000/login")

#     # Remove CSRF token with JavaScript
#     driver.execute_script("""
#         let csrf = document.querySelector('input[name="csrf_token"]');
#         if (csrf) csrf.remove();
#     """)

#     # Submit the form without CSRF token
#     driver.find_element(By.NAME, "username").send_keys("johndoe1234")
#     driver.find_element(By.NAME, "password").send_keys("Password123!")
#     driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

#     # Increase wait time to ensure flash message appears
#     WebDriverWait(driver, 20).until(
#         EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert')]"))
#     )

#     # Verify CSRF failure message
#     flash_message = driver.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text
#     assert "CSRF token is missing or invalid" in flash_message
