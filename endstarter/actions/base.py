"""Base action class for endstarter."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class BaseAction(ABC):
    """Abstract base class for all actions."""

    def __init__(self, driver: "WebDriver") -> None:
        """Initialize the action with a WebDriver."""
        self._driver = driver

    @property
    def driver(self) -> "WebDriver":
        """Get the WebDriver instance."""
        return self._driver

    @abstractmethod
    def execute(self, *args: Any) -> None:
        """Execute the action."""
        ...
