"""
# TTRCの設定ファイル
**Pygame_title**       ⇒ Pygame画面のタイトル\n
**Telop**              ⇒ Pygameウィンドウのテロップメッセージ\n
**Telop_Order**        ⇒ Pygame画面のTelopの初期値\n
**Telop_Speed**        ⇒ Pygame画面のTelopの移動スピード\n
**advertisement_now**  ⇒ Pygame画面の広告の初期値\n
**advertisement_pass** ⇒ Pygame画面の広告のパス\n
**advertisement_time** ⇒ Pygame画面の広告更新秒数\n
**people**             ⇒ 人数の初期値\n
**TkUI_TEMA**          ⇒ customtkinterのテーマ\n
**Counting_method**    ⇒ カウント方法の初期値\n
**RGBs**               ⇒ それぞれのRGBの値\n
**Proglams**           ⇒ その他機能の格納。
"""





# ↓Settings








#CustomTkinter
TkUI_TEMA="System"
Counting_method="Enter" # Enter, Serial
people=999
#Pygame
Pygame_title="TTRC_USER_UI"
Telop = ["Welcome to Toho Computer Club!", "桐朋中学校・高等学校 コンピュータ部へようこそ!", "W e l c o m e   t o   T C C"]
Telop_Order=0
Telop_Speed=5
advertisement_now=0
advertisement_pass=[r"C:\\Users\\ya353\\Downloads\\広告1.png", r"C:\\Users\\ya353\\Downloads\\広告2.png"]
advertisement_time=10
#Others
RGBs={
    "time_text": (96,228,212), 
      "来場者数": (255, 255, 255), 
      "NUMS": (48,192,255), 
      "人": (255, 255, 255), 
      "PygameBACK": (0,0,0), 
      "telop": (255,255,255)
      }

