from post_gis.views import (get_records, get_record_view,
                            add_record_view, delete_record_view,
                            update_record_view)


def setup_routes(app):
    app.router.add_get('/polygon', get_records)
    app.router.add_post('/polygon', add_record_view)

    app.router.add_get('/polygon/{record_id}', get_record_view)
    app.router.add_put('/polygon/{record_id}', update_record_view)

    app.router.add_delete('/polygon/{record_id}', delete_record_view)




