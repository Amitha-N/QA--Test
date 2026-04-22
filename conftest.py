import os
import shutil

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.candidate_page import CandidatePage
from pages.login_page import LoginPage


# Load values from `.env` so tests can run locally without hardcoding secrets.
load_dotenv()

# Base app and credential settings used by tests.
TEST_BASE_URL = os.getenv("TEST_BASE_URL", "http://localhost:5000/")
TEST_EMAIL = os.getenv("TEST_EMAIL", "")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "")
TIMEOUT = int(os.getenv("TIMEOUT", "10"))
HEADLESS = os.getenv("HEADLESS", "true").strip().lower() in {"1", "true", "yes", "on"}
CANDIDATE_COUNT = int(os.getenv("CANDIDATE_COUNT", "100"))

# Add custom CLI option: `--headed` to run with visible browser window.
def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed mode",
    )


@pytest.fixture()
# Create and return a Chrome WebDriver for each test.
def driver(request):
    # If user passes --headed, force non-headless even if env says HEADLESS=true.
    run_headed = request.config.getoption("--headed")
    headless = not run_headed and HEADLESS

    # Standard Chrome options for local + CI stability.
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Driver path priority:
    # 1) CHROMEDRIVER_PATH env
    # 2) chromedriver from PATH
    # 3) Selenium default discovery
    configured_driver = os.getenv("CHROMEDRIVER_PATH")
    if configured_driver:
        web_driver = webdriver.Chrome(service=Service(configured_driver), options=options)
    else:
        path_driver = shutil.which("chromedriver")
        if path_driver:
            web_driver = webdriver.Chrome(service=Service(path_driver), options=options)
        else:
            web_driver = webdriver.Chrome(options=options)

    # Keep implicit wait low; explicit waits in page object control timing.
    web_driver.implicitly_wait(1)
    yield web_driver
    # Always close browser after test to avoid leaked sessions.
    web_driver.quit()


@pytest.fixture()
# Provide a ready-to-use LoginPage object to tests.
def login_page(driver):
    return LoginPage(driver, base_url=TEST_BASE_URL)


@pytest.fixture()
# Log in once and return the authenticated browser instance.
def logged_in_driver(login_page):
    assert TEST_EMAIL and TEST_PASSWORD, "Set TEST_EMAIL and TEST_PASSWORD in UI_Automation/.env"
    login_page.open_login_page()
    login_page.login(TEST_EMAIL, TEST_PASSWORD)
    login_page.handle_multiple_logins_modal()
    login_page.wait_until_logged_in(timeout=20)
    return login_page.driver


@pytest.fixture()
# Provide a ready-to-use CandidatePage object with authenticated browser session.
def candidate_page(logged_in_driver):
    return CandidatePage(logged_in_driver, base_url=TEST_BASE_URL)


@pytest.fixture()
# Backward-compatible alias for older tests.
def logged_in_user(logged_in_driver):
    return logged_in_driver
