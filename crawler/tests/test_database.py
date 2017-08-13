import pytest
from test_crawlers_fixtures import *
from database import get_pages_rows, add_robots, get_robots

def setup_module(module):
    clean_test_db()

def describe_database_module():
    def describe__get_pages_rows():
        def it_method__get_pages_row_return_collection(test_db):
            add_robots()
            rows = get_pages_rows(None)
            assert len(rows) == 2
    def describe_get_robots():
        def it_return_rows_with_robots_files(test_db):
            add_robots()
            rows = get_robots()
            assert len(rows) == 2
