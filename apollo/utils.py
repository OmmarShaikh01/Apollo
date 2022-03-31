import sys
import time
import traceback


def timeit(method):
    def exec(*args, **kwargs):
        try:
            t1 = time.time()
            method(*args, **kwargs)
            print(method, round(time.time() - t1, 8))
        except Exception as e:
            print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
            raise e
    return exec


def execLine(msg, method):
    try:
        t1 = time.time()
        method()
        print(msg, round(time.time() - t1, 8))
    except Exception as e:
        print(e, '\n', traceback.print_tb(sys.exc_info()[-1]))
        raise e
