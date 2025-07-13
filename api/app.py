from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import api_router
from api.db.pool import get_pool, init_pool
from api.common.exceptions import register_exception_handlers

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    init_pool()
    await get_pool().open()


@app.on_event("shutdown")
async def shutdown_event():
    await get_pool().close()


@app.get("/", tags=["Hello"])
def hello_world():
    return {"message": "Hello, world!"}
