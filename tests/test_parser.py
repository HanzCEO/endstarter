"""Tests for YAML parser."""

from endstarter.models.job import Step
from endstarter.parser.yaml_parser import parse_yaml_file


def test_parse_hello_world(tmp_path):
    """Test parsing hello world example."""
    yaml_content = """
name: Hello World
type: test
jobs:
  - use: chrome
  - navigate: https://example.com/
  - assert-visible-in-page: Welcome
"""
    path = tmp_path / "test.yml"
    path.write_text(yaml_content)

    job = parse_yaml_file(path)

    assert job.name == "Hello World"
    assert job.type == "test"
    assert len(job.jobs) == 3
    assert job.jobs[0].use == "chrome"
    assert job.jobs[1].navigate == "https://example.com/"
    assert job.jobs[2].assert_visible_in_page == "Welcome"


def test_parse_job_with_wait(tmp_path):
    """Test parsing job with wait action."""
    yaml_content = """
name: Wait Test
type: test
jobs:
  - use: chrome
  - navigate: https://example.com/
  - wait: 1000
  - assert-title: Example
"""
    path = tmp_path / "wait_test.yml"
    path.write_text(yaml_content)

    job = parse_yaml_file(path)

    assert job.name == "Wait Test"
    assert job.jobs[2].wait == 1000
    assert job.jobs[3].assert_title == "Example"


def test_parse_job_default_values(tmp_path):
    """Test that default values are set."""
    yaml_content = """
name: Minimal Job
jobs:
  - use: chrome
"""
    path = tmp_path / "minimal.yml"
    path.write_text(yaml_content)

    job = parse_yaml_file(path)

    assert job.type == "test"
    assert job.timeout == 300


def test_get_action_returns_correct_field():
    """Test that get_action returns the correct action name."""
    step = Step(navigate="https://example.com")
    assert step.get_action() == "navigate"

    step2 = Step(assert_visible_in_page="text")
    assert step2.get_action() == "assert_visible_in_page"

    step3 = Step(use="chrome")
    assert step3.get_action() == "use"
