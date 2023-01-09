import sqlite3

from flask import g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'flaskr.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

