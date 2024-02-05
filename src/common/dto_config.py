from humps.camel import case
from pydantic import BaseModel as BasePydanticModel, ConfigDict


class BaseModel(BasePydanticModel):
    model_config = ConfigDict(
        from_attributes=True, alias_generator=case, populate_by_name=True
    )
