from fastapi import APIRouter, Depends
from uuid import UUID
from typing import List
from .models import DataSourceOut
from .services import get_data_sources_for_provider
from api.common.security import get_current_user_id

router = APIRouter(prefix="/api/data_sources", tags=["data_sources"])


@router.get("", response_model=List[DataSourceOut])
async def list_data_sources(provider_id: UUID,    user_id: UUID = Depends(get_current_user_id)):
    return await get_data_sources_for_provider(user_id, provider_id)
