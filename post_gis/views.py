import json
from aiohttp import web
from utils import alchemy_encoder
from post_gis.db import get_all, get_record, add_record, delete_record, update_record, RecordNotFound


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
    data = await request.json()
    db = request.app['db']
    try:
        class_id = int(data['class_id'])
        name = data['name']
        props = dict(data['props'])
        geom = data['geom']

    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(
            text='You have not specified {} value'.format(e)) from e

    async with db.acquire() as conn:
        try:
            result = await add_record(
                connection=conn,
                class_id=class_id,
                name=name,
                props=props,
                geom=geom
            )
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
    data = await build_data(req_data)

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


async def build_data(req_data):
    data = dict()
    props = req_data.get('props')
    name = req_data.get('name')
    class_id = req_data.get('class_id')
    geom = req_data.get('geom')
    try:
        if class_id:
            data.update({"class_id": int(class_id)})
        if name:
            data.update({"name": name})
        if props:
            data.update({"props": dict(props)})
        if geom:
            data.update({"geom": geom})

    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(
            text='You have not specified {} value'.format(e)) from e
    else:
        return data


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