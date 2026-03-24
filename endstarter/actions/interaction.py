"""Interaction actions for endstarter."""

from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait

from endstarter.actions.base import BaseAction
from endstarter.errors import JobError


def _is_css_selector(value: str) -> bool:
    """Detect if value is a CSS selector vs text content.

    CSS selectors start with # . [ or contain CSS metacharacters.
    Plain text (especially with spaces) is treated as text content.
    """
    if value.startswith(("#", ".", "[", "//")):
        return True
    css_chars = {"#", ".", "[", "]", ">", "+", "~", "*"}
    if any(c in value for c in css_chars):
        return True
    return False


class ClickAction(BaseAction):
    """Click an element by CSS selector or text."""

    def __init__(self, driver: Any, developer: bool = False) -> None:
        """Initialize the action with a WebDriver."""
        super().__init__(driver)
        self._developer = developer

    def execute(self, selector: str) -> None:
        """Click the element matching the selector or text."""
        if _is_css_selector(selector):
            element = self._wait_for_element(selector)
        else:
            element = self._find_by_text(selector)
        if self._developer:
            href = element.get_attribute("href") or ""
            tag = element.tag_name
            txt = element.text
            print(f"  [DEBUG] Click: <{tag}> text='{txt}' href='{href}'")
        element.click()

    def _wait_for_element(self, selector: str) -> Any:
        """Wait for element to be clickable."""
        try:
            return WebDriverWait(self.driver, 10).until(
                element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
        except Exception as e:
            raise JobError(f"Element not clickable: {selector}") from e

    def _find_by_text(self, text: str) -> Any:
        """Find element by text content."""
        if self._developer:
            print(f"  [DEBUG] Searching for text: '{text}'")
        anchor_xpath = f"//a[contains(normalize-space(.), '{text}')]"
        button_xpath = f"//button[contains(normalize-space(.), '{text}')]"
        generic_xpath = f"//*[contains(normalize-space(.), '{text}')]"
        for xpath in [anchor_xpath, button_xpath, generic_xpath]:
            if self._developer:
                print(f"  [DEBUG] Trying XPath: {xpath}")
            try:
                from selenium.webdriver.support import expected_conditions as EC

                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                if self._developer:
                    href = element.get_attribute("href") or ""
                    tag = element.tag_name
                    txt = element.text[:50]
                    print(f"  [DEBUG] Found: <{tag}> text='{txt}...' href='{href}'")
                return element
            except Exception as e:
                if self._developer:
                    print(f"  [DEBUG] Failed: {e}")
        raise JobError(f"Element not found by text: {text}")


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
    """Hover over an element by CSS selector or text."""

    def execute(self, selector: str) -> None:
        """Hover over the element."""
        from selenium.webdriver.common.action_chains import ActionChains

        if _is_css_selector(selector):
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
        else:
            element = self._find_by_text(selector)
        ActionChains(self.driver).move_to_element(element).perform()

    def _find_by_text(self, text: str) -> Any:
        """Find element by text content."""
        anchor_xpath = f"//a[contains(normalize-space(.), '{text}')]"
        button_xpath = f"//button[contains(normalize-space(.), '{text}')]"
        generic_xpath = f"//*[contains(normalize-space(.), '{text}')]"
        for xpath in [anchor_xpath, button_xpath, generic_xpath]:
            try:
                return self.driver.find_element(By.XPATH, xpath)
            except Exception:
                pass
        raise JobError(f"Element not found by text: {text}")
