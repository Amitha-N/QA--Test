from config.settings import settings
from pages.login_page import LoginPage
from utils.driver_factory import create_chrome_driver


def main() -> None:
    driver = create_chrome_driver(headless=settings.headless)
    driver.implicitly_wait(settings.default_wait_seconds)
    try:
        page = LoginPage(driver, base_url=settings.base_url, timeout=settings.default_wait_seconds)
        page.open_login_page()
        page.login(settings.login_email, settings.login_password)
        print(f"Login submitted. Current URL: {driver.current_url}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
