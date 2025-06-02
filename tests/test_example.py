import pytest
from selenium import webdriver

def test_open_page():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.google.com")
    assert "Google" in driver.title

    driver.quit()
