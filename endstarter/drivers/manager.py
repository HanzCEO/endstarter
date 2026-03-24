"""WebDriver manager for endstarter."""

from __future__ import annotations

from typing import cast

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

from endstarter.errors import DriverError

_driver: WebDriver | None = None


def get_driver(headless: bool = True) -> WebDriver:
    """Get or create the WebDriver singleton."""
    global _driver
    if _driver is None:
        _driver = _create_chrome_driver(headless)
    return _driver


def _create_chrome_driver(headless: bool = True) -> WebDriver:
    """Create a Chrome WebDriver instance."""
    try:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(5)
        return cast(WebDriver, driver)
    except Exception as e:
        raise DriverError(f"Failed to create Chrome driver: {e}") from e


def quit_driver() -> None:
    """Quit the WebDriver and reset the singleton."""
    global _driver
    if _driver is not None:
        _driver.quit()
        _driver = None
