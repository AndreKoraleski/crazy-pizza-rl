from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    """
    Base model for the project settings. All models that make a settings object should inherit from this class.
    """

    model_config = ConfigDict(
        extra="ignore",
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
    )
