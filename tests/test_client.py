import json
from post_gis.db import base_query, gis_polygon


async def test_index(cli, tables_and_data):
    response = await cli.get('/polygon')
    assert response.status == 200
    assert '[]' in await response.text()


async def test_404(cli):
    response = await cli.get('/fake')
    assert response.status == 404


async def test_index_with_data(cli, sample_data_fixture):
    response = await cli.get('/polygon')
    assert response.status == 200
    text = await response.text()
    assert [
               {"_created": "2019-01-19T17:17:49.629000",
                "_updated": "2019-01-19T17:17:49.629000",
                "id": 1, "class_id": 1,
                "name": "sample name",
                "props": {"one": 1, "two": 2},
                "geom": 'POLYGON((0 0,1 0,1 1,0 1,0 0))'
                },
               {"_created": "2019-01-19T17:20:49.629000",
                "_updated": "2019-01-19T17:20:49.629000",
                "id": 2, "class_id": 2,
                "name": "sample name 2",
                "props": {"three": 3, "four": 4},
                "geom": 'POLYGON((0 0,2 0,2 2,0 2,0 0))'
                }
           ] == json.loads(text)


async def test_index_first_record(cli, sample_data_fixture):
    response = await cli.get('/polygon/1')
    assert response.status == 200
    text = await response.text()
    assert {"_created": "2019-01-19T17:17:49.629000",
            "_updated": "2019-01-19T17:17:49.629000",
            "id": 1, "class_id": 1,
            "name": "sample name",
            "props": {"one": 1, "two": 2},
            "geom": 'POLYGON((0 0,1 0,1 1,0 1,0 0))'
            } == json.loads(text)


async def test_add_record(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                    "class_id": 10,
                                    "name": "added name",
                                    "props": {"ten": 10, "eleven": 11},
                                    "geom": "SRID=4326;POLYGON((0 0,5 0,5 5,0 5,0 0))"
                              },
                              )
    assert response.status == 200
    text = await response.text()
    assert json.loads(text) == {"id": 3}


async def test_add_record_without_class_id(cli, sample_data_fixture):
    response = await cli.post('/polygon',
                              json={
                                    "name": "added name",
                                    "props": {"ten": 10, "eleven": 11},
                                    "geom": "SRID=4326;POLYGON((0 0,5 0,5 5,0 5,0 0))"
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
                                    "geom": "SRID=4326;POLYGON((0 0,5 0,5 5,0 5,0 0))"
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
                                    "geom": "SRID=4326;POLYGON((0 0,5 0,5 5,0 5,0 0))"
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


async def test_index_delete_record(cli, sample_data_fixture):
    response = await cli.delete('/polygon/1')
    assert response.status == 200

    async with cli.server.app['db'].acquire() as conn:

        result = await conn.execute(base_query)
        records = await result.fetchall()
    assert len(records) == 1


async def test_index_delete_not_existing_record(cli, sample_data_fixture):
    response = await cli.delete('/polygon/252')
    assert response.status == 404

    text = await response.text()
    assert text == "Record with id 252 not found"

    async with cli.server.app['db'].acquire() as conn:

        result = await conn.execute(base_query)
        records = await result.fetchall()
    assert len(records) == 2


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
