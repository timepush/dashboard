from api.common.security import get_current_user_id
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .models import DataProviderOut, DataProviderCreate
from .services import get_data_providers_for_user, create_data_provider_for_user, set_current_provider_for_user
from fastapi import Body


router = APIRouter(prefix="/api/data_providers", tags=["data_providers"])


@router.get("", response_model=List[DataProviderOut])
async def list_data_providers(user_id: UUID = Depends(get_current_user_id)):
    return await get_data_providers_for_user(user_id)


@router.post("/create", response_model=DataProviderOut, status_code=201)
async def create_provider(data: DataProviderCreate, user_id: UUID = Depends(get_current_user_id)):
    return await create_data_provider_for_user(user_id, data)


@router.post("/set_current", status_code=200)
async def set_current_provider(provider_id: UUID = Body(..., embed=True), user_id: UUID = Depends(get_current_user_id)):
    await set_current_provider_for_user(user_id, provider_id)
    return {"success": True}
