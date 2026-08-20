import tkinter as tk

def button_on():
   but_2.place_forget()
   but_1.place(x=150, y=100)

def button_off():
   but_1.place_forget()
   but_2.place(x=150, y=200)

root = tk.Tk()
cvs = tk.Canvas(width=300, height=300, bg="#ffffff")
but_1 = tk.Button(text="ボタンを消す", command=button_off)
but_2 = tk.Button(text="ボタンを出す", command=button_on)
but_1.place(x=150, y=100)
cvs.pack()
root.mainloop()