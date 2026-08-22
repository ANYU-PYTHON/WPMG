# modern UI
# ログを追加していって
import streamlit as stm
import hashlib
import sqlite3
import pickle
import shutil
import zipfile
import logging
import io
import os
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


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        file_handler = logging.FileHandler('WPMG.log', mode='a', encoding='utf-8')
        # 日時 - ログレベル - メッセージ
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger
log = setup_logger()
@stm.dialog("選択した内容を削除")
def sel_DEL(lists):
    log.debug(f"{stm.session_state.login[0]}_sel_DEL_COLL")
    folders = [Path(p) for p in lists if Path(p).is_dir()]
    files = [Path(p) for p in lists if Path(p).is_file()]
    if len(folders) == 0 and len(files) == 0:
        stm.info("選択されている内容がありません")
        log.error(f"{stm.session_state.login[0]}_sel_DEL> NOT_SELLECT")     # logging!
        stm.stop()
    file_old = files.copy()

    for folder in folders:
        for file in files[:]:
            if folder in file.parents:
                files.remove(file)

    stm.info(f"選択したファイル数は**{len(file_old)}**個、選択したフォルダ数は**{len(folders)}**個です。削除しますか？", title="info")
    if stm.button("削除", width="stretch"):
        for fileee in files:
            fileee.unlink()
        for foldeeer in folders:
            shutil.rmtree(foldeeer)
        log.info(f"{stm.session_state.login[0]}_sel_DEL> SAFTY_DEL:{stm.session_state.prg[0]}")
        stm.rerun()

@stm.dialog("選択した内容をダウンロード")
def sel_DL(lists, root_path):
    log.debug(f"{stm.session_state.login[0]}_sel_DL_COLL")
    folders = [Path(p) for p in lists if Path(p).is_dir()]
    files = [Path(p) for p in lists if Path(p).is_file()]
    stm.info(f"選択したファイル数は**{len(files)}**個、選択したフォルダ数は**{len(folders)}**個です。ダウンロードしますか？", title="info")
    zip_buffer = io.BytesIO()


    if lists:
        
            
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in lists:
                path = Path(path)

                if path.is_file():
                    zf.write(path, path.relative_to(root_path))

                elif path.is_dir():
                    for file in path.rglob("*"):
                        if file.is_file():
                            zf.write(file, file.relative_to(root_path))
        
        stm.download_button(
            "ZIPをダウンロード",
            data=zip_buffer.getvalue(),
            file_name=f"{stm.session_state.prg[0]}_selected.zip",
            mime="application/zip",
            key="selected_download"
        )
    else:
        log.error(f"{stm.session_state.login[0]}_sel_DL> NOT_SELLECT") 
        stm.info("ダウンロードするファイルを選択してください")

    return zip_buffer.getvalue()
def aut(name, pw):
    log.debug(f"{name}(?)_aut_COLL")
    cur.execute("""
        SELECT UserID, name, pw
        FROM Employees
        WHERE name = ?
    """, (name,))

    user = cur.fetchone()

    if user:
        try:
            log.debug(f"{user[0]}(?)_aut> name:{user[1]}_succes.Trying-verify..")
            ph.verify(user[2], pw)
            log.info(f"{user[0]}_aut> name:{user[1]}_LOGINN")
            return user
        except:
            log.info(f"{user[0]}(BAD)_aut> name:{user[1]}_PASSWD_NOT_SUCCESS")
            return None
    log.warning(f"!UnknownUSER_aut> NAME_NOT_SUCCESS")
    return None

def get_zip_data(folder_path):
    log.debug(f"{stm.session_state.login[0]}_get_zip_data_COLL")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                fp = os.path.join(root, file)
                zf.write(fp, os.path.relpath(fp, folder_path))
    return zip_buffer.getvalue()

@stm.dialog("プロジェクト新規作成")
def make_prg_user(usernum):
    stm.text_input("プロジェクト名")

@stm.dialog("すべてダウンロード")
def all_DL(usernum, prg_name):
    log.debug(f"{stm.session_state.login[0]}_all_DL> COLL")
    base_dir = Path(__file__).resolve().parent
    target_path = base_dir / f"WPMG/{usernum}/{prg_name}/Files"
    stm.info(f"環境を丸ごとダウンロードします。 この処理は時間がかかることがあります。", title="info")
    col1, col2 = stm.columns([1,1])
    with col1:
        emp = stm.empty()
        if "data" not in stm.session_state:
            with emp.spinner("作成中.."):
                stm.session_state.data=get_zip_data(target_path)
        if stm.session_state.data:
            emp.download_button(
            label="ZIPをダウンロード",
            data=stm.session_state.data,
            file_name=f"{prg_name}.zip",  # ← 引数としてそのまま渡す
            mime="application/zip",
            )

    with col2:
        if stm.button("閉じる", width="stretch"):
            del stm.session_state.data

            stm.rerun()

@stm.dialog("すべて削除")
def all_DEL(usernum, prg_name):
    log.debug(f"{stm.session_state.login[0]}_all_DEL_COLL")
    log.info(f"{stm.session_state.login[0]}_all_DEL> COLL")
    stm.warning("このプロジェクトのファイルのみが削除されます。 プロジェクト自体は削除されません。 続行しますか？")
    if stm.checkbox("理解しました", key="rikai"):
        if stm.button("削除", width="stretch"):
            path = Path(f"WPMG/{usernum}/{prg_name}/Files")

            for item in path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            log.info(f"{stm.session_state.login[0]}_all_DEL> ALL_DELLD CHECK:{stm.session_state.rikai}")
            stm.rerun()
def create_nodes(path: Path):
    log.debug(f"{stm.session_state.login[0]}_create_nodes_COLL")
    order = {
        ".py": 1, ".css": 1, ".html": 1,
        ".png": 2, ".jpg": 2, ".jpeg": 2, ".gif": 2, ".webp": 2,
        ".mp4": 3, ".avi": 3, ".mov": 3, ".mkv": 3,
        ".txt": 4, ".md": 4, ".log": 4,
        ".pdf": 5,
        ".json": 6, ".csv": 6, ".xml": 6,
        ".db": 7, ".code-workspace": 8
    }

    icons = {
        ".py": "🖋️", ".pdf": "🟥", ".log": "📃", ".code-workspace": "🛠️", ".db": "📑",
        ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️",
        ".gif": "🖼️", ".webp": "🖼️",
        ".mp4": "🎬", ".avi": "🎬", ".mov": "🎬", ".mkv": "🎬",
    }

    nodes = []
    for item in sorted(path.iterdir(),
        key=lambda p: (0 if p.is_dir() else order.get(p.suffix.lower(), 99), p.name.lower())):

        icon = "📁" if item.is_dir() else icons.get(item.suffix.lower(), "📄")
        node = {"label": f"{icon} {item.name}", "value": str(item)}

        if item.is_dir():
            node["children"] = create_nodes(item) # type: ignore

        nodes.append(node)

    return nodes


def rt_prg(usernum):
    log.debug(f"admin_rt_prg_COLL")
    folder = Path(f"./WPMG/{usernum}/")
    file = folder / ".wpmginfo"
    with open(file, "rb") as f:
        data = pickle.load(f)
    rt_list = []
    for i in data:
        rt_list.append(i)
    return rt_list

def del_user(usernum):
    log.debug(f"admin_del_user_COLL")
    cur.execute(
            "DELETE FROM Employees WHERE UserID = ?",
            (usernum,)
        )
    conn.commit()
    path = Path(f"./WPMG/{usernum}")
    if path.exists():
        shutil.rmtree(path)
    log.info(f"admin_del_user> SAFETY_DELETED_{usernum}")



def del_prg(usernum, prgname):
    log.debug(f"admin_del_prg_COLL")
    path = Path(f"./WPMG/{usernum}/{prgname}")
    if path.exists():
        shutil.rmtree(path)
    path = Path(f"./WPMG/{usernum}/")
    file = path / ".wpmginfo"
    if file.exists():
        with open(file, "rb") as f:
            data = pickle.load(f)
    else:
        data={}
    del data[prgname]
    with open(file, "wb") as f:
        pickle.dump(data, f)
    log.info(f"admin_del_prg> SAFETY_DELETED_{usernum}_{prgname}")



def make_prg(usernum, prgname, types="normal"):
    log.debug(f"admin_make_prg_COLL")
    folder = Path(f"./WPMG/{usernum}/{prgname}/Files")
    folder.mkdir(parents=True, exist_ok=True)
    if types == "new_usr":
        file = folder / "WPMGにようこそ.txt"
        file.touch()
    folder = Path(f"./WPMG/{usernum}/")
    file = folder / ".wpmginfo"
    if file.exists():
        with open(file, "rb") as f:
            data = pickle.load(f)
    else:
        data = {}
    if prgname in data:
        return "coll!"
    date = datetime.now().strftime("%Y%m%d.%H%M")
    data[prgname] = {"lastdate": date, "makedate": date}
    with open(file, "wb") as f:
        pickle.dump(data, f)
    log.info(f"admin_make_prg> SAFETY_MAKED_PRG:{prgname},USER:{usernum},TYPE:{types}")

def make_USER(username, passwd, prg):
    log.debug(f"admin_make_USER_COLL")
    passwd = ph.hash(passwd)
    cur.execute("""select *
                FROM Employees
                WHERE name = ?""",
                (username,))
    
    if cur.fetchone():
        log.warning(f"admin_make_USER> USER_NAME_ERROR:{username}")
        
        return "coll1"
    cur.execute("""
        INSERT INTO Employees (name, pw)
        VALUES (?, ?)
    """, (username, passwd,))
    conn.commit()
    if prg:
        if make_prg(cur.lastrowid, "デフォルトのプロジェクト", types="new_usr") == "coll!":
            return "coll2"
        log.info(f"SAFETY_MAKED_USER:{username}_MAKED_PRG")
    else:
        folder = Path(f"./WPMG/{cur.lastrowid}/")
        folder.mkdir(parents=True, exist_ok=True)
        file = folder / ".wpmginfo"
        with open(file, "wb") as f:
            pickle.dump({}, f)
        log.info(f"SAFETY_MAKED_USER:{username}_NOT_MAKED_PRG")




def admin_aut(pw1, pw2, opt=False):
    log.debug(f"admin_admin_aut_COLL")
    with open("admin.pw", "r") as f:
        text = f.read()
        log.debug(f"admin_admin_aut> admin_pwfile_SUCCESS_TO_READ")
    try:
        ph.verify(text, f"a24d{pw1};?HASH!!uiher853976{pw2}")
        if opt:
            log.warning(f"admin_admin_aut> AUT_SUCCESS")
        else:
            log.warning(f"admin_admin_aut> LOGIN_SUCCESS")
        return True
    except:
        if opt:
            log.error(f"admin_admin_aut> ADMIN_AUT_FAILED")
        else:
            log.error(f"admin_admin_aut> ADMIN_LOGIN_FAILED")
        return False
    

def all_prg(usernum, num=None, sar=False, word = ""):
    log.debug(f"{stm.session_state.login[0]}_all_prg_COLL")
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
    log.debug(f"{stm.session_state.login[0]}_Com_COLL")
    if mode == "n":
        mode = "name"
        watasu = name
        cur.execute("""select *
            FROM Employees
            WHERE name = ?""",
            (name,))
        
        if cur.fetchone():
            log.warning(f"{stm.session_state.login[0]}_Com> USER_NAME_ERROR")
            return "coll!"
    elif mode == "p":
        mode = "pw"
        watasu = pw
    else:
        log.warning(f"{stm.session_state.login[0]}_Com> MODE_SELECT_OTHER!")
        return
    
    cur.execute(f"""UPDATE Employees SET {mode} = ? WHERE UserID = ?;""",     # プログラムで値が決まるので安全である
                (watasu, old_name))
    conn.commit()
    log.info(f"{stm.session_state.login[0]}_Com> USER_{mode}_UPDATED")

def News_add(title, date, by, to, text):
    log.debug(f"admin_News_add_COLL")
    cur.execute("""
        INSERT INTO News
        (title, "by", "for", date, text)
        VALUES (?, ?, ?, ?, ?);
    """, (title, by, ",".join(map(str, to)), date, text))
    conn.commit()
    log.info(f"admin_News_add> NEWS_{title}_UPED")

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

def rt_user(opt = False):
    """
    ## ユーザー名:ユーザー番号
    を返す
    """
    log.debug(f"admin_rt_user_COLL")
    user ={}
    for row in cur.execute("""SELECT * FROM Employees;"""):
        user[row[1]]=row[0]
    if opt:
        user_name = []
        for i in user:
            user_name.append(i)
        return user, user_name
    return user


def News_del(num):
    log.debug(f"admin_News_del_COLL")
    cur.execute("""
        DELETE FROM News
        WHERE NewsID = ?
    """, (str(num),))
    conn.commit()
    log.info(f"admin_News_del> NEWS_{num}_DELED")
    

def cash_CL():
    log.info(f"{stm.session_state.login[0]}_cash_CL_COLL")
    lists = ["prg", "data", "ALL_prg", "menu", "新しいユーザー名", "新しいユーザー名n", "prg_OPP","新しいパスワードp", "新しいパスワード"]
    for i in lists:
        if i in stm.session_state:
            del stm.session_state[i]
    stm.rerun()



if "admin" in stm.query_params and "menu" not in stm.session_state:
    if stm.query_params["admin"] == "true":
        log.debug("admin_login_page> ACCESSED")
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
    log.debug("Unknownuser_login_page> ACCESSED")
    stm.markdown("プロジェクト管理ツール")
    stm.title("ユーザーログイン", text_alignment="center")
    with stm.form("LOGIN_FM"):
        usr_name = stm.text_input("ユーザー名")
        pw = stm.text_input("パスワード", type="password")
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
                with stm.container(border=True):
                    col1, col2 = stm.columns([4,8], vertical_alignment="bottom")
                    with col1:
                        stm.markdown("### ログ")
                    with col2:
                        fil = stm.segmented_control("フィルター", ["all", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], selection_mode="single")
                    
                    with open("WPMG.log", "r", encoding="utf-8") as f:
                        texts = f.readlines()
                        texts.reverse()
                    
                    
                    text = ""
                    for i in texts:
                        if fil == "all" or fil == None:
                            text += i
                        else:
                        
                            if fil in i:
                                text += i
                    stm.code(text, language=None, height=300)
                    LOG_KOSIN = stm.button("更新", width="stretch")
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
                select2 = stm.sidebar.selectbox("機能選択", ["ユーザー追加", "ユーザー削除"])
                if select2 == "ユーザー追加":
                    with stm.form("USER_ADD", clear_on_submit=True):
                        stm.markdown("## ユーザー追加", text_alignment="center")
                        col1, col2 = stm.columns([1,1])
                        with col1:
                            n_name = stm.text_input("ユーザー名")
                            new_prg = stm.checkbox("デフォルトの空のプロジェクト", value=True)
                        with col2:
                            n_passwd = stm.text_input("パスワード", type="password")
                        if stm.form_submit_button("作成", width="stretch"):
                            result = make_USER(n_name, n_passwd, new_prg)
                            if result:
                                stm.toast(f"作成エラー:{result}")
                            else:
                                stm.rerun()
                if select2 == "ユーザー削除":
                    with stm.container(border=True):
                        stm.markdown("## ユーザー削除", text_alignment="center")
                        col1, col2 = stm.columns([1,1])
                        user_dic, user_list = rt_user(opt=True)
                        with col1:
                            sel_user = stm.selectbox("**ユーザー**", user_list)
                            prg_del = stm.checkbox("プロジェクトを削除")
                            if prg_del:
                                prg_del_name = stm.selectbox("プロジェクトを選択", rt_prg(user_dic[sel_user]))
                            else:
                                prg_del_name = None

                        with col2:
                            ps1 = stm.text_input("管理者パスワード", type="password")
                            ps2 = stm.text_input("管理者2", label_visibility="collapsed", type="password")
                            stm.space("xxsmall")
                            if stm.button("削除", width="stretch"):
                                if admin_aut(ps1, ps2, opt=True):
                                    if prg_del and prg_del_name:
                                        del_prg(user_dic[sel_user], prg_del_name)
                                    else:
                                        del_user(user_dic[sel_user])
                                    stm.rerun()
                                else:
                                    stm.toast("認証エラー:パスワードが違います")

                
        if "menu" in stm.session_state and "PRG" in stm.session_state["menu"]:
            
            with stm.container(border=True):
                col1, col2 = stm.columns([3,2], vertical_alignment="bottom")
                with col1:
                    stm.markdown(f"# {stm.session_state.prg[0]}", text_alignment="center")     # Ex:['prg8', '2026/07/26.12:30']  sessionstate.prg
                
                info = stm.tabs(["プロジェクト情報", "ファイル編集","プロジェクト設定"])
                
            
                with info[1]:
                    
                    root_path = Path(f"./WPMG/{stm.session_state.login[0]}/{stm.session_state.prg[0]}/Files").resolve()
                    #action = stm.menu_button("オプション", options=["まとめてダウンロード", "選択した内容をダウンロード", "選択した内容を削除", "ファイルを追加"])
                    
                    with stm.expander("**ファイル**"):
                        col1, col2 = stm.columns([3,1])
                        with col1:
                            stm.markdown("### ファイル")
                        with col2:
                            stm.session_state.action = stm.menu_button("オプション", options=["まとめてダウンロード", "まとめて削除",  "選択した内容をダウンロード", "選択した内容を削除"])
                        nodes = create_nodes(root_path)
                        
                        stm.session_state.result = tree_select(nodes)
                        
                        if "action"in stm.session_state and stm.session_state.action == "まとめてダウンロード":
                            all_DL(stm.session_state.login[0], stm.session_state.prg[0])
                        if "action"in stm.session_state and stm.session_state.action == "まとめて削除":
                            all_DEL(stm.session_state.login[0], stm.session_state.prg[0])
                        # stm.session_state.result["checked"]
                        if "action"in stm.session_state and stm.session_state.action == "選択した内容を削除":
                            sel_DEL(stm.session_state.result["checked"])
                        if "action" in stm.session_state and stm.session_state.action == "選択した内容をダウンロード":
                            sel_DL(stm.session_state.result["checked"], root_path)
                    with stm.expander("**ファイルアップロード**"):
                        stm.file_uploader("ここに投下", accept_multiple_files=True)
                    with stm.expander("**ディレクトリアップロード**"):
                        stm.file_uploader("zipファイルのみ", type=".zip")
                    
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
                    if stm.form_submit_button("新規作成", width="stretch"):
                        make_prg_user(stm.session_state.login[0])

                if not stm.session_state.p_sarch or stm.session_state.p_sarBOX=="":
                    listp = all_prg(stm.session_state.login[0], num=True)
                    pass
                else:
                    stm.markdown(f"{len(all_prg(usernum=stm.session_state.login[0],sar=True,word=stm.session_state.p_sarBOX,num=True))}件の結果")
                    listp = all_prg(usernum=stm.session_state.login[0],sar=True,word=stm.session_state.p_sarBOX,num=True)
                for i in listp:
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

        col1, col2, col3 = stm.columns([8,3,2], vertical_alignment="bottom")
        with col1:
            stm.markdown(f"# ホーム", text_alignment="center")
        with col3:
            if stm.button("ログアウト"):
                log.info(f"{stm.session_state.login[0]}_LOGOUT_BYE")
                stm.session_state.clear()
                stm.rerun()
        with col2:
            if stm.button("一時データクリア"):
                cash_CL()
                
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
            if prg == []:
                stm.markdown("### プロジェクトはありません", text_alignment="center")
            else:
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
                        if stm.session_state["新しいユーザー名n"] == "" or stm.session_state["新しいユーザー名n"] == stm.session_state.login[1]:
                            del stm.session_state[f"{stm.session_state.login[1]}_Commits"]
                            del stm.session_state[f"{stm.session_state.login[1]}_Commit"]
                            stm.rerun()

                        com_returns = Com(stm.session_state["新しいユーザー名n"], stm.session_state.login[0], stm.session_state.login[2], "n")
                        if com_returns == "coll!":
                            
                            stm.toast("このユーザー名は使用できません!!", icon="🚨")
                        else:
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

                        
                        Com(stm.session_state.login[2], stm.session_state.login[0], ph.hash(stm.session_state["新しいパスワードp"]), "p")
                        del stm.session_state[f"{stm.session_state.login[1]}_PW_Commits"]
                        del stm.session_state[f"{stm.session_state.login[1]}_PW_Commit"]
                        stm.session_state.login = (stm.session_state.login[0], stm.session_state.login[1], ph.hash(stm.session_state["新しいパスワードp"]))
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
