"""Job runner for endstarter."""

import time
from datetime import datetime
from typing import Any

from rich import print as rprint

from endstarter.actions.assertion import (
    AssertElementAction,
    AssertTitleAction,
    AssertVisibleInPageAction,
)
from endstarter.actions.interaction import (
    ClickAction,
    HoverAction,
    SubmitAction,
    TypeAction,
)
from endstarter.actions.navigation import (
    NavigateAction,
)
from endstarter.actions.utility import ExecuteScriptAction, ScreenshotAction, WaitAction
from endstarter.drivers.manager import get_driver, quit_driver
from endstarter.errors import AssertionError as EndstarterAssertionError
from endstarter.errors import JobError
from endstarter.models.job import Job, Step
from endstarter.models.result import JobResult, StepResult
from endstarter.output import styled_action, styled_ok


class JobRunner:
    """Runs a job and collects results."""

    def __init__(
        self, job: Job, *, verbose: bool = False, headless: bool = True
    ) -> None:
        """Initialize the job runner."""
        self._job = job
        self._verbose = verbose
        self._headless = headless

    def run(self) -> JobResult:
        """Execute the job and return results."""
        result = JobResult(name=self._job.name, passed=True)
        driver = get_driver(headless=self._headless)
        for step in self._job.jobs:
            step_result = self._execute_step(step, driver)
            result.add_step(step_result)
            if not step_result.passed:
                result.fail(step_result.error or "Step failed")
                break
        if result.passed:
            result.completed_at = datetime.now()
            if result.started_at:
                result.duration = (
                    result.completed_at - result.started_at
                ).total_seconds()
        quit_driver()
        return result

    def _execute_step(self, step: Step, driver: Any) -> StepResult:
        """Execute a single step and return its result."""
        action_name = step.get_action()
        if not action_name:
            return StepResult(
                action="unknown", passed=False, duration=0.0, error="No action in step"
            )
        start = time.time()
        try:
            self._dispatch(action_name, step, driver)
            duration = time.time() - start
            return StepResult(action=action_name, passed=True, duration=duration)
        except EndstarterAssertionError as e:
            duration = time.time() - start
            return StepResult(
                action=action_name, passed=False, duration=duration, error=str(e)
            )
        except Exception as e:
            duration = time.time() - start
            return StepResult(
                action=action_name, passed=False, duration=duration, error=str(e)
            )

    def _dispatch(self, action: str, step: Step, driver: Any) -> None:
        """Dispatch action to the appropriate handler."""
        if self._verbose:
            rprint(f"  [{styled_action(action)}] ", end="", flush=True)
        handlers: dict[str, Any] = {
            "use": self._handle_use,
            "navigate": self._handle_navigate,
            "click": self._handle_click,
            "type": self._handle_type,
            "submit": self._handle_submit,
            "hover": self._handle_hover,
            "assert_visible_in_page": self._handle_assert_visible_in_page,
            "assert_title": self._handle_assert_title,
            "assert_element": self._handle_assert_element,
            "wait": self._handle_wait,
            "screenshot": self._handle_screenshot,
            "execute_script": self._handle_execute_script,
        }
        handler = handlers.get(action)
        if not handler:
            raise JobError(f"Unknown action: {action}")
        handler(step, driver)
        if self._verbose:
            rprint(styled_ok())

    def _handle_use(self, step: Step, driver: Any) -> None:
        """Handle browser selection."""
        if step.use:
            pass

    def _handle_navigate(self, step: Step, driver: Any) -> None:
        """Handle navigation."""
        if step.navigate:
            action = NavigateAction(driver)
            action.execute(step.navigate)

    def _handle_click(self, step: Step, driver: Any) -> None:
        """Handle click."""
        if step.click:
            action = ClickAction(driver)
            action.execute(step.click)

    def _handle_type(self, step: Step, driver: Any) -> None:
        """Handle type."""
        if step.type:
            action = TypeAction(driver)
            action.execute(step.type)

    def _handle_submit(self, step: Step, driver: Any) -> None:
        """Handle submit."""
        if step.submit:
            action = SubmitAction(driver)
            action.execute(step.submit)

    def _handle_hover(self, step: Step, driver: Any) -> None:
        """Handle hover."""
        if step.hover:
            action = HoverAction(driver)
            action.execute(step.hover)

    def _handle_assert_visible_in_page(self, step: Step, driver: Any) -> None:
        """Handle assert visible in page."""
        if step.assert_visible_in_page:
            action = AssertVisibleInPageAction(driver)
            action.execute(step.assert_visible_in_page)

    def _handle_assert_title(self, step: Step, driver: Any) -> None:
        """Handle assert title."""
        if step.assert_title:
            action = AssertTitleAction(driver)
            action.execute(step.assert_title)

    def _handle_assert_element(self, step: Step, driver: Any) -> None:
        """Handle assert element."""
        if step.assert_element:
            action = AssertElementAction(driver)
            action.execute(step.assert_element)

    def _handle_wait(self, step: Step, driver: Any) -> None:
        """Handle wait."""
        if step.wait:
            action = WaitAction(driver)
            action.execute(step.wait)

    def _handle_screenshot(self, step: Step, driver: Any) -> None:
        """Handle screenshot."""
        if step.screenshot:
            action = ScreenshotAction(driver)
            action.execute(step.screenshot)

    def _handle_execute_script(self, step: Step, driver: Any) -> None:
        """Handle execute script."""
        if step.execute_script:
            action = ExecuteScriptAction(driver)
            action.execute(step.execute_script)
