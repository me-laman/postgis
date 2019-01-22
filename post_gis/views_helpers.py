from aiohttp import web
from functools import partial

from shapely.geometry import Polygon
from shapely.ops import transform
import pyproj
from geoalchemy2.shape import from_shape


def build_update_data(req_data):

    props = req_data.get('props')
    name = req_data.get('name')
    class_id = req_data.get('class_id')
    geom = req_data.get('geom')
    from_coordinates = req_data.get('from_coordinates')

    return build_data(class_id, name, props, geom, from_coordinates)


def build_add_data(req_data):
    try:
        class_id = req_data['class_id']
        name = req_data['name']
        props = req_data['props']
        geom = req_data['geom']
        from_coordinates = req_data.get('from_coordinates')

    except KeyError as e:
        raise web.HTTPBadRequest(
            text='You have not specified {} value'.format(e)) from e
    else:
        return build_data(class_id, name, props, geom, from_coordinates)


def build_data(class_id, name, props, geom, from_coordinates):
    data = dict()

    try:
        if class_id:
            data.update({"class_id": int(class_id)})
        if name:
            data.update({"name": name})
        if props:
            data.update({"props": dict(props)})
        if geom:
            data.update({"geom": build_geom(geom, from_coordinates)})

    except (TypeError, ValueError) as e:
        raise web.HTTPBadRequest(
            text='You have not specified {} value'.format(e)) from e
    else:
        return data


def build_geom(geom_list, from_coordinates=None):
    polygon = Polygon(geom_list)
    if not from_coordinates:
        p = polygon
    else:
        proj = partial(pyproj.transform,
                       pyproj.Proj(init='epsg:4326'),
                       pyproj.Proj(init=from_coordinates))
        p = transform(proj, polygon)

    geom = from_shape(p, srid=4326)
    return geom