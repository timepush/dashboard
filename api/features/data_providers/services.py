# Set the current provider for the user
from uuid import UUID
from typing import List
from .models import DataProviderOut, DataProviderCreate
from api.db.pool import get_pool


async def set_current_provider_for_user(user_id: UUID, provider_id: UUID) -> None:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                UPDATE users SET current_data_provider_id = %s WHERE id = %s
                """,
                (str(provider_id), str(user_id))
            )


async def get_data_providers_for_user(user_id: int) -> List[DataProviderOut]:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            # Fetch the user's current_data_provider_id
            await cur.execute(
                "SELECT current_data_provider_id FROM users WHERE id = %s",
                (str(user_id),)
            )
            current_row = await cur.fetchone()
            current_provider_id = current_row[0] if current_row else None

            await cur.execute("""
                SELECT dp.id, dp.name, dpu.role, dp.created_at
                FROM data_providers dp
                JOIN data_provider_users dpu ON dp.id = dpu.data_provider_id
                WHERE dpu.user_id = %s
                ORDER BY dp.name
            """, (str(user_id),))
            rows = await cur.fetchall()
            return [
                DataProviderOut(
                    id=row[0],
                    name=row[1],
                    role=row[2],
                    created_at=row[3].isoformat() if row[3] else None,
                    current=(str(row[0]) == str(current_provider_id))
                ) for row in rows
            ]


async def create_data_provider_for_user(user_id: UUID, data: DataProviderCreate) -> DataProviderOut:
    async with get_pool().connection() as conn:
        async with conn.transaction():
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    INSERT INTO data_providers (name)
                    VALUES (%s)
                    RETURNING id, name, created_at
                    """,
                    (data.name,)
                )
                row = await cur.fetchone()
                provider_id, name, created_at = row
                await cur.execute(
                    """
                    INSERT INTO data_provider_users (user_id, data_provider_id, role)
                    VALUES (%s, %s, 'owner')
                    """,
                    (str(user_id), str(provider_id))
                )
                # Set the new provider as current for the user
                await cur.execute(
                    """
                    UPDATE users SET current_data_provider_id = %s WHERE id = %s
                    """,
                    (str(provider_id), str(user_id))
                )
                return DataProviderOut(
                    id=provider_id,
                    name=name,
                    role="owner",
                    created_at=created_at.isoformat() if created_at else None,
                )
