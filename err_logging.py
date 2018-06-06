# python err_logging.py

import logging, time, functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print('Function %s() runs' % func.__name__)
        start = time.time()
        temp = func(*args, **kw)
        end = time.time()
        print('Completed in %ds' % (end - start))
        return temp
    return wrapper



