#!/usr/bin/python3
# import sqlite3 as sq
# import MySQLdb
"""db_connector
    Пути"""
# DB = sq.connect('crawler.db')
# DB=MySQLdb.connect(host='127.0.0.1', user='andrewisakov', password='thua8Ohj', db='dbwpmod')
# DB = MySQLdb.connect(
#     host='127.0.0.1', user='andrewisakov', password='thua8Ohj',
#     db='dbwpmod', use_unicode=True, charset='utf8')

POOL_SIZE = 8 # Количество потоков multiprocessing.pool
CHUNK_SIZE = 512 # Запись в БД страницами чере multiprocessing.pool
WORK_LIMIT = 300
WORK_TIMEOUT = 5

DATABASE = {
    'host': '127.0.0.1',
    'user': 'andrewisakov',
    'password': 'thua8Ohj',
    'db': 'dbwpmod',
    'use_unicode': True,
    'charset': 'utf8'
}

TEST_DATABASE = {
    'host': '127.0.0.1',
    'user': 'andrewisakov',
    'password': 'thua8Ohj',
    'db': 'dbwebpro_test',
    'use_unicode': True,
    'charset': 'utf8'
}

DB = DATABASE

DEBUG = False
LOG_FILE = 'crawler.log'
MULTI_PROCESS = False