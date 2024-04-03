from flask_mysqldb import MySQL
from . import mysql

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = mysql.connect(
            current_app.config['MYSQL_DATABASE'],
            detect_types=mysql.PARSE_DECLTYPES
        )
        g.db.row_factory = mysql.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()