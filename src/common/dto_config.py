from humps.camel import case
from pydantic import BaseModel as BasePydanticModel


class BaseModel(BasePydanticModel):
    class Config:
        alias_generator = case
