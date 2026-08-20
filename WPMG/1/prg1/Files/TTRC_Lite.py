import tkinter as tk
from tkinter import messagebox
import pygame
from Setting import Telop as texts, Pygame_title as Pygame_name, Telop_Speed as speed
from Setting import TkUI_TEMA as tema, Counting_method as countnow, Telop_Order as telpn
from Setting import advertisement_now as adv_now, advertisement_pass as adv_pass, advertisement_time as adv_time
import threading
import time
import keyboard
current_date = "--"
current_time2 = "--:--"
kountrock = False
DATA = open("D:\\TTRC\\NUMS")
NUMS = int(DATA.read())
RGBs={
    "time_text": (96,228,212), 
    "来場者数": (255, 255, 255), 
    "NUMS": (48,192,255), 
    "人": (255, 255, 255), 
    "PygameBACK": (0,0,0), 
    "telop": (255,255,255),
    "設定メニュータイトル": (200,200,200),
    "設定メニューEsc": (200,150,150),
    }
def ADD_NUMS(add=1, option="NOMAL(+)", IN=None):
    global NUMS
    if option == "NOMAL(+)":
        NUMS += add
    elif option == "NOMAL(-)":
        NUMS -= add
    elif option == "return":
        return NUMS
    elif option == "change":
        NUMS = IN
def selial():
    import serial.tools.list_ports
    list1 = []
    list2 = []
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        if "Bluetooth" in desc:
            pass
        else:
            print(f"{port}: {desc}")
            ins = f"{port}: {desc}"
            list1.append(ins)
            list2.append(port)
    return list1, list2
def serealcount():
    global push
    global kountrun
    kountrun = True

    def serialsrerct():
        list1, list2 = selial()
        if not list1 and not list2:
            messagebox.showerror("Error", "有効なシリアルデバイスが認識できません")

            return None

        root = tk.Tk()
        root.title("シリアルデバイス選択")
        root.geometry("400x300")

        var = tk.IntVar(value=0)
        radio = []
        for i in range(len(list1)):
            rb = tk.Radiobutton(root, text=list1[i], variable=var, value=i)
            rb.grid(row=i, column=0, sticky=tk.W, padx=10, pady=3)
            radio.append(rb)

        def crct():
            global a
            a = list2[var.get()]  # ✅ 選択したポートを取得
            root.destroy()

        btn1 = tk.Button(root, text="選択", command=crct)
        btn1.grid(row=len(list1), column=0, pady=10)

        root.mainloop()
        return a

    INa = serialsrerct()
    if INa==None:
        print("NoSerect")
        exit()
    import serial
    try:
        kountrun = True
        ser = serial.Serial(INa, 9600, timeout=None)
        while kountrun:
            line = ser.readline()
            text = line.decode('utf-8').strip()
            if text == "AAA":
                push = True
                if kountrock == False:
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
    kountrun = True
    while kountrun:
        time.sleep(0.01)  # ウィンドウ負荷軽減のため必要

        if keyboard.is_pressed('Enter'):
            push = True
            if not zenkai:
                if kountrock == False:
                    print("Enterキーが押されました")
                    ADD_NUMS()
                    zenkai = True
        else:
            push = False
            zenkai = False


thirde=threading.Thread(target=Entercount)
thirde.start()

def aftr():
    print("aftr run")
    root = tk.Tk()
    root.title("after用メニュー")
    def time_kousin():
        print("timek")

        global current_date            
        global current_time2            
        current_date = time.strftime("%m月%d日")            
                    
                    
        current_time2 = time.strftime("%H時%M分")            
    

        #label2.configure(text=NUMS)            
        root.after(100, time_kousin)     
    def advertisement_kousin():
        print("advk")
        global adv_now
        if adv_now>=len(adv_pass)-1:        
            adv_now=0        
        else:        
            adv_now+=1        
        kousin=adv_time*1000        
        root.after(kousin, advertisement_kousin)                
    time_kousin() 
    advertisement_kousin()   
    #thirds=threading.Thread(target=serealcount)
    
    #d:\きいぼぉどらんにんぐ\JNRfont.ttf d:\きいぼぉどらんにんぐ\kaisoutai.ttfthirds.run()
    #
    root.mainloop()



def gestUI():
    global runing
    runing = True
    print("gestuirun")

    def UI_pygame():
        print("uipygamerun")
        global runing
        global telpn
        menus="main"
        pygame.init()
        pygame.display.set_caption(Pygame_name)

        screen = pygame.display.set_mode((1720, 1016), pygame.RESIZABLE)

        font = pygame.font.Font("JNRfont_n.ttf", 32)
        font2 = pygame.font.Font("Kaisotai-Next-UP-B.ttf", 400)
        font3 = pygame.font.Font("Kaisotai-Next-UP-B.ttf", 64)
        font4 = pygame.font.Font("Kaisotai-Next-UP-B.ttf", 72)

        icon = pygame.image.load('TCC.png')
        pygame.display.set_icon(icon)




        text_x = 1520
        text_y = 0

        while runing:
            if menus=="main":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        runing = False
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key ==pygame.K_KP1:
                            menus="Set"
                time_text = font4.render(f"{current_date} {current_time2}", True, RGBs["time_text"])
                telop = font.render(texts[telpn], True, RGBs["telop"])

                text_surface1 = font3.render("来場者数", True, RGBs["来場者数"])
                text_surface2 = font2.render(str(ADD_NUMS(option="return")), True, RGBs["NUMS"])
                text_surface3 = font3.render("人", True, RGBs["人"])

                advertisement = pygame.image.load(adv_pass[adv_now])
                

                maintext2 = str(ADD_NUMS(option="return"))

            
                nin_x = len(maintext2) * 140 + 192

                text_surface2 = font2.render(maintext2, True, RGBs["NUMS"])

                screen.fill(RGBs["PygameBACK"])

        
                screen.blit(time_text, (208, 80))
                screen.blit(telop, (text_x, text_y))
                screen.blit(text_surface1, (98, 174))
                screen.blit(text_surface2, (208, 240))
                screen.blit(text_surface3, (nin_x, 536))

                advertisement = pygame.image.load(adv_pass[adv_now])
                screen.blit(advertisement, (936, 40))

    
                text_x -= speed
                if text_x + telop.get_width() < 0:
                    text_x = 1520

                    if telpn >= len(texts) - 1:
                        telpn = 0
                    else:
                        telpn += 1

                    telop = font.render(texts[telpn], True, RGBs["telop"])

                
            time.sleep(0.01)
            if menus=="Set":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        runing = False
                        pygame.quit()
                        return
                screen.fill(RGBs["PygameBACK"])
                text1=font3.render("Setting Menu", True, RGBs["設定メニュータイトル"])
                text2=font.render("Esc:戻る", True, RGBs["設定メニューEsc"])
                screen.blit(text1, (600, 10))
                screen.blit(text2, (10, 750))
            pygame.display.flip()
        return

    UI_pygame()
th1=threading.Thread(target=aftr)
th1.start()

gestUI()

