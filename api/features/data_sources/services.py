
from uuid import UUID
from typing import List
from .models import DataSourceOut
from api.db.pool import get_pool
from fastapi import HTTPException, status


async def create_data_source(user_id: UUID, name: str, provider_id: UUID, type_id: UUID, component_id: UUID, aggregation_type_ids: List[UUID]) -> UUID:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            # Check user membership in provider
            await cur.execute(
                '''
                SELECT role FROM data_provider_users
                WHERE user_id = %s AND data_provider_id = %s
                ''',
                (str(user_id), str(provider_id))
            )
            row = await cur.fetchone()
            if not row or row[0] not in ("owner", "editor"):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to add data sources to this provider.")

            # Insert data source
            await cur.execute(
                '''
                INSERT INTO data_sources (name, data_provider_id, data_source_type_id, component_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                ''',
                (name, str(provider_id), str(type_id), str(component_id))
            )
            ds_id = (await cur.fetchone())[0]
            # Insert aggregations
            if aggregation_type_ids:
                await cur.executemany(
                    '''
                    INSERT INTO data_source_aggregations (data_source_id, aggregation_type_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    ''',
                    [(str(ds_id), str(agg_id)) for agg_id in aggregation_type_ids]
                )
            return ds_id


async def get_data_sources_for_provider(user_id: UUID, provider_id: UUID) -> List[DataSourceOut]:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            # Only return data sources if user is a member of the provider
            await cur.execute(
                '''
                SELECT ds.id, ds.name, ds.created_at, dst.name, c.name
                FROM data_sources ds
                JOIN data_source_types dst ON ds.data_source_type_id = dst.id
                JOIN components c ON ds.component_id = c.id
                JOIN data_provider_users dpu ON ds.data_provider_id = dpu.data_provider_id
                WHERE dpu.user_id = %s AND ds.data_provider_id = %s
                ORDER BY ds.created_at DESC
                ''',
                (str(user_id), str(provider_id))
            )
            ds_rows = await cur.fetchall()

            # Get all aggregations for these data sources
            ds_ids = [str(row[0]) for row in ds_rows]
            aggregations_map = {}
            if ds_ids:
                await cur.execute(
                    '''
                    SELECT dsa.data_source_id, at.name
                    FROM data_source_aggregations dsa
                    JOIN aggregation_types at ON dsa.aggregation_type_id = at.id
                    WHERE dsa.data_source_id = ANY(%s)
                    ''',
                    (ds_ids,)
                )
                agg_rows = await cur.fetchall()
                for ds_id, at_name in agg_rows:
                    aggregations_map.setdefault(ds_id, []).append(at_name)

            return [
                DataSourceOut(
                    id=row[0],
                    name=row[1],
                    created_at=row[2].isoformat() if row[2] else None,
                    type=row[3],
                    component_name=row[4],
                    aggregations=aggregations_map.get(str(row[0]), [])
                ) for row in ds_rows
            ]
