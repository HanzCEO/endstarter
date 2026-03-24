"""YAML parser for endstarter."""

import yaml
from pathlib import Path

from endstarter.errors import ParseError
from endstarter.models.job import Job, Step


def parse_yaml_file(path: str | Path) -> Job:
    """Parse a YAML file into a Job model.

    Args:
        path: Path to the YAML file.

    Returns:
        Parsed Job instance.

    Raises:
        ParseError: If the file cannot be parsed or is invalid.
    """
    try:
        file_path = Path(path)
        with open(file_path) as f:
            data = yaml.safe_load(f)
        if data is None:
            raise ParseError(f"Empty YAML file: {path}")
        return Job.model_validate(data)
    except yaml.YAMLError as e:
        raise ParseError(f"Invalid YAML in {path}: {e}") from e
    except Exception as e:
        raise ParseError(f"Failed to parse {path}: {e}") from e
