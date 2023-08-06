from contextlib import contextmanager
from inspect import currentframe
from threading import get_ident

from psycopg2 import connect as pgconnect
from psycopg2.extras import RealDictCursor, execute_batch
from psycopg2.pool import ThreadedConnectionPool

from .psyco import reformat_bind_params

conns = {}


def get_conn(db_url):
    tid = get_ident()

    if db_url not in conns:
        conns[db_url] = ThreadedConnectionPool(1, 2, db_url)

    pool = conns[db_url]

    conn = pool.getconn(tid)

    return conn


def put_conn(conn, db_url):
    tid = get_ident()

    pool = conns[db_url]
    print(conn)
    pool.putconn(conn, tid)


class Rows(list):
    pass


class Transaction:
    def __init__(self):
        self._back = 0

    def ex(self, *args, **kwargs):
        self.c.execute(*args, **kwargs)

    def execute(self, *args, **kwargs) -> Rows:
        self.c.execute(*args, **kwargs)

        fetched = self.c.fetchall()
        descr = list(self.c.description)

        rows = Rows(fetched)
        rows.desc = descr

        return rows

    def q(self, query):
        query = reformat_bind_params(query)

        frame = currentframe()

        try:
            if self._back:
                fback = frame.f_back.f_back
            else:
                fback = frame.f_back

            caller_locals = fback.f_locals

            return self.execute(query, caller_locals)
        finally:
            del frame

    def insert(self, t, rows):
        batch_size = len(rows)
        width = len(rows[0])

        params = ", ".join(["%s"] * width)

        sql = f"insert into {t} values ({params})"
        execute_batch(self.c, sql, rows, page_size=batch_size)


@contextmanager
def transaction(db_url):

    # conn = pgconnect(db_url)

    conn = get_conn(db_url)

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            t = Transaction()
            t.c = curs
            yield t
    finally:
        # conn.close()
        put_conn(conn, db_url)


def db(url):
    return Database(url)


class Database:
    def __init__(self, url):
        self.url = url

    @contextmanager
    def t(self):
        with transaction(self.url) as t:
            yield t

    def __getattr__(self, name):
        def method(*args, **kwargs):
            with self.t() as t:
                t._back = 1
                m = getattr(t, name)
                return m(*args, **kwargs)

        return method
