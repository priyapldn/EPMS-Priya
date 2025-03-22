import tempfile
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time


@pytest.fixture
def driver():
    """Create a unique temporary directory for each test session"""
    user_data_dir = tempfile.mkdtemp()

    chrome_options = Options()
    # Ensure unique user-data-dir
    chrome_options.add_argument(f"user-data-dir={user_data_dir}") 
    chrome_options.add_argument("--headless")

    # Create a new WebDriver instance with the unique user data directory
    driver = webdriver.Chrome(options=chrome_options)

    yield driver
    driver.quit()


def test_submit_review(driver):
    """Submittig a review"""
    driver.get("http://127.0.0.1:5000/login")

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys("johndoe1234")
    password_input.send_keys("Password123!")
    password_input.send_keys(Keys.RETURN)

    # Wait for the "Add Another Review" button to appear and click it
    wait = WebDriverWait(driver, 10)
    add_review_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(text(), 'Add Another Review')]")
        )
    )
    add_review_button.click()

    # Fill out the form
    review_date_input = driver.find_element(By.NAME, "review_date")
    reviewer_id_input = driver.find_element(By.NAME, "reviewer_id")
    performance_rating_select = driver.find_element(
        By.NAME, "overall_performance_rating"
    )
    goals_input = driver.find_element(By.NAME, "goals")
    reviewer_comments_input = driver.find_element(By.NAME, "reviewer_comments")

    # Populate the fields
    review_date_input.send_keys("20/09/2024")
    reviewer_id_input.send_keys("12")
    select = Select(performance_rating_select)
    select.select_by_visible_text("Excellent")
    goals_input.send_keys("Meet Q4 goals, exceed performance metrics")
    reviewer_comments_input.send_keys("Excellent work ethic and performance.")

    # Wait until the submit button is VISIBLE and CLICKABLE (prevents timeout)
    submit_button = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, '//button[normalize-space()="Submit"]')
        )
    )
    submit_button.click()

    # Verify the review was submitted
    time.sleep(2)
    assert "Excellent work ethic and performance." in driver.page_source
