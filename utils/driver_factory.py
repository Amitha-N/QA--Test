import os
import shutil

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService


def create_chrome_driver(headless: bool = False) -> webdriver.Chrome:
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    configured_driver = os.getenv("CHROMEDRIVER_PATH")
    if configured_driver:
        return webdriver.Chrome(service=ChromeService(configured_driver), options=options)

    path_driver = shutil.which("chromedriver")
    if path_driver:
        return webdriver.Chrome(service=ChromeService(path_driver), options=options)

    return webdriver.Chrome(options=options)
