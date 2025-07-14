from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class DataSourceOut(BaseModel):
    id: UUID
    name: str
    created_at: str
    type: str
    aggregations: List[str]
