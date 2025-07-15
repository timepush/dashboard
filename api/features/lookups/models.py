from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class LookupOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
