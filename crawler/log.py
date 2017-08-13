import logging
import settings

log_file = settings.LOG_FILE if settings.LOG_FILE else 'crawler.log'
root_logger = logging.getLogger()

if settings.DEBUG:
    root_logger.setLevel(logging.DEBUG)
else:
    root_logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(log_file, 'w', 'utf-8')
root_logger.addHandler(log_handler)

def log_with(func):
    def wrapper(self, *argv, **kwargv):
        result = func(self, *argv, **kwargv)
        logging.info("%s , result: %s", func.__name__, result)
        return result
    return wrapper

def debug_log(func):
    def wrapper(self, *argv, **kwargv):
        result = func(self, *argv, **kwargv)
        logging.debug("%s , result: %s", func.__name__, result)
        return result
    return wrapper