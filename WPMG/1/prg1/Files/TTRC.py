try:
    import pygame
    import keyboard
    import time
    import customtkinter as ctk
    from tkinter import messagebox
    from win11toast import toast
    import threading as th
    import math
    from Setting import Telop as texts, Pygame_title as Pygame_name, Telop_Speed as speed
    from Setting import TkUI_TEMA as tema, Counting_method as countnow, Telop_Order as telpn
    from Setting import advertisement_now as adv_now, advertisement_pass as adv_pass, advertisement_time as adv_time, RGBs
    ERROR=[]
    TF=None
    NOW=True
    NUMfile=open("NUMS", "r+")
    DATA=NUMfile.readlines()
    for i in DATA:
        ATAI=i.split("=", 1)
        ATAI[0]=ATAI[1]
    push=False
    kountrun=True
    runing=True
    current_date = "--月--日"
    current_time2 = "--時--分"
    current_time = "--:--"
    kountrock=True
    list1= ["pygame"]
    pas=False
    NUMS=0
    ctk.set_appearance_mode(tema)
    ctk.set_default_color_theme("blue")
    def Error(ERR, TreFal=False):
        global TF, ERROR
        ERROR.append(ERR)
        TF=TreFal
    def ADD_NUMS(add=1, option="NOMAL(+)", IN=None):
        global NUMS
        if option=="NOMAL(+)":
            NUMS+=add
        elif option=="NOMAL(-)":
            NUMS-=add
        elif option=="return":
            return NUMS
        elif option=="change":
            NUMS=IN
    def selial():
        import serial.tools.list_ports
        list1=[]
        list2=[]
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            if "Bluetooth" in desc:
                pass
            else:
                print(f"{port}: {desc}")
                ins=f"{port}: {desc}"
                list1.append(ins)
                list2.append(port)

        return list1, list2


    def show_fade_toast(parent, msg, duration=2000):
        

        toast = ctk.CTkToplevel(parent)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        toast.attributes("-alpha", 0.0)  # 透明からスタート

        # ラベル
        label = ctk.CTkLabel(
            toast, text=msg,
            fg_color="gray20", text_color="white",
            corner_radius=8, padx=15, pady=10,
            font=("Arial", 15)
        )
        label.pack()

        # --- 親ウィンドウの右下に配置 ---
        parent.update_idletasks()
        toast.update_idletasks()

        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()
        tw = toast.winfo_width()
        th = toast.winfo_height()

        # 親ウィンドウ右下に表示
        x = px + pw - tw - 20
        y = py + ph - th - 20
        toast.geometry(f"+{x}+{y}")

        # --- フェードイン／アウト処理 ---
        def fade_in(alpha=0.0):
            if alpha < 1.0:
                toast.attributes("-alpha", alpha)
                toast.after(30, fade_in, alpha + 0.1)
            else:
                toast.attributes("-alpha", 1.0)
                toast.after(duration, fade_out)

        def fade_out(alpha=1.0):
            if alpha > 0.0:
                toast.attributes("-alpha", alpha)
                toast.after(30, fade_out, alpha - 0.1)
            else:
                toast.destroy()

        fade_in()
    def spin(root):
        canvas = ctk.CTkCanvas(root, width=20, height=20, highlightthickness=0)
        canvas.pack(pady=20)
        dots = []
        radius = 8      # 円の半径（全体サイズ）
        dot_count = 12  # 点の数
        dot_size = 2    # 各点の大きさ

        # 点を配置
        for i in range(dot_count):
            angle = math.radians(i * (360 / dot_count))
            x = 10 + radius * math.cos(angle)
            y = 10 + radius * math.sin(angle)
            dot = canvas.create_oval(x-dot_size, y-dot_size, x+dot_size, y+dot_size, fill="#1f6aa5", outline="")
            dots.append(dot)

        def spin():
            while True:
                for i in range(dot_count):
                    # 明るさ変化で「回転」表現
                    for j in range(dot_count):
                        fade = (j - i) % dot_count
                        brightness = int(255 - fade * (200 / dot_count))
                        color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
                        canvas.itemconfig(dots[j], fill=color)
                    time.sleep(0.05)

        def start_spinner():
            th.Thread(target=spin, daemon=True).start()

        start_spinner()
    def serealcount():
        global push
        global kountrun
        kountrun = True

        def serialsrerct():
            list1, list2 = selial()
            if list1 == [] and list2 == []:
                messagebox.showerror("Error", "有効なシリアルデバイスが認識できません")
                Error("シリアルデバイス検出エラー")
                return None
            else:
                root = ctk.CTk()
                root.title("シリアルデバイス選択")
                root.geometry("400x300")

                var = ctk.IntVar(value=0)
                radio = []
                for i in range(len(list1)):
                    rb = ctk.CTkRadioButton(root, text=list1[i], variable=var, value=i)
                    rb.grid(row=i, column=0, sticky=ctk.W, padx=10, pady=3)
                    radio.append(rb)

                def crct():
                    global a
                    a = list2[var.get()]  # ✅ ()を付ける
                    root.destroy()

                btn1 = ctk.CTkButton(root, text="選択", command=crct)
                btn1.grid(row=len(list1), column=0, pady=10)

                root.mainloop()
            return a

        INa = serialsrerct()
        import serial
        try:
            kountrun = True
            ser = serial.Serial(INa, 9600, timeout=None)
            while kountrun:
                
                line = ser.readline()
                text = line.decode('utf-8').strip()
                if text == "AAA":
                    push = True
                    if kountrock==False:
                        ADD_NUMS()
                    
                            
                elif text == "LOW":
                    push = False
                elif text == "exit":
                    push = False
                    kountrun = False

                
        finally:
            push = False
            ser.close()


    def Entercount():
        global push
        global kountrun
        zenkai = False
        while kountrun:
            time.sleep(0.01)

            time.sleep(0.01) #これ消すとウィンドウ重くなります


            if keyboard.is_pressed('Enter'):
                push = True
                if not zenkai:
                    if kountrock==False:
                        print("Enterキーが押されました")
                        ADD_NUMS()
                        zenkai = True
            else:
                push = False
                zenkai = False

    thard1=th.Thread(target=Entercount)
    thard2=th.Thread(target=serealcount)

    def logiin():
        if pas==True:
            return
        else:
            root = ctk.CTk()
            root.title("サンプル")
            root.geometry("400x300")

            
            label = ctk.CTkLabel(root, text="パスワード認証", font=("Arial", 30))
            PW = ctk.CTkEntry(root, placeholder_text="パスワード", font=("Arial", 15), show='●', width=230, height=20)
            label.pack()
            label.place(x=90, y=20)
            
            PW.pack()
            PW.place(x=80, y=90)
            
            kaut=0
            
            def on_click():
                nonlocal kaut
                global TF, pas
                innow=PW.get()
                PW.delete(0, ctk.END)
                if innow == "":
                    # show_fade_toast(root, "ログイン成功")
                    root.destroy()
                    TF = True
                    pas=True
                    
                else:
                    show_fade_toast(root, "ログイン失敗")
                    kaut+=1
                    if kaut>=3:
                        PW.configure(state="disabled")
                        show_fade_toast(root, "ログイン試行回数が上限に達しました。")
                        time.sleep(4)
                        root.destroy()
                        TF=False
            

                
            
            button= ctk.CTkButton(root, text="OK", command=on_click)
            button.pack()
            button.place(x=120, y=140)
            root.bind('<Return>', lambda event: on_click())
            root.mainloop()

    def MAIN():
        global NOW
        global tema
        global push
        logiin()
        
        def gestUI():
            global runing
            runing = True
            print("gestuirun")

            def UI_pygame():
                print("uipygamerun")
                global runing
                global telpn
                pygame.init()
                pygame.display.set_caption(Pygame_name)
                screen = pygame.display.set_mode((1900, 1020))

                
                
                font = pygame.font.Font("JNRfont_n.ttf", 40)
                font2=pygame.font.Font("Kaisotai-Next-UP-B.ttf", 500)
                font3=pygame.font.Font("Kaisotai-Next-UP-B.ttf", 80)
                font4=pygame.font.Font("Kaisotai-Next-UP-B.ttf", 90)
                icon = pygame.image.load('TCC.png')
                pygame.display.set_icon(icon)
                time_text=font4.render(f"{current_date} {current_time2}", True, RGBs["time_text"])
                telop = font.render(texts[0], True, RGBs["telop"])
                
                text_surface1 = font3.render("来場者数", True, RGBs["来場者数"])
                
                text_surface2=font2.render(str(ADD_NUMS(option="return")), True, RGBs["NUMS"])
                
                text_surface3=font3.render("人", True, RGBs["人"])
                advertisement = pygame.image.load(adv_pass[adv_now])
                
                text_x = 1900
                text_y = 0  # 画面下から少し上に

                
                #clock = pygame.time.Clock()

                while runing:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            runing = False
                            pygame.quit()
                            return
                    time_text=font4.render(f"{current_date} {current_time2}", True, RGBs["time_text"])
                    maintext2=str(ADD_NUMS(option="return"))
                    nin_x=len(maintext2)*175+240
                    text_surface2=font2.render(maintext2, True, RGBs["NUMS"])
                    screen.fill(RGBs["PygameBACK"])
                    screen.blit(time_text, (260,100))
                    screen.blit(telop, (text_x, text_y))
                    screen.blit(text_surface1, (123,218))
                    screen.blit(text_surface2, (260,300))
                    screen.blit(text_surface3, (nin_x, 670))
                    advertisement = pygame.image.load(adv_pass[adv_now])
                    screen.blit(advertisement, (1170, 50))
                    text_x -= speed
                    if text_x + telop.get_width() < 0:
                        text_x = 1900
                        
                        
                        if telpn>=len(texts)-1:
                            telpn=0
                        else:
                            telpn+=1
                        telop = font.render(texts[telpn], True, RGBs["telop"])

                    pygame.display.flip()
                    

                print("aaa")
                return

            def ask():
           
                root = ctk.CTk()
                root.title("UI選択")
                root.geometry("400x300")

                var = ctk.IntVar(value=0)
                radio = []
                for i in range(len(list1)):
                    rb = ctk.CTkRadioButton(root, text=list1[i], variable=var, value=i)
                    rb.grid(row=i, column=0, sticky=ctk.W, padx=10, pady=3)
                    radio.append(rb)

                def crct():
                    global a
                    a = list1[var.get()]  # ✅ ()を付ける
                    root.destroy()
                    if a=="pygame":
                        runnnn2=th.Thread(target=UI_pygame)
                        runnnn2.start()
                        
                btn1 = ctk.CTkButton(root, text="選択", command=crct)
                btn1.grid(row=len(list1), column=0, pady=10)

                root.mainloop()
                exit()
            runnnn1=th.Thread(target=ask)
            runnnn1.start()
            print("asas")
            




        def count_main(root, main_button, main):
            global kountrun
            global thard1
            global thard2
            global runing
            
            main_button.pack_forget()
            kountrun=True
            def Shatdown():
                global runing
                global kountrun
                global thard1
                global thard2
                top_frame.pack_forget()
                bottom_frame.pack_forget()
                btn1.pack_forget()
                btn2.pack_forget()
                btn3.pack_forget()
                btn4.pack_forget()
                main_button.pack(pady=10)
                runing=False
                kountrun=False
                time.sleep(0.3)
                runing=True
                kountrun=True
                thard1=th.Thread(target=Entercount)
                thard2=th.Thread(target=serealcount)
            def OtherSystems():
                ANS=input(">>>")
                import OtherProglams
                OtherProglams.System(ANS)
            def SystemBOOT():
                thzard=th.Thread(target=OtherSystems)
                thzard.start()

            # --- 上段フレーム ---
            top_frame = ctk.CTkFrame(main, fg_color="transparent")
            top_frame.pack(pady=5)

            # --- 下段フレーム ---
            bottom_frame = ctk.CTkFrame(main, fg_color="transparent")
            bottom_frame.pack(pady=5)

            # --- 上段ボタン（左・右） ---
            btn1 = ctk.CTkButton(top_frame, text="ゲストUI起動", width=300, height=70, font=("Arial", 20), command=gestUI)
            btn1.pack(side="left", padx=5)

            btn2 = ctk.CTkButton(top_frame, text="データ分析", width=300, height=70, font=("Arial", 20))
            btn2.pack(side="left", padx=5)

            # --- 下段ボタン（左・右） ---
            btn3 = ctk.CTkButton(bottom_frame, text="機能名を指定して実行", width=300, height=70, font=("Arial", 20), command=SystemBOOT)
            btn3.pack(side="left", padx=5)

            btn4 = ctk.CTkButton(bottom_frame, text="メインシステム\nシャットダウン", width=300, height=70, font=("Arial", 20), command=Shatdown)
            btn4.pack(side="left", padx=5)

            if countnow=="Enter":
                
                
                thard1.start()
                  
            elif countnow=="Serial":

                thard2.start()
      
                

        def HOME():
            # メインウィンドウ作成
            root = ctk.CTk()
            root.title("CustomTkinter サンプル")
            root.geometry("800x500")

            # サイドバー（左側）
            sidebar = ctk.CTkFrame(root, width=200, corner_radius=0)
            sidebar.pack(side="left", fill="y")

            # メイン画面（右側）
            main_frame = ctk.CTkFrame(root)
            main_frame.pack(side="right", expand=True, fill="both")

            # サイドバーの中身
            label = ctk.CTkLabel(sidebar, text="--:--", font=("Arial", 30))
            label.pack(pady=20)
            """
            label2=ctk.CTkLabel(root, text="===")
            label2.pack(pady=10)
            # ボタンを複数配置
            """

            def show_page2():
                global tema
                if tema == "System":
                    tema="light"
                    ctk.set_appearance_mode(tema)
                    print("a")
                elif tema=="light":
                    tema="dark"
                    ctk.set_appearance_mode(tema)
                    print("b")
                else:
                    tema="System"
                    ctk.set_appearance_mode(tema)
                    print("c")
            def showNOW():
                global NOW
                messagebox.showinfo("現在の状態",f"現在の状態\n {NOW} \nエラー一覧\n{ERROR}")
                NOW=True
                pass

            def Colectcount():
                global countnow
                if countnow=="Enter":
                    countnow="Serial"
                    show_fade_toast(root, msg=f"カウント方式変更\n{countnow}")
                elif countnow=="Serial":
                    countnow="Enter"
                    show_fade_toast(root, msg=f"カウント方式変更\n{countnow}")
                else:
                    Error(f"エラー:countnowがunknownな値です\n{countnow}")

            btn1 = ctk.CTkButton(sidebar, text=f"状態", command=showNOW)
            btn1.pack(pady=10)

            btn2 = ctk.CTkButton(sidebar, text="てーま変更", command=show_page2)
            btn2.pack(pady=10)

            btn3 = ctk.CTkButton(sidebar, text=f"カウント方式変更", command=Colectcount)
            btn3.pack(pady=10)
            # メイン画面の中身
            main_label = ctk.CTkLabel(main_frame, text="HOME", font=("Arial", 50))
            main_label.pack(pady=10)
            main_button = ctk.CTkButton(main_frame, text="メイン起動", font=("Arial", 20), command=lambda: count_main(root, main_button, main_frame)) # type: ignore
            main_button.pack(pady=10)
            def time_kousin():
                global labela
                global current_time
                global current_date
                global current_time2
                current_date = time.strftime("%m月%d日")
                
                
                current_time2 = time.strftime("%H時%M分")
                current_time = time.strftime("%H:%M")
                label.configure(text=current_time)
                #label2.configure(text=NUMS)
                root.after(100, time_kousin)
            def advertisement_kousin():
                
                global adv_now
                if adv_now>=len(adv_pass)-1:
                    adv_now=0
                else:
                    adv_now+=1
                kousin=adv_time*1000
                root.after(kousin, advertisement_kousin)
            time_kousin()
            advertisement_kousin()
            # 実行
            root.mainloop()

        

            
        if TF == True:
            HOME()
        else:
            toast("ログインに失敗しました")
            exit()
    
    MAIN()


finally:
    kountrun=False
    runing=False
    print("BYE")