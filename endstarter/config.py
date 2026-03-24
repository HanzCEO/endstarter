"""Configuration settings for endstarter."""

import os
from pathlib import Path


def is_headless() -> bool:
    """Return whether to run in headless mode.

    Defaults to True unless ENDSTARTER_HEADLESS=0.
    """
    env = os.getenv("ENDSTARTER_HEADLESS", "1")
    return env not in ("0", "false", "no")


def get_screenshot_dir() -> Path:
    """Return the directory for screenshots."""
    path = os.getenv("ENDSTARTER_SCREENSHOT_DIR", "screenshots")
    return Path(path)
