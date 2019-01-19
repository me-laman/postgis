

async def test_index(cli, tables_and_data):
    response = await cli.get('/')
    assert response.status == 200
    assert '[]' in await response.text()


async def test_404(cli):
    response = await cli.get('/fake')
    assert response.status == 404
