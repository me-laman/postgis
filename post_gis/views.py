import json
import sqlalchemy as sa
from aiohttp import web
from utils import alchemy_encoder
from post_gis.db import gis_polygon
from geoalchemy2 import functions


async def index(request: web.Request) -> web.Response:

    db = request.app['db']

    query = (sa.select([gis_polygon.c.id,
                        gis_polygon.c.name,
                        gis_polygon.c._created,
                        gis_polygon.c._updated,
                        gis_polygon.c.class_id,
                        gis_polygon.c.props,
                        functions.ST_AsText(gis_polygon.c.geom).label('geom')]))

    async with db.acquire() as conn:
        result = await conn.execute(query)
        endpoint = await result.fetchall()

        headers = 'application/json'

        return web.json_response(
            text=json.dumps([dict(r) for r in endpoint],
                            default=alchemy_encoder),
            content_type=headers)