import sys
import time
import os
import threading
import sqlite3 as sql

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print ('%r %2.3f s' % (method.__name__, (te - ts)))
        return result
    return timed

def threadit(method):
    def thread_call(*args, **kw):
        print(args, kw)
        thread = threading.Thread(target = method, args = args, kwargs = kw)
        thread.start()
    return thread_call
 
 
def lockthreadit(method):
    def thread_call(*args, **kw):
        lock = threading.Lock()
        with lock:
            thread = threading.Thread(target = method, args = args, kwargs = kw)
            thread.start()
        thread.join()
    return thread_call
    
def database_connector_wrap(funct):
    def database_connector_exec(*args, **kwargs):
        conn = sql.connect('library.db')
        out = funct(conn = conn, *args, **kwargs)
        conn.commit()
        conn.close()            
        return out
    return database_connector_exec

def tryit(method):
    def try_ex(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as e:
            print(f"<{method.__name__}> {e}")        
    return try_ex