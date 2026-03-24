"""Custom exceptions for endstarter."""


class EndstarterError(Exception):
    """Base exception for endstarter."""


class DriverError(EndstarterError):
    """Raised when WebDriver encounters an error."""


class JobError(EndstarterError):
    """Raised when a job fails."""


class AssertionError(JobError):
    """Raised when an assertion fails."""


class ParseError(EndstarterError):
    """Raised when YAML parsing fails."""
