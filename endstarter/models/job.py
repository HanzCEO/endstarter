"""Job and step models for endstarter."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Step(BaseModel):
    """A single step in a job."""

    model_config = {"populate_by_name": True}

    use: Optional[Literal["chrome"]] = None
    navigate: Optional[str] = None
    click: Optional[str] = None
    type: Optional[list[str]] = None
    submit: Optional[str] = None
    hover: Optional[str] = None
    assert_visible_in_page: Optional[str] = Field(
        default=None, validation_alias="assert-visible-in-page"
    )
    assert_title: Optional[str] = Field(default=None, validation_alias="assert-title")
    assert_element: Optional[str] = Field(
        default=None, validation_alias="assert-element"
    )
    wait: Optional[int | str] = None
    screenshot: Optional[str] = None
    execute_script: Optional[str] = Field(
        default=None, validation_alias="execute-script"
    )
    press_key: Optional[str] = Field(default=None, validation_alias="press-key")
    key_combo: Optional[list[str]] = Field(default=None, validation_alias="key-combo")
    mouse_click: Optional[list[int]] = Field(
        default=None, validation_alias="mouse-click"
    )
    right_click: Optional[list[int]] = Field(
        default=None, validation_alias="right-click"
    )
    mouse_move: Optional[list[int]] = Field(default=None, validation_alias="mouse-move")
    drag_and_drop: Optional[dict[str, str]] = Field(
        default=None, validation_alias="drag-and-drop"
    )
    resize: Optional[str | list[int]] = None

    def get_action(self) -> Optional[str]:
        """Return the action key that is set."""
        for field in type(self).model_fields:
            if getattr(self, field) is not None:
                return field
        return None


class Job(BaseModel):
    """A job definition parsed from YAML."""

    name: str
    type: Literal["test", "automation", "scrape"] = "test"
    timeout: int = 300
    jobs: list[Step] = Field(default_factory=list)
