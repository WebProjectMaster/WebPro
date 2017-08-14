from urllib.robotparser import RobotFileParser
from urllib.parse import unquote
import time
import logging
# import database
import sitemap


class RobotsTxt(RobotFileParser):
    def __init__(self, url=''):
        self.__sitemaps = set()
        super().__init__(url)

    @property
    def sitemaps(self):
        """ sitemap type set """
        return self.__sitemaps

    def parse(self, lines):
        sitemaps = set()
        for line in lines:
            line = line.split(':', 1)
            if len(line) == 2:
                line[0] = line[0].strip().lower()
                line[1] = unquote(line[1].strip())
                if line[0] == 'sitemap':
                    sitemaps.add(line[1])
        self.__sitemaps = list(sitemaps)
        super().parse(lines)


def process_robots(robots_url):
    """
        Производит обработку файлов robots.txt
        - добавляет в базу новые файлы robots
        - создает объекты из файла robots.txt,
            которые умеют проверять ссылки и содежрат sitemaps
        - возвращает RobotsTxt
    """
    robots_file = RobotsTxt(robots_url)
    robots_file.read()
    return robots_file


def _is_robot_txt(url):
    return url.upper().endswith('ROBOTS.TXT')
