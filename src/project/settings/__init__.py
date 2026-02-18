from functools import cache

from project.settings.core import Settings


@cache
def get_settings() -> Settings:
    """
    Get the global settings instance. This is a singleton that is initialized on first access.

    Returns:
        Settings: The global settings instance.
    """
    return Settings()


__all__ = ["get_settings", "Settings"]