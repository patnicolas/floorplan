__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2023. All rights reserved."

import time


def timeit(func):
    def wrapper(*args, **kwargs):
        import logging
        start = time.time()
        func(*args, **kwargs)
        duration = time.time() - start
        logging.info(f'Duration: {duration}')
        return 0
    return wrapper
