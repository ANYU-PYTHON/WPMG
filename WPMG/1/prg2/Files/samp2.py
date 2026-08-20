import sqlite3
import hashlib
conn = sqlite3.connect("WPMG.db")
cur = conn.cursor()

def news(num=5):
    if num is None:
        return cur.execute("""
            SELECT NewsID, title, "by", "for", date, text
            FROM News
            ORDER BY date DESC;
        """).fetchall()

    else:
        return cur.execute("""
            SELECT NewsID, title, "by", "for", date, text
            FROM News
            ORDER BY date DESC
            LIMIT ?;
        """, (num,)).fetchall()
print(news())
'''
def news_all_del():
    cur.execute("DELETE FROM News;")
    cur.execute("DELETE FROM sqlite_sequence WHERE name = 'News';")
    conn.commit()
news_all_del()
'''