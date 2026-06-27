import sqlite3
import hashlib
conn = sqlite3.connect("WPMG.db")
cur = conn.cursor()
for row in cur.execute("""SELECT * FROM News;"""):
    print(row)