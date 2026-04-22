import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def _to_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "http://localhost:5000")
    login_email: str = os.getenv("LOGIN_EMAIL", "")
    login_password: str = os.getenv("LOGIN_PASSWORD", "")
    browser: str = os.getenv("BROWSER", "chrome").lower()
    headless: bool = _to_bool(os.getenv("HEADLESS"), default=False)
    default_wait_seconds: int = int(os.getenv("DEFAULT_WAIT_SECONDS", "10"))


settings = Settings()
