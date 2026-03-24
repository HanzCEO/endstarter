"""Tests for interaction actions."""

from endstarter.actions.interaction import _is_css_selector


def test_is_css_selector_id():
    """Test CSS selector detection for id."""
    assert _is_css_selector("#login") is True


def test_is_css_selector_class():
    """Test CSS selector detection for class."""
    assert _is_css_selector(".btn-primary") is True


def test_is_css_selector_attribute():
    """Test CSS selector detection for attribute."""
    assert _is_css_selector("[data-testid='submit']") is True


def test_is_css_selector_xpath():
    """Test CSS selector detection for xpath."""
    assert _is_css_selector("//button[text()='Submit']") is True


def test_is_css_selector_text():
    """Test CSS selector detection for plain text."""
    assert _is_css_selector("Sign In") is False


def test_is_css_selector_text_with_space():
    """Test CSS selector detection for text with space."""
    assert _is_css_selector("Click here") is False


def test_is_css_selector_tag():
    """Test CSS selector detection for tag name is text."""
    assert _is_css_selector("button") is False


def test_is_css_selector_tag_class():
    """Test CSS selector detection for tag with class."""
    assert _is_css_selector("div.container") is True
