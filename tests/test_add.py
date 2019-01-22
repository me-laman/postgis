import json

from post_gis.db import base_query, gis_polygon
from tests.test_client import geom


async def test_add_record(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                    "class_id": 10,
                                    "name": "added name",
                                    "props": {"ten": 10, "eleven": 11},
                                    "geom": geom
                              },
                              )
    assert response.status == 200
    text = await response.text()

    assert json.loads(text) == {"id": 3}


async def test_add_record_another_coordinates(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                  "class_id": 10,
                                  "name": "added name",
                                  "props": {"ten": 10, "eleven": 11},
                                  "geom": geom,
                                  "from_coordinates": 'epsg:3857'
                              })

    assert response.status == 200
    text = await response.text()

    async with cli.server.app['db'].acquire() as conn:
        result = await conn.execute(base_query.where(gis_polygon.c.id == 3))
        records = await result.fetchone()

    assert json.loads(text) == {"id": 3}

    assert records['geom'] == 'POLYGON((0 -7.08115455161362e-10,' \
                              '0 557305.257274575' \
                              ',0 557305.257274575' \
                              ',556597.453966367 -7.08115455161362e-10' \
                              ',556597.453966367 -7.08115455161362e-10' \
                              ',0 -7.08115455161362e-10))'


async def test_add_record_without_class_id(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                    "name": "added name",
                                    "props": {"ten": 10, "eleven": 11},
                                    "geom": geom
                              },
                              )
    assert response.status == 400
    text = await response.text()
    assert text == "You have not specified 'class_id' value"


async def test_add_record_without_name(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                    "class_id": 10,
                                    "props": {"ten": 10, "eleven": 11},
                                    "geom": geom
                              },
                              )
    assert response.status == 400
    text = await response.text()
    assert text == "You have not specified 'name' value"


async def test_add_record_without_props(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                    "class_id": 10,
                                    "name": "added name",
                                    "geom": geom
                              },
                              )
    assert response.status == 400
    text = await response.text()
    assert text == "You have not specified 'props' value"


async def test_add_without_geom(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                    "class_id": 10,
                                    "name": "added name",
                                    "props": {"ten": 10, "eleven": 11},
                              },
                              )
    assert response.status == 400
    text = await response.text()
    assert text == "You have not specified 'geom' value"