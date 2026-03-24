"""Job and step models for endstarter."""

from typing import Annotated, Any, Literal, NotRequired, TypedDict

from pydantic import BaseModel, Field


class ActionType(BaseModel):
    """Action type definitions."""

    use: Literal["chrome"] = "chrome"
    navigate: NotRequired[str]
    click: NotRequired[str]
    type: NotRequired[list[str]]
    submit: NotRequired[str]
    hover: NotRequired[str]
    assert_visible_in_page: NotRequired[str]
    assert_title: NotRequired[str]
    assert_element: NotRequired[str]
    wait: NotRequired[int]
    screenshot: NotRequired[str]
    execute_script: NotRequired[str]


class Step(BaseModel):
    """A single step in a job."""

    use: Annotated[Literal["chrome"], Field(default=None, frozen=True)] = None
    navigate: str | None = None
    click: str | None = None
    type: list[str] | None = None
    submit: str | None = None
    hover: str | None = None
    assert_visible_in_page: str | None = None
    assert_title: str | None = None
    assert_element: str | None = None
    wait: int | None = None
    screenshot: str | None = None
    execute_script: str | None = None

    def get_action(self) -> str | None:
        """Return the action key that is set."""
        for field, value in self.model_fields.items():
            if getattr(self, field) is not None:
                return field
        return None


class Job(BaseModel):
    """A job definition parsed from YAML."""

    name: str
    type: Literal["test", "automation", "scrape"] = "test"
    timeout: int = 300
    jobs: list[Step] = Field(default_factory=list)
