"""Navigation actions for endstarter."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from endstarter.actions.base import BaseAction


class NavigateAction(BaseAction):
    """Navigate to a URL."""

    def execute(self, url: str) -> None:
        """Navigate to the given URL."""
        self.driver.get(url)


class BackAction(BaseAction):
    """Navigate back in browser history."""

    def execute(self) -> None:
        """Go back to previous page."""
        self.driver.back()


class ForwardAction(BaseAction):
    """Navigate forward in browser history."""

    def execute(self) -> None:
        """Go forward to next page."""
        self.driver.forward()


class RefreshAction(BaseAction):
    """Refresh the current page."""

    def execute(self) -> None:
        """Refresh current page."""
        self.driver.refresh()
