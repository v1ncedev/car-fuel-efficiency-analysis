"""
build_database.py
-----------------

Builds a small SQLite database from the cleaned data, then runs the analysis
queries against it and prints the results.

Why SQLite?
    SQLite is a database that lives in a single file on your computer. There is
    no server to install, and Python can talk to it out of the box, so anyone
    can run this project with no setup. The SQL you write here is standard and
    carries over to bigger databases like PostgreSQL or MySQL.

What the script does:
    1. Creates a database file called car_data.db.
    2. Runs 1_create_tables.sql to build the empty table.
    3. Loads the cleaned CSV into that table.
    4. Runs each query in 2_analysis_queries.sql and prints the answer.

Run it (after cleaning the data) with:
    python build_database.py
"""

import sqlite3
import pandas as pd

DB_FILE = "car_data.db"
CLEAN_DATA = "../data/mpg_clean.csv"


def run_sql_file(connection, path):
    """Read a .sql file and run every statement in it."""
    with open(path, "r", encoding="utf-8") as f:
        connection.executescript(f.read())


def split_statements(path):
    """
    Split a .sql file into separate query strings so we can run and label them
    one at a time. We split on the semicolon that ends each statement and skip
    anything that is only comments or blank lines.
    """
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    statements = []
    for chunk in text.split(";"):
        code_lines = [
            line for line in chunk.splitlines()
            if line.strip() and not line.strip().startswith("--")
        ]
        if code_lines:
            statements.append(chunk.strip() + ";")
    return statements


def main():
    connection = sqlite3.connect(DB_FILE)

    print("Creating the table...")
    run_sql_file(connection, "1_create_tables.sql")

    print("Loading the cleaned data into the database...")
    clean = pd.read_csv(CLEAN_DATA)
    clean.to_sql("cars", connection, if_exists="append", index=False)
    print(f"Loaded {len(clean)} rows.\n")

    queries = split_statements("2_analysis_queries.sql")
    for i, query in enumerate(queries, start=1):
        print("=" * 70)
        print(f"QUERY {i}")
        print("=" * 70)
        result = pd.read_sql(query, connection)
        print(result.to_string(index=False))
        print()

    connection.close()
    print("All queries finished. The database is saved as car_data.db")


if __name__ == "__main__":
    main()
