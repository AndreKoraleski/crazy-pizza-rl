from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer

from project.logging.types import LogFormat


def get_renderer(format: LogFormat) -> ConsoleRenderer | JSONRenderer:
    """
    Get the appropriate renderer based on the log format.

    Args:
        format (LogFormat): The log format to use. Supported values are "json" and "console".

    Returns:
        ConsoleRenderer | JSONRenderer: The appropriate renderer for the log format.
    """
    if format == LogFormat.JSON:
        return JSONRenderer()

    elif format == LogFormat.CONSOLE:
        return ConsoleRenderer()

    raise ValueError(f"Unsupported log format: {format}")
