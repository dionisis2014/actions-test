import re
from enum import Enum
from typing import Annotated

from pydantic import AfterValidator, BaseModel as PydanticBaseModel, ConfigDict


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        validate_by_alias=True,
        validate_by_name=True,
        # use_enum_values=True,
        validate_default=True,
        strict=True,
        extra='forbid'
    )


# Why in gods green earth does pydantic not allow to have an optional, non-nullable field
# that is not defined by default? Hence, this monstrosity of a custom singleton type hint bellow.
class _Unset(Enum):
    token = None


Unset = _Unset.token
type Optional[T] = T | _Unset

type Required = None  # Required fields should always be defined like `Annotated[<actual type>, Required]`


def validate_regex_string(value: str) -> str:
    try:
        re.compile(value)
        return value
    except re.error:
        raise ValueError(f"Invalid regex string: {value}")


type Regex = Annotated[str, AfterValidator(validate_regex_string)]


def sanitize_string(string: str) -> str:
    # Replace whitespace character between non-whitespace ones with single underscore
    string = re.sub(r"(\S)\s+(\S)", r"\1_\2", string)
    # Replace non-valid characters with nothing (remove them)
    # This handles any whitespaces that are at the beginning or at the end
    string = re.sub(r"[^a-zA-Z0-9_-]+", '', string)
    return string
