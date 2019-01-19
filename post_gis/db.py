import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column,
    Integer, String, DateTime, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry


Base = declarative_base()


class GisPolygon(Base):
    __tablename__ = 'gis_polygon'

    _created = Column('_created', DateTime(timezone=False))
    _updated = Column('_updated', DateTime(timezone=False))
    id = Column('id', Integer, primary_key=True, autoincrement=True, nullable=False)
    class_id = Column('class_id', Integer)
    name = Column('name', String)
    props = Column('props', JSON)
    geom = Column('geom', Geometry('POLYGON', srid=4326))


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

