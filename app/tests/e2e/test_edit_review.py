# import tempfile
# import pytest
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import Select
# import time


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


# def test_edit_review(driver):
#     """Test the performance review editing process."""
    
#     # Log in
#     driver.get("http://127.0.0.1:5000/login")

#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")

#     username_input.send_keys("johndoe1234")
#     password_input.send_keys("Password123!")
#     password_input.send_keys(Keys.RETURN)

#     # Navigate to the "Edit Review" page
#     wait = WebDriverWait(driver, 10)
#     edit_review_button = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit')]"))
#     )
#     edit_review_button.click()

#     # Fill out the form with new values
#     review_date_input = driver.find_element(By.NAME, "review_date")
#     reviewer_id_input = driver.find_element(By.NAME, "reviewer_id")
#     performance_rating_select = driver.find_element(By.NAME, "overall_performance_rating")
#     goals_input = driver.find_element(By.NAME, "goals")
#     reviewer_comments_input = driver.find_element(By.NAME, "reviewer_comments")

#     # Clear existing values
#     review_date_input.clear()
#     reviewer_id_input.clear()
#     goals_input.clear()
#     reviewer_comments_input.clear()

#     # Populate the fields with new values
#     review_date_input.send_keys("22/03/2025")
#     reviewer_id_input.send_keys("15")
#     select = Select(performance_rating_select)
#     select.select_by_visible_text("Excellent")
#     goals_input.send_keys("Achieve 120% of the sales target.")
#     reviewer_comments_input.send_keys("Outstanding performance throughout the year.")

#     # Click the Save button
#     save_button = wait.until(
#         EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Save")]'))
#     )
#     save_button.click()

#     # Verify the success message and updated data
#     time.sleep(2)
    
#     assert "Review updated successfully" in driver.page_source
#     assert "Outstanding performance throughout the year." in driver.page_source
#     assert "Achieve 120% of the sales target." in driver.page_source


# def test_cancel_review(driver):
#     """Test canceling the review editing."""
    
#     driver.get("http://127.0.0.1:5000/login")

#     username_input = driver.find_element(By.NAME, "username")
#     password_input = driver.find_element(By.NAME, "password")

#     username_input.send_keys("johndoe1234")
#     password_input.send_keys("Password123!")
#     password_input.send_keys(Keys.RETURN)

#     # Navigate to the "Edit Review" page
#     wait = WebDriverWait(driver, 10)
#     edit_review_button = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Edit')]"))
#     )
#     edit_review_button.click()

#     # Click the Cancel button
#     cancel_button = wait.until(
#         EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Cancel")]'))
#     )
#     cancel_button.click()

#     # Confirm cancellation in the modal
#     cancel_modal_button = wait.until(
#         EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Yes, cancel")]'))
#     )
#     cancel_modal_button.click()

#     # Verify you are redirected to the home page
#     time.sleep(2)
    
#     assert "Home" in driver.title
#     assert "Welcome back" in driver.page_source
