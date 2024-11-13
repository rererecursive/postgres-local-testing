import pytest
from fixtures import call_sp_add_entry
from helpers import query_table, call_procedure, read_expected_csv

names = [
    'roger',
    'mike',
]

# Test 1: call the procedure with the fixture passed as a parameter
def test_sp_add_entry(call_sp_add_entry, db_connection):
    actual = query_table(f"select message, username from etl.entries;", db_connection)
    expected = read_expected_csv(f'test_sp_add_entry/data.csv')

    assert len(actual) == len(expected)
    assert actual.astype(str).equals(expected.astype(str))


# Test 2: call the procedure manually - once per name in a list
@pytest.mark.parametrize("name", names)
def test_sp_add_multiple_entries(name, db_connection):
    call_procedure(f"call etl.sp_add_entry('Hello', '{name}')", db_connection)

    actual = query_table(f"select message, username from etl.entries;", db_connection)
    expected = read_expected_csv(f'test_sp_add_multiple_entries/{name}.csv')

    assert len(actual) == len(expected)
    assert actual.astype(str).equals(expected.astype(str))


# Test 3: query the view
def test_view_translate(db_connection):
    actual = query_table(f"select message from etl.translate;", db_connection)
    expected = read_expected_csv(f'test_view_translate/data.csv')

    assert len(actual) == len(expected)
    assert actual.astype(str).equals(expected.astype(str))
