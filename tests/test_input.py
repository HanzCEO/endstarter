"""Tests for input actions."""

from unittest.mock import MagicMock

from endstarter.actions.input import (
    DragAndDropAction,
    KeyComboAction,
    KeyPressAction,
    MouseClickAction,
    MouseMoveAction,
    RightClickAction,
    WindowResizeAction,
)


def test_key_press_action_unknown_key():
    """Test KeyPressAction raises on unknown key."""
    driver = MagicMock()
    action = KeyPressAction(driver)
    try:
        action.execute("UnknownKey")
    except ValueError as e:
        assert "Unknown key: UnknownKey" in str(e)


def test_key_press_action_valid_key():
    """Test KeyPressAction accepts valid key."""
    driver = MagicMock()
    action = KeyPressAction(driver)
    action.execute("Enter")
    driver.execute.assert_called_once()


def test_key_combo_action_unknown_key():
    """Test KeyComboAction raises on unknown key."""
    driver = MagicMock()
    action = KeyComboAction(driver)
    try:
        action.execute(["control", "UnknownKey"])
    except ValueError as e:
        assert "Unknown key: UnknownKey" in str(e)


def test_mouse_click_action_invalid_coords():
    """Test MouseClickAction raises on invalid coords."""
    driver = MagicMock()
    action = MouseClickAction(driver)
    try:
        action.execute([100])
    except ValueError as e:
        assert "Coords must be [x, y]" in str(e)


def test_right_click_action_invalid_coords():
    """Test RightClickAction raises on invalid coords."""
    driver = MagicMock()
    action = RightClickAction(driver)
    try:
        action.execute([100])
    except ValueError as e:
        assert "Coords must be [x, y]" in str(e)


def test_mouse_move_action_invalid_coords():
    """Test MouseMoveAction raises on invalid coords."""
    driver = MagicMock()
    action = MouseMoveAction(driver)
    try:
        action.execute([100])
    except ValueError as e:
        assert "Coords must be [x, y]" in str(e)


def test_drag_and_drop_action_missing_keys():
    """Test DragAndDropAction raises on missing keys."""
    driver = MagicMock()
    action = DragAndDropAction(driver)
    try:
        action.execute({"source": "#elem"})
    except ValueError as e:
        assert "drag_and_drop requires" in str(e)


def test_window_resize_action_minimize():
    """Test WindowResizeAction minimize."""
    driver = MagicMock()
    action = WindowResizeAction(driver)
    action.execute("minimize")
    driver.minimize_window.assert_called_once()


def test_window_resize_action_maximize():
    """Test WindowResizeAction maximize."""
    driver = MagicMock()
    action = WindowResizeAction(driver)
    action.execute("maximize")
    driver.maximize_window.assert_called_once()


def test_window_resize_action_fullscreen():
    """Test WindowResizeAction fullscreen."""
    driver = MagicMock()
    action = WindowResizeAction(driver)
    action.execute("fullscreen")
    driver.fullscreen_window.assert_called_once()


def test_window_resize_action_size():
    """Test WindowResizeAction set size."""
    driver = MagicMock()
    action = WindowResizeAction(driver)
    action.execute([1280, 720])
    driver.set_window_size.assert_called_once_with(1280, 720)


def test_window_resize_action_invalid_string():
    """Test WindowResizeAction raises on invalid string."""
    driver = MagicMock()
    action = WindowResizeAction(driver)
    try:
        action.execute("invalid")
    except ValueError as e:
        assert "Unknown resize value: invalid" in str(e)


def test_window_resize_action_invalid_coords():
    """Test WindowResizeAction raises on invalid coords."""
    driver = MagicMock()
    action = WindowResizeAction(driver)
    try:
        action.execute([1280])
    except ValueError as e:
        assert "Resize coords must be [width, height]" in str(e)
