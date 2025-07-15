from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from .models import DataSourceOut, DataSourceCreateIn
from .services import get_data_sources_for_provider, create_data_source
from fastapi import status
from api.common.security import get_current_user_id

router = APIRouter(prefix="/api/data_sources", tags=["data_sources"])


@router.get("", response_model=List[DataSourceOut])
async def list_data_sources(provider_id: UUID, user_id: UUID = Depends(get_current_user_id)):
    return await get_data_sources_for_provider(user_id, provider_id)


@router.post("/create", status_code=201)
async def create_data_source_route(payload: DataSourceCreateIn,  user_id: UUID = Depends(get_current_user_id)):
    await create_data_source(
        user_id=user_id,
        name=payload.name,
        provider_id=payload.provider_id,
        type_id=payload.type_id,
        component_id=payload.component_id,
        aggregation_type_ids=payload.aggregation_type_ids
    )
    return {"success": True}
