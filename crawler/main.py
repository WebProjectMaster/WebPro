#!/usr/bin/python3

import time
import logging
import settings
import crawler

if __name__ == '__main__':
    logging.basicConfig(filename=settings.LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s')
    crawler.scan(max_limit=10)
