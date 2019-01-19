import logging
import sys
import asyncio

from aiohttp import web

from post_gis.db import close_pg, init_pg
from post_gis.routes import setup_routes
from settings import get_config


def build_application():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    loop.run_until_complete(init_pg)
    # loop.run_until_complete(resources.setup(app))
    return app


async def init_app(argv=None):

    app = web.Application()

    app['config'] = get_config(argv)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    # setup views and routes
    setup_routes(app)

    return app


def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    app = init_app(argv)

    config = get_config(argv)
    web.run_app(app,
                host=config['host'],
                port=config['port'])


if __name__ == '__main__':
    main(sys.argv[1:])