pw_dbname = "WPMG.db"
import sqlite3
conn = sqlite3.connect(pw_dbname)
cur = conn.cursor()
def Com(name,old_name, pw, mode):
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
    cur.execute(f"""UPDATE Employees SET {mode} = ? WHERE name = ?;""",
                (watasu, old_name))
    conn.commit()

import hashlib
mode = input("MODE(p/n) >>>")
if mode in ["p", "n"]:
    pass
else:
    print("ERR")
    quit()
name = input("NEW_NAME>>>")
old_name = input("OLD_NAME>>>")
pw = input("NEW_PW>>>")
if input("OK?(y/n)>>>") == "y":
    pass
else:
    quit()

Com(name, old_name, hashlib.sha256(pw.encode()).hexdigest(), "p")