#!/usr/bin/python3
import datetime
from io import BytesIO
import urllib.request
import re
import gzip
import time
import lxml
import logging
import log
import settings
import sitemap
import parsers
import database
from robots import RobotsTxt


class Crawler:
    def __init__(self, next_step=False, max_limit=0):
        """ п.1 в «Алгоритме ...» """
        self.max_limit = max_limit
        self.keywords = database.load_persons()
        # print('Crawlrer.keywords', self.keywords)

        if next_step:
            # print('Crawler: переходим к шагу 2 ...')
            scan_result = self.scan()

    def _get_content(self, url):
        # print('%s loading ...', url)
        logging.info('%s loading ', url)
        try:
            rd = urllib.request.urlopen(url)
        except Exception as e:
            logging.error('_get_content (%s) exception %s', url, e)
            return ""
        charset = rd.headers.get_content_charset('utf-8')
        logging.debug("_get_content: charset %s", charset)
        content = ""
        if url.strip().endswith('.gz'):
            mem = BytesIO(rd.read())
            mem.seek(0)
            f = gzip.GzipFile(fileobj=mem, mode='rb')
            content = f.read().decode()
        else:
            content = rd.read().decode(charset)

        print('%s loaded ...%s bytes' % (url, len(content)))
        return content

    def _is_robot_txt(self, url):
        return url.upper().endswith('ROBOTS.TXT')

    def process_ranks(self, content, page_id):
        logging.debug('process_ranks: %s', content)
        ranks = parsers.parse_html(content, self.keywords)
        logging.debug('process_ranks: %s', ranks)
        database.update_person_page_rank(page_id, ranks)
        database.update_last_scan_date(page_id)
        return ranks

    def process_robots(self):
        """
            Производит обработку файлов robots.txt
            - добавляет в базу новые файлы robots
            - создает объекты из файлов robots.txt, 
              которые умеют проверять ссылки и содежрат sitemaps
            - возвращает словарь site_id : RobotsTxt
            - если robots.txt не содержит sitemap то подставляется индекс страница
        """
        result = {}
        database.add_robots()
        robots_rows = database.get_robots()
        for robots in robots_rows:
            page_id, url, site_id, base_url = robots
            request_time = time.time()
            logging.info('#BEGIN %s url %s, base_url %s', page_id, url, base_url)
            robots_file = RobotsTxt(url)
            robots_file.read()
            result[site_id] = robots_file
            urls = robots_file.sitemaps
            if urls == []:
                urls.append(base_url)
            urls_count = sitemap.add_urls(urls, robots, sitemap.SM_TYPE_TXT)
            request_time = time.time() - request_time
            logging.info('#END url %s, base_url %s, add urls %s, time %s',
                         url, base_url, urls_count, request_time)
        return result

    def scan(self):
        all_robots = self.process_robots()
        pages = database.get_pages_rows(None)
        # TODO: добавить проверку если len(pages) = 0 то найти наименьшую дату и выбрать по ней.
        add_urls_total = 0
        # print('Crawler.scan: pages=%s' % len(pages))
        for page in pages:
            page_id, url, site_id, base_url = page
            request_time = time.time()
            logging.info('#BEGIN %s url %s, base_url %s', page_id, url, base_url)
            content = self._get_content(url)
            robots = all_robots.get(site_id)

            if add_urls_total >= self.max_limit:
                page_type = sitemap.get_file_type(content)
                add_urls_count = 0
            else:
                page_type, add_urls_count = sitemap.scan_urls(content, page, robots)

            if page_type == sitemap.SM_TYPE_HTML:
                self.process_ranks(content, page_id)

            request_time = time.time() - request_time
            logging.info('#END url %s, base_url %s, add urls %s, time %s',
                         url, base_url, add_urls_count, request_time)
            add_urls_total = add_urls_total + add_urls_count

        logging.info('Crawler.scan: Add %s new urls on date %s', add_urls_total, 'NULL')
        return add_urls_total, len(pages)

if __name__ == '__main__':
    c = Crawler(max_limit=50000)
    logger = logging.getLogger()
    c.scan()
