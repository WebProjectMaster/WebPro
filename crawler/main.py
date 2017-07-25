#!/usr/bin/python3

import time
import random
import multiprocessing as mp
import logging
import settings
# import sqlite3

# import Robot from Robot
import sitemap
from crawlers import Crawler


if __name__ == '__main__':
    c = Crawler()
    c.scan()
    c.fresh()
