# Postgres stored procedures testing
This repository provides a framework for unit testing Postgres stored procedures using a local Docker container.

## Why?
Unit testing stored procedures can be challenging due to the lack of native testing tools. This setup leverages a Postgres container to allow for efficient, isolated tests that run entirely on your own machine.

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run a Postgres container:
```bash
docker run --name pg -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=ea -d postgres:16.1-alpine
```

3. Run the tests
```bash
# The entire test suite
pytest

# Or the tests within a file
pytest test_database.py

# Or a single test
pytest test_database.py::test_sp_add_entry
```
