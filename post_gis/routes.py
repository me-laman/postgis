from aiohttp import web
from post_gis.views import index


def setup_routes(app):
    app.router.add_get('/', index)


