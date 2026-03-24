"""Input actions for endstarter."""

from typing import Any

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

    def execute(self, keys: str | list[str]) -> None:
        """Press a key combination.

        Args:
            keys: List of key names (e.g., ["control", "c"]) or single key string
        """
        if isinstance(keys, str):
            keys = [keys]
        key_constants: list[str] = []
        for key in keys:
            key_constant = getattr(Keys, key.upper(), None)
            if key_constant is None:
                msg = f"Unknown key: {key}"
                raise ValueError(msg)
            key_constants.append(key_constant)
        chain = ActionChains(self.driver)
        for key_constant in key_constants:
            chain.key_down(key_constant)
        for key_constant in reversed(key_constants):
            chain.key_up(key_constant)
        chain.perform()


class MouseClickAction(BaseAction):
    """Click at screen coordinates."""

    def execute(self, coords: int | list[int]) -> None:
        """Click at coordinates.

        Args:
            coords: [x, y] screen coordinates or single integer
        """
        if isinstance(coords, int):
            coords = [coords]
        if len(coords) != 2:
            msg = "Coords must be [x, y]"
            raise ValueError(msg)
        x, y = coords
        ActionChains(self.driver).move_by_offset(x, y).click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()


class RightClickAction(BaseAction):
    """Right-click at screen coordinates."""

    def execute(self, coords: int | list[int]) -> None:
        """Right-click at coordinates.

        Args:
            coords: [x, y] screen coordinates or single integer
        """
        if isinstance(coords, int):
            coords = [coords]
        if len(coords) != 2:
            msg = "Coords must be [x, y]"
            raise ValueError(msg)
        x, y = coords
        ActionChains(self.driver).move_by_offset(x, y).context_click().perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()


class MouseMoveAction(BaseAction):
    """Move mouse to screen coordinates."""

    def execute(self, coords: int | list[int]) -> None:
        """Move mouse to screen coordinates.

        Args:
            coords: [x, y] screen coordinates or single integer
        """
        if isinstance(coords, int):
            coords = [coords]
        if len(coords) != 2:
            msg = "Coords must be [x, y]"
            raise ValueError(msg)
        x, y = coords
        ActionChains(self.driver).move_by_offset(x, y).perform()
        ActionChains(self.driver).move_by_offset(-x, -y).perform()


class DragAndDropAction(BaseAction):
    """Drag element and drop at target."""

    def execute(self, args: dict[str, str]) -> None:
        """Drag source element to target element.

        Args:
            args: {"source": "selector", "target": "selector"}
        """
        if "source" not in args or "target" not in args:
            msg = "drag_and_drop requires {source: selector, target: selector}"
            raise ValueError(msg)
        from selenium.webdriver.common.by import By

        source = self.driver.find_element(By.CSS_SELECTOR, args["source"])
        target = self.driver.find_element(By.CSS_SELECTOR, args["target"])
        ActionChains(self.driver).drag_and_drop(source, target).perform()


class WindowResizeAction(BaseAction):
    """Resize browser window."""

    def __init__(self, driver: Any, developer: bool = False) -> None:
        """Initialize with driver and optional developer flag."""
        super().__init__(driver)
        self._developer = developer

    def execute(self, value: str | list[int]) -> None:
        """Resize window.

        Args:
            value: "minimize", "maximize", "fullscreen", or [width, height]
        """
        if isinstance(value, str):
            if value == "minimize":
                self.driver.minimize_window()
            elif value == "maximize":
                self.driver.maximize_window()
                self._wait_for_maximize()
            elif value == "fullscreen":
                self.driver.fullscreen_window()
            else:
                msg = f"Unknown resize value: {value}"
                raise ValueError(msg)
        else:
            if len(value) != 2:
                msg = "Resize coords must be [width, height]"
                raise ValueError(msg)
            self.driver.set_window_size(value[0], value[1])
        if self._developer:
            size = self.driver.get_window_size()
            print(f"  [DEBUG] Window size: {size}")

    def _wait_for_maximize(self) -> None:
        """Wait for window to actually be maximized."""
        import time

        from selenium.webdriver.support.ui import WebDriverWait

        def is_maximized(driver: Any) -> bool:
            size = driver.get_window_size()
            return bool(size["width"] >= 1000)

        self.driver.maximize_window()
        time.sleep(0.5)
        try:
            WebDriverWait(self.driver, 1).until(is_maximized)
        except Exception:
            time.sleep(0.5)
            self.driver.maximize_window()
            time.sleep(0.3)
            try:
                WebDriverWait(self.driver, 1).until(is_maximized)
            except Exception:
                pass
            size = self.driver.get_window_size()
            if self._developer:
                print(f"  [DEBUG] Size after set_window_size: {size}")
            if size["width"] < 1000:
                self.driver.set_window_size(1920, 1080)
                time.sleep(1)


class PickFileAction(BaseAction):
    """Handle native OS file picker using pyautogui."""

    def execute(self, args: str | list[str | float]) -> None:
        """Pick file from native OS dialog.

        Args:
            args: file_path or [file_path, delay_seconds]
        """
        import time as time_module

        import pyautogui  # type: ignore[import-untyped]

        if isinstance(args, str):
            file_path = args
            delay = 0.5
        else:
            file_path = str(args[0])
            delay = float(args[1]) if len(args) > 1 else 0.5
        time_module.sleep(delay)
        pyautogui.write(file_path)
        pyautogui.press("enter")
