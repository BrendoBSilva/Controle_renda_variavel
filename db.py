import sqlite3

def conectar():
    return sqlite3.connect("finance.db", check_same_thread=False)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        senha TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receita (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        data TEXT,
        valor REAL,
        origem TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gasto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        data TEXT,
        valor REAL,
        categoria TEXT,
        tipo TEXT
    )
    """)

    conn.commit()
    conn.close()