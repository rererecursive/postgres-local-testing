import pandas as pd


def query_table(query, db_connection):
    """
    Run an SQL SELECT query and return its results.
    """
    print(f"Executing query: {query}")
    df = pd.read_sql_query(query, db_connection, dtype_backend='numpy_nullable')    # Prevent nullable ints being cast to floats
    df = df.replace(r'\n',' ', regex=True)
    #print("Returned rows:", df.shape[0])
    return df


def call_procedure(query, conn):
    """
    Call a stored procedure.
    """
    print("Executing:", query)
    with conn.cursor() as cursor:
        cursor.execute(query)


def read_expected_csv(file_path):
    """
    Read the expected CSV output from a file.
    Replace NaN with None to ensure matches against database query results.
    """
    filename = 'data/outputs/' + file_path
    print("Expected output (filename):", filename)
    df = pd.read_csv(filename, dtype_backend='numpy_nullable')     # Prevent nullable ints being cast to floats
    df = df.replace(r'\n','', regex=True)
    return df


def print_outputs(actual: pd.DataFrame, expected: pd.DataFrame):
    print('-' * 40)
    print('+ Actual rows:', len(actual), 'Expected rows:', len(expected))
    print('+ EXPECTED OUTPUT:\n', expected.to_csv())
    print('+ ACTUAL OUTPUT:\n', actual.to_csv())
    print('-' * 40)
