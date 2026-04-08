"""
driver.py – Selenium WebDriver setup and teardown.

This module provides a helper function that creates a Chrome WebDriver
instance.  Using webdriver-manager means you don't have to download
chromedriver manually – it handles that for you.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver(headless: bool = True):
    """
    Create and return a Chrome WebDriver instance.

    Args:
        headless: If True, Chrome runs without opening a visible window.
                  This is useful for CI/CD pipelines. Set to False if you
                  want to watch the browser while debugging.

    Returns:
        A Selenium WebDriver object ready for use.
    """
    options = Options()

    if headless:
        # Run Chrome in headless mode (no visible browser window)
        options.add_argument("--headless=new")

    # Common flags that prevent crashes in restricted environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # webdriver-manager automatically downloads the matching chromedriver
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Give the browser a default wait time for finding elements
    driver.implicitly_wait(10)

    return driver
