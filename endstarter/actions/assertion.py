"""Assertion actions for endstarter."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from endstarter.actions.base import BaseAction
from endstarter.errors import AssertionError as EndstarterAssertionError


class AssertVisibleInPageAction(BaseAction):
    """Assert that text is visible in the page."""

    def execute(self, text: str) -> None:
        """Assert text is visible in page source."""
        if text not in self.driver.page_source:
            raise EndstarterAssertionError(f"Text not found in page: {text}")


class AssertTitleAction(BaseAction):
    """Assert the page title matches expected value."""

    def execute(self, expected: str) -> None:
        """Assert the page title."""
        actual = self.driver.title
        if actual != expected:
            raise EndstarterAssertionError(
                f"Title mismatch: expected '{expected}', got '{actual}'"
            )


class AssertElementAction(BaseAction):
    """Assert that an element exists in the page."""

    def execute(self, selector: str) -> None:
        """Assert element exists."""
        try:
            self.driver.find_element(By.CSS_SELECTOR, selector)
        except Exception:
            raise EndstarterAssertionError(f"Element not found: {selector}")
