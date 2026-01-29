import sqlite3

def get_conn():
    return sqlite3.connect("hospital.db", check_same_thread=False)

def create_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password BLOB,
        role TEXT,
        email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient TEXT,
        doctor TEXT,
        date TEXT,
        status TEXT,
        email TEXT
    )
    """)


    cur.execute("""
    CREATE TABLE IF NOT EXISTS prescriptions(
        id INTEGER PRIMARY KEY,
        patient TEXT,
        doctor TEXT,
        diagnosis TEXT,
        medicines TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS lab_reports(
        id INTEGER PRIMARY KEY,
        patient TEXT,
        test TEXT,
        result TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bills(
        id INTEGER PRIMARY KEY,
        patient TEXT,
        amount REAL,
        status TEXT
    )
    """)

    conn.commit()
