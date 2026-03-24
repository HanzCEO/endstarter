"""Interaction actions for endstarter."""

from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait

from endstarter.actions.base import BaseAction
from endstarter.errors import JobError


class ClickAction(BaseAction):
    """Click an element by CSS selector."""

    def execute(self, selector: str) -> None:
        """Click the element matching the selector."""
        element = self._wait_for_element(selector)
        element.click()

    def _wait_for_element(self, selector: str) -> Any:
        """Wait for element to be clickable."""
        try:
            return WebDriverWait(self.driver, 10).until(
                element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
        except Exception as e:
            raise JobError(f"Element not clickable: {selector}") from e


class TypeAction(BaseAction):
    """Type text into an input element."""

    def execute(self, args: list[str]) -> None:
        """Type text into elements.

        Args:
            args: [selector, text] pair
        """
        if len(args) != 2:
            raise JobError("type requires [selector, text]")
        selector, text = args
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.clear()
        element.send_keys(text)


class SubmitAction(BaseAction):
    """Submit a form."""

    def execute(self, selector: str) -> None:
        """Submit the form containing the element."""
        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        element.submit()


class HoverAction(BaseAction):
    """Hover over an element."""

    def execute(self, selector: str) -> None:
        """Hover over the element."""
        from selenium.webdriver.common.action_chains import ActionChains

        element = self.driver.find_element(By.CSS_SELECTOR, selector)
        ActionChains(self.driver).move_to_element(element).perform()
