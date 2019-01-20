import aiopg.sa
import sqlalchemy as sa
from geoalchemy2 import functions

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


async def get_all(connection):
    query = sa.select([gis_polygon.c.id,
                       gis_polygon.c.name,
                       gis_polygon.c._created,
                       gis_polygon.c._updated,
                       gis_polygon.c.class_id,
                       gis_polygon.c.props,
                       functions.ST_AsText(gis_polygon.c.geom).label('geom')])
    result = await connection.execute(query)
    records = await result.fetchall()
    return records


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

