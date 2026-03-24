"""Input actions for endstarter."""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from endstarter.actions.base import BaseAction


class KeyPressAction(BaseAction):
    """Press a single key."""

    def execute(self, key: str) -> None:
        """Press a key on the keyboard.

        Args:
            key: Key name (Enter, Escape, Tab, ArrowUp, ArrowDown, etc.)
        """
        key_constant = getattr(Keys, key.upper(), None)
        if key_constant is None:
            msg = f"Unknown key: {key}"
            raise ValueError(msg)
        ActionChains(self.driver).send_keys(key_constant).perform()


class KeyComboAction(BaseAction):
    """Press a key combination."""

    def execute(self, keys: list[str]) -> None:
        """Press a key combination.

        Args:
            keys: List of key names (e.g., ["ctrl", "c"] for Ctrl+C)
        """
        chain = ActionChains(self.driver)
        for key in keys:
            key_constant = getattr(Keys, key.upper(), None)
            if key_constant is None:
                msg = f"Unknown key: {key}"
                raise ValueError(msg)
            chain.key_down(key_constant)
        for key in reversed(keys):
            key_constant = getattr(Keys, key.upper(), None)
            chain.key_up(key_constant)
        chain.perform()
