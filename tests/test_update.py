from post_gis.db import base_query, gis_polygon
from tests.test_client import geom


async def test_index_update_record_class_id(cli, sample_data_fixture):
    id = 1
    class_id = 100
    response = await cli.put(f'/polygon/{id}',
                             json={
                                 "class_id": class_id,
                             })
    assert response.status == 200

    async with cli.server.app['db'].acquire() as conn:
        result = await conn.execute(base_query.where(gis_polygon.c.id == id))
        records = await result.fetchone()

    assert records['class_id'] == class_id
    # new updated data
    assert sample_data_fixture[0]['_updated'] != records['_updated']


async def test_index_update_record_props(cli, sample_data_fixture):
    id = 1
    props = {'props_key': 'new props value'}

    response = await cli.put(f'/polygon/{id}',
                             json={
                                 "props": props,
                             })
    assert response.status == 200

    async with cli.server.app['db'].acquire() as conn:
        result = await conn.execute(base_query.where(gis_polygon.c.id == id))
        records = await result.fetchone()
    assert records['props'] == props


async def test_index_update_other_coordinates(cli, sample_data_fixture):
    id = 1
    props = {'props_key': 'new props value'}

    response = await cli.put(f'/polygon/{id}',
                             json={
                                 "geom": geom,
                                 "from_coordinates": 'epsg:3857'
                             })
    assert response.status == 200

    async with cli.server.app['db'].acquire() as conn:
        result = await conn.execute(base_query.where(gis_polygon.c.id == id))
        records = await result.fetchone()
    assert records['geom'] == 'POLYGON((0 -7.08115455161362e-10,' \
                              '0 557305.257274575,' \
                              '0 557305.257274575,' \
                              '556597.453966367 -7.08115455161362e-10' \
                              ',556597.453966367 -7.08115455161362e-10' \
                              ',0 -7.08115455161362e-10))'


async def test_index_update_record_not_valid(cli, sample_data_fixture):
    id = 1
    class_id = 'non valid'

    response = await cli.put(f'/polygon/{id}',
                             json={
                                 "class_id": class_id,
                             })
    assert response.status == 400
    text = await response.text()
    assert text == "You have not specified invalid literal for int() with base 10: 'non valid' value"


async def test_index_update_record_not_valid_props(cli, sample_data_fixture):
    id = 1
    props = 'should be dict'

    response = await cli.put(f'/polygon/{id}',
                             json={
                                 "props": props,
                             })
    assert response.status == 400
    text = await response.text()
    assert text == "You have not specified dictionary update sequence element #0 has length 1; 2 is required value"


async def test_index_update_geom_not_valid(cli, sample_data_fixture):
    id = 1
    geom = 'non valid'

    response = await cli.put(f'/polygon/{id}',
                             json={
                                 "geom": geom,
                             })
    assert response.status == 400
    text = await response.text()
    assert text == "You have not specified Polygon value"
