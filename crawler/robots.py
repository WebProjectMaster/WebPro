from urllib.robotparser import RobotFileParser
from urllib.parse import unquote


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
