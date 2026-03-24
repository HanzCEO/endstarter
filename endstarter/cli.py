"""CLI for endstarter."""

import sys
from pathlib import Path

import click

from endstarter import __version__
from endstarter.errors import EndstarterError, ParseError
from endstarter.parser.yaml_parser import parse_yaml_file
from endstarter.runner.job_runner import JobRunner


@click.command()
@click.argument("job_file", type=click.Path(exists=True, path_type=Path))
@click.option("--verbose", "-v", is_flag=True, help="Print step-by-step output")
@click.option("--headed", is_flag=True, default=False, help="Run in headed mode")
@click.version_option(version=__version__)
def cli(job_file: Path, verbose: bool, headed: bool) -> None:
    """Run an endstarter job from a YAML file."""
    try:
        job = parse_yaml_file(job_file)
        runner = JobRunner(job, verbose=verbose, headless=not headed)
        result = runner.run()
        if verbose:
            print()
        if result.passed:
            click.echo(f"PASS: {result.name} ({result.duration:.2f}s)")
            sys.exit(0)
        else:
            click.echo(f"FAIL: {result.name} - {result.error}")
            sys.exit(1)
    except ParseError as e:
        click.echo(f"Parse error: {e}", err=True)
        sys.exit(3)
    except EndstarterError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(2)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(2)
