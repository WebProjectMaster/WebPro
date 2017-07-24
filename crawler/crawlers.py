#!/usr/bin/python3
import datetime
from io import BytesIO
import urllib.request
import re
import gzip
import time
import lxml
import settings
import sitemap
import parsers


class Crawler:
    def __init__(self, next_step=False):
        """ п.1 в «Алгоритме ...» """
        print('Crawler.__init__ ...')
        self.db = settings.DB
        c = self.db.cursor()
        c.execute('select s.Name, s.ID '
                  'from sites s '
                  'left join pages p on (p.SiteID=s.ID) '
                  'where p.id is Null')
        INSERT = 'insert into pages(SiteID, Url, LastScanDate, FoundDateTime) values (%s, %s, %s, %s)'
        ARGS = [(r[1], '%s/robots.txt' % r[0], None, datetime.datetime.now()) for r in c.fetchall()]
        c.close()
        c = self.db.cursor()
        try:
            print(ARGS)
            c.executemany(INSERT, ARGS)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print('Crawler exception 1 ', e, ARGS)
        c.close()

        self.keywords = self.load_persons()
        if next_step:
            print('Crawler: переходим к шагу 2 ...')
            scan_result = self.scan()

    def load_persons(self):
        c = self.db.cursor()
        SELECT = 'select distinct Name, PersonID from keywords'
        c.execute(SELECT)
        keywords = {}
        for n, i in c.fetchall():
            if not i in keywords.keys():
                keywords[i] = []
            keywords[i] += [n, ]
        c.close()
        return keywords

    def update_last_scan_date(self, page_id):
        c = self.db.cursor()
        c.execute('update pages set LastScanDate=%s where ID=%s',
                  (datetime.datetime.now(), page_id))
        self.db.commit()
        c.close()

    def update_person_page_rank(self, page_id, ranks):
        if ranks:
            SELECT = 'select id from person_page_rank where PageID=%s and PersonID=%s'
            UPDATE = 'update person_page_rank set Rank=%s where ID=%s'
            INSERT = 'insert into person_page_rank (PageID, PersonID, Rank) values (%s, %s, %s)'
            for person_id, rank in ranks.items():
                c = self.db.cursor()
                c.execute(SELECT, (page_id, person_id))
                rank_id = c.fetchone()
                c.close()
                # Реализация INSERT OR UPDATE, т.к. кое кто отказался добавить UNIQUE_KEY :)
                c = self.db.cursor()
                if rank_id:
                    c.execute(UPDATE, (rank, rank_id))
                else:
                    c.execute(INSERT, (page_id, person_id, rank))
                self.db.commit()
                c.close()

    def scan(self):
        SELECT = 'select distinct p.id, p.Url, p.SiteID, s.Name '\
                 'from pages p '\
                 'join sites s on (s.ID=p.SiteID) '\
                 'where p.LastScanDate is null'
        c = self.db.cursor()
        c.execute(SELECT)
        pages = c.fetchall()
        c.close()
        rows = 0
        for row in pages:
            rows += 1
            print(row)
            page_id, url, site_id, base_url = row
            url = ('http://' + url) if not (url.startswith('http://') or url.startswith('https://')) else url
            urls = []
            request_time = time.time()
            try:
                # print('Загрузка', url)
                rd = urllib.request.urlopen(url)
            except Exception as e:
                print('Crawler.scan (%s) exception %s' % (url, e))
            else:
                try:
                    if not url.strip().endswith('.gz'):
                        rd = rd.read()
                    else:
                        """
                            sitemap.xml.gz
                        """
                        mem = BytesIO(rd.read())
                        mem.seek(0)
                        f = gzip.GzipFile(fileobj=mem, mode='rb')
                        rd = f.read()
                except Exception as e:
                    print('Crowlrer.read exception', e, url)
                else:
                    if url.upper().endswith('ROBOTS.TXT'):
                        urls, sitemaps = list({r for r in re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', rd.decode())}), []
                    else:
                        try:
                            urls, sitemaps = sitemap.get_urls(rd.decode(), base_url)
                            rd = rd.decode()
                        except Exception as e:
                            print(base_url, rd[:20], ' ... ', rd[-20:], e)
                            urls, sitemaps = [], []
                        else:
                            if sitemap._get_sitemap_type(rd.split('\n')[0]) == sitemap.SM_TYPE_HTML:
                                print('Crawler.html.parsing ...')
                                ranks = parsers.parse_html(rd, self.keywords)
                                print('Crawler:', ranks)
                                self.update_person_page_rank(page_id, ranks)
                    urls += sitemaps
                    urls = [(site_id, u, datetime.datetime.now(), None) for u in urls if url]
                    # print('Crawler: urls %s' % urls)
                    INSERT = 'insert into pages (SiteID, Url, FoundDateTime, LastScanDate) values (%s, %s, %s, %s)'
                    c = self.db.cursor()
                    c.executemany(INSERT, urls)
                    self.db.commit()
                    c.close()
                    self.update_last_scan_date(page_id)
            request_time = time.time() - request_time
        return rows

    def fresh(self):
        SELECT = ''


if __name__ == '__main__':
    c = Crawler()
    c.scan()
    c.fresh()
