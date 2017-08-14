import datetime
import logging
import settings
import MySQLdb

connection = None


def connect(conn_settings=None):
    conn_settings = conn_settings or settings.DB
    global connection
    connection = MySQLdb.connect(**conn_settings)
    return connection


def close():
    connection.close()


def get_connect(conn_settings=None):
    conn_settings = conn_settings or settings.DB
    logging.debug("get_connect: connect to %s", conn_settings)

    if settings.MULTI_PROCESS:
        logging.debug('get_connect multiprocessing: %s', conn_settings)
        return MySQLdb.connect(**conn_settings)
    else:
        logging.debug('get_connect solo: %s', conn_settings)
        return connection if connection else connect(conn_settings)


def load_persons(conn_settings=None):
    conn_settings = conn_settings or settings.DB

    keywords = {}
    try:
        db = get_connect(conn_settings)
        with db.cursor() as c:
            SELECT = 'select distinct Name, PersonID from keywords'
            c.execute(SELECT)
            logging.debug('load_persons: %s', c._last_executed)
            for n, i in c.fetchall():
                if i not in keywords.keys():
                    keywords[i] = []
                keywords[i] += [n.lower(), ]
    except Exception as e:
        logging.error("load_persons exception: %s", e)
        if settings.MULTI_PROCESS:
            db.close()

    logging.debug("load_persons result: %s", keywords)
    return keywords


def get_robots(conn_settings=None):
    conn_settings = conn_settings or settings.DB

    SELECT = ('SELECT p.ID, p.Url, p.SiteID, s.Name FROM pages p '
              'JOIN sites s ON (s.ID=p.SiteID) '
              'WHERE p.Url like "%/robots.txt"')
    try:
        db = get_connect(conn_settings)
        with db.cursor() as c:
            c.execute(SELECT)
            for row in c.fetchall():
                yield row
        if settings.MULTI_PROCESS:
            db.close()
    except Exception as e:
        logging.error('get_robots exception: %s', e)


def add_robots(conn_settings=None):
    conn_settings = conn_settings or settings.DB
    """ Добавляет в pages ссылки на robots.txt,
        если их нет для определенных сайтов  """
    conn_settings = conn_settings or settings.DB
    new_sites = _not_have_pages(conn_settings)
    ARGS = [{
            'site_id': r[1],
            'url': '%s/robots.txt' % r[0],
            'found_date_time': datetime.datetime.now(),
            'last_scan_date': None
            } for r in new_sites]
    _add_robots = add_urls(ARGS)

    logging.debug('add_robots: %s robots url was add', _add_robots)
    return _add_robots


def _not_have_pages(conn_settings=None):
    """ Возвращает rows([site_name, site_id]) у которых нет страниц"""
    conn_settings = conn_settings or settings.DB
    try:
        db = get_connect(conn_settings)
        with db.cursor() as c:
            c.execute('select s.Name, s.ID '
                      'from sites s '
                      'left join pages p on (p.SiteID=s.ID) '
                      'where p.id is Null')
            rows = c.fetchall()
    except Exception as e:
        rows = []
        logging.error('_not_have_pages exception: %s', e)
    return rows


def update_person_page_rank(page_id, ranks, conn_settings=None):
    conn_settings = conn_settings or settings.DB
    logging.info('update_person_page_rank: %s %s', page_id, ranks)
    if ranks:
        # logging.debug('update_person_page_rank: %s %s', page_id, ranks)
        SELECT = ('select id, rank from person_page_rank '
                  'where PageID=%s and PersonID=%s and Scan_date_datetime=%s')
        UPDATE = 'update person_page_rank set Rank=%s where ID=%s'
        INSERT = ('insert into person_page_rank '
                  '(PageID, PersonID, Rank, Scan_date_datetime) '
                  'values (%s, %s, %s, %s)')
        found_datetime = datetime.datetime.now()
        try:
            db = get_connect(conn_settings)
            for person_id, rank in ranks.items():
                if rank > 0:
                    # Реализация INSERT OR UPDATE, т.к.
                    # кое кто отказался добавить UNIQUE_KEY :)

                    with db.cursor() as c:
                        try:
                            c.execute(SELECT, (page_id, person_id,
                                               found_datetime))
                            rank_id, rank_ = c.fetchone()
                        except:
                            rank_id, rank_ = None, 0

                    with db.cursor() as c:
                        if rank_id:
                            c.execute(UPDATE, (rank, rank_id, ))
                        else:
                            c.execute(INSERT, (page_id, person_id, rank,
                                      found_datetime))
                db.commit()
            if settings.MULTI_PROCESS:
                db.close()
        except Exception as e:
            logging.error('update_person_page_rank exception: %s', e)


def update_last_scan_date(page_id, conn_settings=None):
    conn_settings = conn_settings or settings.DB

    rows = -1
    try:
        db = get_connect(conn_settings)
        with db.cursor() as c:
            last_scan_date = datetime.datetime.now()
            logging.debug('update_last_scan_date: %s %s', last_scan_date,
                          page_id)
            c.execute('update pages set LastScanDate=%s where ID=%s',
                      (last_scan_date, page_id))
            rows = c.rowcount

            db.commit()
        if settings.MULTI_PROCESS:
            db.close()

    except Exception as e:
        logging.error('update_last_scan_date exception: %s %s %s',
                      last_scan_date, page_id, e)

    return rows


def get_pages_rows(last_scan_date=None, max_limit=0, conn_settings=None):
    conn_settings = conn_settings or settings.DB
    logging.debug('get_pages_rows: %s', last_scan_date)
    SELECT = 'select p.id, p.Url, p.SiteID, s.Name '\
             'from pages p '\
             'join sites s on (s.ID=p.SiteID)'
    LIMIT = (' LIMIT %s' % max_limit) if max_limit > 0 else ''
    if last_scan_date is None:
        WHERE = 'where p.LastScanDate is null'
    else:
        WHERE = 'where p.LastScanDate = %s'

    query = ' '.join([SELECT, WHERE, LIMIT])

    try:
        db = get_connect(conn_settings=settings.DB)
        with db.cursor() as c:
            c.execute(query, (last_scan_date))
            for page in c.fetchall():
                yield page
        if settings.MULTI_PROCESS:
            db.close()
    except Exception as e:
        logging.error('get_pages_rows exception: %s', e)
        return []


def add_urls(pages_data, page_id=None, conn_settings=None):
    conn_settings = conn_settings or settings.DB
    logging.debug('add_urls%s inserting %s', ' multiprocessing' if settings.MULTI_PROCESS else ' solo', len(pages_data))
    rows = -1  # Для корректного возврата в sp
    INSERT = ('INSERT INTO pages '
              '(SiteID, Url, FoundDateTime, LastScanDate, hash_url) '
              'VALUES (%(site_id)s, %(url)s, %(found_date_time)s, '
              '%(last_scan_date)s, MD5(%(url)s)) '
              'ON DUPLICATE KEY UPDATE FoundDateTime=%(found_date_time)s')

    try:
        db = get_connect(conn_settings)
        with db.cursor() as c:

            logging.info('add_urls%s inserting %s start', ' multiprocessing' if settings.MULTI_PROCESS else ' solo', len(pages_data))
            c.executemany(INSERT, pages_data)
            rows = c.rowcount
            db.commit()
        if settings.MULTI_PROCESS:
            db.close()
    except MySQLdb.Error as e:
        logging.error('add_urls%s exception %s', ' multiprocessing' if settings.MULTI_PROCESS else ' solo', e)
        if settings.MULTI_PROCESS:
            # передать управление в crawlers.add_urls_error
            raise Exception(e, pages_data, page_id)

    logging.info('add_urls%s complete %s', ' multiprocessing' if settings.MULTI_PROCESS else ' solo', len(pages_data))

    return rows, page_id
