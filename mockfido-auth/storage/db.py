import sqlite3

def init_db():
    conn = sqlite3.connect("users.sqlite")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, public_key TEXT)''')
    conn.commit()
    return conn

def save_user(username, public_key_pem):
    conn = init_db()
    conn.execute('REPLACE INTO users (username, public_key) VALUES (?, ?)', (username, public_key_pem))
    conn.commit()
    conn.close()
