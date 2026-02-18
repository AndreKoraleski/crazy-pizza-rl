import logging
import structlog

from project.logging.renderer import get_renderer
from project.logging.types import LogFormat, LogLevel


def configure_logging(level: LogLevel, format: LogFormat) -> None:
    """
    Configure structlog for the application. Should be called once at startup.

    Args:
        level (LogLevel): The log level to use. Supported values are "CRITICAL", "ERROR", "WARNING", "INFO", and "DEBUG".
        format (LogFormat): The log format to use. Supported values are "json" and "console".
    """

    renderer = get_renderer(format)

    # Convert the log level string to a logging constant
    log_level = getattr(logging, level.value.upper())

    logging.basicConfig(
        level=log_level,
        format="%(message)s",
    )

    structlog.configure(
        processors=[
            # Add log level to the event dict
            structlog.stdlib.add_log_level,
            # Add logger name to the event dict
            structlog.stdlib.add_logger_name,
            # Add timestamp to the event dict
            structlog.processors.TimeStamper(fmt="iso"),
            # Add file, line, and function information to the event dict
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.LINENO,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                }
            ),
            # Extract stack information and add it to the event dict if the log level is ERROR or higher
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            # Render the final log message using the appropriate renderer
            renderer,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
