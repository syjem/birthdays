from datetime import datetime, date
import sqlitecloud
import sqlite3
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

def format_date(date_str):
    """Format date string to readable format"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')
    except:
        return date_str
    

def get_days_until(birthday_str):
    """Calculate days until next birthday"""
    try:
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
        today = date.today()
        
        # Get this year's birthday
        this_year_birthday = birthday.replace(year=today.year)
        
        # If birthday has passed this year, get next year's
        if this_year_birthday < today:
            next_birthday = birthday.replace(year=today.year + 1)
        else:
            next_birthday = this_year_birthday
            
        days_until = (next_birthday - today).days
        
        if days_until == 0:
            return "🎉 Today!"
        elif days_until == 1:
            return "🎂 Tomorrow!"
        elif days_until <= 7:
            return f"🎈 In {days_until} days"
        else:
            return f"In {days_until} days"
    except:
        return "Invalid date"