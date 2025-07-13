from api.db.pool import get_pool
from .models import DataProviderOut
from typing import List


async def get_data_providers_for_user(user_id: int) -> List[DataProviderOut]:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT dp.id, dp.name, dpu.role, dp.created_at
                FROM data_providers dp
                JOIN data_provider_users dpu ON dp.id = dpu.data_provider_id
                WHERE dpu.user_id = %s
                ORDER BY dp.created_at DESC
            """, (str(user_id),))
            rows = await cur.fetchall()
            return [
                DataProviderOut(
                    id=row[0],
                    name=row[1],
                    role=row[2],
                    created_at=row[3].isoformat() if row[3] else None,
                ) for row in rows
            ]
