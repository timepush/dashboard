# Example model for a data provider
from pydantic import BaseModel
from typing import Any


from uuid import UUID


class DataProviderOut(BaseModel):
    id: UUID
    name: str
    role: str
    created_at: str
    current: bool = False

# Model for creating a provider


class DataProviderCreate(BaseModel):
    name: str
