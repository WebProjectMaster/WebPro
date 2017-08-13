import pytest
import log
from test_crawlers_fixtures import *
from test_parsers_fixtures import *

from crawlers import Crawler
from robots import RobotsTxt
from database import get_pages_rows, add_robots

def setup_module(module):
    clean_test_db()

def describe_crawlers_module():
    def describe_crawler_class():
        def it_create_obj():
            crawler = Crawler()
            assert isinstance(crawler, Crawler)
        
        #@pytest.mark.skip(reason="no way of currently testing this")
        def it_method_process_robots_return_robots(test_db):
            crawler = Crawler(max_limit=300)
            robots = crawler.process_robots()
            assert len(robots) == 2
            assert isinstance(robots[1], RobotsTxt)
        
        #@pytest.mark.skip(reason="no way of currently testing this")
        def it_method_scan_urls_return_add_urls_count():
            crawler = Crawler(max_limit=1000)
            result = crawler.scan()
            assert result[0] > 0
        
        @pytest.mark.skip(reason="very long operation 54s")
        def it_method_scan_urls_return_add_urls_count_50000():
            crawler = Crawler(max_limit=50000)
            result = crawler.scan()
            assert result[0] > 50000
        
        @pytest.mark.skip(reason="very long operation 54s")
        def it_method_scan_urls_return_add_urls_count_html():
            crawler = Crawler(max_limit=50000)
            result = crawler.scan()
            assert result[0] == 51770

        def it_method_process_ranks_update_ranks(page_content):
            crawler = Crawler()
            result = crawler.process_ranks(page_content, 1)
            assert result == {1:1}
