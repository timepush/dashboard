from fastapi import APIRouter

from api.features.auth.routes import router as auth_router
from api.features.data_providers.routes import router as data_providers_router
from api.features.data_sources.routes import router as data_sources_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(data_providers_router)
api_router.include_router(data_sources_router)
