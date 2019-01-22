from typing import Dict
import aiopg.sa
import sqlalchemy as sa
from sqlalchemy.engine import RowProxy
from aiopg.sa import SAConnection
from sqlalchemy.sql import func
from geoalchemy2 import functions

from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, DateTime, JSON
)
from geoalchemy2 import Geometry


meta = MetaData()

gis_polygon = Table(
    'gis_polygon', meta,

    Column('_created', DateTime(timezone=False), server_default=func.now()),
    Column('_updated', DateTime(timezone=False), onupdate=func.now()),
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('class_id', Integer),
    Column('name', String),
    Column('props', JSON),
    Column('geom', Geometry('POLYGON', srid=4326)),
)

base_query = sa.select([gis_polygon.c.id,
                       gis_polygon.c.name,
                       gis_polygon.c._created,
                       gis_polygon.c._updated,
                       gis_polygon.c.class_id,
                       gis_polygon.c.props,
                       functions.ST_AsText(gis_polygon.c.geom).label('geom')])


async def get_all(connection: SAConnection) -> RowProxy:

    result = await connection.execute(base_query)
    records = await result.fetchall()
    return records


async def get_record(connection: SAConnection, record_id: int) -> RowProxy:
    query = base_query.where(gis_polygon.c.id == record_id)

    result = await connection.execute(query)
    records = await result.first()
    return records


async def delete_record(connection: SAConnection, record_id: int) -> RowProxy:
    query = sa.delete(gis_polygon).where(gis_polygon.c.id == int(record_id))
    result = await connection.execute(query)
    if result.rowcount == 0:
        msg = "Record with id {} not found".format(record_id)
        raise RecordNotFound(msg)
    return result


async def add_record(connection: SAConnection, data):

    result = await connection.execute(
        gis_polygon.insert().values(data)
    )

    record = await result.fetchone()
    if not record:
        msg = "Record not inserted"
        raise RecordNotFound(msg)
    return record


async def update_record(connection: SAConnection,
                        record_id: int,
                        data):

    result = await connection.execute(
        gis_polygon.update().where(
            gis_polygon.c.id == int(record_id)).values(data))
    if result.rowcount == 0:
        msg = "Record with id {} not found".format(record_id)
        raise RecordNotFound(msg)
    return result


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

