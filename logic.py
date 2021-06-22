#!/usr/bin/env python3
import base64
from contextlib import contextmanager
import psycopg2
import os

import config

import logging

log = logging.getLogger(__name__)

@contextmanager
def make_conn():
    conn = psycopg2.connect(config.DB_URL)
    cur = conn.cursor()
    yield cur
    conn.commit()
    cur.close()
    conn.close()

def has_exit(token):
    """
    return true if this token is allowed to access the exit
    """
    try:
        token = token.decode('ascii')
        log.info("check for {}".format(token))
        with make_conn() as cur:
            cur.execute("SELECT count(*) FROM authed_exits WHERE token = %s", (token,))
            return cur.fetchone()[0] > 0
    except Exception as ex:
        log.warn("failed to check for exit status: {}".format(ex))
        return False



def grant_exit_for(subaddr, token, exit_addr):
    """
    allow a token on subaddress to use the exit at exit_addr
    """
    with make_conn() as cur:
        cur.execute("INSERT INTO authed_exits(token, subaddr, lokiaddr) VALUES(%s, %s, %s)", (token, subaddr, exit_addr))

def create_tables():
    """
    create database tables
    """
    with make_conn() as cur:
        cur.execute("CREATE TABLE IF NOT EXISTS authed_exits(token TEXT PRIMARY KEY, subaddr BIGINT NOT NULL, created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'), lokiaddr TEXT NOT NULL)")

if __name__ == '__main__':
    import sys
    if has_exit(base64.b64decode(sys.argv[2])):
        log.info("auth success for {}".format(sys.argv[1]))
        sys.exit(0)
    else:
        log.info("auth failed for {}".format(sys.argv[1]))
        sys.exit(1)
