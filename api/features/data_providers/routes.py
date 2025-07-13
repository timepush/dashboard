from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .models import DataProviderOut

from .services import get_data_providers_for_user
from uuid import UUID
from api.common.security import get_current_user_id

router = APIRouter(prefix="/api/data_providers", tags=["data_providers"])


@router.get("", response_model=List[DataProviderOut])
async def list_data_providers(user_id: UUID = Depends(get_current_user_id)):
    """Get all data providers for the authenticated user."""
    return await get_data_providers_for_user(user_id)
