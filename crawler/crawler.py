#!/usr/bin/python3
import datetime
from io import BytesIO
from multiprocessing import Pool, log_to_stderr, SUBDEBUG
# , BoundedSemaphore, Semaphore
from threading import Semaphore, BoundedSemaphore
import urllib.request
# import asyncio
import re
import gzip
import time
import lxml
import logging
# import log
import database
import settings
import sitemap
import parsers
import robots
# from robots import RobotsTxt


def _get_content(url, timeout=60):
    logging.info('_get_content: %s loading ...' % url)

    """ Дадим просто упасть, дабы выйти на get_content_error"""
    rd = urllib.request.urlopen(url, timeout=timeout)

    charset = rd.headers.get_content_charset('utf-8')
    logging.debug('_get_content: charset %s', charset)
    content = ''

    try:
        if url.strip().endswith('.gz'):
            mem = BytesIO(rd.read())
            mem.seek(0)
            f = gzip.GzipFile(fileobj=mem, mode='rb')
            content = f.read().decode()
        else:
            content = rd.read().decode(charset)
    except UnicodeDecodeError as e:
        logging.error('_get_content: url = %s, charset = %s, error = %s',
                      url, charset, e)
        if settings.MULTI_PROCESS:
            raise UnicodeDecodeError(e)
    except Exception as e:
        logging.error('_get_content: url = %s, error = %s',
                      url, e)
        if settings.MULTI_PROCESS:
            raise Exception(e)
    logging.info('_get_content: %s loaded ...%s bytes' % (url, len(content)))
    return content


def _get_content_mp(page, all_robots, timeout=60):
    logging.info('get_content: start %s', page)
    page_id, url, site_id, base_url = page
    content = _get_content(url, timeout)
    logging.info('get_content: finish %s', page)
    # TODO: Выяснить тип контента
    return content, page, all_robots


def _init_crawler():
    database.add_robots()
    all_robots = {}
    for robots_page in database.get_robots():
        page_id, robots_url, site_id, base_url = robots_page
        all_robots[site_id] = robots.process_robots(robots_url)
        if all_robots[site_id].sitemaps == []:
            index_page = [{
                         'site_id': site_id,
                         'url': base_url,
                         'found_date_time': datetime.datetime.now(),
                         'last_scan_date': None
                          }]
            database.add_urls(index_page)
    keywords = database.load_persons()
    return keywords, all_robots


def scan(next_step=False, max_limit=0):
    if settings.MULTI_PROCESS:
        result = scan_mp(next_step, max_limit)
    else:
        result = scan_sp(next_step, max_limit)
    return result


def scan_sp(next_step=False, max_limit=0):
    logging.info('solo crawler start')
    keywords, all_robots = _init_crawler()
    pages = database.get_pages_rows(None)
    # TODO: добавить проверку если len(pages) = 0
    # то найти наименьшую дату и выбрать по ней.
    add_urls_total = 0
    for page in pages:
        page_id, url, site_id, base_url = page
        request_time = time.time()
        logging.info('#BEGIN %s url %s, base_url %s', page_id, url, base_url)
        content = _get_content(url)
        robots = all_robots.get(site_id)

        if add_urls_total >= max_limit:
            page_type = sitemap.get_file_type(content)
            add_urls_count = 0
        else:
            new_pages_data, page_id, page_type = sitemap.scan_urls(content,
                                                                   page,
                                                                   robots)
            if len(new_pages_data) > max_limit:
                new_pages_data = new_pages_data[:max_limit + 1]
            add_urls_count, page_id = database.add_urls(new_pages_data,
                                                        page_id)
            if page_type != sitemap.SM_TYPE_HTML:
                database.update_last_scan_date(page_id)

        if page_type == sitemap.SM_TYPE_HTML:
            ranks, page_id = parsers.process_ranks(content,
                                                   page_id,
                                                   keywords,
                                                   )
            database.update_person_page_rank(page_id, ranks)

        request_time = time.time() - request_time
        logging.info('#END url %s, base_url %s, add urls %s, time %s',
                     url, base_url, add_urls_count, request_time)
        add_urls_total = add_urls_total + add_urls_count

    logging.info('Crawler.scan: Add %s new urls on date %s', add_urls_total,
                 'NULL')
    return add_urls_total


def scan_mp(next_step=False, max_limit=0):
    urls_limits = {}

    def get_content_error(*error):
        logging.error('get_content_error: %s', error)

    def get_content_complete(*args):
        content, page, all_robots = args[0]
        page_id, url, site_id, base_url = page
        page_type = parsers.get_file_type(content)
        if site_id not in urls_limits.keys():
            urls_limits[site_id] = 0
        urls_limits[site_id] += 1
        logging.info('get_content_complete.')
        if (max_limit == 0) or (urls_limits[site_id] < max_limit):
            robots = all_robots.get(site_id)
            with pool_sem:
                logging.info('get_content_complete: add %s/%s %s',
                             urls_limits[site_id], max_limit, page)
                """Сканирование на наличие url'ов"""
                pool.apply_async(sitemap.scan_urls, (content, page, robots,),
                                 callback=scan_page_complete,
                                 error_callback=scan_page_error)
                logging.info('get_content_complete: added sitemap.scan_urls %s',
                             page)
            if page_type == parsers.SM_TYPE_HTML:
                """Сканирование keywords"""
                with pool_sem:
                    pool.apply_async(parsers.process_ranks,
                                     (content, page_id, keywords),
                                     callback=process_ranks_complete,
                                     error_callback=process_ranks_error)
                    time.sleep(1)

    def process_ranks_complete(*args):
        ranks, page_id = args[0]
        database.update_person_page_rank(page_id, ranks)

    def process_ranks_error(*error):
        logging.error('process_ranks_error: %s', error)

    def scan_page_complete(*args):
        new_pages_data, page_id, page_type = args[0]
        logging.info('scan_page_complete: %s %s %s',
                     page_id, len(new_pages_data), page_type)

        chunk_size = settings.CHUNK_SIZE if max_limit > settings.CHUNK_SIZE else max_limit
        for r in range(0, max_limit if max_limit > 0 else len(new_pages_data), chunk_size):
            with pool_sem:
                pool.apply_async(database.add_urls,
                                 (new_pages_data[r:r + chunk_size],
                                  page_id,
                                  settings.DB,),
                                 callback=add_urls_complete,
                                 error_callback=add_urls_error)

    def add_urls_complete(*args):
        rows, page_id = args[0]
        logging.info('add_urls_complete: %s %s', page_id, rows)
        if rows > 0:
            database.update_last_scan_date(page_id, )

    def add_urls_error(*error):
        logging.error('add_urls_error: %s', (error,))
        # TODO: Поставить сбойнувший CHUNK в очередь (см.ниже)
        chunk = error[0][1]
        with pool_sem:
            pool.apply_async(database.add_urls, (chunk, page_id,),
                             callback=add_urls_complete,
                             error_callback=add_urls_error)

    def scan_page_error(*error):
        logging.error('scan_page_error: %s', (error,))

    logging.info('multiprocessing crawler start')
    global pool
    pool = Pool(settings.POOL_SIZE)
    global pool_sem
    # pool_sem = BoundedSemaphore(settings.POOL_SIZE * 2)
    pool._taskqueue._maxsize = settings.POOL_SIZE * 2
    pool_sem = pool._taskqueue._sem = BoundedSemaphore(settings.POOL_SIZE * 2)
    # pool._taskqueue.maxsize = settings.POOL_SIZE * 2

    keywords, all_robots = _init_crawler()
    # TODO: добавить проверку если len(pages) = 0 то
    # найти наименьшую дату и выбрать по ней.
    add_urls_total = 0
    for page in database.get_pages_rows(max_limit=max_limit):
        with pool_sem:
            add_urls_total += 1
            pool.apply_async(_get_content_mp, (page, all_robots,),
                             callback=get_content_complete,
                             error_callback=get_content_error)
            logging.info('page_added: %s %s', len(pool._cache), page)
            if len(pool._cache) > settings.POOL_SIZE * 2:
                time.sleep(1)
            time.sleep(len(pool._cache) // settings.POOL_SIZE + 1)

    close_pool_wait(add_urls_total)
    # logging.info('Crawler.scan: Add %s new urls on date %s',
    # add_urls_total, 'NULL')

    return close_pool_wait(add_urls_total)


def close_pool_wait(add_urls_total):
    """Ожидание исчерпания очереди выполнения"""
    count = 0
    logging.info('close_pool_wait: %s %s', count, len(pool._cache))
    while len(pool._cache) > 0:
        # Ожидание опустошения пула
        count = max(count, max(pool._cache if pool._cache else [0, ]))
        time.sleep(1)
    pool.close()
    pool.join()
    return add_urls_total
