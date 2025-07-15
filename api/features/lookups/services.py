from typing import List
from uuid import UUID
from api.db.pool import get_pool
from .models import LookupOut


async def get_data_source_types() -> List[LookupOut]:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, name, description FROM data_source_types ORDER BY name")
            rows = await cur.fetchall()
            return [LookupOut(id=row[0], name=row[1], description=row[2]) for row in rows]


async def get_aggregation_types() -> List[LookupOut]:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, name, description FROM aggregation_types ORDER BY name")
            rows = await cur.fetchall()
            return [LookupOut(id=row[0], name=row[1], description=row[2]) for row in rows]


async def get_components() -> List[LookupOut]:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, name, NULL as description FROM components ORDER BY name")
            rows = await cur.fetchall()
            return [LookupOut(id=row[0], name=row[1], description=row[2]) for row in rows]
