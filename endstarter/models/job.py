"""Job and step models for endstarter."""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Step(BaseModel):
    """A single step in a job."""

    use: Optional[Literal["chrome"]] = None
    navigate: Optional[str] = None
    click: Optional[str] = None
    type: Optional[list[str]] = None
    submit: Optional[str] = None
    hover: Optional[str] = None
    assert_visible_in_page: Optional[str] = None
    assert_title: Optional[str] = None
    assert_element: Optional[str] = None
    wait: Optional[int] = None
    screenshot: Optional[str] = None
    execute_script: Optional[str] = None

    def get_action(self) -> Optional[str]:
        """Return the action key that is set."""
        for field in self.model_fields:
            if getattr(self, field) is not None:
                return field
        return None


class Job(BaseModel):
    """A job definition parsed from YAML."""

    name: str
    type: Literal["test", "automation", "scrape"] = "test"
    timeout: int = 300
    jobs: list[Step] = Field(default_factory=list)
