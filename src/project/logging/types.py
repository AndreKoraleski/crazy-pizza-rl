from enum import Enum


class LogLevel(str, Enum):
    """
    Enum for log levels.
    """

    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LogFormat(str, Enum):
    """
    Enum for log output formats.
    """

    JSON = "json"
    CONSOLE = "console"
