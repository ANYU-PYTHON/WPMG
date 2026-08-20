import tkinter as tk
from tkinter import messagebox
import pygame
from Setting import Telop as texts, Pygame_title as Pygame_name, Telop_Speed as speed
from Setting import TkUI_TEMA as tema, Counting_method as countnow, Telop_Order as telpn
from Setting import advertisement_now as adv_now, advertisement_pass as adv_pass, advertisement_time as adv_time, RGBs
import threading
import time

current_date = "--"
current_time2 = "--:--"
kountrock = False
DATA = open("D:\\重要A\\MY_PRG\\Python\\project\\P4 TTRC\\メインプロジェクト\\NUMS", "r+")
NUMS = int(DATA.read())
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
serealcount()