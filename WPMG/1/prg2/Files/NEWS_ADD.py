import sqlite3
conn = sqlite3.connect("WPMG.db")
cur = conn.cursor()

if True:
    cur.execute("""CREATE TABLE IF NOT EXISTS News (
                NewsID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE,
                by TEXT NOT NULL,
                for TEXT NOT NULL,
                date TEXT NOT NULL,
                text TEXT NOT NULL UNIQUE);""")
    conn.commit()
'''
if True:
    cur.execute("DROP TABLE Employees;")
    conn.commit()

'''