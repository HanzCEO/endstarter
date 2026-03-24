"""Utility actions for endstarter."""

import re
import time

from endstarter.actions.base import BaseAction


def parse_time(value: int | str) -> float:
    """Parse time value to seconds.

    Args:
        value: Milliseconds as int, or time string like "1s", "30m", "1h"

    Returns:
        Duration in seconds as float.

    Raises:
        ValueError: If format is invalid.
    """
    if isinstance(value, int):
        return value / 1000
    match = re.match(r"^(\d+)([smh])$", value.lower())
    if not match:
        msg = f"Invalid time format: {value}"
        raise ValueError(msg)
    number, unit = match.groups()
    seconds = int(number)
    if unit == "m":
        seconds *= 60
    elif unit == "h":
        seconds *= 3600
    return float(seconds)


class WaitAction(BaseAction):
    """Wait for a specified duration."""

    def execute(self, value: int | str) -> None:
        """Wait for the given duration.

        Args:
            value: Milliseconds as int, or time string like "1s", "30m", "1h"
        """
        time.sleep(parse_time(value))


class ScreenshotAction(BaseAction):
    """Take a screenshot of the current page."""

    def execute(self, path: str = "screenshot.png") -> None:
        """Take a screenshot and save to the given path."""
        self.driver.save_screenshot(path)


class ExecuteScriptAction(BaseAction):
    """Execute arbitrary JavaScript."""

    def execute(self, script: str) -> None:
        """Execute JavaScript in the browser context."""
        self.driver.execute_script(script)
