import json
from aiohttp import web

from post_gis.db import get_all, get_record, add_record, delete_record, update_record, RecordNotFound
from post_gis.views_helpers import build_update_data, build_add_data
from utils import alchemy_encoder


async def get_records(request: web.Request) -> web.Response:

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


async def add_record_view(request: web.Request) -> web.Response:
    req_data = await request.json()
    db = request.app['db']
    data = build_add_data(req_data)

    async with db.acquire() as conn:
        try:
            result = await add_record(
                connection=conn,
                data=data)

        except RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

    headers = 'application/json'

    return web.json_response(
        text=json.dumps(dict(result),
                        default=alchemy_encoder),
        content_type=headers)


async def update_record_view(request: web.Request) -> web.Response:
    record_id = request.match_info['record_id']
    req_data = await request.json()
    db = request.app['db']
    data = build_update_data(req_data)

    async with db.acquire() as conn:
        try:
            result = await update_record(
                connection=conn,
                record_id=record_id,
                data=data)

        except (Exception, RecordNotFound) as e:
            raise web.HTTPNotFound(text=str(e))

    headers = 'application/json'

    return web.json_response(
        text=json.dumps(dict(result),
                        default=alchemy_encoder),
        content_type=headers)


async def delete_record_view(request: web.Request) -> web.Response:
    record_id = request.match_info['record_id']
    db = request.app['db']

    async with db.acquire() as conn:

        try:
            result = await delete_record(connection=conn, record_id=record_id)
        except RecordNotFound as e:
            raise web.HTTPNotFound(text=str(e))

        headers = 'application/json'

        return web.json_response(
            text=json.dumps(dict(result),
                            default=alchemy_encoder),
            content_type=headers)