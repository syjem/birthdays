import sqlitecloud
import sqlite3  # Only for using quote() safely
from flask import g
from configs import Config

def get_db():
    if 'db' not in g:
        g.db = sqlitecloud.connect(Config.SQLITECLOUD_URL)
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def sql_escape(value):
    return sqlite3.connect(":memory:").execute("SELECT quote(?)", (value,)).fetchone()[0]

def run_query(query_template, *params, as_dicts=True):
    # Escape and format
    safe_params = [sql_escape(p) for p in params]
    query = query_template.format(*safe_params)

    conn = get_db()
    cursor = conn.execute(query)
    columns = [desc[0] for desc in cursor.description] if as_dicts else None
    rows = cursor.fetchall()

    if as_dicts and columns:
        return [dict(zip(columns, row)) for row in rows]
    return rows

def run_exec(query_template, *params):
    safe_params = [sql_escape(p) for p in params]
    query = query_template.format(*safe_params)
    conn = get_db()
    conn.execute(query)
    conn.commit()
