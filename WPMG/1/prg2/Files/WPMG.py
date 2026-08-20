import streamlit as stm
import hashlib
import asyncio
import sqlite3
import pickle
from pathlib import Path
from streamlit_tree_select import tree_select
from argon2 import PasswordHasher
from datetime import datetime
from zoneinfo import ZoneInfo
# ユーザー認証Argon2へ切り替え
ph = PasswordHasher()
pw_dbname = "WPMG.db"
conn = sqlite3.connect(pw_dbname)
cur = conn.cursor()
stm.set_page_config(page_title="WPMG")
def aut(name, pw):
    cur.execute("""select *
                FROM Employees
                WHERE name = ? AND pw = ?""",
                (name, pw))
    return cur.fetchone()


from pathlib import Path

from pathlib import Path

def create_nodes(path: Path):
    order = {
        ".png": 1, ".jpg": 1, ".jpeg": 1, ".gif": 1, ".webp": 1,
        ".mp4": 2, ".avi": 2, ".mov": 2, ".mkv": 2,
        ".py": 3,
        ".txt": 4, ".md": 4, ".log": 4,
        ".pdf": 5,
        ".json": 6, ".csv": 6, ".xml": 6
    }

    nodes = []

    for item in sorted(
        path.iterdir(),
        key=lambda p: (
            0 if p.is_dir() else order.get(p.suffix.lower(), 99),
            p.name.lower()
        )
    ):
        if item.is_dir():
            node = {
                "label": f"📁 {item.name}",
                "value": str(item),
                "children": create_nodes(item)
            }
        else:
            node = {
                "label": f"📄 {item.name}",
                "value": str(item)
            }

        nodes.append(node)

    return nodes
def admin_aut(pw1, pw2):
    
    with open("admin.pw", "r") as f:
        text = f.read()
    try:
        ph.verify(text, f"a24d{pw1};?HASH!!uiher853976{pw2}")
        return True
    except:
        
        return False
    

def all_prg(usernum, num=None, sar=False, word = ""):
    base_dir = Path(__file__).resolve().parent
    target_path = base_dir / f"WPMG/{usernum}/.wpmginfo"

    with open(target_path, "rb") as f:
        loaded_data = pickle.load(f)
    if sar:
        results = {}
        word = word.split("?")
        for i in loaded_data:
            kekka = []
            for e in word:
                if e in i:
                    kekka.append(True)
                else:
                    kekka.append(False)
            if False not in kekka:
                results[i]=loaded_data[i]

        result = [
            [
                name,
                datetime.strptime(data["lastdate"], "%Y%m%d.%H%M").strftime("%Y/%m/%d.%H:%M")
            ]
            for name, data in sorted(
                results.items(),
                key=lambda x: x[1]["lastdate"],
                reverse=True
            )
        ]
    else:
        result = [
                    [
                        name,
                        datetime.strptime(data["lastdate"], "%Y%m%d.%H%M").strftime("%Y/%m/%d.%H:%M")
                    ]
                    for name, data in sorted(
                        loaded_data.items(),
                        key=lambda x: x[1]["lastdate"],
                        reverse=True
                    )
                ]
    

    if num:
        return result
    else:
        return result[:3]



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
        
        return
    cur.execute(f"""UPDATE Employees SET {mode} = ? WHERE name = ?;""",     # プログラムで値が決まるので安全である
                (watasu, old_name))
    conn.commit()

def News_add(title, date, by, to, text):
    cur.execute("""
        INSERT INTO News
        (title, "by", "for", date, text)
        VALUES (?, ?, ?, ?, ?);
    """, (title, by, ",".join(map(str, to)), date, text))
    conn.commit()

def news(num=5, user=None):
    if user == True:
        if num == 0:
            return cur.execute("""
                SELECT NewsID, title, by, for, date, text
                FROM News
                ORDER BY date DESC;
            """).fetchall()
        else:
            return cur.execute("""
                SELECT NewsID, title, by, for, date, text
                FROM News
                ORDER BY date DESC
                LIMIT ?;
            """, (num,)).fetchall()
    elif num == 0:
        return cur.execute("""
            SELECT NewsID, title, "by", "for", date, text
            FROM News
            WHERE instr(',' || "for" || ',', ',' || ? || ',') > 0
            ORDER BY date DESC;
        """, (user,)).fetchall()
    else:
        return cur.execute("""
            SELECT NewsID, title, "by", "for", date, text
            FROM News
            WHERE instr(',' || "for" || ',', ',' || ? || ',') > 0
            ORDER BY date DESC
            LIMIT ?;
        """, (user,num)).fetchall()

def rt_user():
    """
    ## ユーザー名:ユーザー番号
    を返す
    """
    user ={}
    for row in cur.execute("""SELECT * FROM Employees;"""):
        user[row[1]]=row[0]
    return user


def News_del(num):
    cur.execute("""
        DELETE FROM News
        WHERE NewsID = ?
    """, (str(num),))
    conn.commit()

if "admin" in stm.query_params and "menu" not in stm.session_state:
    if stm.query_params["admin"] == "true":
        stm.title("管理者ログイン")
        with stm.form("ADM_LOGIN"):
            pw1 = stm.text_input("1stパスワード", type="password")
            pw2 = stm.text_input("2ndパスワード", type="password")
            LOGIN_BTN = stm.form_submit_button("LOGIN")
        if LOGIN_BTN:
            TF = admin_aut(pw1, pw2)
            if TF:
                stm.session_state.menu = "ADMIN"
                stm.session_state.login = "ADMIN"
                stm.rerun()
            else:
                stm.toast("パスワードが不正です", icon="❗")
    stm.stop()


if "login" not in stm.session_state:
    stm.markdown("プロジェクト管理ツール")
    stm.title("ユーザーログイン", text_alignment="center")
    with stm.form("LOGIN_FM"):
        usr_name = stm.text_input("ユーザー名")
        pw = hashlib.sha256(stm.text_input("パスワード", type="password").encode()).hexdigest()
        LOGIN_BTN = stm.form_submit_button("ログイン")
    
    if LOGIN_BTN:
        user = aut(usr_name, pw)
        if user:
            stm.session_state.login = user
            
            stm.rerun()

        else:
            stm.toast("パスワード・ユーザー名が不正です", icon="❗", duration=1)
            
            




elif stm.session_state.login:
    if "menu" in stm.session_state:
        if "ADMIN" in stm.session_state["menu"]:
            with stm.sidebar:
                select2 = None
                select1 = stm.sidebar.selectbox("機能選択", ["ホーム画面", "ニュース", "ユーザー管理"])
                if select1 == "ニュース":
                    select2 = stm.sidebar.selectbox("機能", ["追加", "削除"])

            if select1 == "ホーム画面":
                for i in news(num=0, user=True):
                    if f"{i[0]}" in stm.session_state and stm.session_state[f"{i[0]}"] == True:
                        col1, col2 = stm.columns([6,3], vertical_alignment="bottom")
                        with col1:
                            stm.markdown(f"# {i[1]}", text_alignment="center")
                            stm.markdown(f"**宛先:{i[3]}**")
                        with col2:
                            stm.markdown(f"**FROM:{i[2]}**", text_alignment="center")
                            stm.markdown(f"**{i[4]}**", text_alignment="center")
                            
                        stm.divider()
                        infos = i[5].split("\n")
                        for i in infos:
                            stm.markdown(i)
                        
                        BACK = stm.button("ホームに戻る")
                        if BACK:
                            
                            
                            stm.rerun()
                        stm.stop()
                if "ALL_NEWS" in stm.session_state and stm.session_state["ALL_NEWS"]:
                    stm.markdown("## NEWS 全件表示", text_alignment="center")
                    with stm.form("ALL_NEWSs"):
                        for i in news(num=0, user=True):
                            with stm.container(border=True):
                                col1, col2, col3 = stm.columns([6,2,2], vertical_alignment="center")
                                with col1:
                                    stm.markdown(f"### {i[1]}")
                                with col2:
                                    stm.markdown(f'**{i[4].split(" ")[0]}**', text_alignment="center")
                                with col3:
                                    stm.form_submit_button("詳細", key=f"{i[0]}", width="stretch")
                    if stm.button("戻る"):
                        stm.rerun()
                    stm.stop()
                stm.markdown("# 管理画面", text_alignment="center")
                with stm.form("INFO"):
                    stm.markdown("### ログ")
                    with open("WPMG.log", "r", encoding="utf-8") as f:
                        text = f.read()
                    
                    stm.code(text, language=None, height=300)
                    LOG_KOSIN = stm.form_submit_button("更新", width="stretch")
                    if LOG_KOSIN:
                        stm.rerun()
                
                with stm.form("NEWS"):
                    col1, col2 = stm.columns([5,1])
                    with col1:
                        stm.markdown("### ニュース")
                    with col2:
                        ALL_NEWS = stm.form_submit_button("全件表示", key="ALL_NEWS")
                    for i in news(user=True):
                        with stm.container(border=True):
                            col1, col2, col3 = stm.columns([6,2,2], vertical_alignment="center")
                            with col1:
                                stm.markdown(f"### {i[1]}")
                            with col2:
                                stm.markdown(f'**{i[4].split(" ")[0]}**', text_alignment="center")
                            with col3:
                                stm.form_submit_button("詳細", key=f"{i[0]}", width="stretch")
                    
            
            if select1 == "ニュース":
                stm.markdown("# ニュース管理", text_alignment="center")
                if select2 == "追加":
                    with stm.form("NEWS_ADD", clear_on_submit=True):
                        stm.markdown("### ニュース追加")
                        col8, col9 = stm.columns([5,5], vertical_alignment="bottom")
                        with col8:
                            tit = stm.text_input("タイトル", key = "N_title", max_chars=9)
                            dte = stm.datetime_input("日付", datetime.now(ZoneInfo("Asia/Tokyo")))
                        with col9:
                            sou = stm.text_input("送信者", key = "N_by")
                            users = []
                            rt_user_list = rt_user()
                            for i in rt_user_list:
                                users.append(i)
                            ate = stm.multiselect("宛先",users, key = "N_for")
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
                    for i in news(num=0, user=True):
                        if f"{i[0]}_del" in stm.session_state and stm.session_state[f"{i[0]}_del"]:
                            News_del(i[0])
                    with stm.form("NEWS_DEL"):
                        col1, col2 = stm.columns([7,2], vertical_alignment="center")
                        with col1:
                            stm.markdown("## ニュース削除")
                        with col2:
                            stm.markdown("**削除ボタンで削除**")
                        for i in news(num=0, user=True):
                            with stm.container(border=True):
                                col1, col2, col3 = stm.columns([6,2,2], vertical_alignment="center")
                                with col1:
                                    stm.markdown(f"### {i[1]}")
                                with col2:
                                    stm.markdown(f'**{i[4].split(" ")[0]}**', text_alignment="center")
                                with col3:
                                    stm.form_submit_button("削除", key=f"{i[0]}_del", width="stretch")
                
                

            if select1 == "ユーザー管理":
                stm.info("現在この機能は開発中です")
            
        if "menu" in stm.session_state and "PRG" in stm.session_state["menu"]:
            with stm.container(border=True):
                col1, col2 = stm.columns([3,2], vertical_alignment="bottom")
                with col1:
                    stm.markdown(f"# {stm.session_state.prg[0]}", text_alignment="center")     # Ex:['prg8', '2026/07/26.12:30']  sessionstate.prg
                with col2:
                    stm.markdown(f"**最終アクセス:{stm.session_state.prg[1]}**")
                info = stm.tabs(["プロジェクト情報", "ファイル編集","プロジェクト設定"])
                
            
                with info[1]:
                    
                    root_path = Path(f"./WPMG/{stm.session_state.login[0]}/{stm.session_state.prg[0]}/Files").resolve()
                    action = stm.menu_button("オプション", options=["まとめてダウンロード", "選択した内容をダウンロード", "選択した内容を削除", "ファイルを追加"])
                        
                    
                    with stm.expander("**ファイル**"):
                        
                        stm.markdown("### ファイル")
                        
                        
                        nodes = create_nodes(root_path)
                        
                        stm.session_state.result = tree_select(nodes)
                    
                    
                with info[0]:
                    stm.markdown("## hello")
                with info[2]:
                    stm.markdown("# Hello")
                back_buton = stm.button("Back to HOME", key=f"{stm.session_state.prg[0]}_back")
                if back_buton:
                    del stm.session_state.menu
                    stm.rerun()
            stm.stop()


    
        #########


    else:
        for i in news(num=0, user=str(stm.session_state.login[0])):
            if f"{i[0]}" in stm.session_state and stm.session_state[f"{i[0]}"] == True:
                col1, col2 = stm.columns([6, 3], vertical_alignment="bottom")
                with col1:
                    stm.markdown(f"# {i[1]}", text_alignment="center")
                with col2:
                    stm.markdown(f"**FROM:{i[2]}**", text_alignment="center")
                    stm.markdown(f"**{i[4]}**", text_alignment="center")
                stm.divider()

                infos = i[5].split("\n")
                for info in infos:
                    stm.markdown(info)

                BACK = stm.button("ホームに戻る")
                if BACK:
                    stm.rerun()

                stm.stop()
        
        for i in all_prg(stm.session_state.login[0], num=True):
            if f"GO_{i[0]}" in stm.session_state and stm.session_state[f"GO_{i[0]}"]:
                stm.session_state.menu = f"PRG_{i[0]}"
                stm.session_state.prg = i
                stm.rerun()
        
        if "ALL_NEWS" in stm.session_state and stm.session_state["ALL_NEWS"]:
            
            stm.markdown("## NEWS 全件表示", text_alignment="center")

            with stm.form("ALL_NEWSs"):
                for i in news(num=0, user=str(stm.session_state.login[0])):
                    with stm.container(border=True):
                        col1, col2, col3 = stm.columns([6, 2, 2], vertical_alignment="center")

                        with col1:
                            stm.markdown(f"### {i[1]}")

                        with col2:
                            stm.markdown(f'**{i[4].split(" ")[0]}**', text_alignment="center")

                        with col3:
                            stm.form_submit_button("詳細", key=f"{i[0]}", width="stretch")

            if stm.button("戻る"):
                stm.rerun()

            stm.stop()
        if "p_sarch" in stm.session_state and stm.session_state.p_sarch:
            stm.session_state.prg_OPP = True


        if "prg_OPP" in stm.session_state and stm.session_state["prg_OPP"]:
            with stm.form("PRG_LIST"):
                stm.markdown("# プロジェクト", text_alignment="center")
                col1, col2, col3, col4 = stm.columns([1,5,3,6.2], vertical_alignment="center")
                with col1:
                    stm.markdown("**検索**", text_alignment="left")
                with col2:
                    stm.text_input("検索ボックス",placeholder="プロジェクト名を検索...",label_visibility="collapsed", width=250, key = "p_sarBOX")
                with col3:
                    stm.form_submit_button("検索", key="p_sarch",help="ヘルプ:「?」を挟むことで複数単語の検索が可能です")
                with col4:
                    stm.form_submit_button("新規作成", key="new_prg", width="stretch")
                if not stm.session_state.p_sarch or stm.session_state.p_sarBOX=="":
                    list = all_prg(stm.session_state.login[0], num=True)
                    pass
                else:
                    stm.markdown(f"{len(all_prg(usernum=stm.session_state.login[0],sar=True,word=stm.session_state.p_sarBOX,num=True))}件の結果")
                    list = all_prg(usernum=stm.session_state.login[0],sar=True,word=stm.session_state.p_sarBOX,num=True)
                for i in list:
                    with stm.container(border=True):
                        col1, col2, col3 = stm.columns([2,3,2], vertical_alignment="center")
                        with col1:
                            stm.markdown(f'**{i[0]}**', text_alignment="center")
                        with col2:
                            stm.markdown(f'{i[1].split(".")[0]}', text_alignment="center")
                        with col3:
                            go_btn = stm.form_submit_button("GO", width="stretch", key=f"GO_{i[0]}")
                        
                if stm.form_submit_button("戻る"):
                    del stm.session_state["prg_OPP"]
                    stm.rerun()

            stm.stop()

        col1, col2 = stm.columns([5,1])
        with col1:
            stm.markdown(f"# ホーム", text_alignment="center")
        with col2:
            if stm.button("ログアウト"):
                stm.session_state.clear()
                stm.rerun()
        stm.markdown(f"**こんにちは！** ***{stm.session_state.login[1]}*** **さん**")
        prg = all_prg(stm.session_state.login[0])
        with stm.form("PRG_HOME"):
            col1, col2 = stm.columns([5,1], vertical_alignment="center")
            with col1:
                stm.markdown("## プロジェクト")
            with col2:
                other_btn = stm.form_submit_button("その他", key = "prg_OPP_button")
                if other_btn:
                    stm.session_state.prg_OPP = True
                    stm.rerun()
            stm.markdown("**最近開いたプロジェクト(上位三件)**", text_alignment="left")
            for i in prg:
                with stm.container(border=True):
                    col1, col2, col3 = stm.columns([2,3,2], vertical_alignment="center")
                    with col1:
                        stm.markdown(f'**{i[0]}**', text_alignment="center")
                    with col2:
                        stm.markdown(f'{i[1].split(".")[0]}', text_alignment="center")
                    with col3:
                        go_btn = stm.form_submit_button("GO", width="stretch", key=f"GO_{i[0]}")
                    ###########
                    ###########
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
                
                if f"{stm.session_state.login[1]}_PW_Commits" in stm.session_state:
                    
                    if stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"] and "新しいパスワードp" in stm.session_state:
                        
                        if stm.session_state["新しいパスワードp"] == "":
                            
                            del stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"]
                            del stm.session_state[f"{stm.session_state.login[1]}_PW_Commit"]
                            stm.rerun()

                        
                        Com(stm.session_state.login[2], stm.session_state.login[1], hashlib.sha256(stm.session_state["新しいパスワードp"].encode()).hexdigest(), "p")
                        del stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"]
                        del stm.session_state[f"{stm.session_state.login[1]}_PW_Commit"]
                        stm.session_state.login = (stm.session_state.login[0], stm.session_state.login[1], hashlib.sha256(stm.session_state["新しいパスワードp"].encode()).hexdigest())
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
        with stm.form("NEWS"):
            col1, col2 = stm.columns([5,1])
            with col1:
                stm.markdown("### ニュース")
            with col2:
                if news(user=str(stm.session_state.login[0])) == []:
                    pass
                else:
                    ALL_NEWS = stm.form_submit_button("全件表示", key="ALL_NEWS")
            if news(user=stm.session_state.login[0]) == []:
                stm.markdown("### 現在お知らせはありません", text_alignment="center")
                stm.form_submit_button("最新の情報に更新", width="stretch")
            for i in news(user=str(stm.session_state.login[0])):
                with stm.container(border=True):
                    col1, col2, col3 = stm.columns([6,2,2], vertical_alignment="center")
                    with col1:
                        stm.markdown(f"### {i[1]}")
                    with col2:
                        stm.markdown(f'**{i[4].split(" ")[0]}**', text_alignment="center")
                    with col3:
                        stm.form_submit_button("詳細", key=f"{i[0]}", width="stretch")


conn.close()
