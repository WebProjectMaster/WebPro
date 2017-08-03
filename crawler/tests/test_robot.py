import pytest
import os
from urllib.request import pathname2url
from robots import RobotsTxt
from test_robot_fixtures import *


def describe_robots_module():
    def describe_robottxt_class():
        def it_create_obj():
            rp = RobotsTxt()
            assert isinstance(rp, RobotsTxt)
        def it_read_sitemap_file(list_ya_sitemaps):
            robot_url = "file:" + pathname2url(
                os.path.abspath("./tests/fixtures/yandex_robots.txt"))
            rp = RobotsTxt()
            rp.set_url(robot_url)
            rp.read()
            assert not (set(rp.sitemaps) - set(list_ya_sitemaps))