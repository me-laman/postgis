from sqlalchemy import create_engine, MetaData

from post_gis.db import gis_polygon
from settings import BASE_DIR, get_config


DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"

ADMIN_DB_URL = DSN.format(
    user='postgres', password='postgres', database='postgres',
    host='localhost', port=5432
)

admin_engine = create_engine(ADMIN_DB_URL, isolation_level='AUTOCOMMIT')

USER_CONFIG_PATH = BASE_DIR / 'configs' / 'config.yaml'
USER_CONFIG = get_config(['-c', USER_CONFIG_PATH.as_posix()])
USER_DB_URL = DSN.format(**USER_CONFIG['postgres'])
user_engine = create_engine(USER_DB_URL)

TEST_CONFIG_PATH = BASE_DIR / 'configs' / 'config_test.yaml'
TEST_CONFIG = get_config(['-c', TEST_CONFIG_PATH.as_posix()])
TEST_DB_URL = DSN.format(**TEST_CONFIG['postgres'])
test_engine = create_engine(TEST_DB_URL)


def setup_db(config):

    db_name = config['database']
    db_user = config['user']
    db_pass = config['password']

    conn = admin_engine.connect()
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.execute("CREATE USER %s WITH PASSWORD '%s' SUPERUSER" % (db_user, db_pass))
    conn.execute("CREATE DATABASE %s ENCODING 'UTF8'" % db_name)
    conn.execute("GRANT ALL PRIVILEGES ON DATABASE %s TO %s" %
                 (db_name, db_user))
    conn.close()

    conn = test_engine.connect()
    conn.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    conn.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology")
    conn.close()


def teardown_db(config):

    db_name = config['database']
    db_user = config['user']

    conn = admin_engine.connect()
    conn.execute("""
      SELECT pg_terminate_backend(pg_stat_activity.pid)
      FROM pg_stat_activity
      WHERE pg_stat_activity.datname = '%s'
        AND pid <> pg_backend_pid();""" % db_name)
    conn.execute("DROP DATABASE IF EXISTS %s" % db_name)
    # conn.execute("DROP ROLE IF EXISTS %s" % db_user)
    conn.close()


def create_tables(engine=test_engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[gis_polygon])


def drop_tables(engine=test_engine):
    meta = MetaData()
    meta.drop_all(bind=engine, tables=[gis_polygon])


def sample_data(engine=test_engine):
    conn = engine.connect()
    conn.execute(gis_polygon.insert(), [
        {'_created': '2019-01-19 17:17:49.629',
         '_updated': '2019-01-19 17:17:49.629',
         'class_id': 1,
         'name': 'sample name',
         'props': {"one": 1, "two": 2},
         'geom': 'SRID=4326;POLYGON((0 0,1 0,1 1,0 1,0 0))'}
    ])

    conn.close()


if __name__ == '__main__':

    setup_db(USER_CONFIG['postgres'])
    create_tables(engine=user_engine)
