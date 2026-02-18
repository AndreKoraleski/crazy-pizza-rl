from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Base settings for the project. All high-level settings should inherit from this class.
    Each settings class is a different reader of the same configuration, allowing for different views of it.
    """

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        env_nested_delimiter="__",
        env_prefix="PROJECT_",
        extra="ignore",
        validate_assignment=True,
        use_enum_values=True,
    )
