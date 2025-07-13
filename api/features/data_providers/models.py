# Example model for a data provider
from pydantic import BaseModel
from typing import Any


from uuid import UUID


class DataProviderOut(BaseModel):
    id: UUID
    name: str
    role: str
    created_at: str
