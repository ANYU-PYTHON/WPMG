import sqlite3
conn = sqlite3.connect("WPMG.db")
cur = conn.cursor()
print("##########################################")
for row in cur.execute("""SELECT * FROM Employees;"""):
    print(row)
print("##########################################")
for row in cur.execute("""SELECT * FROM News;"""):
    print(row)
print("##########################################")