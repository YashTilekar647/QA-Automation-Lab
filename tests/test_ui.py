"""
test_ui.py – Selenium UI tests for a login page.

Target site: https://the-internet.herokuapp.com/login
This is a free practice site maintained by Dave Haeffner.

Tests demonstrate:
  • Opening a page and checking its title / heading
  • Filling in a form and clicking a button
  • Asserting success and failure messages
  • Data-driven login testing with @pytest.mark.parametrize
"""

# NOTE: We use WebDriverWait + expected_conditions for reliable waits.

import json
import logging
import os
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import our driver helper
from utils.driver import get_chrome_driver

# ──────────────────────────────────────────────
# Setup: load test data
# ──────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(PROJECT_ROOT, "test_data.json")

with open(DATA_FILE, "r") as f:
    TEST_DATA = json.load(f)

UI_DATA = TEST_DATA["ui"]

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Fixture: create & quit the browser for each test
# ──────────────────────────────────────────────
@pytest.fixture
def browser():
    """
    Pytest fixture that provides a fresh browser for each test.
    The browser is automatically closed after the test finishes.
    """
    driver = get_chrome_driver(headless=True)
    logger.info("Browser started")
    yield driver
    driver.quit()
    logger.info("Browser closed")


# ──────────────────────────────────────────────
# Helper: perform login
# ──────────────────────────────────────────────
def _do_login(driver, username: str, password: str):
    """Fill in the login form and click the Login button."""
    driver.get(UI_DATA["login_url"])

    # Find form elements and fill them in
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


# ──────────────────────────────────────────────
# Test 1 – Page loads correctly
# ──────────────────────────────────────────────
class TestLoginPageLoad:
    """Verify the login page loads and displays expected content."""

    def test_page_title(self, browser):
        """The page title should contain 'The Internet'."""
        browser.get(UI_DATA["login_url"])
        # Wait until the page title is non-empty (avoids race condition)
        WebDriverWait(browser, 10).until(EC.title_contains("The Internet"))
        assert "The Internet" in browser.title, f"Unexpected title: {browser.title}"

    def test_login_heading_visible(self, browser):
        """The h2 heading should read 'Login Page'."""
        browser.get(UI_DATA["login_url"])
        heading = browser.find_element(By.TAG_NAME, "h2")
        assert heading.text == UI_DATA["expected_texts"]["login_heading"], (
            f"Expected '{UI_DATA['expected_texts']['login_heading']}', got '{heading.text}'"
        )


# ──────────────────────────────────────────────
# Test 2 – Successful login
# ──────────────────────────────────────────────
class TestSuccessfulLogin:
    """Verify that valid credentials lead to the secure area."""

    def test_login_success_message(self, browser):
        """After a valid login, a success flash message should appear."""
        creds = UI_DATA["valid_credentials"]
        _do_login(browser, creds["username"], creds["password"])

        flash = browser.find_element(By.ID, "flash")
        expected = UI_DATA["expected_texts"]["success_message"]
        assert expected in flash.text, f"Flash text: {flash.text}"

    def test_login_redirects_to_secure(self, browser):
        """The URL should change to /secure after a successful login."""
        creds = UI_DATA["valid_credentials"]
        _do_login(browser, creds["username"], creds["password"])

        assert "/secure" in browser.current_url, (
            f"Expected /secure in URL, got {browser.current_url}"
        )


# ──────────────────────────────────────────────
# Test 3 – Failed login
# ──────────────────────────────────────────────
class TestFailedLogin:
    """Verify that invalid credentials show an error message."""

    def test_login_failure_message(self, browser):
        """An error flash should appear when credentials are wrong."""
        creds = UI_DATA["invalid_credentials"]
        _do_login(browser, creds["username"], creds["password"])

        flash = browser.find_element(By.ID, "flash")
        expected = UI_DATA["expected_texts"]["failure_message"]
        assert expected in flash.text, f"Flash text: {flash.text}"

    def test_stays_on_login_page(self, browser):
        """The URL should still contain /login after a failed attempt."""
        creds = UI_DATA["invalid_credentials"]
        _do_login(browser, creds["username"], creds["password"])

        assert "/login" in browser.current_url, (
            f"Expected /login in URL, got {browser.current_url}"
        )


# ──────────────────────────────────────────────
# Test 4 – Data-driven login (parametrize)
# ──────────────────────────────────────────────
@pytest.mark.parametrize(
    "username, password, should_succeed",
    [
        ("tomsmith", "SuperSecretPassword!", True),
        ("wrong_user", "wrong_password", False),
        ("tomsmith", "bad_password", False),
        ("", "", False),
    ],
    ids=["valid-creds", "invalid-creds", "wrong-password", "empty-fields"],
)
def test_login_data_driven(browser, username, password, should_succeed):
    """
    Data-driven test: try several username/password combinations and verify
    that the outcome (success or failure) matches expectations.
    """
    _do_login(browser, username, password)

    if should_succeed:
        assert "/secure" in browser.current_url, "Login should have succeeded"
    else:
        assert "/login" in browser.current_url, "Login should have failed"
