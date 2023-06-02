"""Stricter models to avoid mistaken attribute names."""
from pydantic import BaseModel


class StrictBaseModel(BaseModel):

    class Config:  # noqa: WPS306, WPS431
        extra = 'forbid'
