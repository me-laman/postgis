from post_gis.db import base_query


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