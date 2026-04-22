from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchWindowException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from xpaths import login_xpaths


class LoginPage:
 # Set up login page once with driver, base URL, and element locators.
    def __init__(
        self,
        driver: WebDriver,
        base_url: str,
        timeout: int = 10,
    ):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout

        self.email_xpath = login_xpaths.EMAIL_INPUT
        self.password_xpath = login_xpaths.PASSWORD_INPUT
        self.submit_xpath = login_xpaths.SUBMIT_BUTTON

    MULTI_LOGIN_MODAL_BUTTON_XPATHS = [
        "//button[contains(text(), 'Continue')]",
        "//button[contains(text(), 'OK')]",
        "//button[contains(text(), 'Yes')]",
        "//button[contains(text(), 'Proceed')]",
    ]
    COOKIE_BANNER_ACTION_XPATHS = [
        "//div[@class='cookie-banner-container']/span[@class='link-text' and text()='Got it!']",
        "//div[contains(@class, 'cookie-banner-container')]//span[contains(@class, 'link-text') and text()='Got it!']",
    ]

    # Step 1: open the login page URL (works for base URL or direct /login).
    def open_login_page(self):
        if "login" in self.base_url.lower():
            self.driver.get(self.base_url)
        else:
            self.driver.get(self.base_url.rstrip("/") + "/login")

    # Utility: wait for an element to be visible, or return None if optional.
    def _get_visible(self, xpath: str, timeout: float | None = None, required: bool = True):
        if not self._is_window_alive():
            return None

        wait_timeout = self.timeout if timeout is None else timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
        except (TimeoutException, NoSuchWindowException):
            if required:
                raise RuntimeError(f"Could not locate visible element: {xpath}")
            return None

    # Step 2: enter email/password and click Sign in (with cookie-banner handling).
    def login(self, email: str, password: str):
        email_input = self._get_visible(self.email_xpath, timeout=4)
        password_input = self._get_visible(self.password_xpath, timeout=4)

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)

        submit_button = self._get_visible(self.submit_xpath, timeout=4)
        self.handle_cookie_banner()
        try:
            submit_button.click()
        except ElementClickInterceptedException:
            self.handle_cookie_banner()
            if self._is_window_alive():
                self.driver.execute_script("arguments[0].click();", submit_button)
        except NoSuchWindowException as exc:
            raise RuntimeError("Browser window closed during login submit.") from exc

    # Step 3: if a multiple-login popup appears, close it so flow can continue.
    def handle_multiple_logins_modal(self):
        for xpath in self.MULTI_LOGIN_MODAL_BUTTON_XPATHS:
            modal_button = self._get_visible(xpath, timeout=0.8, required=False)
            if modal_button is not None:
                modal_button.click()
                return

    # Remove cookie banner noise so clicks on the login button do not get blocked.
    def handle_cookie_banner(self):
        if not self._is_window_alive():
            return
        for xpath in self.COOKIE_BANNER_ACTION_XPATHS:
            cookie_button = self._get_visible(xpath, timeout=0.8, required=False)
            if cookie_button is not None:
                try:
                    cookie_button.click()
                    return
                except NoSuchWindowException:
                    return
                except Exception:
                    pass

        # Fallback: hide overlay if banner blocks clicks but no action button is found.
        try:
            banners = self.driver.find_elements(
                By.XPATH, "//div[contains(@class, 'cookie-banner-container')]"
            )
        except NoSuchWindowException:
            return
        for banner in banners:
            try:
                self.driver.execute_script("arguments[0].style.display='none';", banner)
            except NoSuchWindowException:
                return
            except Exception:
                continue

    # Safety check before any action: confirm browser window is still open.
    def _is_window_alive(self) -> bool:
        try:
            return bool(self.driver.window_handles)
        except NoSuchWindowException:
            return False
        except Exception:
            return False

    # Final login check: URL should leave login page and password field should disappear.
    def wait_until_logged_in(self, timeout: int = 20):
        """Wait until we are clearly past the login screen (URL + password field)."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: "login" not in d.current_url.lower()
            and len(d.find_elements(By.XPATH, "//input[@type='password']")) == 0
        )

#login flow.