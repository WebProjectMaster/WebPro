import pytest
import settings
from test_crawlers_fixtures import *
import database


def setup_module(module):
    clean_test_db()

def describe_database_module():
    def describe__get_pages_rows():
        def it_method__get_pages_row_return_collection():
            database.connect(settings.TEST_DATABASE)
            database.add_robots()
            rows = list(database.get_pages_rows(None))
            database.close()
            assert len(rows) == 2
    def describe_get_robots():
        def it_return_rows_with_robots_files():
            database.connect(settings.TEST_DATABASE)
            database.add_robots()
            rows = list(database.get_robots())
            database.close()
            assert len(rows) == 2
