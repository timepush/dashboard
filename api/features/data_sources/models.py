from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID


class DataSourceCreateIn(BaseModel):
    name: str
    provider_id: UUID
    type_id: UUID
    component_id: UUID
    aggregation_type_ids: List[UUID] = []


class DataSourceOut(BaseModel):
    id: UUID
    name: str
    created_at: str
    type: str
    component_name: str
    aggregations: List[str]
