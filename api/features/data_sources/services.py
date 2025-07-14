from api.db.pool import get_pool
from .models import DataSourceOut
from typing import List
from uuid import UUID


async def get_data_sources_for_provider(user_id: UUID, provider_id: UUID) -> List[DataSourceOut]:
    async with get_pool().connection() as conn:
        async with conn.cursor() as cur:
            # Only return data sources if user is a member of the provider
            await cur.execute(
                '''
                SELECT ds.id, ds.name, ds.created_at, dst.name
                FROM data_sources ds
                JOIN data_source_types dst ON ds.data_source_type_id = dst.id
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
                    aggregations=aggregations_map.get(str(row[0]), [])
                ) for row in ds_rows
            ]
