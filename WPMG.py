import streamlit as stm
import hashlib
import sqlite3
pw_dbname = "WPMG.db"
conn = sqlite3.connect(pw_dbname)
cur = conn.cursor()
def aut(name, pw):
    cur.execute("""select *
                FROM Employees
                WHERE name = ? AND pw = ?""",
                (name, pw))
    return cur.fetchone()

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

def News_add(title, date, by, to, text):
    cur.execute(f"""INSERT INTO News
                (title, by, for, date, text) VALUES
                ('{title}', '{by}', '{to}', '{date}', '{text}');""")
    conn.commit()

def rt_user():
    """
    ## ユーザー名:ユーザー番号
    を返す
    """
    user ={}
    for row in cur.execute("""SELECT * FROM Employees;"""):
        user[row[1]]=row[0]
    return user
if "LOCK" not in stm.session_state:
    stm.session_state.LOCK = 0
    stm.rerun()
if stm.session_state.LOCK == True:
    stm.error("一定回数失敗したのでこれ以上トライすることができません。もう一度リロードしてお試しください")
    print("EERR")
if "login" not in stm.session_state and not stm.session_state.LOCK == True:
    stm.markdown("プロジェクト管理ツール")
    stm.title("ユーザーログイン")
    with stm.form("LOGIN_FM"):
        usr_name = stm.text_input("ユーザー名")
        pw = hashlib.sha256(stm.text_input("パスワード", type="password").encode()).hexdigest()
        LOGIN_BTN = stm.form_submit_button("ログイン")
    ADMIN = stm.button("管理者ログイン")

    if ADMIN:
        stm.session_state["menu"] = "ADMIN"
        stm.session_state["login"] = "ADMIN"
        print("adminがログイン")
        stm.rerun()
    elif LOGIN_BTN:
        user = aut(usr_name, pw)
        if user:
            stm.session_state.login = user
            stm.rerun()

        else:
            stm.toast("パスワード・ユーザー名が不正です", icon="❗", duration=1)
            
            stm.session_state.LOCK += 1
            if stm.session_state.LOCK >= 4:
                print(stm.session_state.LOCK)
                stm.session_state.LOCK = True
                

elif "login" not in stm.session_state:
    stm.rerun()



elif stm.session_state.login:
    if "menu" in stm.session_state:
        if "ADMIN" in stm.session_state["menu"]:
            with stm.sidebar:
                select2 = None
                select1 = stm.sidebar.selectbox("機能選択", ["ホーム画面", "ニュース", "ユーザー管理", "その他"])
                if select1 == "ニュース":
                    select2 = stm.sidebar.selectbox("機能", ["追加", "削除", "更新"])
            if select1 == "ホーム画面":
                stm.markdown("# 管理画面", text_alignment="center")
            if select1 == "ニュース":
                stm.markdown("# ニュース管理", text_alignment="center")
                if select2 == "追加":
                    with stm.form("NEWS_ADD", clear_on_submit=True):
                        stm.markdown("### ニュース追加")
                        col8, col9 = stm.columns([5,5], vertical_alignment="bottom")
                        with col8:
                            tit = stm.text_input("タイトル", key = "N_title")
                            dte = stm.text_input("日付(None:今日, 直表示)", key = "N_date")
                        with col9:
                            sou = stm.text_input("送信者", key = "N_by")
                            users = []
                            rt_user_list = rt_user()
                            for i in rt_user_list:
                                users.append(i)
                            ate = stm.multiselect("宛先(全員:all)",users, key = "N_for")
                            ates = []
                            for i in ate:
                                ates.append(rt_user_list[i])
                                ate = ates
                            
                        nai = stm.text_area("内容(Markdown)", key="N_text", height=300, width=900)
                        stm.form_submit_button("アップロード", width="stretch", key="N_add")
                        if stm.session_state["N_add"]:
                            if tit == "" or sou == "" or ate == "" or nai == "":
                                stm.toast("空欄があります", icon="❗", duration=1)
                            else:
                                News_add(tit, dte, sou, ate, nai)
                                stm.rerun()

                if select2 == "削除":
                    with stm.form("NEWS_DEL"):
                        stm.markdown("## ニュース削除")
                        stm.info("未実装です。仕事しろ()")
                        era_kesi = stm.form_submit_button("エラー消し用")
                
                if select2 == "更新":
                    with stm.form("NEWS_COM"):
                        stm.markdown("## ニュース更新")
                        stm.info("未実装です。仕事しろ()")
                        era_kesi = stm.form_submit_button("エラー消し用")



        if "PRG" in stm.session_state["menu"]:
            stm.title(stm.session_state.prg, text_alignment="center")
            back_buton = stm.button("Back to HOME", key=f"{stm.session_state.prg[0]}_back")
            if stm.session_state[f"{stm.session_state.prg[0]}_back"]:
                del stm.session_state.menu
                stm.rerun()
                

    else:
        stm.markdown(f"# ホーム", text_alignment="center")
        stm.markdown(f"**こんにちは！** ***{stm.session_state.login[1]}*** **さん**")
        prg = [["main", "2026/6/5"], ["日本語", "2026/6/3"]]
        with stm.form("PRG"):
            stm.markdown("## プロジェクト")
            for i in prg:
                col1, col2, col3 = stm.columns([2,2,2], vertical_alignment="bottom")
                with col1:
                    stm.markdown(f'**{i[0]}**')
                with col2:
                    stm.markdown(f'**{i[1]}** ')
                with col3:
                    go_btn = stm.form_submit_button("GO", width="stretch" ,key=i[0])
                if stm.session_state[i[0]]:
                    stm.session_state.menu = f"PRG_{i[0]}"
                    stm.session_state.prg = i
                    stm.rerun()
        stm.text("")
        with stm.form("AC"):
            stm.markdown("### アカウント")
            
            
            if f"{stm.session_state.login[1]}_Commit" in stm.session_state:
                if f"{stm.session_state.login[1]}_Commits" in stm.session_state:
                    if stm.session_state[f"{stm.session_state.login[1]}_Commit"] and "新しいユーザー名n" in stm.session_state:
                        if stm.session_state["新しいユーザー名n"] == "":
                            del stm.session_state[f"{stm.session_state.login[1]}_Commits"]
                            del stm.session_state[f"{stm.session_state.login[1]}_Commit"]
                            stm.rerun()

                        Com(stm.session_state["新しいユーザー名n"], stm.session_state.login[1], stm.session_state.login[2], "n")
                        del stm.session_state[f"{stm.session_state.login[1]}_Commits"]
                        del stm.session_state[f"{stm.session_state.login[1]}_Commit"]
                        stm.session_state.login = (stm.session_state.login[0], stm.session_state["新しいユーザー名n"], stm.session_state.login[2])
                        stm.markdown("**ユーザー名**")
                        stm.toast("ユーザー名を変更しました", icon="✔️")
                        stm.rerun()
                    else:
                        stm.markdown("**ユーザー名**")
                else:
                    if stm.session_state[f"{stm.session_state.login[1]}_Commit"]:
                        pass
                    else:
                        stm.markdown("**ユーザー名**")
            else:
                stm.markdown("**ユーザー名**")

            col4, col5 = stm.columns([2,1],vertical_alignment="center")
            with col4:
                if f"{stm.session_state.login[1]}_Commit" in stm.session_state:
                    if stm.session_state[f"{stm.session_state.login[1]}_Commit"]:
                        new_name = stm.text_input("新しいユーザー名", key = "新しいユーザー名n")
                        stm.session_state[f"{stm.session_state.login[1]}_Commits"] = True
                    else:
                        stm.text(stm.session_state.login[1])
                else:
                    stm.text(stm.session_state.login[1])
            with col5:
                stm.form_submit_button("変更", width="content", key=f"{stm.session_state.login[1]}_Commit")



            if f"{stm.session_state.login[1]}_PW_Commit" in stm.session_state:
                print("1")
                if f"{stm.session_state.login[1]}_PW_Commits" in stm.session_state:
                    print("2")
                    if stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"] and "新しいパスワードp" in stm.session_state:
                        print("3")
                        if stm.session_state["新しいパスワードp"] == "":
                            print("空欄")
                            del stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"]
                            del stm.session_state[f"{stm.session_state.login[1]}_PW_Commit"]
                            stm.rerun()

                        print("更新")
                        Com(stm.session_state.login[1], stm.session_state.login[1], hashlib.sha256(stm.session_state["新しいパスワードp"].encode()).hexdigest(), "p")
                        del stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"]
                        del stm.session_state[f"{stm.session_state.login[1]}_PW_Commit"]
                        stm.session_state.login = (stm.session_state.login[1], hashlib.sha256(stm.session_state["新しいパスワードp"].encode()).hexdigest())
                        stm.markdown("**パスワード**")
                        stm.toast("パスワードを変更しました", icon="✔️")
                        stm.rerun()
                else:
                    if stm.session_state[f"{stm.session_state.login[1]}_PW_Commit"]:
                        pass
                    else:
                        stm.markdown("**パスワード**")
            else:
                stm.markdown("**パスワード**")
            col6, col7 = stm.columns([2,1],vertical_alignment="center")
            with col6:
                if f"{stm.session_state.login[1]}_PW_Commit" in stm.session_state:
                    if stm.session_state[f"{stm.session_state.login[1]}_PW_Commit"]:
                        new_pw = stm.text_input("新しいパスワード", type="password", key = "新しいパスワードp")#円巣名変更
                        stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"] = True
                    else:
                        stm.text("*******")
                else:
                    stm.text("*******")



            with col7:
                stm.form_submit_button("変更", width="content", key=f"{stm.session_state.login[1]}_PW_Commit")
        stm.text("")
        with stm.form("News"):
            stm.markdown("### お知らせ")


conn.close()
