from typing import Any

from pydantic import BaseModel, Field


class Locator(BaseModel):
    state_class_locator: str

    params: dict[str, Any] = Field(default_factory=dict)

    class Config:
        allow_mutation = True
        validate_assignment = True
        validate_all = True  # default values should be validated too
        extra = 'forbid'

    def __init__(self, state_class_locator, **kwargs):
        super().__init__(state_class_locator=state_class_locator, **kwargs)


class FrozenLocator(Locator):
    class Config:
        allow_mutation = False
