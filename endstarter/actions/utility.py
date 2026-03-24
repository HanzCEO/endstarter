"""Utility actions for endstarter."""

import time
from selenium.webdriver.remote.webdriver import WebDriver

from endstarter.actions.base import BaseAction


class WaitAction(BaseAction):
    """Wait for a specified duration."""

    def execute(self, milliseconds: int) -> None:
        """Wait for the given duration in milliseconds."""
        time.sleep(milliseconds / 1000)


class ScreenshotAction(BaseAction):
    """Take a screenshot of the current page."""

    def execute(self, path: str = "screenshot.png") -> str:
        """Take a screenshot and save to the given path."""
        self.driver.save_screenshot(path)
        return path


class ExecuteScriptAction(BaseAction):
    """Execute arbitrary JavaScript."""

    def execute(self, script: str) -> None:
        """Execute JavaScript in the browser context."""
        self.driver.execute_script(script)
