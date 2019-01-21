import json


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
