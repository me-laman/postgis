from aiohttp import web


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