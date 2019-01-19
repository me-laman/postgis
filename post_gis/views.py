import json
from aiohttp import web
from utils import alchemy_encoder
from post_gis.db import GisPolygon


async def index(request: web.Request) -> web.Response:

    db = request.app['db']
    gis_polygon_table = GisPolygon.__table__

    async with db.acquire() as conn:
        result = await conn.execute(gis_polygon_table.select())
        endpoint = await result.fetchall()

        headers = 'application/json'

        return web.json_response(text=json.dumps([dict(r) for r in endpoint], default=alchemy_encoder), content_type=headers)