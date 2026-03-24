"""User-facing output styling with rich."""

from rich.console import Console

console = Console()


def styled_pass(text: str) -> str:
    """Return green-styled PASS text."""
    return f"[bold green]PASS[/bold green]: {text}"


def styled_fail(text: str) -> str:
    """Return red-styled FAIL text."""
    return f"[bold red]FAIL[/bold red]: {text}"


def styled_error(text: str) -> str:
    """Return red-styled error text."""
    return f"[bold red]Error[/bold red]: {text}"


def styled_action(text: str) -> str:
    """Return cyan-styled action text."""
    return f"[cyan]{text}[/cyan]"


def styled_ok() -> str:
    """Return green OK text."""
    return "[bold green]OK[/bold green]"
