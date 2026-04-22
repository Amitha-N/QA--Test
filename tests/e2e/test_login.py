"""
Simple login: open the app login URL (local from `.env`), enter email and password, submit.

Configure in `UI_Automation/.env`:
  `TEST_BASE_URL` — e.g. `http://localhost:5000/`
  `TEST_EMAIL`, `TEST_PASSWORD`

Run (from `UI_Automation/`):
    pytest tests/e2e/test_login.py -v
    pytest tests/e2e/test_login.py -v --headed
"""

from conftest import TEST_EMAIL, TEST_PASSWORD


class TestLogin:
    """Minimal happy-path login."""

    # Smoke test: make sure login works with credentials from .env.
    def test_login_with_email_and_password(self, driver, login_page):
        """Go to login page -> email + password from env -> submit -> land on app (dashboard)."""
        assert TEST_EMAIL and TEST_PASSWORD, (
            "Set TEST_EMAIL and TEST_PASSWORD in .env or environment variables"
        )

        login_page.open_login_page()
        login_page.login(TEST_EMAIL, TEST_PASSWORD)
        login_page.handle_multiple_logins_modal()
        login_page.wait_until_logged_in(timeout=12)
