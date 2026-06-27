import sqlite3
import hashlib
conn = sqlite3.connect("WPMG.db")
cur = conn.cursor()
for row in cur.execute("""SELECT * FROM News;"""):
    print(row)
name = input("USER_NAME>>>")
PW = input("PASSWORD>>>")
print(f"NAME:{name} PW:{PW}")
TF = input("OK?(y/n)")
if TF == "y":
    pass
else:
    exit()
try:
    
    cur.execute(f"""INSERT INTO Employees
                (name, pw)
                VALUES
                ("{name}", "{hashlib.sha256(PW.encode()).hexdigest()}");""")
    conn.commit()
except sqlite3.OperationalError:
    cur.execute("""CREATE TABLE IF NOT EXISTS Employees (
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                pw TEXT NOT NULL);""")
    conn.commit()
    cur.execute(f"""INSERT INTO Employees
                (name, pw)
                VALUES
                ("{name}", "{hashlib.sha256(PW.encode()).hexdigest()}");""")
    conn.commit()
    print("Create Emplyees")

for row in cur.execute("""SELECT * FROM Employees;"""):
    print(row)