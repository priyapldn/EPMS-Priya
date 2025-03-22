# import tempfile
# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options


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

# def test_authenticated_admin(driver):
#     """Login as an admin and verify access."""
#     driver.get("http://127.0.0.1:5000/login")

#     # Enter admin credentials
#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")

#     username_input.send_keys("johndoe1234")
#     password_input.send_keys("Password123!")
#     password_input.send_keys(Keys.RETURN)

#     # Wait until the admin page loads
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Welcome')]"))
#     )

#     # Validate admin sees their info
#     welcome_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Welcome')]").text
#     admin_privileges = driver.find_element(By.XPATH, "//h6[contains(text(), 'You have admin privileges')]").text

#     assert "Welcome, John Doe" in welcome_text
#     assert "You have admin privileges" in admin_privileges

#     # Ensure admin buttons are visible
#     view_reviews_button = driver.find_element(By.XPATH, "//a[contains(text(), 'View All Reviews')]")
#     assert view_reviews_button.is_displayed()

# def test_authenticated_user(driver):
#     """Login as a regular user and verify access."""
#     driver.get("http://127.0.0.1:5000/login")

#     # Enter regular user credentials
#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")

#     username_input.send_keys("lucyhayes006")
#     password_input.send_keys("Password123!")
#     password_input.send_keys(Keys.RETURN)

#     # Wait until the user page loads
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, "//h4[contains(text(), 'Welcome')]"))
#     )

#     # Validate regular user info
#     welcome_text = driver.find_element(By.XPATH, "//h4[contains(text(), 'Welcome')]").text
#     regular_privileges = driver.find_element(By.XPATH, "//h6[contains(text(), 'You have regular user privileges')]").text

#     assert "Welcome, Lucy H" in welcome_text
#     assert "You have regular user privileges" in regular_privileges

#     # Ensure regular user cannot see admin buttons
#     try:
#         driver.find_element(By.XPATH, "//a[contains(text(), 'View All Reviews')]")
#         assert False, "Admin button should not be visible to regular users"
#     except:
#         pass

# def test_unauthenticated_user(driver):
#     """Access a protected route without logging in."""
#     driver.get("http://127.0.0.1:5000/home")

#     # Wait for the flash message
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "flash-message"))
#     )

#     # Verify the warning message is displayed
#     warning_message = driver.find_element(By.ID, "flash-message").text
#     assert "Please log in to access this page" in warning_message

# def test_invalid_login(driver):
#     """Test login with invalid credentials."""
#     driver.get("http://127.0.0.1:5000/login")

#     # Enter incorrect credentials
#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")

#     username_input.send_keys("wronguser")
#     password_input.send_keys("wrongpassword")
#     password_input.send_keys(Keys.RETURN)

#     WebDriverWait(driver, 20).until(
#     EC.visibility_of_element_located((By.XPATH, "//div[@class='alert']"))
#     )

#     # Verify flash message is displayed
#     flash_message = driver.find_element(By.XPATH, "//div[@class='alert']").text
#     assert "Invalid username or password. Please try again" in flash_message

# def test_csrf_protection(driver):
#     """Test that CSRF protection is enforced."""
#     driver.get("http://127.0.0.1:5000/login")

#     # Attempt login without CSRF token (manipulate request)
#     driver.execute_script("""
#         document.querySelector('input[name="csrf_token"]').remove();
#     """)

#     # Submit the form without CSRF token
#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")

#     username_input.send_keys("johndoe1234")
#     password_input.send_keys("Password123!")
#     password_input.send_keys(Keys.RETURN)

#     # Wait for flash message
#     WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "flash-message"))
#     )

#     # Verify CSRF failure message
#     flash_message = driver.find_element(By.ID, "flash-message").text
#     assert "CSRF token is missing or invalid" in flash_message
