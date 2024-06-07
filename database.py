import os
import uuid

from google.cloud.spanner_admin_database_v1.types import spanner_database_admin
from google.cloud import spanner


SPANNER_ID = os.getenv('SPANNER_ID')
SPANNER_DATABASE_ID = os.getenv('SPANNER_DATABASE_ID')


def create_query_table():
    # Create a Spanner client
    client = spanner.Client()

    # Get a reference to the Spanner instance and database
    instance = client.instance(SPANNER_ID)
    database = instance.database(SPANNER_DATABASE_ID)

    database_admin_api = client.database_admin_api

    request = spanner_database_admin.UpdateDatabaseDdlRequest(
        database=database_admin_api.database_path(
            client.project, SPANNER_ID, SPANNER_DATABASE_ID
        ),
        statements=[
            """CREATE TABLE IF NOT EXISTS Queries (
                id varchar(36) DEFAULT (spanner.generate_uuid()),
                username VARCHAR(100) NOT NULL,
                place VARCHAR(200),
                adventure_type VARCHAR(50),
                duration INTEGER,
                PRIMARY KEY (id)
            );"""
        ],
    )
    operation = database_admin_api.update_database_ddl(request)

    print("Waiting for operation to complete...")
    operation.result(30)


def insert_query(username, place, adventure_type, duration):
    client = spanner.Client()
    instance = client.instance(SPANNER_ID)
    database = instance.database(SPANNER_DATABASE_ID)

    def insert_query(transaction):
        row_ct = transaction.execute_update(
            "INSERT INTO Queries (username, place, adventure_type, duration) VALUES "
            f"('{username}', '{place}', '{adventure_type}', {duration})"
        )

    # Define the mutation (change) to be applied
    database.run_in_transaction(insert_query)
