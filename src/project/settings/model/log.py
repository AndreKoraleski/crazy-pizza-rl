from pydantic import Field

from project.logging.types import LogFormat, LogLevel
from project.settings.base import BaseModel


class LogSettings(BaseModel):
    """
    Settings related to logging.

    Attributes:
        level: LogLevel - The log level to use for the project.
        format: LogFormat - The format of logging output (json or console).
    """

    level: LogLevel = Field(
        default=LogLevel.INFO,
        description="The log level to use for the project.",
    )

    format: LogFormat = Field(
        default=LogFormat.CONSOLE,
        description="The format of logging output (json or console).",
    )
