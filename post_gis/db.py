import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, DateTime, JSON
)
from geoalchemy2 import Geometry


meta = MetaData()

gis_polygon = Table(
    'gis_polygon', meta,

    Column('_created', DateTime(timezone=False)),
    Column('_updated', DateTime(timezone=False)),
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('class_id', Integer),
    Column('name', String),
    Column('props', JSON),
    Column('geom', Geometry('POLYGON', srid=4326)),
)


class RecordNotFound(Exception):
    """Requested record in database was not found"""


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()

