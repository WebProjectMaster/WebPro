import datetime
import logging
import settings
import MySQLdb


db = MySQLdb.connect(**settings.DATABASE)


def load_persons():
    # db = settings.DB
    c = db.cursor()
    SELECT = 'select distinct Name, PersonID from keywords'
    c.execute(SELECT)
    logging.debug('load_persons: %s', c._last_executed)
    keywords = {}
    for n, i in c.fetchall():
        if not i in keywords.keys():
            keywords[i] = []
        keywords[i] += [n.lower(), ]
    c.close()
    logging.debug("load_persons: %s", keywords)
    return keywords


def get_robots():
    SELECT = ('SELECT p.ID, p.Url, p.SiteID, s.Name FROM pages p ' 
              'JOIN sites s ON (s.ID=p.SiteID) ' 
              'WHERE RIGHT(p.Url, 10) = "robots.txt"')
    c = db.cursor()
    c.execute(SELECT)
    logging.debug('get_robots: %s', c._last_executed)
    rows = c.fetchall()
    logging.info('get_robots: %s', rows)
    c.close()
    return rows


def add_robots():
    """ Добавляет в pages ссылки на robots.txt, если их нет для определенных сайтов  """
    # db = settings.DB
    # INSERT = 'insert into pages(SiteID, Url, FoundDateTime, LastScanDate) values (%s, %s, %s, %s)'
    new_sites = _not_have_pages()
    # ARGS = [(r[1], '%s/robots.txt' % r[0], None, datetime.datetime.now(), hashlib.md5(('%s/robots.txt' % r[0]).encode()).hexdigest()) for r in new_sites]
    ARGS = [{
            'site_id': r[1],
            'url': '%s/robots.txt' % r[0],
            'found_date_time': datetime.datetime.now(),
            'last_scan_date': None } for r in new_sites]
    add_robots = add_urls(ARGS)

    logging.info('add_robots: %s robots url was add', add_robots)
    return add_robots


def _not_have_pages():
    """ Возвращает rows([site_name, site_id]) у которых нет страниц"""
    c = db.cursor()
    c.execute('select s.Name, s.ID '
                'from sites s '
                'left join pages p on (p.SiteID=s.ID) '
                'where p.id is Null')
    rows = c.fetchall()
    c.close()
    return rows


def update_person_page_rank(page_id, ranks):
    if ranks:
        logging.debug('update_person_page_rank: %s %s', page_id, ranks)
        SELECT = 'select id from person_page_rank where PageID=%s and PersonID=%s'
        UPDATE = 'update person_page_rank set Rank=%s where ID=%s'
        INSERT = 'insert into person_page_rank (PageID, PersonID, Rank) values (%s, %s, %s)'
        for person_id, rank in ranks.items():
            if rank > 0:
                # Реализация INSERT OR UPDATE, т.к. кое кто отказался добавить UNIQUE_KEY :)
                c = db.cursor()
                c.execute(SELECT, (page_id, person_id))
                logging.debug('update_person_page_rank: %s', c._last_executed)
                rank_id = c.fetchone()
                c.close()
                c = db.cursor()
                if rank_id:
                    c.execute(UPDATE, (rank, rank_id))
                else:
                    c.execute(INSERT, (page_id, person_id, rank))
                logging.debug('update_person_page_rank: %s', c._last_executed)
                c.close()
        db.commit()


def update_last_scan_date(page_id):
    c = db.cursor()
    c.execute('update pages set LastScanDate=%s where ID=%s',
              (datetime.datetime.now(), page_id))
    logging.debug('update_last_scan_date: %s', c._last_executed)

    db.commit()
    c.close()

def get_pages_rows(last_scan_date):
    # db = settings.DB
    SELECT = ('select p.id, p.Url, p.SiteID, s.Name '
              'from pages p '
              'join sites s on (s.ID=p.SiteID)')

    if last_scan_date is None:
        WHERE = 'where p.LastScanDate is null'
    else:
        WHERE = 'where p.LastScanDate = %s'

    query = ' '.join([SELECT, WHERE])

    with db.cursor() as c:
        c.execute(query, (last_scan_date))
        logging.debug('get_pages_rows: %s', c._last_executed)
        pages = c.fetchall()

    return pages


def add_urls(pages_data):
    """
        pages_data - dict(site_id, url, found_date_time, last_scan_date)
        добавляет url в таблицу pages если такой ссылки нет
    """
    logging.info('add_urls inserting %s', len(pages_data))

    # медленный вариант, но работает без добавления дополнительного поля
    # отчасти был медленным из-за настройки mysql сервера, но и так разница в 3 раза
    # INSERT = ('INSERT INTO pages (SiteID, Url, FoundDateTime, LastScanDate) '
    #         'SELECT * FROM (SELECT %s, %s, %s, %s) AS tmp '
    #         'WHERE NOT EXISTS (SELECT Url FROM pages WHERE Url = %s ) LIMIT 1')

    INSERT = ('INSERT INTO pages (SiteID, Url, FoundDateTime, LastScanDate, hash_url) '
              'VALUES (%(site_id)s, %(url)s, %(found_date_time)s, '
              '%(last_scan_date)s, MD5(%(url)s)) '
              'ON DUPLICATE KEY UPDATE FoundDateTime=%(found_date_time)s')

    c = db.cursor()
    rows = 0

    for page in pages_data:
        try:
            c.execute(INSERT, page)
            logging.debug('database.add_urls: %s', c._last_executed)
            row = c.rowcount
            rows = rows + (row if row > 0 else 0)
            db.commit()
            # print('+', end='', flush=True)
        except Exception as e:
            logging.error('database.add_urls exception %s', e)
            # print('.', end='', flush=True)
            db.rollback()

    c.close()
    logging.debug('database.add_urls %s completed...' % rows)
    return rows
