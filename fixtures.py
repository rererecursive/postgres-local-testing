import pytest
import pandas as pd
from helpers import call_procedure

name = 'john'
message = 'Farewell'

@pytest.fixture
def call_sp_add_entry(db_connection):
    call_procedure(f"call etl.sp_add_entry('{message}', '{name}');", db_connection)
