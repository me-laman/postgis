import json


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