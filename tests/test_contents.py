"""
Functions to test the database contents
As users add their own data, these tests should be modified to reflect the new data.
"""


def test_table_presence(db):
    # Confirm the tables that should be present
    assert set(db.metadata.tables.keys()) == {"Sources", "Publications"}
