from pydantic import Field

from project.settings.base import BaseSettings
from project.settings.model.log import LogSettings


class Settings(BaseSettings):
    """
    Main settings for the project. This is the main reader of the configuration, and should be used throughout the project.

    Attributes:
        log: LogSettings - Settings related to logging.
    """

    log: LogSettings = Field(
        default_factory=LogSettings,
        description="Settings related to logging.",
    )
