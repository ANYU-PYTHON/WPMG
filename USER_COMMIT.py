pw_dbname = "WPMG.db"
import sqlite3
conn = sqlite3.connect(pw_dbname)
cur = conn.cursor()
def Com(name,usernum, pw, mode):
    """
    ## mode : n name更新, p pw更新(入力値)  
    """
    if mode == "n":
        mode = "name"
        watasu = name
    elif mode == "p":
        mode = "pw"
        watasu = pw
    else:
        print("Conでストップ")
        return
    cur.execute(f"""UPDATE Employees SET {mode} = ? WHERE UserID = ?;""",
                (watasu, usernum))
    conn.commit()

from argon2 import PasswordHasher
ph = PasswordHasher()
for row in cur.execute("""SELECT * FROM Employees;"""):
    print(row)
mode = input("MODE(p/n) >>>")
if mode in ["p", "n"]:
    pass
else:
    print("ERR")
    quit()
name = input("NEW_NAME>>>")
old_name = input("USER_NUM>>>")
pw = input("NEW_PW>>>")
if input("OK?(y/n)>>>") == "y":
    pass
else:
    quit()

Com(name, old_name, ph.hash(pw), mode)