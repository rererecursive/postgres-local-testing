import os
import pandas as pd
import pytest
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine

"""
The fixtures in this file are executed first -- before anything in fixtures.py
"""

DB_PARAMS = {
    'host': 'localhost',
    'port': '5432',
    'dbname': 'ea',
    'user': 'postgres',
    'password': 'password',
}
SCHEMAS_TO_DROP = [
    'etl',
    'raw',
]
engine = create_engine('postgresql://%s:%s@%s:%s/%s' % (DB_PARAMS['user'], DB_PARAMS['password'], DB_PARAMS['host'], DB_PARAMS['port'], DB_PARAMS['dbname']))


@pytest.fixture(scope='module')
def db_connection():
    conn = psycopg2.connect(**DB_PARAMS)
    conn.set_session(autocommit=True)
    yield conn
    conn.close()


# Run once per function
@pytest.fixture(autouse=True, scope='function')
def recreate_objects(drop_schemas, create_schemas, create_tables, create_views, create_procedures, copy_csv_files_into_tables):
    """
    Create all the database objects and load data into them from files on disk.
    """
    yield


@pytest.fixture
def create_schemas(db_connection):
    print("Creating schemas.")
    with open('objects/schemas/schemas.sql') as fh:
        contents = fh.read()
    with db_connection.cursor() as cursor:
        cursor.execute(contents)
    yield


@pytest.fixture
def create_tables(db_connection):
    print("Creating tables.")
    with open('objects/tables/tables.sql') as fh:
        contents = fh.read()
    with db_connection.cursor() as cursor:
        cursor.execute(contents)
    yield


@pytest.fixture
def create_views(db_connection):
    print("Creating views.")
    with open('objects/views/views.sql') as fh:
        contents = fh.read()
    with db_connection.cursor() as cursor:
        cursor.execute(contents)
    yield


@pytest.fixture
def create_procedures(db_connection):
    print("Creating procedures.")
    with open('objects/procedures/procedures.sql') as fh:
        contents = fh.read()
    with db_connection.cursor() as cursor:
        cursor.execute(contents)
    yield


# Run once per testing session
@pytest.fixture
def drop_schemas(db_connection):
    print(f"Dropping all schemas.")

    with db_connection.cursor() as cursor:
        for schema_name in SCHEMAS_TO_DROP:
            statement = sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE;").format(
                sql.Identifier(schema_name),
            )
            cursor.execute(statement)


@pytest.fixture
def copy_csv_files_into_tables(db_connection):
    """
    Copy Parquet files from directories into their respective tables.
    """
    base_path = 'data/inputs'

    # Traverse the directory structure: <schema>/<table>/<CSV files>
    print("Populating tables with data from CSV files.")
    for schema in os.listdir(base_path):
        schema_path = os.path.join(base_path, schema)

        if os.path.isdir(schema_path):
            for table in os.listdir(schema_path):
                table_path = os.path.join(schema_path, table)

                for file in os.listdir(table_path):
                    if not file.endswith('.csv'):
                        continue

                    csv_file = os.path.join(table_path, file)
                    print(f"+ Copying into {schema}.{table} from {csv_file}")
                    df = pd.read_csv(csv_file)
                    df.to_sql(schema=schema, name=table, con=engine, if_exists='append', index=False)
