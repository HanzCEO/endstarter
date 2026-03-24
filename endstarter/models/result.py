"""Result models for endstarter."""

from datetime import datetime

from pydantic import BaseModel, Field


class StepResult(BaseModel):
    """Result of a single step."""

    action: str
    passed: bool
    duration: float
    error: str | None = None
    screenshot: str | None = None


class JobResult(BaseModel):
    """Result of a job execution."""

    name: str
    passed: bool = True
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime | None = None
    duration: float = 0.0
    steps: list[StepResult] = Field(default_factory=list)
    error: str | None = None

    def add_step(self, step_result: StepResult) -> None:
        """Add a step result."""
        self.steps.append(step_result)

    def fail(self, error: str) -> None:
        """Mark job as failed."""
        self.passed = False
        self.error = error
        self.completed_at = datetime.now()
        if self.started_at:
            self.duration = (self.completed_at - self.started_at).total_seconds()
