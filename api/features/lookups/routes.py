from fastapi import APIRouter, Depends
from .models import LookupOut
from .services import get_data_source_types, get_aggregation_types, get_components
from typing import List

router = APIRouter(prefix="/api/lookups", tags=["lookups"])


@router.get("/data_source_types", response_model=List[LookupOut])
async def list_data_source_types():
    return await get_data_source_types()


@router.get("/aggregation_types", response_model=List[LookupOut])
async def list_aggregation_types():
    return await get_aggregation_types()


@router.get("/components", response_model=List[LookupOut])
async def list_components():
    return await get_components()
