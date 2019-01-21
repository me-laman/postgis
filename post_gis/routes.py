from aiohttp import web
from post_gis.views import index, get_record_view, add_record_view


def setup_routes(app):
    app.router.add_get('/polygon', index)
    app.router.add_post('/polygon', add_record_view)

    app.router.add_get('/polygon/{record_id}', get_record_view)



