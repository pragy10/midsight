import sqlite3
import os

DB_PATH = os.path.expanduser('~/.midsight/midsight.db')

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS process_findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        pid INTEGER,
        ppid INTEGER,
        name TEXT,
        exe TEXT,
        cmdline TEXT,
        username TEXT,
        reason TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS file_findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        file_path TEXT,
        change_type TEXT,
        details TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS network_findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        event_type TEXT,
        details TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS honeytoken_findings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        file_path TEXT,
        event_type TEXT,
        details TEXT
    )''')
    conn.commit()
    conn.close()


def get_recent_suspicious_processes(limit=10):
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM process_findings ORDER BY id DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
