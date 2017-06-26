#!/usr/bin/env python
# coding=utf-8

__author__ = 'Felix Zhou'

'''
Database operation module.
'''

import time, uuid, functools, threading, logging

class Dict(dict):
    '''
    d = Dict()
    d.x = 5

    print d.x
    print d['x']
    #print d.y

    d2 = Dict(('x', 'y', 'z'), (1, 2, 3))
    print d2['y']
    print d2.y
    '''
    def __init__(self, keys = (), values = (), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(keys, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def next_id(t = None):
    '''
    Return next id as 50-char string
    '''
    if t is None:
        t = time.time()
    return '%015d%s000' % (int(t * 1000), uuid.uuid4().hex)

def _profiling(start, sql = ''):
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING] [DB] %s: %s' % (t, sql))
    else:
        logging.info('[PROFILING] [DB] %s: %s' % (t, sql))

class _LasyConnection(object):
    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            self.connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(self.connection)))
        
        return self.connection.cursor()

    def commit(self):
        return self.connection.commit()

    def rollback(self):
        return self.connection.rollback()

    def cleanup(self):
        if self.connection:
            self.connection.close()
        logging.info('open connection <%s>...' % hex(id(self.connection)))
        self.connection = None

class _DbCtx(threading.local):
    pass

_db_ctx = _DbCtx()

engine = None

class _Engine(object):
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()


def create_engine(user, password, database, host='127.0.0.1', port=3306, **kw):
    import mysql.connector
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
        params.update(kw)
        params['buffered'] = True
        engine = _Engine(lambda: mysql.connector.connect(**params))
        # test connection...
        logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))

if __name__ == "__main__":
    print next_id()
    print time.time()
    print _profiling(1498466390.93, '123')
