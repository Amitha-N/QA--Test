"""Minimal page object for candidate creation."""

import platform

from faker import Faker
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchWindowException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from xpaths import candidate_xpaths as xpaths


class CandidatePage:
    def __init__(
        self,
        driver: WebDriver,
        base_url: str,
        timeout: int = 12,
    ):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.fake = Faker()

        self.add_candidate_xpath = xpaths.ADD_CANDIDATE_BUTTON_XPATH
        self.create_candidate_xpath = xpaths.CREATE_CANDIDATE_BUTTON_XPATH

    def create_candidate(self):
        """Create one candidate with only required fields."""
        self._open_add_candidate_page()

        self._fill_by_xpath(xpaths.FIRST_NAME_INPUT, self.fake.first_name())
        self._fill_by_xpath(xpaths.LAST_NAME_INPUT, self.fake.last_name())
        self._fill_by_xpath(xpaths.EMAIL_INPUT, self.fake.unique.email())

        self._click_create()
        self._wait_for_submission()

    def _open_add_candidate_page(self):
        self.driver.get(f"{self.base_url}/candidates")
        WebDriverWait(self.driver, self.timeout).until(EC.url_contains("/candidates"))
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, self.add_candidate_xpath))
        ).click()
        WebDriverWait(self.driver, self.timeout).until(EC.url_contains("/candidates/add"))

    def _fill_by_xpath(self, xpath: str, value: str):
        element = WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
        )
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", element)

        select_all = Keys.COMMAND if platform.system() == "Darwin" else Keys.CONTROL
        element.send_keys(select_all, "a")
        element.send_keys(Keys.BACKSPACE)
        element.send_keys(value)

    def _click_create(self):
        WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable((By.XPATH, self.create_candidate_xpath))
        ).click()

    def _wait_for_submission(self):
        if not self._is_window_alive():
            raise RuntimeError("Browser window closed during candidate creation.")

        wait = WebDriverWait(self.driver, max(self.timeout, 45))
        try:
            wait.until(
                lambda d: "/candidates/add" not in (d.current_url or "") or self._has_blocking_error()
            )
        except TimeoutException:
            if self._has_blocking_error():
                raise RuntimeError(self._error_text() or "Candidate form error after submit.")
            raise TimeoutException("Timed out waiting to leave /candidates/add after Create candidate.")

        if self._has_blocking_error():
            raise RuntimeError(self._error_text() or "Candidate form error after submit.")

    def _has_blocking_error(self) -> bool:
        if self._error_text():
            return True
        return any(self.driver.find_elements(By.XPATH, xp) for xp in xpaths.FORM_FIELD_ERROR_XPATHS)

    def _error_text(self) -> str | None:
        for element in self.driver.find_elements(By.XPATH, xpaths.ERROR_MESSAGE_ALERT):
            if not element.is_displayed():
                continue
            text = (element.text or "").strip()
            if len(text) >= 2:
                return text
        return None

    def _is_window_alive(self) -> bool:
        try:
            return bool(self.driver.window_handles)
        except NoSuchWindowException:
            return False
        except Exception:
            return False
