import json
from aiohttp import web
from utils import alchemy_encoder
from post_gis.db import get_all, get_record


async def index(request: web.Request) -> web.Response:

    db = request.app['db']

    async with db.acquire() as conn:
        result = await get_all(connection=conn)

        headers = 'application/json'

        return web.json_response(
            text=json.dumps([dict(r) for r in result],
                            default=alchemy_encoder),
            content_type=headers)


async def get_record_view(request: web.Request) -> web.Response:
    record_id = request.match_info['record_id']
    db = request.app['db']

    async with db.acquire() as conn:
        result = await get_record(connection=conn, record_id=record_id)

        headers = 'application/json'

        return web.json_response(
            text=json.dumps(dict(result),
                            default=alchemy_encoder),
            content_type=headers)